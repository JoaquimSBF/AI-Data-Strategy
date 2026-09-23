(function () {
  "use strict";

  var STORAGE_KEY = "portal-intelligence-v1";
  var MAX_BYTES = 5 * 1024 * 1024;
  var state = {
    data: null,
    periodo: "2026-06",
    backlog: [],
    historico: []
  };

  function $(id) { return document.getElementById(id); }
  function text(el, value) { el.textContent = value == null ? "sem evidencia" : String(value); }
  function clear(el) { while (el.firstChild) el.removeChild(el.firstChild); }
  function el(tag, attrs, children) {
    var node = document.createElement(tag);
    Object.keys(attrs || {}).forEach(function (key) {
      if (key === "className") node.className = attrs[key];
      else if (key.slice(0, 2) === "on") node.addEventListener(key.slice(2).toLowerCase(), attrs[key]);
      else if (key === "value") node.value = attrs[key];
      else node.setAttribute(key, attrs[key]);
    });
    (children || []).forEach(function (child) {
      node.appendChild(typeof child === "string" ? document.createTextNode(child) : child);
    });
    return node;
  }
  function num(value) { return Number(value); }
  function fmt(value, digits) {
    var n = Number(value);
    if (!isFinite(n)) return "sem evidencia";
    return n.toLocaleString("pt-BR", { maximumFractionDigits: digits == null ? 2 : digits });
  }
  function evid(id) {
    return (state.data.evidencias || []).find(function (item) { return item.evidencia_id === id; }) || null;
  }
  function kpiDoMes(mes) {
    return state.data.kpis.find(function (row) { return row.ano_mes === mes; }) || null;
  }
  function save() {
    localStorage.setItem(STORAGE_KEY, JSON.stringify({
      schemaVersion: 1,
      periodo: state.periodo,
      backlog: state.backlog,
      historico: state.historico
    }));
  }
  function loadLocal() {
    try {
      var raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return;
      var parsed = JSON.parse(raw);
      if (parsed.schemaVersion !== 1) return;
      if (parsed.periodo) state.periodo = parsed.periodo;
      if (Array.isArray(parsed.backlog)) state.backlog = parsed.backlog;
      if (Array.isArray(parsed.historico)) state.historico = parsed.historico;
    } catch (err) {
      text($("status-app"), "Dados locais ignorados por esquema inválido.");
    }
  }

  function cloneSample() {
    return JSON.parse(JSON.stringify(window.SAMPLE_DATA));
  }

  function setStatus(msg) { text($("status-app"), msg); }

  function openEvidence(id) {
    var item = evid(id);
    var body = $("dlg-corpo");
    clear(body);
    if (!item) {
      text($("dlg-titulo"), "sem evidencia");
      body.appendChild(el("p", {}, ["Identificador não encontrado."]));
    } else {
      text($("dlg-titulo"), item.evidencia_id);
      ["afirmacao", "tipo", "valor", "unidade", "periodo", "formula", "limitacao"].forEach(function (key) {
        body.appendChild(el("p", {}, [key + ": " + (item[key] == null ? "sem evidencia" : item[key])]));
      });
      body.appendChild(el("p", {}, ["fonte: " + (item.fonte || []).join(", ")]));
    }
    $("dlg-evidencia").showModal();
  }

  function metaDoKpi(kpi, mes) {
    return (state.data.metas || []).find(function (row) {
      return row.kpi === kpi && row.ano_mes === mes;
    }) || null;
  }

  function renderExecutiva() {
    var root = $("view-executiva");
    clear(root);
    var mes = state.periodo === "todos" ? "2026-06" : state.periodo;
    var kpi = kpiDoMes(mes);
    var busca = state.data.busca.find(function (row) { return row.ano_mes === mes; });
    var share = state.data.visibilidade.find(function (row) {
      return row.ano_mes === mes && row.dominio === "portal_proprio";
    });
    root.appendChild(el("h2", {}, ["Visão executiva"]));
    root.appendChild(el("p", { className: "warn" }, [
      "Dados sintéticos. Correlação não é causa. IA é amostra de 10 testes no mês."
    ]));
    if (!kpi) {
      root.appendChild(el("p", {}, ["sem evidencia"]));
      return;
    }
    var cards = el("div", { className: "kpis" });
    function card(label, value, metaRow, evidId, digits) {
      var ok = metaRow && metaRow.status === "atingida";
      var node = el("article", { className: "card " + (metaRow ? (ok ? "ok" : "bad") : "") }, [
        el("span", { className: "label" }, [label]),
        el("span", { className: "value" }, [fmt(value, digits)]),
        el("p", {}, [metaRow ? ("Meta " + fmt(metaRow.meta, digits) + " · " + metaRow.status) : "sem meta neste recorte"]),
        el("button", { type: "button", onClick: function () { openEvidence(evidId); } }, ["Ver evidência"])
      ]);
      cards.appendChild(node);
    }
    card("Usuários", kpi.usuarios_mensais, metaDoKpi("usuarios_mensais", mes), "EVD-001", 0);
    card("Tempo médio (s)", kpi.tempo_medio_seg, metaDoKpi("tempo_medio_seg", mes), "EVD-002", 2);
    card("Rejeição (%)", kpi.taxa_rejeicao_pct, metaDoKpi("taxa_rejeicao_pct", mes), "EVD-003", 2);
    card("CTR busca (%)", busca ? busca.ctr_pct : null, null, "EVD-006", 2);
    card("Share IA observado (%)", share ? share.share_citacao_pct : null, metaDoKpi("share_citacao_ia_pct", mes), "EVD-010", 2);
    root.appendChild(cards);
    var table = el("table", {}, []);
    table.appendChild(el("thead", {}, [el("tr", {}, ["ano_mes", "usuarios", "sessoes", "tempo", "rejeicao"].map(function (h) { return el("th", {}, [h]); }))]));
    var body = el("tbody", {}, []);
    state.data.kpis.filter(function (row) {
      return state.periodo === "todos" || row.ano_mes === state.periodo;
    }).forEach(function (row) {
      body.appendChild(el("tr", {}, [
        row.ano_mes, fmt(row.usuarios_mensais, 0), fmt(row.sessoes, 0), fmt(row.tempo_medio_seg, 2), fmt(row.taxa_rejeicao_pct, 2)
      ].map(function (c) { return el("td", {}, [c]); })));
    });
    table.appendChild(body);
    root.appendChild(table);
  }

  function renderBars(root, title, rows, key, evidId) {
    root.appendChild(el("h2", {}, [title]));
    rows.forEach(function (row) {
      var pct = num(row[key]);
      var wrap = el("div", {}, [
        el("p", {}, [row.editoria + " · " + fmt(pct, 2) + "%"]),
        el("div", { className: "bar" }, [el("span", { style: "width:" + pct + "%" }, [])])
      ]);
      wrap.firstChild.nextSibling.firstChild.style.width = Math.max(0, Math.min(100, pct)) + "%";
      root.appendChild(wrap);
    });
    root.appendChild(el("button", { type: "button", onClick: function () { openEvidence(evidId); } }, ["Ver evidência"]));
  }

  function renderAudiencia() {
    var root = $("view-audiencia");
    clear(root);
    var mes = state.periodo === "todos" ? "2026-06" : state.periodo;
    var rows = state.data.mix.filter(function (row) { return row.ano_mes === mes; });
    renderBars(root, "Mix de usuários por editoria", rows, "mix_usuarios_pct", "EVD-004");
    var table = el("table", {}, []);
    table.appendChild(el("thead", {}, [el("tr", {}, ["editoria", "usuarios", "sessoes", "mix %"].map(function (h) { return el("th", {}, [h]); }))]));
    var body = el("tbody", {}, []);
    rows.forEach(function (row) {
      body.appendChild(el("tr", {}, [row.editoria, fmt(row.usuarios, 0), fmt(row.sessoes, 0), fmt(row.mix_usuarios_pct, 2)].map(function (c) { return el("td", {}, [c]); })));
    });
    table.appendChild(body);
    root.appendChild(table);
  }

  function renderBusca() {
    var root = $("view-busca");
    clear(root);
    root.appendChild(el("h2", {}, ["Busca"]));
    root.appendChild(el("p", { className: "warn" }, ["Exportação sintética. ART025 e ART026 não existem no inventário."]));
    var table = el("table", {}, []);
    table.appendChild(el("thead", {}, [el("tr", {}, ["ano_mes", "impressoes", "cliques", "ctr %", "posição"].map(function (h) { return el("th", {}, [h]); }))]));
    var body = el("tbody", {}, []);
    state.data.busca.filter(function (row) {
      return state.periodo === "todos" || row.ano_mes === state.periodo;
    }).forEach(function (row) {
      body.appendChild(el("tr", {}, [row.ano_mes, fmt(row.impressoes, 0), fmt(row.cliques, 0), fmt(row.ctr_pct, 2), fmt(row.posicao_media, 2)].map(function (c) { return el("td", {}, [c]); })));
    });
    table.appendChild(body);
    root.appendChild(table);
    root.appendChild(el("button", { type: "button", onClick: function () { openEvidence("EVD-005"); } }, ["Ver evidência"]));
  }

  function renderBenchmark() {
    var root = $("view-benchmark");
    clear(root);
    root.appendChild(el("h2", {}, ["Benchmark sintético"]));
    root.appendChild(el("p", { className: "warn" }, ["Concorrentes fictícios. Sem score composto."]));
    var table = el("table", {}, []);
    table.appendChild(el("thead", {}, [el("tr", {}, ["data", "site", "performance", "seo", "estruturados", "mobile", "carga"].map(function (h) { return el("th", {}, [h]); }))]));
    var body = el("tbody", {}, []);
    state.data.benchmark.filter(function (row) {
      return state.periodo === "todos" || row.ano_mes === state.periodo;
    }).forEach(function (row) {
      body.appendChild(el("tr", {}, [
        row.data_coleta, row.site, row.performance_score, row.seo_tecnico_score,
        row.dados_estruturados_pct, row.mobile_score, row.tempo_carregamento_seg
      ].map(function (c) { return el("td", {}, [String(c)]); })));
    });
    table.appendChild(body);
    root.appendChild(table);
    root.appendChild(el("button", { type: "button", onClick: function () { openEvidence("EVD-008"); } }, ["Ver evidência"]));
  }

  function renderIa() {
    var root = $("view-ia");
    clear(root);
    root.appendChild(el("h2", {}, ["Visibilidade em IA"]));
    root.appendChild(el("p", { className: "warn" }, [
      "Amostra de 10 testes por mês. Não é market share universal."
    ]));
    var table = el("table", {}, []);
    table.appendChild(el("thead", {}, [el("tr", {}, ["ano_mes", "domínio", "testes", "total", "share %"].map(function (h) { return el("th", {}, [h]); }))]));
    var body = el("tbody", {}, []);
    state.data.visibilidade.filter(function (row) {
      return state.periodo === "todos" || row.ano_mes === state.periodo;
    }).forEach(function (row) {
      body.appendChild(el("tr", {}, [row.ano_mes, row.dominio, row.testes, row.total_testes, row.share_citacao_pct].map(function (c) { return el("td", {}, [String(c)]); })));
    });
    table.appendChild(body);
    root.appendChild(table);
    root.appendChild(el("button", { type: "button", onClick: function () { openEvidence("EVD-010"); } }, ["Ver evidência"]));
  }

  function updateOpp(id, field, value) {
    state.backlog.forEach(function (item) {
      if (item.oportunidade_id === id) item[field] = value;
    });
    state.historico.push({ id: id, field: field, value: value, at: new Date().toISOString() });
    save();
    renderOps();
  }

  function renderOps() {
    var root = $("view-ops");
    clear(root);
    root.appendChild(el("h2", {}, ["Oportunidades"]));
    var statuses = ["nova", "em_analise", "aprovada", "em_execucao", "concluida", "descartada"];
    var board = el("div", { className: "kanban" });
    statuses.forEach(function (status) {
      var col = el("div", { className: "col" }, [el("h3", {}, [status])]);
      state.backlog.filter(function (item) { return item.status === status; }).forEach(function (item) {
        var select = el("select", { value: item.status, onChange: function (ev) { updateOpp(item.oportunidade_id, "status", ev.target.value); } },
          statuses.map(function (st) { return el("option", { value: st }, [st]); })
        );
        select.value = item.status;
        var note = el("input", {
          value: item.nota || "",
          placeholder: "nota",
          onChange: function (ev) { updateOpp(item.oportunidade_id, "nota", ev.target.value); }
        });
        var owner = el("input", {
          value: item.responsavel_sugerido || "",
          placeholder: "papel",
          onChange: function (ev) { updateOpp(item.oportunidade_id, "responsavel_sugerido", ev.target.value); }
        });
        col.appendChild(el("article", { className: "ticket" }, [
          el("strong", {}, [item.oportunidade_id + " · " + item.titulo]),
          el("p", {}, [item.problema_observado]),
          el("p", {}, ["prioridade " + item.prioridade + " · confiança " + item.confianca]),
          el("p", {}, ["evidências: " + (item.evidencias || []).join(", ")]),
          select, owner, note,
          el("button", { type: "button", onClick: function () { openEvidence((item.evidencias || [])[0]); } }, ["Ver evidência"])
        ]));
      });
      board.appendChild(col);
    });
    root.appendChild(board);
  }

  function csvEscape(value) {
    var textValue = String(value == null ? "" : value);
    if (/^[=+\-@]/.test(textValue)) textValue = "'" + textValue;
    if (/[",\n]/.test(textValue)) return '"' + textValue.replace(/"/g, '""') + '"';
    return textValue;
  }

  function looksLikePii(textValue) {
    return /@/.test(textValue) || /\b\d{3}\.\d{3}\.\d{3}-\d{2}\b/.test(textValue);
  }

  function handleFiles(fileList) {
    var log = $("import-log");
    clear(log);
    Array.prototype.forEach.call(fileList, function (file) {
      if (file.size > MAX_BYTES) {
        log.appendChild(document.createTextNode(file.name + ": rejeitado, acima de 5 MB\n"));
        return;
      }
      if (!/\.(csv|json)$/i.test(file.name)) {
        log.appendChild(document.createTextNode(file.name + ": extensão inválida\n"));
        return;
      }
      var reader = new FileReader();
      reader.onload = function () {
        var content = String(reader.result || "");
        if (looksLikePii(content)) {
          log.appendChild(document.createTextNode(file.name + ": PII detectada, arquivo bloqueado\n"));
          return;
        }
        if (/\.json$/i.test(file.name)) {
          try { JSON.parse(content); }
          catch (err) {
            log.appendChild(document.createTextNode(file.name + ": JSON inválido\n"));
            return;
          }
        }
        log.appendChild(document.createTextNode(file.name + ": aceito como dado não confiável, sem execução\n"));
      };
      reader.readAsText(file);
    });
  }

  function exportJson() {
    download("backlog.json", JSON.stringify(state.backlog, null, 2), "application/json");
  }
  function exportCsv() {
    var header = ["oportunidade_id", "titulo", "status", "prioridade", "responsavel_sugerido", "nota"];
    var lines = [header.join(",")].concat(state.backlog.map(function (item) {
      return header.map(function (key) { return csvEscape(item[key]); }).join(",");
    }));
    download("backlog.csv", lines.join("\n"), "text/csv");
  }
  function exportMd() {
    var kpi = kpiDoMes(state.periodo === "todos" ? "2026-06" : state.periodo);
    var lines = [
      "# Resumo Inteligência do Portal",
      "",
      "fato_observado: usuários em " + (kpi ? kpi.ano_mes : "sem evidencia") + " = " + (kpi ? kpi.usuarios_mensais : "sem evidencia") + ". Fonte: kpis_mensais.csv.",
      "limitacao: dados sintéticos; sem evidencia causal.",
      "Oportunidades: " + state.backlog.length + "."
    ];
    download("resumo.md", lines.join("\n"), "text/markdown");
  }
  function download(name, content, type) {
    var blob = new Blob([content], { type: type });
    var url = URL.createObjectURL(blob);
    var link = el("a", { href: url, download: name }, []);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  }

  function renderAll() {
    renderExecutiva();
    renderAudiencia();
    renderBusca();
    renderBenchmark();
    renderIa();
    renderOps();
  }

  function fillPeriodos() {
    var select = $("filtro-periodo");
    clear(select);
    select.appendChild(el("option", { value: "todos" }, ["Todos"]));
    state.data.kpis.forEach(function (row) {
      select.appendChild(el("option", { value: row.ano_mes }, [row.ano_mes]));
    });
    select.value = state.periodo;
  }

  function init() {
    if (!window.SAMPLE_DATA) {
      setStatus("sem evidencia de demonstração.");
      return;
    }
    state.data = cloneSample();
    state.backlog = cloneSample().oportunidades;
    loadLocal();
    fillPeriodos();
    renderAll();
    setStatus("Demonstração carregada. Persistência local ativa.");

    document.querySelectorAll(".nav button").forEach(function (btn) {
      btn.addEventListener("click", function () {
        document.querySelectorAll(".nav button").forEach(function (other) { other.classList.remove("active"); });
        btn.classList.add("active");
        document.querySelectorAll(".view").forEach(function (view) { view.classList.add("hidden"); });
        $("view-" + btn.getAttribute("data-view")).classList.remove("hidden");
      });
    });
    $("filtro-periodo").addEventListener("change", function (ev) {
      state.periodo = ev.target.value;
      save();
      renderAll();
    });
    $("btn-restaurar").addEventListener("click", function () {
      localStorage.removeItem(STORAGE_KEY);
      state.data = cloneSample();
      state.backlog = cloneSample().oportunidades;
      state.historico = [];
      state.periodo = "2026-06";
      fillPeriodos();
      renderAll();
      setStatus("Demonstração restaurada.");
    });
    $("btn-apagar").addEventListener("click", function () {
      localStorage.removeItem(STORAGE_KEY);
      setStatus("Dados locais apagados. Recarregue ou restaure a demonstração.");
    });
    $("file-input").addEventListener("change", function (ev) { handleFiles(ev.target.files); });
    $("btn-export-json").addEventListener("click", exportJson);
    $("btn-export-csv").addEventListener("click", exportCsv);
    $("btn-export-md").addEventListener("click", exportMd);
  }

  document.addEventListener("DOMContentLoaded", init);
})();
