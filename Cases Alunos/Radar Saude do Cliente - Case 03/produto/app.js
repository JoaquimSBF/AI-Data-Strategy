(function () {
  "use strict";

  var STORAGE_KEY = "client-health-radar-v1";
  var MAX_BYTES = 5 * 1024 * 1024;
  var CHURN_FORBIDDEN = /probabilidade de churn|% de churn|churn_clientes_pct\s*=\s*\d/i;
  var state = { data: null, segmento: "todos", nivel: "todos", cliente: "CL02", backlog: [], historico: [] };

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
  function evid(id) {
    return (state.data.evidencias || []).find(function (item) { return item.evidencia_id === id; }) || null;
  }
  function save() {
    localStorage.setItem(STORAGE_KEY, JSON.stringify({
      schemaVersion: 1,
      segmento: state.segmento,
      nivel: state.nivel,
      cliente: state.cliente,
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
      if (parsed.segmento) state.segmento = parsed.segmento;
      if (parsed.nivel) state.nivel = parsed.nivel;
      if (parsed.cliente) state.cliente = parsed.cliente;
      if (Array.isArray(parsed.backlog)) state.backlog = parsed.backlog;
      if (Array.isArray(parsed.historico)) state.historico = parsed.historico;
    } catch (err) {
      text($("status-app"), "Dados locais ignorados por esquema inválido.");
    }
  }
  function cloneSample() { return JSON.parse(JSON.stringify(window.SAMPLE_DATA)); }
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

  function metaDoKpi(kpi) {
    return (state.data.metas || []).find(function (row) { return row.kpi === kpi; }) || null;
  }
  function kpiValor(nome) {
    var row = (state.data.kpis || []).find(function (item) { return item.kpi === nome; });
    return row ? row.valor : "sem evidencia";
  }
  function filtrados() {
    return state.data.sinais.filter(function (row) {
      var okSeg = state.segmento === "todos" || row.segmento === state.segmento;
      var okNivel = state.nivel === "todos" || row.nivel_sinal === state.nivel;
      return okSeg && okNivel;
    });
  }

  function renderExecutiva() {
    var root = $("view-executiva");
    clear(root);
    root.appendChild(el("h2", {}, ["Visão executiva"]));
    root.appendChild(el("p", { className: "warn" }, [
      "Sinal ≠ alerta ≠ inativo ≠ churn. Score é soma de flags. churn_clientes_pct = sem evidencia."
    ]));
    var cards = el("div", { className: "kpis" });
    function card(label, value, metaRow, evidId, klass) {
      cards.appendChild(el("article", { className: "card " + (klass || "") }, [
        el("span", { className: "label" }, [label]),
        el("span", { className: "value" }, [String(value)]),
        el("p", {}, [metaRow ? ("Meta " + metaRow.meta + " · " + metaRow.status) : "sem meta neste recorte"]),
        el("button", { type: "button", onClick: function () { openEvidence(evidId); } }, ["Ver evidência"])
      ]));
    }
    var alto = metaDoKpi("clientes_com_sinal_alto");
    var sla = metaDoKpi("tickets_sla_estourado");
    var churn = metaDoKpi("churn_clientes_pct");
    card("Clientes válidos", kpiValor("clientes_validos"), null, "EVD-001");
    card("Sinal alto", kpiValor("clientes_com_sinal_alto"), alto, "EVD-009", alto && alto.status === "atingida" ? "ok" : "bad");
    card("SLA estourado", kpiValor("tickets_sla_estourado"), sla, "EVD-003", sla && sla.status === "atingida" ? "ok" : "bad");
    card("Churn mensal", "sem evidencia", churn, "EVD-007");
    root.appendChild(cards);
  }

  function tableFrom(headers, rows) {
    var table = el("table", {}, []);
    table.appendChild(el("thead", {}, [el("tr", {}, headers.map(function (h) { return el("th", {}, [h]); }))]));
    var body = el("tbody", {}, []);
    rows.forEach(function (row) {
      body.appendChild(el("tr", {}, row.map(function (c) { return el("td", {}, [String(c)]); })));
    });
    table.appendChild(body);
    return table;
  }

  function renderCarteira() {
    var root = $("view-carteira");
    clear(root);
    root.appendChild(el("h2", {}, ["Carteira"]));
    var rows = filtrados().map(function (row) {
      return [row.cliente_id, row.segmento, row.status, row.score_risco, row.nivel_sinal, row.nps, row.atraso_dias_max, row.tickets_abertos, row.churn_confirmado];
    });
    root.appendChild(tableFrom(["cliente", "segmento", "status", "score", "nível", "nps", "atraso", "tickets", "churn"], rows));
    root.appendChild(el("button", { type: "button", onClick: function () { openEvidence("EVD-002"); } }, ["Ver evidência"]));
  }

  function renderCliente() {
    var root = $("view-cliente");
    clear(root);
    root.appendChild(el("h2", {}, ["Cliente"]));
    var select = el("select", { onChange: function (ev) { state.cliente = ev.target.value; save(); renderCliente(); } },
      state.data.sinais.map(function (row) { return el("option", { value: row.cliente_id }, [row.cliente_id]); })
    );
    select.value = state.cliente;
    root.appendChild(select);
    var row = state.data.sinais.find(function (item) { return item.cliente_id === state.cliente; });
    if (!row) {
      root.appendChild(el("p", {}, ["sem evidencia"]));
      return;
    }
    root.appendChild(el("p", { className: "warn" }, ["churn_confirmado: " + row.churn_confirmado]));
    root.appendChild(tableFrom(
      ["campo", "valor"],
      ["cliente_id", "segmento", "status", "score_risco", "nivel_sinal", "nps", "atraso_dias_max", "ausencias", "tickets_abertos", "tickets_sla"].map(function (key) {
        return [key, row[key]];
      })
    ));
    var evidId = row.cliente_id === "CL02" ? "EVD-004" : row.cliente_id === "CL04" ? "EVD-005" : row.cliente_id === "CL06" ? "EVD-006" : "EVD-001";
    root.appendChild(el("button", { type: "button", onClick: function () { openEvidence(evidId); } }, ["Ver evidência"]));
  }

  function renderSinais() {
    var root = $("view-sinais");
    clear(root);
    root.appendChild(el("h2", {}, ["Sinais"]));
    root.appendChild(el("p", { className: "warn" }, ["Flags binários. Score não é probabilidade de churn."]));
    var rows = filtrados().map(function (row) {
      return [row.cliente_id, row.atraso_projeto, row.ausencia_evento, row.ticket_aberto, row.sla_estourado, row.nps_baixo, row.nps_ausente, row.status_inativo, row.score_risco];
    });
    root.appendChild(tableFrom(["cliente", "atraso", "ausência", "ticket", "SLA", "NPS baixo", "NPS ausente", "inativo", "score"], rows));
    root.appendChild(el("button", { type: "button", onClick: function () { openEvidence("EVD-007"); } }, ["Ver evidência"]));
  }

  function updateOpp(id, field, value) {
    if (field === "nota" && CHURN_FORBIDDEN.test(value || "")) {
      setStatus("Rótulo de probabilidade de churn bloqueado.");
      return;
    }
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
    root.appendChild(el("h2", {}, ["Ações"]));
    var statuses = ["nova", "em_analise", "aprovada", "em_execucao", "concluida", "descartada"];
    var board = el("div", { className: "kanban" });
    statuses.forEach(function (status) {
      var col = el("div", { className: "col" }, [el("h3", {}, [status])]);
      state.backlog.filter(function (item) { return item.status === status; }).forEach(function (item) {
        var select = el("select", { value: item.status, onChange: function (ev) { updateOpp(item.oportunidade_id, "status", ev.target.value); } },
          statuses.map(function (st) { return el("option", { value: st }, [st]); })
        );
        select.value = item.status;
        col.appendChild(el("article", { className: "ticket" }, [
          el("strong", {}, [item.oportunidade_id + " · " + item.titulo]),
          el("p", {}, [item.problema_observado]),
          el("p", {}, ["cliente " + (item.cliente_id || "carteira") + " · " + item.responsavel_sugerido]),
          el("p", {}, ["evidências: " + (item.evidencias || []).join(", ")]),
          select,
          el("input", { value: item.nota || "", placeholder: "nota", onChange: function (ev) { updateOpp(item.oportunidade_id, "nota", ev.target.value); } }),
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
        if (CHURN_FORBIDDEN.test(content)) {
          log.appendChild(document.createTextNode(file.name + ": rótulo de churn inventado, arquivo bloqueado\n"));
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
  function download(name, content, type) {
    var blob = new Blob([content], { type: type });
    var url = URL.createObjectURL(blob);
    var link = el("a", { href: url, download: name }, []);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  }
  function exportJson() { download("acoes.json", JSON.stringify(state.backlog, null, 2), "application/json"); }
  function exportCsv() {
    var header = ["oportunidade_id", "titulo", "status", "cliente_id", "responsavel_sugerido", "nota"];
    var lines = [header.join(",")].concat(state.backlog.map(function (item) {
      return header.map(function (key) { return csvEscape(item[key]); }).join(",");
    }));
    download("acoes.csv", lines.join("\n"), "text/csv");
  }
  function exportMd() {
    var lines = [
      "# Resumo Radar de Saúde do Cliente",
      "",
      "fato_observado: clientes_com_sinal_alto = " + kpiValor("clientes_com_sinal_alto") + ".",
      "fato_observado: churn_clientes_pct = sem evidencia.",
      "limitacao: score não é probabilidade."
    ];
    download("resumo.md", lines.join("\n"), "text/markdown");
  }

  function renderAll() {
    renderExecutiva();
    renderCarteira();
    renderCliente();
    renderSinais();
    renderOps();
  }

  function fillFiltros() {
    var seg = $("filtro-segmento");
    var niv = $("filtro-nivel");
    clear(seg);
    clear(niv);
    seg.appendChild(el("option", { value: "todos" }, ["Todos"]));
    niv.appendChild(el("option", { value: "todos" }, ["Todos"]));
    var segs = {};
    var niveis = {};
    state.data.sinais.forEach(function (row) {
      segs[row.segmento] = true;
      niveis[row.nivel_sinal] = true;
    });
    Object.keys(segs).forEach(function (value) { seg.appendChild(el("option", { value: value }, [value])); });
    Object.keys(niveis).forEach(function (value) { niv.appendChild(el("option", { value: value }, [value])); });
    seg.value = state.segmento;
    niv.value = state.nivel;
  }

  function init() {
    if (!window.SAMPLE_DATA) {
      setStatus("sem evidencia de demonstração.");
      return;
    }
    state.data = cloneSample();
    state.backlog = cloneSample().oportunidades;
    loadLocal();
    fillFiltros();
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
    $("filtro-segmento").addEventListener("change", function (ev) {
      state.segmento = ev.target.value;
      save();
      renderAll();
    });
    $("filtro-nivel").addEventListener("change", function (ev) {
      state.nivel = ev.target.value;
      save();
      renderAll();
    });
    $("btn-restaurar").addEventListener("click", function () {
      localStorage.removeItem(STORAGE_KEY);
      state.data = cloneSample();
      state.backlog = cloneSample().oportunidades;
      state.historico = [];
      state.segmento = "todos";
      state.nivel = "todos";
      state.cliente = "CL02";
      fillFiltros();
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
