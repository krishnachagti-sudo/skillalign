// SkillAlign front end. All the analysis happens in Python (engine/api.py),
// run in the browser by Pyodide. This file only loads it and draws results.

const PYODIDE_URL = "https://cdn.jsdelivr.net/pyodide/v0.28.3/full/";
let api = null;
let META = null;
const rendered = new Set();

const $ = (sel, root = document) => root.querySelector(sel);
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const pct = (x) => (x == null ? "–" : `${Math.round(x * 100)}%`);
const fmt = (n) => Number(n).toLocaleString("en-IN");
function growth(g) {
  if (g == null) return '<span class="mute">–</span>';
  if (g >= 9.9) return '<span class="up">new</span>';
  const v = Math.round(g * 100);
  if (v === 0) return '<span class="mute">0%</span>';
  return v > 0 ? `<span class="up">+${v}%</span>` : `<span class="down">−${-v}%</span>`;
}
function scoreColor(s) {
  return s >= 75 ? "var(--signal)" : s >= 50 ? "var(--warn)" : "var(--bad)";
}

// ---- Python bridge ----------------------------------------------------------
function call(fn, ...args) {
  try {
    return JSON.parse(api[fn](...args));
  } catch (err) {
    const lines = String(err.message || err).trim().split("\n");
    throw new Error(lines[lines.length - 1].replace(/^\w+Error: /, ""));
  }
}

async function boot() {
  const step = $("#boot-step");
  try {
    const pyodide = await loadPyodide({ indexURL: PYODIDE_URL });
    step.textContent = "Loading the SkillAlign engine and data…";
    const manifest = await (await fetch(`py/manifest.json?t=${Date.now()}`)).json();
    const files = manifest.files;
    pyodide.FS.mkdirTree("/app/engine");
    pyodide.FS.mkdirTree("/app/data");
    await Promise.all(files.map(async (f) => {
      const text = await (await fetch(`py/${f}?v=${manifest.version}`)).text();
      pyodide.FS.writeFile(`/app/${f}`, text);
    }));
    pyodide.runPython("import sys; sys.path.insert(0, '/app')");
    api = pyodide.pyimport("engine.api");
    step.textContent = "Reading job postings…";
    META = call("init", "/app/data");
    $("#boot").remove();
    setupStatic();
    showTab(location.hash.slice(1) || "pulse");
  } catch (err) {
    $("#boot").classList.add("failed");
    step.innerHTML = `Could not start: ${esc(err.message)}. Check your connection and reload.`;
    console.error(err);
  }
}

// ---- tabs -------------------------------------------------------------------
const RENDER = { pulse: renderPulse, programs: renderPrograms, matrix: renderMatrix,
  syllabus: renderSyllabusDetect, learner: () => {}, data: renderExtract, method: () => {} };

function showTab(name) {
  if (!RENDER[name]) name = "pulse";
  document.querySelectorAll(".tabs button").forEach((b) => b.setAttribute("aria-selected", b.dataset.tab === name));
  document.querySelectorAll(".tab").forEach((s) => (s.hidden = s.id !== `tab-${name}`));
  if (!rendered.has(name)) {
    rendered.add(name);
    RENDER[name]();
  }
  if (location.hash.slice(1) !== name) history.replaceState(null, "", `#${name}`);
}

document.querySelectorAll(".tabs button").forEach((b) => b.addEventListener("click", () => {
  if (api) showTab(b.dataset.tab);
}));

function dataChanged() {
  rendered.clear();
  $("#program-detail").innerHTML = "";
  $("#syllabus-result").innerHTML = "";
  $("#learner-result").innerHTML = "";
  $("#trend-card").hidden = true;
  setupStatic();
  const current = document.querySelector('.tabs [aria-selected="true"]').dataset.tab;
  rendered.add(current);
  RENDER[current]();
}

