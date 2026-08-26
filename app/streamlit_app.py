"""Allura Finance Lab — assistente Streamlit com RAG lexical e guardrails.

Rode na pasta do repositório:

    python -m pip install -r requirements.txt
    streamlit run app/streamlit_app.py
"""

from __future__ import annotations

import json
import os
import re
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
    "carteira", "entrada", "saida", "recursos", "board",
}
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
    for line in env_path.read_text(encoding="utf-8").splitlines():
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


def is_in_scope(question: str) -> bool:
    tokens = set(normalize_search_text(question).split())
    return bool(tokens & SCOPE_TERMS)


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
    model = os.getenv("GEMINI_MODEL", "gemini-flash-latest")
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
    if not is_in_scope(question):
        return guardrail_payload(
            "Fora de escopo: respondo somente sobre o caso sintético da Allura Finance.",
            "guardrail_escopo",
        )

    chunks = retriever.retrieve(question)
    best_score = float(chunks[0]["score"]) if chunks else 0.0
    if not chunks or best_score < MIN_RETRIEVAL_SCORE:
        return guardrail_payload(
            "Não tenho evidência suficiente na base para responder.",
            "guardrail_sem_evidencia",
        )

    generated = generate_with_gemini(question, chunks)
    if generated is not None:
        return generated
    return answer_from_chunks(chunks)


def render_answer(payload: dict) -> None:
    st.markdown(payload["resposta"])
    cols = st.columns(4)
    cols[0].metric("Confiança", payload.get("confianca", "—"))
    cols[1].metric("Escopo", "sim" if payload.get("dentro_do_escopo") else "não")
    cols[2].metric("Não sei", "sim" if payload.get("nao_sei") else "não")
    cols[3].metric("Método", payload.get("metodo_recuperacao", "—"))
    fontes = payload.get("fontes") or []
    if fontes:
        st.caption("Fontes: " + " · ".join(str(item) for item in fontes))


def main() -> None:
    load_env()
    st.set_page_config(page_title="Allura Finance Lab", page_icon="📊", layout="wide")
    st.title("Allura Finance Lab")
    st.caption("Caso sintético didático · RAG lexical · guardrails de PII, injection e escopo")

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
    st.sidebar.success(f"{len(docs)} chunks carregados")
    st.sidebar.write("Modelo Gemini:", "configurado" if has_key else "ausente — responde só com evidência lexical")
    st.sidebar.write("Pasta do projeto:", str(ROOT))

    if "messages" not in st.session_state:
        st.session_state.messages = []

    st.subheader("Perguntas sugeridas")
    cols = st.columns(len(SUGGESTED_QUESTIONS))
    clicked = None
    for col, suggestion in zip(cols, SUGGESTED_QUESTIONS):
        if col.button(suggestion, use_container_width=True):
            clicked = suggestion

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if message["role"] == "assistant":
                render_answer(message["payload"])
            else:
                st.markdown(message["content"])

    prompt = clicked or st.chat_input("Pergunte sobre captação, resgate, receita, mix ou metas")
    if not prompt:
        return

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    payload = ask(prompt, retriever)
    st.session_state.messages.append({"role": "assistant", "payload": payload})
    with st.chat_message("assistant"):
        render_answer(payload)


if __name__ == "__main__":
    main()
