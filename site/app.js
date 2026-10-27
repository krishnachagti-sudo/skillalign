// SkillAlign front end. All the analysis happens in Python (engine/api.py),
// run in the browser by Pyodide. This file only loads it and draws results.

const VERSION = window.SKILLALIGN_VERSION || "dev";
let api = null;
let PY = null;
let MANIFEST = null;
let META = null;
const rendered = new Set();

const $ = (sel, root = document) => root.querySelector(sel);
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const pct = (x) => (x == null ? "–" : `${Math.round(x * 100)}%`);
const fmt = (n) => Number(n).toLocaleString("en-IN");
const range = (lo, hi) => (lo == null ? "" : `${Math.round(lo * 100)}–${Math.round(hi * 100)}%`);

function growth(row) {
  if (row.is_new) return '<span class="up">new</span>';
  const g = row.growth;
  if (g == null) return '<span class="mute">–</span>';
  const v = Math.round(g * 100);
  const cls = !row.significant ? "mute" : v > 0 ? "up" : v < 0 ? "down" : "mute";
  const txt = v > 0 ? `+${v}%` : v < 0 ? `−${-v}%` : "0%";
  return `<span class="${cls}" title="${row.significant ? "beyond chance" : "within chance: not a trend"}">${txt}</span>`;
}
const growthText = (row) => (row.is_new ? "new" : row.growth == null ? "-" : `${Math.round(row.growth * 100)}%${row.significant ? "" : " (not significant)"}`);
const scoreColor = (s) => (s >= 75 ? "var(--signal)" : s >= 50 ? "var(--warn)" : "var(--bad)");
const borderline = (r) => r.score_low != null && [50, 75].some((cut) => r.score_low < cut && r.score_high >= cut);
const titleCase = (s) => s.replace(/\b\w/g, (c) => c.toUpperCase()).replace(/\bPv\b/, "PV").replace(/\bEv\b/, "EV").replace(/\bCnc\b/, "CNC").replace(/\bAc\b/, "AC");