function setupStatic() {
  const q = META.quarters;
  const tag = META.source === "sample" ? '<span class="tag sample">Sample data</span>' : '<span class="tag uploaded">Your data</span>';
  $("#source").innerHTML = `${tag}<b>${fmt(META.postings)}</b> postings · ${esc(q[0] || "")} to ${esc(q[q.length - 1] || "")}`;
  fillSelect($("#f-sector"), META.sectors, "All sectors");
  fillSelect($("#f-city"), META.cities, "All cities");
  $("#role-list").innerHTML = META.roles.map(([r]) => `<option value="${esc(r)}">`).join("");
  $("#l-role").innerHTML = META.roles.map(([r, n]) => `<option value="${esc(r)}">${esc(titleCase(r))} (${n} postings)</option>`).join("");
  $("#m-skills").textContent = META.skills.length;
  if (META.roles.some(([r]) => r === "data analyst")) $("#l-role").value = "data analyst";
}

function fillSelect(sel, values, allLabel) {
  const keep = sel.value;
  sel.innerHTML = `<option value="">${allLabel}</option>` + values.map((v) => `<option>${esc(v)}</option>`).join("");
  sel.value = values.includes(keep) ? keep : "";
}
const titleCase = (s) => s.replace(/\b\w/g, (c) => c.toUpperCase()).replace(/\bPv\b/, "PV").replace(/\bEv\b/, "EV").replace(/\bCnc\b/, "CNC");

// ---- charts -----------------------------------------------------------------
function sparkline(series, w = 70, h = 22) {
  const ys = series.map((p) => p[1]);
  const max = Math.max(...ys, 0.01);
  const pts = ys.map((y, i) => `${(i / Math.max(ys.length - 1, 1)) * w},${h - 2 - (y / max) * (h - 4)}`).join(" ");
  return `<svg viewBox="0 0 ${w} ${h}" width="${w}" height="${h}" aria-hidden="true"><polyline points="${pts}" fill="none" stroke="var(--signal)" stroke-width="1.6"/></svg>`;
}

function lineChart(row) {
  const W = 640, H = 220, L = 40, R = 16, T = 12, B = 28;
  const series = row.series;
  const n = series.length;
  const steps = n + 3; // 4 forecast quarters after the last real one
  const max = Math.max(...series.map((p) => p[1]), row.forecast, 0.05) * 1.15;
  const x = (i) => L + (i / (steps)) * (W - L - R);
  const y = (v) => T + (1 - v / max) * (H - T - B);
  const pts = series.map((p, i) => `${x(i)},${y(p[1])}`).join(" ");
  const grid = [0, 0.25, 0.5, 0.75, 1].map((f) => {
    const v = max * f;
    return `<line x1="${L}" x2="${W - R}" y1="${y(v)}" y2="${y(v)}" stroke="var(--hair)"/><text x="${L - 6}" y="${y(v) + 4}" text-anchor="end">${Math.round(v * 100)}%</text>`;
  }).join("");
  const labels = series.map((p, i) => (i % 2 === 0 || n <= 6 ? `<text x="${x(i)}" y="${H - 8}" text-anchor="middle">${esc(p[0])}</text>` : "")).join("");
  const last = series[n - 1];
  const fx = x(n - 1 + 4);
  return `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Share of postings mentioning ${esc(row.name)} by quarter">
    ${grid}${labels}
    <polyline points="${pts}" fill="none" stroke="var(--signal)" stroke-width="2.4"/>
    ${series.map((p, i) => `<circle cx="${x(i)}" cy="${y(p[1])}" r="3" fill="var(--signal)"><title>${esc(p[0])}: ${pct(p[1])}</title></circle>`).join("")}
    <line x1="${x(n - 1)}" y1="${y(last[1])}" x2="${fx}" y2="${y(row.forecast)}" stroke="var(--signal)" stroke-width="2" stroke-dasharray="5 5"/>
    <circle cx="${fx}" cy="${y(row.forecast)}" r="4" fill="var(--paper)" stroke="var(--signal)" stroke-width="2"/>
    <text x="${fx}" y="${y(row.forecast) - 9}" text-anchor="end" style="fill:var(--ink-soft)">forecast ${pct(row.forecast)}</text>
  </svg>`;
}

