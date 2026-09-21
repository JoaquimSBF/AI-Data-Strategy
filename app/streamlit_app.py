"""Allura Finance Lab — assistente Streamlit com RAG lexical e guardrails.

Rode na pasta do repositório:

    python -m pip install -r requirements.txt
    streamlit run app/streamlit_app.py
"""

from __future__ import annotations

import json
import os
import re
import time
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = ROOT / "outputs"
HARNESS = ROOT / "Harness Engineering"
MIN_RETRIEVAL_SCORE = 0.12

PII_PATTERNS = {
    "cpf": re.compile(r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b"),
    "email": re.compile(r"\b[\w.+-]+@[\w.-]+\.\w{2,}\b", re.I),
    "telefone": re.compile(r"\b(?:\+55\s?)?\(?\d{2}\)?\s?9?\d{4}-?\d{4}\b"),
}
INJECTION_PATTERNS = [
    re.compile(r"ignore\s+(all\s+)?(previous|prior|above)\s+instructions?", re.I),
    re.compile(r"disregard\s+(all\s+)?(previous|prior|above)", re.I),
    re.compile(r"forget\s+(everything|your\s+instructions|the\s+rules)", re.I),
    re.compile(r"\bDAN\b|\bjailbreak\b|\bdeveloper\s+mode\b", re.I),
    re.compile(r"reveal\s+(your\s+)?(system\s+)?prompt", re.I),
    re.compile(r"ignore\s+(todas\s+as\s+)?instru[cç][oõ]es", re.I),
    re.compile(r"esque[cç]a\s+(suas\s+)?(instru[cç][oõ]es|regras)", re.I),
    re.compile(r"revele\s+(o\s+)?(seu\s+)?prompt", re.I),
    re.compile(r"</?\s*system\s*>", re.I),
]
SCOPE_TERMS = {
    "allura", "finance", "banco", "bancario", "captacao", "resgate",
    "liquida", "receita", "churn", "meta", "metas", "produto",
    "produtos", "canal", "canais", "cliente", "clientes", "segmento",
    "kpi", "mix", "fee", "diretoria", "resultado", "investimento",
    "carteira", "entrada", "saida", "recursos", "board", "trimestre",
    "mensal", "liquidez", "fee", "captar", "resgatar", "analise",
}
ANALYTICAL_TERMS = {
    "explique", "resumo", "resuma", "analise", "analisar", "compare",
    "comparar", "tendencia", "insight", "insights", "performance",
    "dados", "cenario", "panorama", "visao", "executivo", "destaque",
    "principais", "motivos", "riscos", "oportunidades", "evolucao",
    "comportamento", "situacao", "contexto", "interpretar", "avaliar",
}
OFF_TOPIC_PHRASES = (
    "capital do japao",
    "capital da franca",
    "capital do brasil",
    "quem ganhou o jogo",
    "previsao do tempo",
    "como fazer bolo",
    "receita de bolo",
)
PORTUGUESE_STOPWORDS = {
    "a", "ao", "aos", "as", "com", "como", "da", "das", "de", "do", "dos",
    "e", "em", "entre", "esta", "estao", "foi", "mais", "na", "nas", "no",
    "nos", "o", "os", "ou", "para", "por", "qual", "que", "se", "um", "uma",
}
SUGGESTED_QUESTIONS = [
    "Como está a captação líquida por mês?",
    "Qual produto teve maior captação?",
    "Qual canal puxa a captação?",
    "A receita ficou acima da meta?",
    "A captação líquida ficou acima da meta?",
]


def load_env() -> None:
    env_path = ROOT / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def normalize_search_text(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", str(text or ""))
    normalized = "".join(char for char in normalized if not unicodedata.combining(char))
    normalized = normalized.lower()
    return re.sub(r"[^a-z0-9\s]", " ", normalized)


def chunk_text(text: str, max_chars: int = 1000, overlap: int = 120) -> list[str]:
    clean = re.sub(r"\n{3,}", "\n\n", text.strip())
    if len(clean) <= max_chars:
        return [clean]
    chunks: list[str] = []
    start = 0
    while start < len(clean):
        end = min(start + max_chars, len(clean))
        if end < len(clean):
            paragraph_break = clean.rfind("\n", start, end)
            if paragraph_break > start + max_chars // 2:
                end = paragraph_break
        chunks.append(clean[start:end].strip())
        if end >= len(clean):
            break
        start = max(end - overlap, start + 1)
    return chunks


def _read_table(path: Path) -> str:
    df = pd.read_csv(path)
    return df.to_string(index=False)


def build_docs_from_files() -> list[dict]:
    sources: list[tuple[Path, str, str, str]] = []
    seen_sources: set[str] = set()

    def add(path: Path | None, source: str, kind: str, title: str) -> None:
        if path is None or not path.exists() or source in seen_sources:
            return
        seen_sources.add(source)
        sources.append((path, source, kind, title))

    add(OUTPUTS / "analise_final.md", "analise_final.md", "narrativa", "texto")
    add(HARNESS / "outputs" / "analise_final.md", "analise_final.md", "narrativa", "texto")

    gold_pairs = [
        ("kpis_mensais.csv", "gold.kpis_mensais", "KPIs mensais"),
        ("mix_produto.csv", "gold.mix_produto", "Captação por produto"),
        ("mix_canal.csv", "gold.mix_canal", "Captação por canal"),
        ("receita_mensal.csv", "gold.receita_mensal", "Receita mensal"),
        ("status_snapshot.csv", "gold.churn_snapshot", "Snapshot de clientes ativos/inativos"),
    ]
    for filename, source, title in gold_pairs:
        add(ROOT / "data" / "gold" / filename, source, "tabela", title)
        add(HARNESS / "data" / "gold" / filename, source, "tabela", title)

    add(ROOT / "data" / "silver" / "metas.csv", "metas.csv", "regra_negocio", "Metas mensais")
    add(HARNESS / "data" / "silver" / "metas.csv", "metas.csv", "regra_negocio", "Metas mensais")

    docs: list[dict] = []
    for path, source, kind, title in sources:
        raw = path.read_text(encoding="utf-8") if path.suffix.lower() == ".md" else f"{title}:\n{_read_table(path)}"
        for chunk_index, chunk in enumerate(chunk_text(raw)):
            docs.append(
                {
                    "id": f"{source}#{chunk_index}",
                    "source": source,
                    "kind": kind,
                    "chunk_index": chunk_index,
                    "text": chunk,
                }
            )
    return docs


def load_docs() -> list[dict]:
    rag_path = OUTPUTS / "rag_context.json"
    if rag_path.exists():
        payload = json.loads(rag_path.read_text(encoding="utf-8"))
        docs = payload.get("docs") if isinstance(payload, dict) else payload
        if docs:
            return docs
    return build_docs_from_files()


def detect_pii(text: str) -> list[str]:
    found = [name for name, pattern in PII_PATTERNS.items() if pattern.search(text or "")]
    if re.search(r"\b(cpf|e-?mail|telefone|celular)\b", text or "", re.I):
        found.append("pedido_pii")
    return list(dict.fromkeys(found))


def has_prompt_injection(text: str) -> bool:
    return any(pattern.search(text or "") for pattern in INJECTION_PATTERNS)


def is_clearly_off_topic(question: str) -> bool:
    normalized = normalize_search_text(question)
    return any(phrase in normalized for phrase in OFF_TOPIC_PHRASES)


def is_in_scope(question: str, retrieval_score: float = 0.0) -> bool:
    if retrieval_score >= MIN_RETRIEVAL_SCORE:
        return True
    tokens = set(normalize_search_text(question).split())
    if tokens & SCOPE_TERMS:
        return True
    if tokens & ANALYTICAL_TERMS and len(tokens) >= 3:
        return True
    interrogatives = {"como", "qual", "quais", "quanto", "onde", "quando", "porque", "por"}
    return bool(tokens & interrogatives) and len(tokens) >= 4


def guardrail_payload(message: str, source: str) -> dict:
    return {
        "resposta": message,
        "fontes": [source],
        "confianca": "alta",
        "dentro_do_escopo": False,
        "nao_sei": True,
        "metodo_recuperacao": "guardrail",
        "score_recuperacao": 0.0,
    }


class Retriever:
    def __init__(self, docs: list[dict]):
        self.docs = docs
        self.vectorizer = TfidfVectorizer(
            preprocessor=normalize_search_text,
            stop_words=sorted(PORTUGUESE_STOPWORDS),
            ngram_range=(1, 2),
            min_df=1,
            sublinear_tf=True,
        )
        self.matrix = self.vectorizer.fit_transform([doc["text"] for doc in docs])

    def retrieve(self, question: str, top_k: int = 4) -> list[dict]:
        question_vector = self.vectorizer.transform([question])
        scores = cosine_similarity(question_vector, self.matrix)[0]
        ranked_indexes = np.argsort(scores)[::-1][:top_k]
        return [
            {**self.docs[index], "score": float(scores[index]), "retrieval_method": "lexical"}
            for index in ranked_indexes
            if scores[index] > 0
        ]


def _is_retryable_gemini_error(exc: Exception) -> bool:
    status_code = getattr(exc, "status_code", None)
    if status_code in {429, 500, 502, 503, 504}:
        return True
    message = str(exc).lower()
    return any(
        token in message
        for token in ("503", "429", "unavailable", "high demand", "rate limit", "overloaded")
    )


def generate_with_gemini(question: str, chunks: list[dict]) -> dict | None:
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        return None
    try:
        from google import genai
    except ImportError:
        return None

    context = "\n\n---\n\n".join(f"FONTE: {chunk['source']}\n{chunk['text']}" for chunk in chunks)
    prompt = (
        "Você é analista do caso sintético Allura Finance. "
        "Responda só com as evidências. Não invente número. Sem dica de investimento. Sem PII. "
        "Se faltar evidência, diga que não sabe.\n\n"
        f"CONTEXTO:\n<<<\n{context}\n>>>\n\nPERGUNTA:\n<<<\n{question}\n>>>\n\n"
        "Devolva JSON com chaves: resposta, fontes (lista), confianca (alta|media|baixa), "
        "dentro_do_escopo (bool), nao_sei (bool)."
    )
    client = genai.Client(api_key=api_key)
    configured_model = os.getenv("GEMINI_MODEL", "gemini-flash-latest")
    model_candidates = list(dict.fromkeys([configured_model, "gemini-2.0-flash", "gemini-1.5-flash"]))
    last_error: Exception | None = None

    for attempt in range(3):
        for model in model_candidates:
            try:
                response = client.models.generate_content(model=model, contents=prompt)
                text = (response.text or "").strip()
                match = re.search(r"\{.*\}", text, re.S)
                if not match:
                    return None
                parsed = json.loads(match.group(0))
                fontes = parsed.get("fontes") or [chunk["source"] for chunk in chunks[:2]]
                return {
                    "resposta": str(parsed.get("resposta") or text),
                    "fontes": fontes if isinstance(fontes, list) else [str(fontes)],
                    "confianca": parsed.get("confianca") or "media",
                    "dentro_do_escopo": bool(parsed.get("dentro_do_escopo", True)),
                    "nao_sei": bool(parsed.get("nao_sei", False)),
                    "metodo_recuperacao": "hybrid",
                    "score_recuperacao": round(float(chunks[0]["score"]), 4),
                }
            except Exception as exc:
                last_error = exc
                if not _is_retryable_gemini_error(exc):
                    return None
        if attempt < 2:
            time.sleep(2 ** attempt)

    if last_error is not None:
        st.warning(
            "Gemini indisponível no momento (ex.: alta demanda). "
            "Respondendo com evidência lexical da base."
        )
    return None


def answer_from_chunks(chunks: list[dict]) -> dict:
    best = chunks[0]
    return {
        "resposta": (
            "Evidência recuperada na base (modo lexical, sem chamar o modelo):\n\n"
            + best["text"][:900]
        ),
        "fontes": sorted({chunk["source"] for chunk in chunks}),
        "confianca": "media",
        "dentro_do_escopo": True,
        "nao_sei": False,
        "metodo_recuperacao": "lexical",
        "score_recuperacao": round(float(best["score"]), 4),
    }


def ask(question: str, retriever: Retriever) -> dict:
    pii_types = detect_pii(question)
    if pii_types:
        return guardrail_payload(
            f"Pergunta bloqueada: possível PII ({', '.join(pii_types)}).",
            "guardrail_pii",
        )
    if has_prompt_injection(question):
        return guardrail_payload(
            "Bloqueado: tentativa de alterar as regras do assistente.",
            "guardrail_injection",
        )
    if is_clearly_off_topic(question):
        return guardrail_payload(
            "Fora de escopo: respondo somente sobre o caso sintético da Allura Finance.",
            "guardrail_escopo",
        )

    chunks = retriever.retrieve(question)
    best_score = float(chunks[0]["score"]) if chunks else 0.0
    if not chunks or best_score < MIN_RETRIEVAL_SCORE:
        return guardrail_payload(
            "Não tenho evidência suficiente na base para responder. "
            "Tente reformular com termos como captação, receita, produtos, canais ou metas.",
            "guardrail_sem_evidencia",
        )
    if not is_in_scope(question, best_score):
        return guardrail_payload(
            "Fora de escopo: respondo somente sobre o caso sintético da Allura Finance.",
            "guardrail_escopo",
        )

    generated = generate_with_gemini(question, chunks)
    if generated is not None:
        return generated
    return answer_from_chunks(chunks)


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
            max-width: 920px;
        }
        header[data-testid="stHeader"] { background: rgba(255,255,255,0.92); }
        section[data-testid="stSidebar"] {
            border-right: 1px solid #e8edf3;
            background: #fbfcfe;
        }
        .app-header {
            display: flex;
            align-items: center;
            gap: 1.25rem;
            padding: 1.35rem 1.5rem;
            margin-bottom: 1.75rem;
            border: 1px solid #e7edf4;
            border-radius: 20px;
            background: #ffffff;
            box-shadow: 0 8px 24px rgba(15, 23, 42, 0.04);
        }
        .brand-mark {
            flex: 0 0 auto;
            font-size: 2rem;
            font-weight: 700;
            letter-spacing: -0.04em;
            line-height: 1;
            color: #111111;
            padding-right: 1.25rem;
            border-right: 1px solid #e7edf4;
        }
        .header-copy h1 {
            margin: 0;
            font-size: 1.55rem;
            font-weight: 700;
            color: #111827;
            letter-spacing: -0.02em;
        }
        .header-copy p {
            margin: 0.4rem 0 0;
            color: #64748b;
            font-size: 0.92rem;
            line-height: 1.45;
        }
        .section-title {
            margin: 1.6rem 0 0.55rem;
            font-size: 0.95rem;
            font-weight: 700;
            color: #111827;
            letter-spacing: -0.01em;
        }
        .section-hint {
            margin: 0 0 0.85rem;
            color: #64748b;
            font-size: 0.88rem;
        }
        .panel {
            padding: 1rem 1.1rem 0.35rem;
            border: 1px solid #e7edf4;
            border-radius: 16px;
            background: #ffffff;
            margin-bottom: 1rem;
        }
        div[data-testid="stButton"] > button {
            border-radius: 12px !important;
            border: 1px solid #dbe3ec !important;
            background: #ffffff !important;
            color: #1f2937 !important;
            font-weight: 500 !important;
            min-height: 2.65rem !important;
            box-shadow: none !important;
        }
        div[data-testid="stButton"] > button:hover {
            border-color: #00c86f !important;
            color: #0f172a !important;
            background: #f7fffb !important;
        }
        div[data-testid="stButton"] > button[kind="primary"] {
            background: #00c86f !important;
            border-color: #00c86f !important;
            color: #ffffff !important;
            font-weight: 600 !important;
        }
        div[data-testid="stTextArea"] textarea {
            border-radius: 14px !important;
            border: 1px solid #dbe3ec !important;
            background: #fbfcfe !important;
        }
        div[data-testid="stVerticalBlockBorderWrapper"]:has([data-testid="stChatMessage"]),
        div[data-testid="stVerticalBlockBorderWrapper"]:has(.chat-empty) {
            margin-top: 0.25rem;
            padding: 0.35rem 0.55rem 0.15rem;
            border-radius: 22px !important;
            border: 1px solid #e3eaf2 !important;
            background:
                radial-gradient(circle at top right, rgba(0, 200, 111, 0.07), transparent 34%),
                linear-gradient(180deg, #ffffff 0%, #f8fbff 100%) !important;
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.85);
            min-height: 320px;
        }
        .chat-empty {
            text-align: center;
            padding: 2.4rem 1.2rem 2rem;
            color: #64748b;
        }
        .chat-empty .emoji {
            font-size: 2rem;
            margin-bottom: 0.55rem;
        }
        .chat-empty h3 {
            margin: 0;
            color: #111827;
            font-size: 1.05rem;
            font-weight: 700;
        }
        .chat-empty p {
            margin: 0.45rem auto 0;
            max-width: 34rem;
            font-size: 0.9rem;
            line-height: 1.55;
        }
        div[data-testid="stChatMessage"] {
            border: none !important;
            background: transparent !important;
            padding: 0.15rem 0 !important;
            margin-bottom: 0.95rem !important;
        }
        div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p {
            margin-bottom: 0;
        }
        .user-bubble {
            display: inline-block;
            max-width: 92%;
            margin-left: auto;
            padding: 0.85rem 1rem;
            border-radius: 18px 18px 4px 18px;
            background: linear-gradient(135deg, #00c86f 0%, #00b4d8 100%);
            color: #ffffff;
            font-size: 0.95rem;
            line-height: 1.5;
            box-shadow: 0 10px 24px rgba(0, 180, 120, 0.18);
        }
        .assistant-card {
            max-width: 96%;
            padding: 1rem 1.05rem;
            border-radius: 18px 18px 18px 4px;
            border: 1px solid #e4ebf3;
            background: #ffffff;
            box-shadow: 0 10px 28px rgba(15, 23, 42, 0.05);
        }
        .assistant-card .answer-text {
            color: #1f2937;
            font-size: 0.95rem;
            line-height: 1.65;
            white-space: pre-wrap;
        }
        .meta-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.45rem;
            margin-top: 0.85rem;
        }
        .meta-pill {
            display: inline-flex;
            align-items: center;
            gap: 0.3rem;
            padding: 0.28rem 0.62rem;
            border-radius: 999px;
            font-size: 0.74rem;
            font-weight: 600;
            border: 1px solid transparent;
        }
        .pill-hybrid { background: #ecfdf5; color: #047857; border-color: #bbf7d0; }
        .pill-lexical { background: #eff6ff; color: #1d4ed8; border-color: #bfdbfe; }
        .pill-guardrail { background: #fff7ed; color: #c2410c; border-color: #fed7aa; }
        .pill-neutral { background: #f8fafc; color: #475569; border-color: #e2e8f0; }
        .pill-high { background: #ecfdf5; color: #047857; border-color: #bbf7d0; }
        .pill-medium { background: #eff6ff; color: #1d4ed8; border-color: #bfdbfe; }
        .pill-low { background: #fef2f2; color: #b91c1c; border-color: #fecaca; }
        .sources-row {
            margin-top: 0.8rem;
            padding-top: 0.75rem;
            border-top: 1px dashed #e2e8f0;
        }
        .sources-label {
            font-size: 0.72rem;
            font-weight: 700;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            margin-bottom: 0.45rem;
        }
        .source-chip {
            display: inline-block;
            margin: 0 0.35rem 0.35rem 0;
            padding: 0.22rem 0.55rem;
            border-radius: 999px;
            background: #f1f5f9;
            color: #334155;
            font-size: 0.72rem;
            border: 1px solid #e2e8f0;
        }
        div[data-testid="stChatInput"] {
            border-top: 1px solid #e7edf4;
            padding-top: 0.75rem;
        }
        div[data-testid="stChatInput"] > div {
            border-radius: 16px !important;
            border: 1px solid #dbe3ec !important;
            background: #ffffff !important;
            box-shadow: 0 8px 24px rgba(15, 23, 42, 0.04);
        }
        [data-testid="stSpinner"] {
            padding: 0.35rem 0;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header() -> None:
    st.markdown(
        """
        <div class="app-header">
          <div class="brand-mark">alura</div>
          <div class="header-copy">
            <h1>Allura Finance Lab</h1>
            <p>Skills &amp; Go · Data Strategy + IA · caso sintético · RAG + guardrails</p>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_section(title: str, hint: str | None = None) -> None:
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
    if hint:
        st.markdown(f'<div class="section-hint">{hint}</div>', unsafe_allow_html=True)


def _method_pill_class(method: str) -> str:
    if method == "hybrid":
        return "pill-hybrid"
    if method == "lexical":
        return "pill-lexical"
    if method == "guardrail":
        return "pill-guardrail"
    return "pill-neutral"


def _confidence_pill_class(confidence: str) -> str:
    normalized = str(confidence or "").lower()
    if normalized == "alta":
        return "pill-high"
    if normalized == "media":
        return "pill-medium"
    if normalized == "baixa":
        return "pill-low"
    return "pill-neutral"


def _escape_html(text: str) -> str:
    return (
        str(text or "")
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def render_user_message(content: str) -> None:
    st.markdown(
        f'<div style="display:flex; justify-content:flex-end;"><div class="user-bubble">{_escape_html(content)}</div></div>',
        unsafe_allow_html=True,
    )


def render_answer(payload: dict) -> None:
    method = str(payload.get("metodo_recuperacao", "—"))
    confidence = str(payload.get("confianca", "—"))
    escopo = "sim" if payload.get("dentro_do_escopo") else "não"
    fontes = payload.get("fontes") or []
    source_html = "".join(f'<span class="source-chip">{_escape_html(item)}</span>' for item in fontes)
    sources_block = (
        f'<div class="sources-row"><div class="sources-label">Fontes consultadas</div>{source_html}</div>'
        if fontes
        else ""
    )
    st.markdown(
        f"""
        <div class="assistant-card">
          <div class="answer-text">{_escape_html(payload["resposta"])}</div>
          <div class="meta-row">
            <span class="meta-pill {_confidence_pill_class(confidence)}">Confiança · {confidence}</span>
            <span class="meta-pill {_method_pill_class(method)}">Método · {method}</span>
            <span class="meta-pill pill-neutral">Escopo · {escopo}</span>
          </div>
          {sources_block}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_chat_empty_state() -> None:
    st.markdown(
        """
        <div class="chat-empty">
          <div class="emoji">💬</div>
          <h3>Comece uma conversa com o assistente</h3>
          <p>Use as perguntas rápidas, escreva uma pergunta aberta ou continue o chat abaixo.
          As respostas usam evidências do caso Allura Finance com RAG e guardrails.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def handle_prompt(prompt: str, retriever: Retriever) -> None:
    clean_prompt = prompt.strip()
    if not clean_prompt:
        return
    st.session_state.messages.append({"role": "user", "content": clean_prompt})
    payload = ask(clean_prompt, retriever)
    st.session_state.messages.append({"role": "assistant", "payload": payload})


def main() -> None:
    load_env()
    st.set_page_config(
        page_title="Allura Finance Lab | Alura",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    inject_styles()
    render_header()

    docs = load_docs()
    if not docs:
        st.error(
            "Não achei evidência para o assistente. Rode o notebook até a célula de RAG "
            "(gera `outputs/rag_context.json`) **ou** execute o harness até `analise_final.md`."
        )
        st.code("streamlit run app/streamlit_app.py", language="bash")
        st.stop()

    retriever = Retriever(docs)
    has_key = bool(os.getenv("GEMINI_API_KEY", "").strip())

    with st.sidebar:
        st.markdown("#### alura")
        st.caption("Assistente didático do caso Allura Finance")
        st.divider()
        st.metric("Evidências carregadas", len(docs))
        st.metric("Modelo Gemini", "Ativo" if has_key else "Modo lexical")
        st.caption(
            "Dados 100% sintéticos · sem recomendação de investimento · guardrails de PII ativos"
        )
        st.divider()
        if st.button("Limpar conversa", use_container_width=True):
            st.session_state.messages = []
            st.session_state.open_q_version = st.session_state.get("open_q_version", 0) + 1
            st.rerun()

    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "pending_prompt" not in st.session_state:
        st.session_state.pending_prompt = None
    if "open_q_version" not in st.session_state:
        st.session_state.open_q_version = 0

    render_section("Perguntas rápidas", "Clique em uma sugestão para começar.")
    with st.container(border=True):
        row1 = st.columns(2, gap="small")
        row2 = st.columns(3, gap="small")
        quick_rows = [row1, row2]
        for index, suggestion in enumerate(SUGGESTED_QUESTIONS):
            target_row = quick_rows[0] if index < 2 else quick_rows[1]
            col_index = index if index < 2 else index - 2
            with target_row[col_index]:
                if st.button(suggestion, use_container_width=True, key=f"chip_{index}"):
                    st.session_state.pending_prompt = suggestion

    render_section(
        "Pergunta aberta",
        "Escreva em linguagem natural — resumos, comparações, análises e perguntas livres sobre o caso.",
    )
    with st.container(border=True):
        open_question = st.text_area(
            "Pergunta aberta",
            placeholder=(
                "Ex.: Me dê um resumo executivo da captação líquida, destaque os produtos "
                "e canais que mais influenciaram o resultado e comente se a meta foi atingida."
            ),
            height=120,
            key=f"open_question_input_{st.session_state.open_q_version}",
            label_visibility="collapsed",
        )
        send_open = st.button("Enviar pergunta", type="primary", use_container_width=True)

    render_section("Conversa", "Histórico da interação com o assistente.")
    with st.container(border=True):
        if not st.session_state.messages:
            render_chat_empty_state()
        for message in st.session_state.messages:
            if message["role"] == "assistant":
                with st.chat_message("assistant", avatar="🤖"):
                    render_answer(message["payload"])
            else:
                with st.chat_message("user", avatar="👤"):
                    render_user_message(message["content"])

    prompt = None
    used_open_question = False
    if send_open and open_question.strip():
        prompt = open_question.strip()
        used_open_question = True
    elif st.session_state.pending_prompt:
        prompt = st.session_state.pending_prompt
        st.session_state.pending_prompt = None

    chat_prompt = st.chat_input("Continue a conversa aqui...")
    if chat_prompt:
        prompt = chat_prompt

    if not prompt:
        return

    with st.status("Consultando evidências e montando a resposta...", expanded=False):
        handle_prompt(prompt, retriever)
    if used_open_question:
        st.session_state.open_q_version += 1
    st.rerun()


if __name__ == "__main__":
    main()