// ---- Python bridge ----------------------------------------------------------
function call(fn, ...args) {
  try {
    return JSON.parse(api[fn](...args));
  } catch (err) {
    const lines = String(err.message || err).trim().split("\n");
    throw new Error(lines[lines.length - 1].replace(/^\w+Error: /, "").replace(/^['"]|['"]$/g, ""));
  }
}

async function fetchText(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`could not load ${url} (${res.status})`);
  return res.text();
}

async function boot() {
  const step = $("#boot-step");
  try {
    if (typeof loadPyodide !== "function") throw new Error("the Python runtime did not load");
    const pyodide = await loadPyodide({ indexURL: new URL("vendor/pyodide/", location.href).href });
    step.textContent = "Loading the SkillAlign engine and data…";
    const manifest = (MANIFEST = JSON.parse(await fetchText(`py/manifest.json?v=${VERSION}`)));
    PY = pyodide;
    pyodide.FS.mkdirTree("/app/engine");
    pyodide.FS.mkdirTree("/app/data");
    await Promise.all(manifest.files.map(async (f) => {
      pyodide.FS.writeFile(`/app/${f}`, await fetchText(`py/${f}?v=${manifest.version}`));
    }));
    pyodide.runPython("import sys; sys.path.insert(0, '/app')");
    api = pyodide.pyimport("engine.api");
    step.textContent = "Reading job postings…";
    META = call("init", "/app/data");
    $("#boot")?.remove();
    setupStatic();
    showTab(location.hash.slice(1) || "pulse");
    if ("serviceWorker" in navigator && location.protocol === "https:") navigator.serviceWorker.register("sw.js").catch(() => {});
  } catch (err) {
    const boot = $("#boot");
    if (boot) {
      boot.classList.add("failed");
      step.innerHTML = `Could not start: ${esc(err.message)}. Check your connection and reload.`;
    }
    console.error(err);
  }
}

// ---- tabs -------------------------------------------------------------------
const RENDER = {
  pulse: renderPulse, programs: renderPrograms, matrix: renderMatrix,
  syllabus: renderSyllabusDetect, learner: () => {}, data: renderExtract, method: () => {},
};
const TABS = [...document.querySelectorAll('.tabs [role="tab"]')];

function showTab(name, focus = false) {
  if (!Object.hasOwn(RENDER, name)) name = "pulse";
  TABS.forEach((b) => {
    const on = b.dataset.tab === name;
    b.setAttribute("aria-selected", on);
    b.tabIndex = on ? 0 : -1;
    if (on && focus) b.focus();
  });
  document.querySelectorAll(".tab").forEach((s) => (s.hidden = s.id !== `tab-${name}`));
  if (!rendered.has(name)) {
    rendered.add(name);
    RENDER[name]();
  }
  if (location.hash.slice(1) !== name) history.replaceState(null, "", `#${name}`);
}

TABS.forEach((b, i) => {
  b.addEventListener("click", () => api && showTab(b.dataset.tab));
  b.addEventListener("keydown", (e) => {
    const next = { ArrowRight: i + 1, ArrowLeft: i - 1, Home: 0, End: TABS.length - 1 }[e.key];
    if (next == null || !api) return;
    e.preventDefault();
    showTab(TABS[(next + TABS.length) % TABS.length].dataset.tab, true);
  });
});
window.addEventListener("hashchange", () => api && showTab(location.hash.slice(1)));

function currentTab() {
  return TABS.find((b) => b.getAttribute("aria-selected") === "true")?.dataset.tab || "pulse";
}

function dataChanged() {
  rendered.clear();
  for (const id of ["#program-detail", "#syllabus-result", "#learner-result"]) $(id).innerHTML = "";
  $("#trend-card").hidden = true;
  delete LAST_REPORTS.custom;
  setupStatic();
  const tab = currentTab();
  rendered.add(tab);
  RENDER[tab]();
}

const SHORT = { sample: "Synthetic demo data", real: "Real postings: India 2026", uploaded: "Your uploaded file" };

function setupStatic() {
  const q = META.quarters;
  const ds = $("#dataset");
  const names = Object.keys(META.datasets).concat(META.source === "uploaded" ? ["uploaded"] : []);
  ds.innerHTML = names.map((k) => `<option value="${esc(k)}">${esc(SHORT[k] || k)}</option>`).join("");
  ds.value = META.source;
  ds.disabled = false;
  $("#source").innerHTML = `<b>${fmt(META.postings)}</b> postings · ${esc(q[0] || "")} to ${esc(q[q.length - 1] || "")}`;
  const banner = $("#demo-banner");
  banner.classList.toggle("real", META.source !== "sample");
  if (META.source === "sample") {
    banner.innerHTML = '<b>Demo data.</b> These job postings are synthetic, generated to show how the method works, so the numbers are not facts about real jobs. Switch the data menu to <b>Real postings</b>, or <a href="#data">upload your own</a>.';
  } else if (META.source === "real") {
    banner.innerHTML = `<b>Real postings.</b> ${fmt(META.postings)} Indian job ads, ${esc(q[0])} to ${esc(q[q.length - 1])}, from Fliar Research (<a href="https://huggingface.co/datasets/fliarbi/job-postings-2026">CC BY-NC 4.0</a>). Two quarters only, so shares and scores but no trends or forecasts. Online job boards list few vocational jobs, so trade courses may have no matching postings.`;
  } else {
    banner.innerHTML = q.length < 6 ? `<b>Your data.</b> ${q.length} quarter${q.length === 1 ? "" : "s"} of postings: shares and scores, but at least six quarters are needed for forecasts and eight for year-on-year trends.` : "<b>Your data.</b> Every number on the site is computed from your file.";
  }
  banner.hidden = false;
  fillSelect($("#f-sector"), META.sectors, "All sectors");
  fillSelect($("#f-state"), META.states, "All states");
  $("#f-state-wrap").hidden = META.states.length < 2;
  fillSelect($("#f-district"), META.districts, "All districts");
  $("#role-list").innerHTML = META.roles.map(([r]) => `<option value="${esc(r)}">`).join("");
  $("#l-role").innerHTML = META.roles.map(([r, n]) => `<option value="${esc(r)}">${esc(titleCase(r))} (${n} postings)</option>`).join("");
  if (META.roles.some(([r]) => r === "data analyst")) $("#l-role").value = "data analyst";
  $("#m-skills").textContent = META.skills.length;
  $("#m-syn").textContent = META.synonyms;
}

function fillSelect(sel, values, allLabel) {
  const keep = sel.value;
  sel.innerHTML = `<option value="">${allLabel}</option>` + values.map((v) => `<option>${esc(v)}</option>`).join("");
  sel.value = values.includes(keep) ? keep : "";
}

function busy(on) {
  document.body.classList.toggle("busy", on);
}

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
  const steps = row.forecast_ok ? n + 3 : Math.max(n - 1, 1);
  const max = Math.max(...series.map((p) => p[1]), row.forecast_ok ? row.forecast : 0, 0.05) * 1.15;
  const x = (i) => L + (i / steps) * (W - L - R);
  const y = (v) => T + (1 - v / max) * (H - T - B);
  const pts = series.map((p, i) => `${x(i)},${y(p[1])}`).join(" ");
  const grid = [0, 0.25, 0.5, 0.75, 1].map((f) => {
    const v = max * f;
    return `<line x1="${L}" x2="${W - R}" y1="${y(v)}" y2="${y(v)}" stroke="var(--hair)"/><text x="${L - 6}" y="${y(v) + 4}" text-anchor="end">${Math.round(v * 100)}%</text>`;
  }).join("");
  const labels = series.map((p, i) => (i % 2 === 0 || n <= 6 ? `<text x="${x(i)}" y="${H - 8}" text-anchor="middle">${esc(p[0])}</text>` : "")).join("");
  const last = series[n - 1];
  const fx = x(n - 1 + 4);
  const forecast = row.forecast_ok ? `<line x1="${x(n - 1)}" y1="${y(last[1])}" x2="${fx}" y2="${y(row.forecast)}" stroke="var(--signal)" stroke-width="2" stroke-dasharray="5 5"/>
    <circle cx="${fx}" cy="${y(row.forecast)}" r="4" fill="var(--paper)" stroke="var(--signal)" stroke-width="2"/>
    <text x="${fx}" y="${y(row.forecast) - 9}" text-anchor="end" style="fill:var(--ink-soft)">forecast ${pct(row.forecast)}</text>` : "";
  return `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Share of postings mentioning ${esc(row.name)} by quarter">
    ${grid}${labels}
    <polyline points="${pts}" fill="none" stroke="var(--signal)" stroke-width="2.4"/>
    ${series.map((p, i) => `<circle cx="${x(i)}" cy="${y(p[1])}" r="3" fill="var(--signal)"><title>${esc(p[0])}: ${pct(p[1])}</title></circle>`).join("")}
    ${forecast}
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
  PULSE = call("overview", $("#f-sector").value, $("#f-district").value, $("#f-state").value);
  const o = PULSE;
  $("#kpis").innerHTML = [
    [fmt(o.postings), "postings in this view"],
    [o.skills_seen, "different skills found in them"],
    [o.avg_alignment == null ? "–" : `${o.avg_alignment}`, "average program alignment here (out of 100)"],
    [o.programs_total ? `${o.programs_total - o.programs_strong} of ${o.programs_total}` : "–", "programs below Strong here"],
  ].map(([v, l]) => `<div class="kpi"><div class="v">${v}</div><div class="l">${l}</div></div>`).join("");

  const max = Math.max(...o.top.map((r) => r.share), 0.01);
  $("#top-skills").innerHTML = o.top.length ? o.top.map((r) => `<li><button type="button" data-skill="${esc(r.id)}" title="95% range ${range(r.low, r.high)}">
      <span class="name">${esc(r.name)}</span>
      <span class="track"><span class="fill" style="width:${(r.share / max) * 100}%"></span></span>
      <span class="num">${pct(r.share)}</span><span class="num">${growth(r)}</span></button></li>`).join("")
    : '<li class="empty">No postings match these filters.</li>';
  const mover = (r) => `<li><button type="button" data-skill="${esc(r.id)}"><span>${esc(r.name)}<span class="sub">${pct(r.share)} of postings${r.within_growth != null ? ` · ${r.within_growth > 0 ? "+" : "−"}${Math.abs(Math.round(r.within_growth * 100))}% within roles` : ""}</span></span>${sparkline(r.series)}<span class="num">${growth(r)}</span></button></li>`;
  const quiet = !o.has_previous
    ? `Trends compare the latest four quarters with the four before; this data has no earlier year to compare with (${o.quarters_present} quarter${o.quarters_present === 1 ? "" : "s"}).`
    : `No change here passes the significance test with ${fmt(o.recent_postings)} recent postings. Smaller samples need bigger changes before SkillAlign calls them a trend.`;
  $("#emerging").innerHTML = o.emerging.map(mover).join("") || `<li class="empty">${quiet}</li>`;
  $("#declining").innerHTML = o.declining.map(mover).join("") || `<li class="empty">${quiet}</li>`;
}

$("#tab-pulse").addEventListener("click", (e) => {
  const b = e.target.closest("[data-skill]");
  if (!b || !PULSE) return;
  const row = [...PULSE.top, ...PULSE.emerging, ...PULSE.declining].find((r) => r.id === b.dataset.skill);
  if (!row) return;
  $("#trend-title").textContent = `${row.name}: share of postings by quarter`;
  $("#trend-chart").innerHTML = lineChart(row);
  $("#trend-note").textContent = `${pct(row.share)} of the latest four quarters' postings (95% range ${range(row.low, row.high)}, ${fmt(row.postings)} of ${fmt(row.n)}). ` +
    (row.is_new ? "New this year. " : row.growth == null ? "" : `${growthText(row)} on the year before. `) +
    (row.forecast_ok ? "The dashed line is a straight-line forecast four quarters ahead." : "Fewer than six quarters of data, so no forecast is drawn.");
  $("#trend-card").hidden = false;
  $("#trend-card").scrollIntoView({ behavior: "smooth", block: "nearest" });
});
$("#trend-close").addEventListener("click", () => ($("#trend-card").hidden = true));
$("#f-sector").addEventListener("change", renderPulse);
$("#f-district").addEventListener("change", renderPulse);
$("#f-state").addEventListener("change", renderPulse);