function ring(value) {
  const r = 50, c = 2 * Math.PI * r, f = Math.max(0, Math.min(100, value)) / 100;
  return `<svg class="ring" viewBox="0 0 120 120" role="img" aria-label="Readiness ${Math.round(value)}%">
    <circle cx="60" cy="60" r="${r}" fill="none" stroke="var(--paper-sink)" stroke-width="12"/>
    <circle cx="60" cy="60" r="${r}" fill="none" stroke="${scoreColor(value)}" stroke-width="12" stroke-linecap="round"
      stroke-dasharray="${c * f} ${c}" transform="rotate(-90 60 60)"/>
    <text x="60" y="69" text-anchor="middle">${Math.round(value)}%</text></svg>`;
}

// ---- market pulse ------------------------------------------------------------
let PULSE = null;
function renderPulse() {
  PULSE = call("overview", $("#f-sector").value, $("#f-city").value);
  const o = PULSE;
  $("#kpis").innerHTML = [
    [fmt(o.postings), "postings analysed"],
    [o.skills_seen, "skills found in them"],
    [o.avg_alignment == null ? "–" : `${o.avg_alignment}`, "average program alignment (out of 100)"],
    [`${o.programs_total - countStrong()} of ${o.programs_total}`, "programs below Strong"],
  ].map(([v, l]) => `<div class="kpi"><div class="v">${v}</div><div class="l">${l}</div></div>`).join("");

  const max = Math.max(...o.top.map((r) => r.share), 0.01);
  $("#top-skills").innerHTML = o.top.length ? o.top.map((r) => `<li><button data-skill="${r.id}">
      <span class="name" title="${esc(r.name)}">${esc(r.name)}</span>
      <span class="track"><span class="fill" style="width:${(r.share / max) * 100}%"></span></span>
      <span class="num">${pct(r.share)}</span><span class="num">${growth(r.growth)}</span></button></li>`).join("")
    : '<li class="empty">No postings match these filters.</li>';
  const mover = (r) => `<li><button data-skill="${r.id}"><span>${esc(r.name)}<span class="sub">${pct(r.share)} of postings</span></span>${sparkline(r.series)}<span class="num">${growth(r.growth)}</span></button></li>`;
  $("#emerging").innerHTML = o.emerging.map(mover).join("") || '<li class="empty">Nothing is rising fast enough here.</li>';
  $("#declining").innerHTML = o.declining.map(mover).join("") || '<li class="empty">Nothing is clearly falling here.</li>';
}
function countStrong() {
  return call("programs_summary").filter((p) => p.grade === "Strong" && p.postings).length;
}

$("#tab-pulse").addEventListener("click", (e) => {
  const b = e.target.closest("[data-skill]");
  if (!b) return;
  const all = [...PULSE.top, ...PULSE.emerging, ...PULSE.declining];
  const row = all.find((r) => r.id === b.dataset.skill);
  $("#trend-title").textContent = `${row.name}: share of postings by quarter`;
  $("#trend-chart").innerHTML = lineChart(row);
  $("#trend-note").textContent = `${pct(row.share)} of postings in the latest four quarters (${fmt(row.postings)} postings). The dashed line is a straight-line forecast four quarters ahead.`;
  $("#trend-card").hidden = false;
  $("#trend-card").scrollIntoView({ behavior: "smooth", block: "nearest" });
});
$("#trend-close").addEventListener("click", () => ($("#trend-card").hidden = true));
$("#f-sector").addEventListener("change", renderPulse);
$("#f-city").addEventListener("change", renderPulse);

