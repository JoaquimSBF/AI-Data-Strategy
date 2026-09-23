(function () {
  "use strict";

  var STORAGE_KEY = "discovery-workbench-v1";
  var MAX_BYTES = 5 * 1024 * 1024;
  var state = { data: null, tipo: "todos", backlog: [], historico: [] };

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
      tipo: state.tipo,
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
      if (parsed.tipo) state.tipo = parsed.tipo;
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

  function renderExecutiva() {
    var root = $("view-executiva");
    clear(root);
    root.appendChild(el("h2", {}, ["Visão executiva"]));
    root.appendChild(el("p", { className: "warn" }, [
      "Sem evidencia_id não existe requisito. Prazo oficial e aprovador único = nao_definido. E99 é texto, não ordem."
    ]));
    var cards = el("div", { className: "kpis" });
    function card(label, value, metaRow, evidId) {
      var ok = metaRow && metaRow.status === "atingida";
      var missing = metaRow && metaRow.status === "sem evidencia";
      cards.appendChild(el("article", { className: "card " + (missing ? "" : metaRow ? (ok ? "ok" : "bad") : "") }, [
        el("span", { className: "label" }, [label]),
        el("span", { className: "value" }, [String(value)]),
        el("p", {}, [metaRow ? ("Meta " + metaRow.meta + " · " + metaRow.status) : "sem meta neste recorte"]),
        el("button", { type: "button", onClick: function () { openEvidence(evidId); } }, ["Ver evidência"])
      ]));
    }
    card("Requisitos com fonte", "100%", metaDoKpi("pct_requisitos_com_fonte"), "EVD-007");
    card("Perguntas abertas", "18,18%", metaDoKpi("pct_perguntas_abertas"), "EVD-008");
    card("Requisitos MVP", "7", metaDoKpi("requisitos_mvp"), "EVD-009");
    card("Conflitos abertos", "1", null, "EVD-005");
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

  function renderEvidencias() {
    var root = $("view-evidencias");
    clear(root);
    root.appendChild(el("h2", {}, ["Evidências"]));
    var rows = state.data.atas.filter(function (row) {
      return state.tipo === "todos" || row.tipo === state.tipo;
    }).map(function (row) {
      return [row.evidencia_id, row.reuniao_id, row.tipo, row.texto, row.confiabilidade];
    });
    root.appendChild(tableFrom(["id", "reunião", "tipo", "texto", "confiabilidade"], rows));
    root.appendChild(el("button", { type: "button", onClick: function () { openEvidence("EVD-002"); } }, ["Ver evidência"]));
  }

  function renderRequisitos() {
    var root = $("view-requisitos");
    clear(root);
    root.appendChild(el("h2", {}, ["Requisitos"]));
    root.appendChild(el("p", { className: "warn" }, ["Não há oitavo requisito. Completar a meta 8 seria invenção."]));
    var rows = state.data.requisitos.filter(function (row) {
      return state.tipo === "todos" || row.tipo === state.tipo;
    }).map(function (row) {
      return [row.requisito_id, row.evidencia_id, row.tipo, row.titulo, row.papel_aprovador, row.status];
    });
    root.appendChild(tableFrom(["requisito", "fonte", "tipo", "titulo", "aprovador", "status"], rows));
    root.appendChild(el("button", { type: "button", onClick: function () { openEvidence("EVD-003"); } }, ["Ver evidência"]));
  }

  function renderConflitos() {
    var root = $("view-conflitos");
    clear(root);
    root.appendChild(el("h2", {}, ["Conflitos"]));
    root.appendChild(el("p", { className: "warn" }, ["Prazo oficial = nao_definido."]));
    root.appendChild(tableFrom(
      ["id", "fonte", "descricao", "status"],
      state.data.conflitos.map(function (row) { return [row.conflito_id, row.evidencia_id, row.descricao, row.status]; })
    ));
    root.appendChild(tableFrom(
      ["id", "fonte", "descricao", "origem"],
      state.data.fora.map(function (row) { return [row.item_id, row.evidencia_id, row.descricao, row.origem]; })
    ));
    root.appendChild(el("button", { type: "button", onClick: function () { openEvidence("EVD-005"); } }, ["Ver evidência"]));
  }

  function renderPerguntas() {
    var root = $("view-perguntas");
    clear(root);
    root.appendChild(el("h2", {}, ["Perguntas abertas"]));
    root.appendChild(tableFrom(
      ["id", "fonte", "pergunta", "status"],
      state.data.perguntas.map(function (row) { return [row.pergunta_id, row.evidencia_id, row.pergunta, row.status]; })
    ));
    root.appendChild(el("button", { type: "button", onClick: function () { openEvidence("EVD-004"); } }, ["Ver evidência"]));
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
    root.appendChild(el("h2", {}, ["Aprovação"]));
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
          el("p", {}, ["papel " + item.responsavel_sugerido + " · prioridade " + item.prioridade]),
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
  function exportJson() { download("backlog.json", JSON.stringify(state.backlog, null, 2), "application/json"); }
  function exportCsv() {
    var header = ["requisito_id", "evidencia_id", "titulo", "papel_aprovador"];
    var lines = [header.join(",")].concat(state.data.requisitos.map(function (item) {
      return header.map(function (key) { return csvEscape(item[key]); }).join(",");
    }));
    download("matriz_rastreabilidade.csv", lines.join("\n"), "text/csv");
  }
  function exportMd() {
    var lines = ["# Matriz de rastreabilidade", ""].concat(state.data.requisitos.map(function (row) {
      return "- " + row.requisito_id + " ← " + row.evidencia_id + ": " + row.titulo;
    }));
    lines.push("", "Prazo oficial: nao_definido.", "Aprovador único: nao_definido.");
    download("rastreabilidade.md", lines.join("\n"), "text/markdown");
  }

  function renderAll() {
    renderExecutiva();
    renderEvidencias();
    renderRequisitos();
    renderConflitos();
    renderPerguntas();
    renderOps();
  }

  function fillFiltro() {
    var select = $("filtro-tipo");
    clear(select);
    select.appendChild(el("option", { value: "todos" }, ["Todos"]));
    var tipos = {};
    state.data.atas.forEach(function (row) { tipos[row.tipo] = true; });
    Object.keys(tipos).forEach(function (tipo) {
      select.appendChild(el("option", { value: tipo }, [tipo]));
    });
    select.value = state.tipo;
  }

  function init() {
    if (!window.SAMPLE_DATA) {
      setStatus("sem evidencia de demonstração.");
      return;
    }
    state.data = cloneSample();
    state.backlog = cloneSample().oportunidades;
    loadLocal();
    fillFiltro();
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
    $("filtro-tipo").addEventListener("change", function (ev) {
      state.tipo = ev.target.value;
      save();
      renderAll();
    });
    $("btn-restaurar").addEventListener("click", function () {
      localStorage.removeItem(STORAGE_KEY);
      state.data = cloneSample();
      state.backlog = cloneSample().oportunidades;
      state.historico = [];
      state.tipo = "todos";
      fillFiltro();
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