$("#dataset").addEventListener("change", async (e) => {
  if (!api || e.target.value === META.source || e.target.value === "uploaded") return;
  e.target.disabled = true;
  $("#source").textContent = "Loading postings…";
  busy(true);
  await new Promise((r) => setTimeout(r, 30)); // let the message paint before Python runs
  try {
    const lazy = MANIFEST.lazy?.[e.target.value];
    if (lazy && !PY.FS.analyzePath(`/app/${lazy}`).exists) {
      $("#source").textContent = "Downloading postings…";
      PY.FS.writeFile(`/app/${lazy}`, await fetchText(`py/${lazy}?v=${MANIFEST.version}`));
      $("#source").textContent = "Reading postings…";
      await new Promise((r) => setTimeout(r, 30));
    }
    META = call("use_dataset", e.target.value);
    for (const id of ["#f-sector", "#f-state", "#f-district"]) $(id).value = "";
    dataChanged();
  } catch (ex) {
    $("#source").textContent = `Could not load: ${ex.message}`;
    e.target.value = META.source;
  } finally {
    e.target.disabled = false;
    busy(false);
  }
});

// ---- programs -----------------------------------------------------------------
function scoreCell(r) {
  if (!r.scored) return '<span class="grade Unscored">Unscored</span>';
  const tags = [`<span class="grade ${r.grade}">${r.grade}</span>`];
  if (borderline(r)) tags.push('<span class="grade Borderline" title="the score range crosses a grade line">borderline</span>');
  if (r.low_data) tags.push('<span class="grade Borderline">low data</span>');
  return `<b class="num">${Math.round(r.score)}</b><span class="num mute small"> ${r.score_low != null ? `${Math.round(r.score_low)}–${Math.round(r.score_high)}` : ""}</span> ${tags.join(" ")}`;
}