// ---- programs -----------------------------------------------------------------
function renderPrograms() {
  const rows = call("programs_summary");
  $("#program-list").innerHTML = `<div class="prow head"><span>Program</span><span class="col-meter">Alignment</span><span>Score</span><span>Next year</span><span class="col-hours">Hours on demand</span></div>` +
    rows.map((r) => `<button class="prow" data-program="${esc(r.id)}">
      <span class="pname">${esc(r.name)}<span class="psub">${esc(r.provider)} · ${esc(r.duration)} · ${fmt(r.postings)} matching postings</span></span>
      <span class="meter col-meter"><i style="width:${r.score}%;background:${scoreColor(r.score)}"></i></span>
      <span><b class="num">${Math.round(r.score)}</b> <span class="grade ${r.grade}">${r.grade}</span></span>
      <span class="num">${Math.round(r.future_score)} ${r.future_score < r.score - 2 ? '<span class="down">↓</span>' : r.future_score > r.score + 2 ? '<span class="up">↑</span>' : ""}</span>
      <span class="num col-hours">${Math.round(r.hours_on_demand_pct)}%</span></button>`).join("");
}

$("#program-list").addEventListener("click", (e) => {
  const b = e.target.closest("[data-program]");
  if (!b) return;
  document.querySelectorAll(".prow.active").forEach((x) => x.classList.remove("active"));
  b.classList.add("active");
  const report = call("program_report", b.dataset.program);
  $("#program-detail").innerHTML = reportHTML(report);
  $("#program-detail").scrollIntoView({ behavior: "smooth", block: "start" });
});

function reportHTML(r) {
  const recs = r.recommendations.length
    ? `<ul class="recs">${r.recommendations.map((x) => `<li><span class="act ${x.action}">${x.action}</span><span><b>${esc(x.skill)}</b>: ${esc(x.reason)}.</span></li>`).join("")}</ul>`
    : '<p class="mute">No changes needed: the program covers every core skill and nothing it teaches is low-demand.</p>';
  const skillsRows = r.skills.map((s) => `<tr>
      <td>${esc(s.name)}</td>
      <td class="bar"><div class="meter"><i style="width:${s.share * 100}%;background:var(--signal)"></i></div></td>
      <td class="num">${pct(s.share)}</td><td class="num">${growth(s.growth)}</td><td class="num">${pct(s.forecast)}</td>
      <td>${s.taught ? '<span class="yes">✓ taught</span>' : s.share >= 0.15 ? '<span class="no">✗ missing</span>' : '<span class="mute">not taught</span>'}</td>
      <td class="num">${s.hours ? s.hours : ""}</td></tr>`).join("");
  const modules = r.modules.map((m) => `<li><b>${esc(m.title)}</b><span class="num mute">${m.hours} h</span>
      <div class="chips">${m.skills.length ? m.skills.map((s) => `<span class="chip">${esc(s)}</span>`).join("") : '<span class="chip none">no in-demand skill detected</span>'}</div></li>`).join("");
  return `<div class="report">
    <div class="report-head"><div><h2>${esc(r.name)}</h2><p class="mute small">${esc(r.provider)}${r.duration ? " · " + esc(r.duration) : ""} · compared with ${fmt(r.postings)} postings for: ${r.target_roles.map(esc).join(", ")}</p></div>
      <button class="btn ghost" type="button" onclick='downloadReport(${JSON.stringify(r.id)})'>Download report</button></div>
    ${r.warning ? `<p class="notice">${esc(r.warning)}</p>` : ""}
    <div class="scores">
      <div class="kpi"><div class="v" style="color:${scoreColor(r.score)}">${Math.round(r.score)}</div><div class="l">alignment today · ${r.grade}</div></div>
      <div class="kpi"><div class="v">${Math.round(r.future_score)}</div><div class="l">alignment next year if unchanged</div></div>
      <div class="kpi"><div class="v">${r.covered_count} / ${r.core_count}</div><div class="l">core skills taught</div></div>
      <div class="kpi"><div class="v">${Math.round(r.hours_on_demand_pct)}%</div><div class="l">of ${fmt(r.hours_total)} training hours on core skills</div></div>
    </div>
    <article class="card"><h2>What to change</h2>${recs}</article>
    <article class="card"><h2>Skill by skill</h2>
      <div class="table-wrap"><table class="skills"><thead><tr><th>Skill</th><th>Share of postings</th><th></th><th>Year on year</th><th>Forecast</th><th>In program</th><th>Hours</th></tr></thead><tbody>${skillsRows}</tbody></table></div></article>
    <article class="card"><h2>Modules and the skills found in them</h2><ul class="modules">${modules}</ul></article>
  </div>`;
}

