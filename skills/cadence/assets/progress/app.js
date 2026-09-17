"use strict";
const byId = id => document.getElementById(id);
const labels = {pending:"Not started",working:"In progress",waiting:"Waiting for you",blocked:"Blocked",complete:"Complete",skipped:"Skipped",queued:"Queued",interrupted:"Interrupted",draft:"Draft saved",checked:"Checked",missing:"File missing"};
const phaseNames = {analysis:"Analysis",design:"Design",development:"Development",implementation:"Implementation",evaluation:"Evaluation"};
const marks = {pending:"○",working:"●",waiting:"Ⅱ",blocked:"!",interrupted:"!",complete:"✓",skipped:"–"};
let latest = null;
let signature = "";
let connected = false;
let lastActivePhase = null;
function element(tag, text, className) {
  const node = document.createElement(tag);
  if (text !== undefined) node.textContent = text;
  if (className) node.className = className;
  return node;
}
function badge(status) {
  const node = element("span", labels[status] || status, "badge");
  node.dataset.status = status;
  return node;
}
function row(title, status, detail) {
  const item = element("li", undefined, "row");
  item.append(element("span", title, "row-title"), badge(status));
  if (detail) item.append(element("span", detail, "row-detail"));
  return item;
}
function clock() {
  if (!latest) return;
  const seconds = Math.max(0, Math.floor((Date.now() - Date.parse(latest.updated_at)) / 1000));
  const age = seconds < 60 ? "just now" : seconds < 3600 ? `${Math.floor(seconds / 60)} min ago` : `${Math.floor(seconds / 3600)} hr ago`;
  byId("updated").textContent = `Last recorded milestone ${age}` + (seconds >= 120 && latest.status === "working" ? " · Waiting for the next checkpoint" : "");
}
function renderSections(state) {
  const phases = Object.entries(state.sections || {});
  byId("sections-panel").hidden = phases.length === 0;
  const previous = new Map([...byId("sections").querySelectorAll("details")].map(node => [node.dataset.phase, node.open]));
  const active = Object.keys(state.phases).find(name => ["working", "waiting", "blocked"].includes(state.phases[name].status));
  byId("sections").replaceChildren(...phases.map(([phase, definitions]) => {
    const rows = Object.values(definitions);
    const done = rows.filter(row => row.status === "complete").length;
    const skipped = rows.filter(row => row.status === "skipped").length;
    const panel = element("details", undefined, "phase-sections");
    panel.dataset.phase = phase;
    panel.open = active === phase && active !== lastActivePhase ? true : previous.get(phase) ?? (phase === active);
    const summary = element("summary");
    summary.append(element("span", phaseNames[phase]), element("span", `${done} / ${rows.length} complete${skipped ? ` · ${skipped} skipped` : ""}`, "quiet"));
    panel.append(summary);
    if (phase !== "development" && rows.length) panel.append(element("p", rows[0].document, "section-document"));
    let group = null;
    let list;
    for (const section of rows) {
      if (section.group !== group) {
        group = section.group;
        if (group) panel.append(element("h3", group, "section-group"));
        list = element("ul", undefined, "checklist");
        panel.append(list);
      }
      const item = element("li", undefined, "check-row");
      item.dataset.status = section.status;
      item.dataset.sectionId = section.id;
      const marker = element("span", marks[section.status] || "!", "check-marker");
      marker.setAttribute("aria-hidden", "true");
      item.append(marker, element("span", `${section.number} ${section.title}`, "check-title"), badge(section.status));
      const evidence = (section.files || []).map(file => file.split("/").pop()).join(" · ");
      if (evidence || section.note) item.append(element("span", [evidence, section.note].filter(Boolean).join(" · "), "check-detail"));
      list.append(item);
    }
    return panel;
  }));
  lastActivePhase = active;
}
function render(state) {
  latest = state;
  byId("title").textContent = state.title;
  byId("mode").textContent = {review:"Course review",build:"Course development",revise:"Curriculum revision",orient:"Course planning"}[state.mode] || state.mode;
  byId("profile").hidden = !state.intake;
  byId("profile-answers").replaceChildren(...(state.intake || []).flatMap(item => [element("dt", item.question), element("dd", item.answer)]));
  byId("demo").hidden = !state.demo;
  byId("run-status").textContent = labels[state.status] || state.status;
  byId("run-status").dataset.status = state.status;
  byId("note").textContent = state.note;
  const completed = Object.values(state.phases).filter(p => p.status === "complete").length;
  const skipped = Object.values(state.phases).filter(p => p.status === "skipped").length;
  byId("phase-count").textContent = `${completed} of 5 completed` + (skipped ? ` · ${skipped} skipped` : "");
  byId("phases").replaceChildren(...Object.entries(state.phases).map(([name, phase]) => {
    const item = element("li", undefined, "phase");
    item.dataset.status = phase.status;
    if (phase.status === "working") item.setAttribute("aria-current", "step");
    const marker = element("span", undefined, "phase-marker");
    marker.setAttribute("aria-hidden", "true");
    marker.append(element("span", marks[phase.status], "phase-dot"));
    item.append(marker, element("span", phaseNames[name], "phase-name"), element("span", labels[phase.status], "phase-state"));
    if (phase.note) item.append(element("p", phase.note, "phase-note"));
    return item;
  }));
  renderSections(state);
  const agents = Object.values(state.agents);
  byId("agents").replaceChildren(...agents.map(a => row(a.role, a.status, `${a.execution === "native" ? "Subagent" : "Sequential check"}${a.note ? ` · ${a.note}` : ""}`)));
  byId("no-agents").hidden = agents.length > 0;
  const artifacts = Object.entries(state.artifacts);
  byId("artifacts").replaceChildren(...artifacts.map(([path, a]) => row(a.label, a.exists ? a.status : "missing", path)));
  byId("no-artifacts").hidden = artifacts.length > 0;
  byId("libraries").textContent = state.libraries ? `Available sources: ${state.libraries.content} course content · ${state.libraries.institution} institutional. Availability does not mean reviewed.` : "Source-library counts are not available yet.";
  byId("events").replaceChildren(...[...state.events].reverse().map(event => {
    const item = element("li");
    const date = new Date(event.at);
    const time = element("time", date.toLocaleTimeString([], {hour:"2-digit", minute:"2-digit"}));
    time.dateTime = event.at;
    item.append(time, element("span", event.message));
    return item;
  }));
  clock();
}
async function refresh() {
  try {
    const response = await fetch("state", {cache:"no-store", signal:AbortSignal.timeout(5000)});
    if (!response.ok) throw new Error("Progress unavailable");
    const state = await response.json();
    const nextSignature = JSON.stringify(state);
    if (signature !== nextSignature) {
      render(state);
      signature = nextSignature;
      byId("connection").textContent = "Connected · Latest saved progress";
    } else if (!connected) byId("connection").textContent = "Connected · Latest saved progress";
    byId("connection").classList.remove("offline");
    connected = true;
  } catch (_) {
    if (connected || !latest) byId("connection").textContent = "Disconnected · Showing the last received milestone. Reopen the progress viewer to reconnect.";
    byId("connection").classList.add("offline");
    connected = false;
  }
  setTimeout(refresh, 2000);
}
setInterval(clock, 1000);
refresh();