function renderPrograms() {
  const rows = call("programs_summary");
  $("#program-list").innerHTML = `<div class="prow head"><span>Program</span><span class="col-meter">Alignment</span><span>Score and range</span><span>Next year</span><span class="col-hours">Hours on demand</span></div>` +
    rows.map((r) => `<button type="button" class="prow" data-program="${esc(r.id)}">
      <span class="pname">${esc(r.name)}<span class="psub">${esc(r.provider)} · ${esc(r.duration)} · ${fmt(r.postings)} matching postings${r.warning ? ` · <span class="warn-text">${esc(r.warning)}</span>` : ""}</span></span>
      <span class="meter col-meter">${r.scored ? `<i style="width:${r.score}%;background:${scoreColor(r.score)}"></i>` : ""}</span>
      <span>${scoreCell(r)}</span>
      <span class="num">${r.scored && r.forecast_ok ? Math.round(r.future_score) : "–"} ${r.scored && r.forecast_ok && r.future_score < r.score - 2 ? '<span class="down">↓</span>' : r.scored && r.forecast_ok && r.future_score > r.score + 2 ? '<span class="up">↑</span>' : ""}</span>
      <span class="num col-hours">${r.scored ? `${Math.round(r.hours_on_demand_pct)}%` : "–"}</span></button>`).join("");
}