const LAST_REPORTS = {};
window.downloadReport = function (id) {
  const r = id === "custom" ? LAST_REPORTS.custom : call("program_report", id);
  const lines = [
    `# SkillAlign report: ${r.name}`, "",
    `Compared with ${r.postings} job postings for: ${r.target_roles.join(", ")} (${META.source === "sample" ? "sample data" : "uploaded data"}, ${META.quarters[0]} to ${META.quarters[META.quarters.length - 1]}).`, "",
    `- Alignment today: ${r.score} / 100 (${r.grade})`,
    `- Alignment next year if unchanged: ${r.future_score} / 100`,
    `- Core skills taught: ${r.covered_count} of ${r.core_count}`,
    `- Training hours on core skills: ${r.hours_on_demand_pct}% of ${r.hours_total}`, "",
    "## What to change", "",
    ...(r.recommendations.length ? r.recommendations.map((x) => `- **${x.action} ${x.skill}**: ${x.reason}.`) : ["- No changes needed."]), "",
    "## Skill by skill", "", "| Skill | Share | Year on year | Forecast | Taught | Hours |", "|---|---|---|---|---|---|",
    ...r.skills.map((s) => `| ${s.name} | ${pct(s.share)} | ${s.growth == null ? "-" : Math.round(s.growth * 100) + "%"} | ${pct(s.forecast)} | ${s.taught ? "yes" : "no"} | ${s.hours || ""} |`),
  ];
  const blob = new Blob([lines.join("\n")], { type: "text/markdown" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = `skillalign-${r.id}.md`;
  a.click();
  URL.revokeObjectURL(a.href);
};

// ---- matrix -------------------------------------------------------------------
function renderMatrix() {
  const m = call("matrix");
  const head = `<thead><tr><th></th>${m.skills.map((s) => `<th scope="col"><span>${esc(s.name)}</span></th>`).join("")}</tr></thead>`;
  const body = m.rows.map((row) => `<tr><th scope="row">${esc(row.name)}</th>${row.cells.map((c, i) => {
    const a = Math.min(0.95, c.share * 1.1);
    const cls = [a > 0.55 ? "dark" : "light", !c.taught && c.share >= 0.15 ? "gap" : ""].join(" ");
    const tip = `${row.name} · ${m.skills[i].name}: in ${pct(c.share)} of target postings, ${c.taught ? "taught" : "not taught"}`;
    return `<td class="${cls}" style="--a:${a.toFixed(2)}" title="${esc(tip)}">${c.taught ? "✓" : ""}</td>`;
  }).join("")}</tr>`).join("");
  $("#matrix").innerHTML = head + `<tbody>${body}</tbody>`;
}

// ---- syllabus -----------------------------------------------------------------
function renderSyllabusDetect() {
  const found = call("extract", $("#s-text").value);
  $("#syllabus-detected").innerHTML = `<p class="small mute" style="margin-bottom:.35rem">Skills found in this syllabus as you type:</p>
    <div class="chips">${found.length ? found.map((s) => `<span class="chip" title="matched: ${esc(s.matched.join(", "))}">${esc(s.name)}</span>`).join("") : '<span class="chip none">none yet</span>'}</div>`;
}
let detectTimer = null;
$("#s-text").addEventListener("input", () => {
  clearTimeout(detectTimer);
  detectTimer = setTimeout(() => api && renderSyllabusDetect(), 250);
});
$("#syllabus-form").addEventListener("submit", (e) => {
  e.preventDefault();
  const err = $("#s-error");
  err.hidden = true;
  try {
    const r = call("analyse_syllabus", $("#s-name").value, $("#s-roles").value, $("#s-text").value);
    LAST_REPORTS.custom = r;
    $("#syllabus-result").innerHTML = reportHTML(r);
    $("#syllabus-result").scrollIntoView({ behavior: "smooth", block: "start" });
  } catch (ex) {
    err.textContent = ex.message;
    err.hidden = false;
  }
});
$("#s-example").addEventListener("click", () => {
  $("#s-name").value = "Two-wheeler mechanic course";
  $("#s-roles").value = "automotive service technician, ev service technician";
  $("#s-text").value = "Petrol engine servicing and engine overhaul (120 hrs)\nBrakes, clutch and suspension (60 hrs)\nWorkshop safety and PPE (20 hrs)\nTalking to customers: customer service at the service desk (15 hrs)\nIntroduction to electric vehicles (10 hrs)";
  renderSyllabusDetect();
});

// ---- learner ------------------------------------------------------------------
$("#learner-form").addEventListener("submit", (e) => {
  e.preventDefault();
  const role = $("#l-role").value;
  const r = call("learner", role, "[]", $("#l-text").value);
  const req = r.required.map((s) => `<span class="chip ${s.have ? "have" : "none"}">${s.have ? "✓" : "✗"} ${esc(s.name)} <small>${pct(s.share)}</small></span>`).join("");
  const programs = r.programs.length
    ? `<ul class="recs">${r.programs.map((p) => `<li><span class="act Add">${esc(p.duration || "")}</span><span><b>${esc(p.name)}</b>${p.for_this_job ? '<span class="fit">built for this job</span>' : ""}<br>covers ${p.covers.map(esc).join(", ")}.</span></li>`).join("")}</ul>`
    : '<p class="mute">None of the listed programs teaches your missing skills.</p>';
  $("#learner-result").innerHTML = `<div class="report">
    <article class="card"><div class="ready">${ring(r.readiness)}<div>
      <h2>${Math.round(r.readiness)}% ready for ${esc(titleCase(role))}</h2>
      <p class="mute small">Weighted by how often each skill appears in ${fmt(r.postings)} postings for this job.</p>
      ${r.next_skill ? `<p style="margin-top:.5rem">Learn next: <b>${esc(r.next_skill.name)}</b>, asked for in ${pct(r.next_skill.share)} of these postings${r.next_skill.growth > 0 ? " and rising" : ""}.</p>` : "<p>You have every skill these postings commonly ask for.</p>"}
    </div></div></article>
    <article class="card"><h2>What employers ask for</h2><p class="mute small">Skills in at least 20% of postings. Green: you have it. Red: missing.</p><div class="chips">${req}</div>
      ${r.have.length ? `<p class="small mute">Skills we read from your text: ${r.have.map(esc).join(", ")}.</p>` : '<p class="small mute">We did not recognise any skills in your text. Try naming tools and topics, like "Excel" or "house wiring".</p>'}</article>
    <article class="card"><h2>Programs that close your gaps</h2>${programs}</article>
  </div>`;
});

// ---- your data ----------------------------------------------------------------
function renderExtract() {
  const found = call("extract", $("#x-text").value);
  $("#x-out").innerHTML = found.length
    ? found.map((s) => `<span class="chip"><b>${esc(s.name)}</b> <small>from “${esc(s.matched.join("”, “"))}”</small></span>`).join("")
    : '<span class="chip none">no skills recognised</span>';
}
$("#x-text").addEventListener("input", () => api && renderExtract());

$("#upload").addEventListener("change", async (e) => {
  const file = e.target.files[0];
  if (!file) return;
  const status = $("#upload-status");
  status.textContent = "Reading…";
  try {
    META = call("load_uploaded", await file.text());
    status.innerHTML = `Loaded <b>${fmt(META.postings)}</b> postings from ${esc(file.name)}.` +
      (META.problem_count ? ` Skipped ${META.problem_count} rows: ${META.problems.slice(0, 3).map(esc).join("; ")}${META.problem_count > 3 ? "…" : ""}` : "");
    dataChanged();
  } catch (ex) {
    status.innerHTML = `<span class="error">${esc(ex.message)}</span>`;
  }
  e.target.value = "";
});
$("#reset-sample").addEventListener("click", () => {
  META = call("use_sample");
  $("#upload-status").textContent = "Back on the sample data.";
  dataChanged();
});

boot();
