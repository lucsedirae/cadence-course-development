"use strict";
const byId = id => document.getElementById(id);
let questions = [], step = 0, busy = false;
const answers = {};
function element(tag, text) {
  const node = document.createElement(tag);
  if (text !== undefined) node.textContent = text;
  return node;
}
function error(message) {
  byId("error").textContent = message;
  byId("error").hidden = !message;
}
function render() {
  error("");
  const q = questions[step];
  const legend = element("legend", q.question);
  legend.tabIndex = -1;
  byId("question").replaceChildren(legend);
  byId("steps").replaceChildren(...questions.map((_, index) => {
    const item = element("li", `${index + 1}`);
    if (index === step) item.setAttribute("aria-current", "step");
    item.setAttribute("aria-label", `Question ${index + 1}${index < step ? ", answered" : ""}`);
    return item;
  }));
  if (q.type === "text") {
    const input = element("input");
    input.type = "text";
    input.id = q.id;
    input.name = q.id;
    input.required = true;
    input.maxLength = 160;
    input.autocomplete = "off";
    input.setAttribute("aria-label", q.question);
    input.placeholder = "e.g., Small-unit leadership";
    input.value = answers[q.id] || "";
    input.addEventListener("input", () => { answers[q.id] = input.value; error(""); });
    byId("question").append(input);
    input.focus();
  } else {
    const options = element("div");
    options.className = "options";
    for (const [value, text] of q.options) {
      const label = element("label");
      const input = element("input");
      input.type = "radio";
      input.name = q.id;
      input.value = value;
      input.required = true;
      input.checked = answers[q.id] === value;
      input.addEventListener("change", () => { answers[q.id] = value; error(""); });
      label.append(input, element("span", text));
      options.append(label);
    }
    byId("question").append(options);
    legend.focus();
  }
  byId("hint").textContent = q.hint || (step === 0 ? "You can refine the name later with Cadence." : q.options.some(([id]) => id === "unsure") ? "Not sure yet is fine—we can work it out together." : "Choose the option that best describes your role.");
  byId("back").hidden = step === 0;
  byId("next").textContent = step === questions.length - 1 ? "Save answers" : "Continue";
}
function saved(state) {
  byId("intake").hidden = true;
  byId("loading").hidden = true;
  byId("saved").hidden = false;
  if (state.status === "existing") {
    byId("saved-heading").textContent = "This course is already started.";
    byId("saved-note").textContent = "Return to chat to pick up where you left off. You don’t need to repeat intake.";
  } else {
    byId("answers").replaceChildren(...questions.flatMap(q => [element("dt", q.question),
      element("dd", !(q.id in state.answers) ? "Not asked in earlier intake" : q.type === "text" ? state.answers[q.id] : q.options.find(([id]) => id === state.answers[q.id])[1])]));
  }
  byId("saved").focus();
}
byId("back").addEventListener("click", () => { if (!busy && step > 0) { step--; render(); } });
byId("intake").addEventListener("submit", async event => {
  event.preventDefault();
  if (busy) return;
  const q = questions[step];
  if (!answers[q.id]?.trim()) { error("Please add an answer before continuing."); return; }
  if (step < questions.length - 1) { step++; render(); return; }
  busy = true;
  byId("next").disabled = byId("back").disabled = true;
  byId("next").textContent = "Saving…";
  error("");
  try {
    const response = await fetch("answers", {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify(answers), signal:AbortSignal.timeout(8000)});
    const state = await response.json();
    if (!response.ok) throw new Error(state.error || "Could not save your answers.");
    saved(state);
  } catch (failure) {
    error(failure.name === "TypeError" || failure.name === "TimeoutError" ? "Could not connect. Your entries are still here—retry or return to chat." : failure.message);
  } finally {
    busy = false;
    byId("next").disabled = byId("back").disabled = false;
    byId("next").textContent = "Save answers";
  }
});
(async () => {
  try {
    const response = await fetch("state", {cache:"no-store", signal:AbortSignal.timeout(8000)});
    const state = await response.json();
    if (!response.ok) throw new Error(state.error);
    questions = state.questions;
    byId("preview").hidden = !state.demo;
    byId("loading").hidden = true;
    if (state.status !== "pending") { saved(state); return; }
    byId("intake").hidden = false;
    render();
  } catch (_) {
    byId("loading").textContent = "Could not load the intake. Return to chat to reopen it.";
  }
})();