$("#program-list").addEventListener("click", (e) => {
  const b = e.target.closest("[data-program]");
  if (!b) return;
  document.querySelectorAll(".prow.active").forEach((x) => x.classList.remove("active"));
  b.classList.add("active");
  $("#program-detail").innerHTML = reportHTML(call("program_report", b.dataset.program));
  $("#program-detail").scrollIntoView({ behavior: "smooth", block: "start" });
});

function reportHTML(r) {
  const recs = !r.scored ? "" : r.recommendations.length
    ? `<ul class="recs">${r.recommendations.map((x) => `<li><span class="act ${x.action}">${x.action}</span><span><b>${esc(x.skill)}</b>: ${esc(x.reason)}.</span></li>`).join("")}</ul>`
    : '<p class="mute">No changes needed: every core skill is taught with enough hours and nothing taught is low-demand or falling beyond chance.</p>';
  const skillsRows = r.skills.map((s) => `<tr>
      <td>${esc(s.name)}${s.mandatory ? ' <span class="chip tiny">mandatory</span>' : ""}</td>
      <td class="bar"><div class="meter" title="95% range ${range(s.low, s.high)}"><i style="width:${s.share * 100}%;background:var(--signal)"></i></div></td>
      <td class="num">${pct(s.share)}</td><td class="num">${growth(s)}</td><td class="num">${pct(s.forecast)}</td>
      <td>${s.taught ? (s.credit != null && s.credit < 1 ? `<span class="part">◐ ${Math.round(s.credit * 100)}% credit</span>` : '<span class="yes">✓ taught</span>') : s.share >= 0.15 ? '<span class="no">✗ missing</span>' : '<span class="mute">not taught</span>'}</td>
      <td class="num">${s.hours ? s.hours : ""}${s.fair_hours ? `<span class="mute"> / ${s.fair_hours}</span>` : ""}</td></tr>`).join("");
  const modules = r.modules.map((m) => `<li><b>${esc(m.title)}${m.mandatory ? ' <span class="chip tiny">mandatory</span>' : ""}</b><span class="num mute">${m.hours} h</span>
      <div class="chips">${m.skills.length ? m.skills.map((s) => `<span class="chip">${esc(s)}</span>`).join("") : '<span class="chip none">no skill recognised: not counted</span>'}</div></li>`).join("");
  const meta = [r.provider, r.duration, r.nsqf_level && `NSQF level ${r.nsqf_level}`, r.qp_code && `QP ${r.qp_code}`].filter(Boolean).map(esc).join(" · ");
  return `<div class="report">
    <div class="report-head"><div><h2>${esc(r.name)}</h2><p class="mute small">${meta} · compared with ${fmt(r.postings)} postings for: ${r.target_roles.map(esc).join(", ")}</p></div>
      ${r.scored ? `<button class="btn ghost" type="button" data-download="${esc(r.id)}">Download report</button>` : ""}</div>
    ${r.warnings.map((w) => `<p class="notice">${esc(w)}</p>`).join("")}
    ${r.scored ? `<div class="scores">
      <div class="kpi"><div class="v" style="color:${scoreColor(r.score)}">${Math.round(r.score)}</div><div class="l">alignment today · ${r.grade}${borderline(r) ? " (borderline)" : ""}${r.score_low != null ? `<br>range ${Math.round(r.score_low)}–${Math.round(r.score_high)}` : ""}</div></div>
      <div class="kpi"><div class="v">${r.forecast_ok ? Math.round(r.future_score) : "–"}</div><div class="l">${r.forecast_ok ? "alignment next year if unchanged" : "no forecast: needs six quarters of postings"}</div></div>
      <div class="kpi"><div class="v">${r.covered_count} / ${r.core_count}</div><div class="l">core skills taught</div></div>
      <div class="kpi"><div class="v">${Math.round(r.hours_on_demand_pct)}%</div><div class="l">of ${fmt(r.hours_total)} hours on core skills</div></div>
    </div>
    <article class="card"><h2>What to change</h2>${recs}</article>
    <article class="card"><h2>Skill by skill</h2>
      <p class="mute small">Hours column: hours given / hours needed for full credit.</p>
      <div class="table-wrap"><table class="skills"><thead><tr><th>Skill</th><th>Share of postings</th><th></th><th>Year on year</th><th>Forecast</th><th>In program</th><th>Hours</th></tr></thead><tbody>${skillsRows}</tbody></table></div></article>` : ""}
    <article class="card"><h2>Modules and the skills found in them</h2><ul class="modules">${modules}</ul></article>
  </div>`;
}

const LAST_REPORTS = {};
document.addEventListener("click", (e) => {
  const b = e.target.closest("[data-download]");
  if (!b) return;
  const id = b.dataset.download;
  const r = id === "custom" ? LAST_REPORTS.custom : call("program_report", id);
  if (r) downloadReport(r);
});

function downloadReport(r) {
  const lines = [
    `# SkillAlign report: ${r.name}`, "",
    `Compared with ${r.postings} job postings for: ${r.target_roles.join(", ")} (${META.source === "sample" ? "SYNTHETIC demo data" : META.source === "real" ? "real postings, Fliar Research 2026, CC BY-NC 4.0" : "uploaded data"}, ${META.quarters[0]} to ${META.quarters[META.quarters.length - 1]}).`, "",
    `- Alignment today: ${r.score} / 100 (${r.grade}${borderline(r) ? ", borderline" : ""}), range ${r.score_low ?? "-"} to ${r.score_high ?? "-"}`,
    `- Alignment next year if unchanged: ${r.forecast_ok ? `${r.future_score} / 100` : "no forecast (fewer than six quarters of postings)"}`,
    `- Core skills taught: ${r.covered_count} of ${r.core_count}`,
    `- Training hours on core skills: ${r.hours_on_demand_pct}% of ${r.hours_total}`,
    ...r.warnings.map((w) => `- Note: ${w}`), "",
    "## What to change", "",
    ...(r.recommendations.length ? r.recommendations.map((x) => `- **${x.action} ${x.skill}**: ${x.reason}.`) : ["- No changes needed."]), "",
    "## Skill by skill", "", "| Skill | Share | 95% range | Year on year | Forecast | Taught | Hours given / needed |", "|---|---|---|---|---|---|---|",
    ...r.skills.map((s) => `| ${s.name} | ${pct(s.share)} | ${range(s.low, s.high)} | ${growthText(s)} | ${pct(s.forecast)} | ${s.taught ? (s.credit != null && s.credit < 1 ? `partly (${Math.round(s.credit * 100)}%)` : "yes") : "no"} | ${s.hours || ""}${s.fair_hours ? ` / ${s.fair_hours}` : ""} |`),
  ];
  const a = document.createElement("a");
  a.href = URL.createObjectURL(new Blob([lines.join("\n")], { type: "text/markdown" }));
  a.download = `skillalign-${r.id}.md`;
  a.click();
  setTimeout(() => URL.revokeObjectURL(a.href), 1000);
}

// ---- matrix -------------------------------------------------------------------
function renderMatrix() {
  const m = call("matrix");
  const head = `<thead><tr><th></th>${m.skills.map((s) => `<th scope="col"><span>${esc(s.name)}</span></th>`).join("")}</tr></thead>`;
  const body = m.rows.map((row) => `<tr><th scope="row">${esc(row.name)}</th>${row.cells.map((c, i) => {
    const a = Math.min(0.95, c.share * 1.1);
    const gap = !c.taught && c.share >= 0.15;
    const label = `${row.name}, ${m.skills[i].name}: in ${pct(c.share)} of its target postings, ${c.taught ? "taught" : gap ? "not taught, a gap" : "not taught"}`;
    return `<td class="${a > 0.55 ? "dark" : "light"}${gap ? " gap" : ""}" style="--a:${a.toFixed(2)}" title="${esc(label)}" aria-label="${esc(label)}">${c.taught ? "✓" : gap ? '<span class="gap-mark" aria-hidden="true">!</span>' : ""}</td>`;
  }).join("")}</tr>`).join("");
  $("#matrix").innerHTML = head + `<tbody>${body}</tbody>`;
}

// ---- syllabus -----------------------------------------------------------------
function chipsFor(found) {
  const known = found.skills.length ? found.skills.map((s) => `<span class="chip" title="matched: ${esc(s.matched.join(", "))}">${esc(s.name)}</span>`).join("") : '<span class="chip none">none yet</span>';
  const missed = found.unrecognised.length ? `<p class="small mute" style="margin:.5rem 0 .3rem">Not recognised, so not counted:</p><div class="chips">${found.unrecognised.map((u) => `<span class="chip none">${esc(u)}</span>`).join("")}</div>` : "";
  return { known, missed };
}

function renderSyllabusDetect() {
  const { known, missed } = chipsFor(call("extract", $("#s-text").value));
  $("#syllabus-detected").innerHTML = `<p class="small mute" style="margin-bottom:.35rem">Skills found in this syllabus as you type:</p><div class="chips">${known}</div>${missed}`;
}
let detectTimer = null;
$("#s-text").addEventListener("input", () => {
  clearTimeout(detectTimer);
  detectTimer = setTimeout(() => api && renderSyllabusDetect(), 250);
});
$("#syllabus-form").addEventListener("submit", (e) => {
  e.preventDefault();
  if (!api) return;
  const err = $("#s-error");
  err.hidden = true;
  try {
    const r = call("analyse_syllabus", $("#s-name").value, $("#s-roles").value, $("#s-text").value, $("#s-nsqf").value.trim(), $("#s-qp").value.trim());
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
  $("#s-text").value = "Petrol engine servicing and engine overhaul (120 hrs)\nBrakes, clutch and suspension system (60 hrs)\nWorkshop safety and PPE (20 hrs)\nTalking to customers: customer service at the service desk (15 hrs) [mandatory]\nIntroduction to electric vehicles (10 hrs)";
  if (api) renderSyllabusDetect();
});

// ---- learner ------------------------------------------------------------------
$("#learner-form").addEventListener("submit", (e) => {
  e.preventDefault();
  if (!api) return;
  const err = $("#l-error");
  err.hidden = true;
  const role = $("#l-role").value;
  let r;
  try {
    r = call("learner", role, "[]", $("#l-text").value);
  } catch (ex) {
    err.textContent = ex.message;
    err.hidden = false;
    return;
  }
  const req = r.required.map((s) => `<span class="chip ${s.have ? "have" : "none"}">${s.have ? "✓" : "✗"} ${esc(s.name)} <small>${pct(s.share)}</small></span>`).join("");
  const programs = r.programs.length
    ? `<ul class="recs">${r.programs.map((p) => `<li><span class="act Add">${esc(p.duration || "")}</span><span><b>${esc(p.name)}</b>${p.for_this_job ? '<span class="fit">built for this job</span>' : ""}<br>covers ${p.covers.map(esc).join(", ")}.</span></li>`).join("")}</ul>`
    : '<p class="mute">None of the listed programs teaches your missing skills.</p>';
  const missed = r.unrecognised.length ? `<p class="small mute">Not recognised, so not counted (if these are skills, readiness is understated): ${r.unrecognised.map((u) => `<span class="chip none">${esc(u)}</span>`).join(" ")}</p>` : "";
  $("#learner-result").innerHTML = `<div class="report">
    <article class="card"><div class="ready">${ring(r.readiness)}<div>
      <h2>${Math.round(r.readiness)}% ready for ${esc(titleCase(role))}</h2>
      <p class="mute small">Weighted by how often each skill appears in ${fmt(r.postings)} postings for this job.</p>
      ${r.next_skill ? `<p style="margin-top:.5rem">Learn next: <b>${esc(r.next_skill.name)}</b>, asked for in ${pct(r.next_skill.share)} of these postings${r.next_skill.is_new || (r.next_skill.significant && r.next_skill.growth > 0) ? " and rising" : ""}.</p>` : "<p>You have every skill these postings commonly ask for.</p>"}
    </div></div></article>
    <article class="card"><h2>What employers ask for</h2><p class="mute small">Skills in at least 15% of postings. Green: you have it. Red: missing.</p><div class="chips">${req}</div>
      ${r.have.length ? `<p class="small mute">Skills we read from your text: ${r.have.map(esc).join(", ")}.</p>` : ""}${missed}</article>
    <article class="card"><h2>Programs that close your gaps</h2>${programs}</article>
  </div>`;
});

// ---- your data ----------------------------------------------------------------
let extractTimer = null;
function renderExtract() {
  const found = call("extract", $("#x-text").value);
  const known = found.skills.map((s) => `<span class="chip"><b>${esc(s.name)}</b> <small>from “${esc(s.matched.join("”, “"))}”</small></span>`).join("");
  const missed = found.unrecognised.map((u) => `<span class="chip none">not recognised: ${esc(u)}</span>`).join("");
  $("#x-out").innerHTML = known + missed || '<span class="chip none">no skills recognised</span>';
}
$("#x-text").addEventListener("input", () => {
  clearTimeout(extractTimer);
  extractTimer = setTimeout(() => api && renderExtract(), 250);
});

$("#upload").addEventListener("change", async (e) => {
  const file = e.target.files[0];
  if (!file || !api) return;
  const status = $("#upload-status");
  status.textContent = `Reading ${file.name}…`;
  busy(true);
  await new Promise((r) => setTimeout(r, 30)); // let the message paint before Python runs
  try {
    META = call("load_uploaded", await file.text());
    status.innerHTML = `Loaded <b>${fmt(META.postings)}</b> postings from ${esc(file.name)}.` +
      (META.problem_count ? ` Skipped ${META.problem_count} rows: ${META.problems.slice(0, 3).map(esc).join("; ")}${META.problem_count > 3 ? "…" : ""}` : "");
    dataChanged();
  } catch (ex) {
    status.innerHTML = `<span class="error">Nothing changed: ${esc(ex.message)}</span>`;
  } finally {
    busy(false);
  }
  e.target.value = "";
});
$("#reset-sample").addEventListener("click", () => {
  if (!api) return;
  META = call("use_sample");
  $("#upload-status").textContent = "Back on the sample data.";
  dataChanged();
});

boot();
