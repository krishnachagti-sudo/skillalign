// SkillAlign front end. All the analysis happens in Python (engine/api.py),
// run in the browser by Pyodide. This file only loads it and draws results.
// The pages are plain HTML, so they show at once; anything that needs the
// engine waits for it (whenReady) while a status line says what is loading.

const VERSION = window.SKILLALIGN_VERSION || "dev";
let api = null;
let PY = null;
let MANIFEST = null;
let META = null;
const rendered = new Set();
const waiting = [];

const $ = (sel, root = document) => root.querySelector(sel);
const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const pct = (x) => (x == null ? "–" : `${Math.round(x * 100)}%`);
const fmt = (n) => Number(n).toLocaleString("en-IN");
const range = (lo, hi) => (lo == null || hi == null ? "" : `${Math.round(lo * 100)}–${Math.round(hi * 100)}%`);
const plural = (n, word) => `${fmt(n)} ${word}${n === 1 ? "" : "s"}`;

// a change is shown as a number only when it is beyond chance; otherwise it says so in words
function growth(row) {
  if (row.is_new) return '<span class="up">new</span>';
  const g = row.growth;
  if (g == null) return '<span class="mute">–</span>';
  if (!row.significant) return '<span class="mute" title="the change is within chance">steady</span>';
  const v = Math.round(g * 100);
  return v > 0 ? `<span class="up">↑ ${v}%</span>` : `<span class="down">↓ ${-v}%</span>`;
}
const growthText = (row) => (row.is_new ? "new" : row.growth == null ? "-" : row.significant ? `${Math.round(row.growth * 100)}%` : "steady (within chance)");
const scoreColor = (s) => (s >= 75 ? "var(--signal)" : s >= 50 ? "var(--warn)" : "var(--bad)");
const borderline = (r) => r.score_low != null && [50, 75].some((cut) => r.score_low < cut && r.score_high >= cut);
const titleCase = (s) => s.replace(/\b\w/g, (c) => c.toUpperCase()).replace(/\bPv\b/, "PV").replace(/\bEv\b/, "EV").replace(/\bCnc\b/, "CNC").replace(/\bAc\b/, "AC");
// a growth rate means little without its base, so say "from 2% to 5%"
const fromTo = (r) => `${pct(r.share / (1 + r.growth))} to ${pct(r.share)}`;
const recentQuarters = () => Math.min(4, META?.quarters.length || 4);

// whole numbers count up from zero when they first appear (skipped for reduced motion)
const calm = matchMedia("(prefers-reduced-motion: reduce)").matches;
function countUp(root) {
  if (calm) return;
  $$(".kpi .v, .fact b, .verdict .big", root).forEach((el) => {
    const node = el.firstChild;
    if (!node || node.nodeType !== 3 || !/^[\d,]+$/.test(node.textContent.trim())) return;
    const end = Number(node.textContent.replace(/,/g, ""));
    const t0 = performance.now();
    const tick = (now) => {
      const f = Math.min(1, (now - t0) / 800);
      node.textContent = fmt(Math.round(end * (1 - (1 - f) ** 3)));
      if (f < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  });
}

// ---- Python bridge ----------------------------------------------------------
function call(fn, ...args) {
  try {
    return JSON.parse(api[fn](...args));
  } catch (err) {
    const lines = String(err.message || err).trim().split("\n");
    throw new Error(lines[lines.length - 1].replace(/^\w+Error: /, "").replace(/^['"]|['"]$/g, ""));
  }
}

function whenReady(fn) {
  if (api) fn();
  else waiting.push(fn);
}

async function fetchText(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`could not load ${url} (${res.status})`);
  return res.text();
}

// Some hosts (conyso.com's nginx) serve .wasm as application/octet-stream.
// Browsers then refuse WebAssembly.instantiateStreaming, and Pyodide has no
// fallback, so the engine hangs forever. Retry from the bytes instead.
if (WebAssembly.instantiateStreaming) {
  const streaming = WebAssembly.instantiateStreaming.bind(WebAssembly);
  WebAssembly.instantiateStreaming = async (source, imports) => {
    const res = await source;
    try {
      return await streaming(res.clone(), imports);
    } catch (err) {
      return WebAssembly.instantiate(await res.arrayBuffer(), imports);
    }
  };
}

async function boot() {
  const step = $("#boot-step");
  try {
    if (typeof loadPyodide !== "function") throw new Error("the Python runtime did not load");
    const pyodide = await loadPyodide({ indexURL: new URL("vendor/pyodide/", location.href).href });
    step.textContent = "Loading the SkillAlign engine and job postings…";
    const manifest = (MANIFEST = JSON.parse(await fetchText(`py/manifest.json?v=${VERSION}`)));
    PY = pyodide;
    pyodide.FS.mkdirTree("/app/engine");
    pyodide.FS.mkdirTree("/app/data");
    await Promise.all(manifest.files.map(async (f) => {
      pyodide.FS.writeFile(`/app/${f}`, await fetchText(`py/${f}?v=${manifest.version}`));
    }));
    pyodide.runPython("import sys; sys.path.insert(0, '/app')");
    api = pyodide.pyimport("engine.api");
    META = call("init", "/app/data");
    $("#engine-status").hidden = true;
    document.body.classList.add("engine-ready");
    setupStatic();
    waiting.splice(0).forEach((fn) => fn());
    route();
    if ("serviceWorker" in navigator && location.protocol === "https:") navigator.serviceWorker.register("sw.js").catch(() => {});
  } catch (err) {
    $("#engine-status").classList.add("failed");
    step.textContent = `Could not start the engine: ${err.message}. Check your connection and reload.`;
    console.error(err);
  }
}

// ---- routing ----------------------------------------------------------------
const PAGES = ["home", "course", "job", "market", "data", "method"];
const VIEWS = ["skills", "courses", "gaps"];
const RENDER = {
  home: renderHome, course: renderCourse, job: () => {}, data: renderExtract, method: () => {},
  "market/skills": renderPulse, "market/courses": renderPrograms, "market/gaps": renderMatrix,
};

function route() {
  let [page, view] = location.hash.slice(1).split("/");
  if (!PAGES.includes(page)) page = "home";
  if (page === "market" && !VIEWS.includes(view)) view = "skills";
  $$(".page").forEach((s) => (s.hidden = s.id !== `page-${page}`));
  $$("[data-route]").forEach((a) => a.toggleAttribute("aria-current", a.dataset.route === page));
  if (page === "market") {
    $$(".view").forEach((v) => (v.hidden = v.id !== `view-${view}`));
    $$(".segments a").forEach((a) => a.toggleAttribute("aria-current", a.dataset.view === view));
  }
  const key = page === "market" ? `market/${view}` : page;
  if (api && !rendered.has(key)) {
    rendered.add(key);
    RENDER[key]();
  }
  document.body.dataset.page = page;
}

let lastPage = null;
window.addEventListener("hashchange", () => {
  route();
  // a new page starts at the top; switching views inside the job market keeps your place
  if (document.body.dataset.page !== lastPage) window.scrollTo(0, 0);
  lastPage = document.body.dataset.page;
});

function dataChanged() {
  rendered.clear();
  toggleDataMenu(false);
  for (const id of ["#syllabus-result", "#learner-result", "#example-result"]) $(id).innerHTML = "";
  delete LAST_REPORTS.custom;
  setupStatic();
  route();
}

// ---- data pill and menu -------------------------------------------------------
const SHORT = { sample: "Practice data", real: "Real job ads, India 2026", uploaded: "Your file" };

function explainData() {
  const q = META.quarters;
  if (META.source === "sample") {
    return `<b>Practice data.</b> These ${fmt(META.postings)} job ads are made up, to show how SkillAlign works, so the numbers are not facts about real jobs. <button class="link" type="button" data-use="real">Switch to real job ads</button> or <a href="#data">use your own file</a>.`;
  }
  if (META.source === "real") {
    return `<b>Real job ads.</b> ${fmt(META.postings)} Indian job ads, ${esc(q[0])} to ${esc(q[q.length - 1])}, from Fliar Research (<a href="https://creativecommons.org/licenses/by-nc/4.0/">CC BY-NC 4.0</a>, <a href="https://github.com/krishnachagti-sudo/skillalign/blob/main/docs/DATA-SOURCES.md">what we cleaned</a>). A 6% sample of companies: it describes this sample, not the whole market. Only two quarters, so no trends. Very few trade jobs, so ITI courses mostly cannot be scored.`;
  }
  return q.length < 6
    ? `<b>Your file.</b> ${plural(q.length, "quarter")} of job ads: skill shares and course scores, but trends need two years of ads.`
    : "<b>Your file.</b> Every number on the site is worked out from your file.";
}

function setupStatic() {
  const q = META.quarters;
  const ds = $("#dataset");
  const names = Object.keys(META.datasets).concat(META.source === "uploaded" ? ["uploaded"] : []);
  ds.innerHTML = names.map((k) => `<option value="${esc(k)}">${esc(SHORT[k] || k)}</option>`).join("");
  ds.value = META.source;
  ds.disabled = false;
  $("#source").textContent = `${fmt(META.postings)} job ads · ${q[0] || ""} to ${q[q.length - 1] || ""}`;
  $("#data-pill-text").textContent = { sample: "Practice data", real: "Real job ads" }[META.source] || "Your file";
  $("#data-pill").dataset.source = META.source;
  $("#data-explain").innerHTML = explainData();
  fillSelect($("#f-sector"), META.sectors, "All sectors");
  fillSelect($("#f-state"), META.states, "All states");
  $("#f-state-wrap").hidden = META.states.length < 2;
  if (META.states.length < 2) $("#f-state").value = "";
  fillSelect($("#f-district"), META.districts, "All districts");
  $("#role-list").innerHTML = META.roles.map(([r]) => `<option value="${esc(r)}">`).join("");
  $("#l-roles").innerHTML = META.roles.map(([r, n]) => `<option value="${esc(r)}">${n} job ads</option>`).join("");
  if (!META.roles.some(([r]) => r === $("#l-role").value)) $("#l-role").value = META.roles.some(([r]) => r === "data analyst") ? "data analyst" : (META.roles[0]?.[0] || "");
  $("#m-skills").textContent = META.skills.length;
  $("#m-syn").textContent = META.synonyms;
  $("#example-courses").innerHTML = META.programs.map((p) => `<button class="chip pick" type="button" data-example="${esc(p.id)}">${esc(p.name)}</button>`).join("");
}

function fillSelect(sel, values, allLabel) {
  const keep = sel.value;
  sel.innerHTML = `<option value="">${allLabel}</option>` + values.map((v) => `<option>${esc(v)}</option>`).join("");
  sel.value = values.includes(keep) ? keep : "";
}

function toggleDataMenu(open) {
  const menu = $("#data-menu");
  open = open ?? menu.hidden;
  menu.hidden = !open;
  $("#data-pill").setAttribute("aria-expanded", open);
}
$("#data-pill").addEventListener("click", () => toggleDataMenu());
document.addEventListener("keydown", (e) => e.key === "Escape" && toggleDataMenu(false));

function lockData(on) {
  for (const id of ["#dataset", "#upload", "#reset-sample"]) $(id).disabled = on;
  document.body.classList.toggle("busy", on);
}

async function useDataset(want) {
  if (!api || want === META.source || want === "uploaded") return;
  lockData(true);
  $("#source").textContent = "Loading job ads…";
  await new Promise((r) => setTimeout(r, 30)); // let the message paint before Python runs
  try {
    const lazy = MANIFEST.lazy?.[want];
    if (lazy && !PY.FS.analyzePath(`/app/${lazy}`).exists) {
      $("#source").textContent = "Downloading job ads (about 9 MB)…";
      PY.FS.writeFile(`/app/${lazy}`, await fetchText(`py/${lazy}?v=${MANIFEST.version}`));
      $("#source").textContent = "Reading job ads…";
      await new Promise((r) => setTimeout(r, 30));
    }
    META = call("use_dataset", want);
    for (const id of ["#f-sector", "#f-state", "#f-district"]) $(id).value = "";
    dataChanged();
  } catch (ex) {
    setupStatic(); // put the header back for the data still loaded
    $("#data-explain").innerHTML = `<b>Could not load those job ads</b> (${esc(ex.message)}). Still using the previous data. ` + explainData();
  } finally {
    lockData(false);
  }
}
$("#dataset").addEventListener("change", (e) => useDataset(e.target.value));
document.addEventListener("click", (e) => {
  const b = e.target.closest("[data-use]");
  if (b) useDataset(b.dataset.use);
});

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
  const max = Math.max(...series.map((p) => p[1]), row.forecast_ok ? row.forecast_high ?? row.forecast : 0, 0.05) * 1.15;
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
  const band = row.forecast_ok && row.forecast_low != null
    ? `<line x1="${fx}" x2="${fx}" y1="${y(row.forecast_low)}" y2="${y(row.forecast_high)}" stroke="var(--signal)" stroke-width="6" stroke-opacity=".18" stroke-linecap="round"/>` : "";
  const forecast = row.forecast_ok ? `${band}<line x1="${x(n - 1)}" y1="${y(last[1])}" x2="${fx}" y2="${y(row.forecast)}" stroke="var(--signal)" stroke-width="2" stroke-dasharray="5 5"/>
    <circle cx="${fx}" cy="${y(row.forecast)}" r="4" fill="var(--paper)" stroke="var(--signal)" stroke-width="2"/>
    <text x="${fx}" y="${y(row.forecast) - 9}" text-anchor="end" style="fill:var(--ink-soft)">next year ${pct(row.forecast)}</text>` : "";
  return `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Share of job ads mentioning ${esc(row.name)} by quarter">
    ${grid}${labels}
    ${n >= 3 ? `<polyline points="${pts}" fill="none" stroke="var(--signal)" stroke-width="2.4"/>` : ""}
    ${series.map((p, i) => `<circle cx="${x(i)}" cy="${y(p[1])}" r="3" fill="var(--signal)"><title>${esc(p[0])}: ${pct(p[1])}</title></circle>`).join("")}
    ${forecast}
  </svg>`;
}

function ring(value) {
  const r = 50, c = 2 * Math.PI * r, f = Math.max(0, Math.min(100, value)) / 100;
  return `<svg class="ring" viewBox="0 0 120 120" role="img" aria-label="Ready: ${Math.round(value)}%">
    <circle cx="60" cy="60" r="${r}" fill="none" stroke="var(--paper-sink)" stroke-width="12"/>
    <circle cx="60" cy="60" r="${r}" fill="none" stroke="${scoreColor(value)}" stroke-width="12" stroke-linecap="round"
      stroke-dasharray="${c * f} ${c}" transform="rotate(-90 60 60)"/>
    <text x="60" y="69" text-anchor="middle">${Math.round(value)}%</text></svg>`;
}

// ---- home -------------------------------------------------------------------
function renderHome() {
  const rows = call("programs_summary", "", "", "");
  const scored = rows.filter((r) => r.scored);
  const weak = scored.filter((r) => r.grade !== "Strong");
  const o = call("overview", "", "", "");
  const where = META.source === "sample" ? "On made-up practice job ads, " : META.source === "real" ? "On real Indian job ads, " : "On your file, ";
  $("#home-answer").innerHTML = scored.length
    ? `${where}<b>${weak.length} of ${scored.length} example courses</b> miss skills that their own jobs ask for. Check yours in a minute.`
    : `${where}none of the example courses has enough matching job ads to be scored. Check your own course to see how it compares.`;
  const top = o.top[0];
  const riser = o.emerging[0];
  $("#home-facts").innerHTML = [
    top && `<div class="fact"><span class="l">Asked for most</span><b>${esc(top.name)}</b><span class="l">in ${pct(top.share)} of job ads</span></div>`,
    riser && `<div class="fact"><span class="l">Rising fastest</span><b>${esc(riser.name)}</b><span class="l">${riser.is_new ? "new this year" : `from ${fromTo(riser)} of job ads in a year`}</span></div>`,
    `<div class="fact"><span class="l">Job ads read</span><b>${fmt(o.postings)}</b><span class="l">${META.source === "sample" ? 'made up for practice · <button class="link" type="button" data-use="real">use real ads</button>' : esc(SHORT[META.source] || "your file")}</span></div>`,
  ].filter(Boolean).join("");
  countUp($("#home-facts"));
}

// ---- market: skills -----------------------------------------------------------
let PULSE = null;
const filters = () => [$("#f-sector").value, $("#f-district").value, $("#f-state").value];
function filterNote() {
  const [sector, district, state] = filters();
  const parts = [state && `state ${state}`, district && `district ${district}`, sector && `sector ${sector}`].filter(Boolean);
  return parts.length ? `<p class="notice soft">Only job ads in ${parts.map(esc).join(", ")}.</p>` : "";
}

function renderPulse() {
  PULSE = call("overview", ...filters());
  const o = PULSE;
  const k = recentQuarters();
  $("#kpis").innerHTML = [
    [fmt(o.postings), "job ads in this view"],
    [o.skills_seen, "different skills asked for"],
    [o.programs_total ? `${o.programs_total - o.programs_strong} of ${o.programs_total}` : "–", "example courses that miss some core skills"],
    [o.emerging.length, o.has_previous ? "skills rising beyond chance" : "trends: need two years of ads"],
  ].map(([v, l]) => `<div class="kpi"><div class="v">${v}</div><div class="l">${l}</div></div>`).join("");
  countUp($("#kpis"));

  $("#top-note").textContent = `Share of job ads in the latest ${k === 1 ? "quarter" : `${k} quarters`} that mention each skill${o.has_previous ? ", and the change on the year before" : ""}. Tap one to see its trend.`;
  const max = Math.max(...o.top.map((r) => r.share), 0.01);
  $("#top-skills").classList.toggle("no-change", !o.has_previous);
  $("#top-skills").innerHTML = o.top.length ? o.top.map((r) => `<li><button type="button" data-skill="${esc(r.id)}" aria-expanded="false" title="95% range ${range(r.low, r.high)}">
      <span class="name">${esc(r.name)}</span>
      <span class="track"><span class="fill" style="width:${(r.share / max) * 100}%"></span></span>
      <span class="num">${pct(r.share)}</span><span class="num chg">${growth(r)}</span></button></li>`).join("")
    : '<li class="empty">No job ads match these filters.</li>';
  const mover = (r) => `<li><button type="button" data-skill="${esc(r.id)}" aria-expanded="false"><span>${esc(r.name)}<span class="sub">${r.is_new || r.growth == null ? `${pct(r.share)} of job ads` : `from ${fromTo(r)} of job ads`}</span></span>${sparkline(r.series)}<span class="num">${growth(r)}</span></button></li>`;
  const quiet = !o.has_previous
    ? `Trends compare the latest year with the year before; this data has only ${plural(o.quarters_present, "quarter")}.`
    : `No change passes the chance test with ${fmt(o.recent_postings)} recent job ads. Smaller samples need bigger changes before SkillAlign calls them a trend.`;
  $("#emerging").innerHTML = o.emerging.map(mover).join("") || `<li class="empty">${quiet}</li>`;
  $("#declining").innerHTML = o.declining.map(mover).join("") || `<li class="empty">${quiet}</li>`;
}

// the trend opens right under the skill that was tapped
$("#view-skills").addEventListener("click", (e) => {
  const b = e.target.closest("[data-skill]");
  if (!b || !PULSE) return;
  const li = b.closest("li");
  const open = li.nextElementSibling?.classList.contains("trend-li");
  $$(".trend-li", $("#view-skills")).forEach((x) => x.remove());
  $$("[data-skill][aria-expanded='true']").forEach((x) => x.setAttribute("aria-expanded", "false"));
  if (open) return;
  const row = [...PULSE.top, ...PULSE.emerging, ...PULSE.declining].find((r) => r.id === b.dataset.skill);
  if (!row) return;
  b.setAttribute("aria-expanded", "true");
  const k = Math.min(4, row.series.length);
  const note = `${pct(row.share)} of job ads in the latest ${k === 1 ? "quarter" : `${k} quarters`} (${fmt(row.postings)} of ${fmt(row.n)}; likely ${range(row.low, row.high)}). ` +
    (row.series.length < 3 ? "Too few quarters to draw a line. " : "") +
    (row.is_new ? "New this year. " : row.growth == null ? "" : row.significant ? `${row.growth > 0 ? "Up" : "Down"} ${Math.abs(Math.round(row.growth * 100))}% on the year before, beyond chance. ` : "No change beyond chance on the year before. ") +
    (row.forecast_ok ? `Dashed line: a straight-line forecast a year ahead, about ${pct(row.forecast)} (likely ${range(row.forecast_low, row.forecast_high)}).` : "No forecast: it needs six quarters of job ads.");
  li.insertAdjacentHTML("afterend", `<li class="trend-li"><div class="trend"><div class="chart">${lineChart(row)}</div><p class="mute small">${note}</p></div></li>`);
});

function onFilter() {
  for (const k of ["market/skills", "market/courses", "market/gaps"]) rendered.delete(k);
  route();
}
for (const id of ["#f-sector", "#f-district", "#f-state"]) $(id).addEventListener("change", () => api && onFilter());

// ---- market: example courses ----------------------------------------------------
function gradeTag(r) {
  if (!r.scored) return `<span class="grade Unscored">${esc(r.grade)}</span>`;
  return `<span class="grade ${r.grade}">${r.grade}</span>${borderline(r) ? ' <span class="grade Borderline" title="the score range crosses a grade line">borderline</span>' : ""}`;
}

function renderPrograms() {
  const rows = call("programs_summary", ...filters());
  $("#program-filter-note").innerHTML = filterNote();
  $("#program-list").innerHTML = `<div class="prow head" aria-hidden="true"><span>Example course</span><span class="col-meter">Covers what its jobs ask for</span><span>Score</span><span class="col-next">Next year if unchanged</span></div>` +
    rows.map((r) => `<div class="pitem"><button type="button" class="prow" data-program="${esc(r.id)}" aria-expanded="false">
      <span class="pname">${esc(r.name)}<span class="psub">${esc(r.duration)} · ${plural(r.postings, "matching job ad")}${r.warning ? ` · <span class="warn-text">${esc(r.warning)}</span>` : ""}</span></span>
      <span class="meter col-meter">${r.scored ? `<i style="width:${r.score}%;background:${scoreColor(r.score)}"></i>` : ""}</span>
      <span class="pscore">${r.scored ? `<b class="num">${Math.round(r.score)}</b> ` : ""}${gradeTag(r)}</span>
      <span class="num col-next">${r.scored && r.forecast_ok ? `${Math.round(r.future_score)}${r.future_score < r.score - 2 ? ' <span class="down" title="lower, because the jobs are changing">↓</span>' : r.future_score > r.score + 2 ? ' <span class="up">↑</span>' : ""}` : "–"}</span>
      <span class="chev" aria-hidden="true">▾</span></button><div class="pdetail" hidden></div></div>`).join("") +
    (META.source === "real" && rows.some((r) => !r.scored) ? `<p class="notice soft">Courses marked "too few" or "unscored" have almost no matching ads in this sample. <button class="link" type="button" data-use="sample">See them scored on practice data</button>.</p>` : "");
}

// the report opens inside the list, right under the course that was tapped
$("#program-list").addEventListener("click", (e) => {
  const b = e.target.closest("[data-program]");
  if (!b) return;
  const detail = b.nextElementSibling;
  const opening = detail.hidden;
  $$(".pdetail", $("#program-list")).forEach((d) => { d.hidden = true; d.innerHTML = ""; });
  $$(".prow[aria-expanded='true']").forEach((x) => x.setAttribute("aria-expanded", "false"));
  if (!opening) return;
  b.setAttribute("aria-expanded", "true");
  detail.innerHTML = reportHTML(call("program_report", b.dataset.program, ...filters()), { example: true });
  detail.hidden = false;
  countUp(detail);
  b.scrollIntoView({ behavior: "smooth", block: "start" });
});

// ---- the course report ------------------------------------------------------------
function sharedNote(rec, r) {
  // when one module teaches two skills its hours are split; say so where the hours are quoted
  const mods = r.modules.filter((m) => m.skills.includes(rec.skill) && m.skills.length > 1);
  if (!mods.length) return "";
  const m = mods[0];
  return ` (its ${m.hours} h module "${esc(m.title)}" is shared with ${m.skills.filter((s) => s !== rec.skill).map(esc).join(", ")})`;
}

function plainScore(r) {
  const s = Math.round(r.score);
  return `It teaches about <b>${s}%</b> of what these jobs ask for${r.grade === "Strong" ? "" : `, so it is <b>${r.grade.toLowerCase()}</b>`}.`;
}

function reportHTML(r, { example = false } = {}) {
  const recList = (list) => list.map((x) => `<li><span class="act ${x.action}">${x.action}</span><span><b>${esc(x.skill)}</b>: ${esc(x.reason.replace(/postings/g, "job ads").replace(/95% range /g, "likely "))}${x.action === "Expand" ? sharedNote(x, r) : ""}.</span></li>`).join("");
  const top = r.recommendations.slice(0, 3);
  const rest = r.recommendations.slice(3);
  const recs = !r.scored ? "" : r.recommendations.length
    ? `<ol class="recs">${recList(top)}</ol>${rest.length ? `<details class="more"><summary>Show ${rest.length} more change${rest.length === 1 ? "" : "s"}</summary><ol class="recs">${recList(rest)}</ol></details>` : ""}`
    : '<p class="mute">No changes needed: every core skill is taught with enough hours and nothing taught is rarely asked for or falling.</p>';
  const skillsRows = r.skills.map((s) => `<tr>
      <td>${esc(s.name)}${s.mandatory ? ' <span class="chip tiny">mandatory</span>' : ""}</td>
      <td class="bar"><div class="meter" title="95% range ${range(s.low, s.high)}"><i style="width:${s.share * 100}%;background:var(--signal)"></i></div></td>
      <td class="num">${pct(s.share)}</td><td class="num">${growth(s)}</td>
      <td>${s.taught ? (s.credit != null && s.credit < 1 ? `<span class="part">◐ part (${Math.round(s.credit * 100)}%)</span>` : '<span class="yes">✓ taught</span>') : s.share >= 0.15 ? '<span class="no">✗ missing</span>' : '<span class="mute">not taught</span>'}</td>
      <td class="num">${s.hours ? s.hours : "–"}${s.fair_hours ? `<span class="mute"> of ${s.fair_hours}</span>` : ""}</td></tr>`).join("");
  const modules = r.modules.map((m) => `<li><b>${esc(m.title)}${m.mandatory ? ' <span class="chip tiny">mandatory</span>' : ""}</b><span class="num mute">${m.hours} h${m.skills.length > 1 ? ` · ${Math.round(m.hours / m.skills.length)} h each` : ""}</span>
      <div class="chips">${m.skills.length ? m.skills.map((s) => `<span class="chip">${esc(s)}</span>`).join("") : '<span class="chip none">no skill recognised: not counted</span>'}</div></li>`).join("");
  const meta = [example ? "Example course (made up)" : "Your course", r.duration, r.nsqf_level && `NSQF level ${r.nsqf_level}`, r.qp_code && `QP ${r.qp_code}`].filter(Boolean).map(esc).join(" · ");
  const missing = r.scored ? r.core_count - r.covered_count : 0;
  return `<div class="report" data-report="${esc(r.id)}">
    <div class="report-head"><div><h2>${esc(r.name)}</h2><p class="mute small">${meta}<br>Compared with ${plural(r.postings, "job ad")} for: ${r.target_roles.map(esc).join(", ")} · ${esc(SHORT[META.source] || "your file")}</p></div>
      ${r.scored ? `<button class="btn ghost no-print" type="button" data-print>Print or save as PDF</button>` : ""}</div>
    ${r.warnings.map((w) => `<p class="notice">${esc(w)}</p>`).join("")}
    ${r.scored ? `<div class="verdict" style="--c:${scoreColor(r.score)}">
      <div class="big">${Math.round(r.score)}<span>/100</span></div>
      <div><p>${plainScore(r)} ${missing ? `It misses <b>${missing} of ${r.core_count}</b> skills that 15% or more of these job ads ask for.` : "It teaches every skill that 15% or more of these job ads ask for."}</p>
      <p class="mute small">Likely between ${Math.round(r.score_low)} and ${Math.round(r.score_high)}${borderline(r) ? " (so it could fall in the next grade either way: borderline)" : ""}.${r.forecast_ok ? ` If the course stays the same, roughly <b>${Math.round(r.future_score)}</b> next year, because the jobs are changing (a straight-line guess).` : ""}</p></div>
    </div>
    <article class="card"><h2>What to change, most important first</h2>${recs}</article>
    <details class="card fold"><summary><h2>Skill by skill</h2></summary>
      <p class="mute small">Hours: hours the course gives / hours for full credit.</p>
      <div class="table-wrap"><table class="skills"><thead><tr><th>Skill</th><th>Job ads asking</th><th></th><th>Change</th><th>In course</th><th>Hours</th></tr></thead><tbody>${skillsRows}</tbody></table></div></details>` : ""}
    <details class="card fold"><summary><h2>Modules and the skills found in them</h2></summary><ul class="modules">${modules}</ul></details>
  </div>`;
}

const LAST_REPORTS = {};
document.addEventListener("click", (e) => {
  const b = e.target.closest("[data-print]");
  if (!b) return;
  const report = b.closest(".report");
  $$(".report.print-me").forEach((x) => x.classList.remove("print-me"));
  report.classList.add("print-me");
  $$("details", report).forEach((d) => (d.open = true)); // print everything
  document.body.classList.add("printing");
  window.print();
});
window.addEventListener("afterprint", () => document.body.classList.remove("printing"));

// ---- market: gaps -------------------------------------------------------------------
function renderMatrix() {
  const m = call("matrix", ...filters());
  $("#matrix-filter-note").innerHTML = filterNote();
  const head = `<thead><tr><th></th>${m.skills.map((s) => `<th scope="col"><span>${esc(s.name)}</span></th>`).join("")}</tr></thead>`;
  const body = m.rows.map((row) => `<tr><th scope="row">${esc(row.name)}</th>${row.cells.map((c, i) => {
    const a = Math.min(0.95, c.share * 1.1);
    const gap = !c.taught && c.share >= 0.15;
    const label = `${row.name}, ${m.skills[i].name}: in ${pct(c.share)} of its job ads, ${c.taught ? "taught" : gap ? "missing" : "not taught"}`;
    return `<td class="${a > 0.55 ? "dark" : "light"}${gap ? " gap" : ""}" style="--a:${a.toFixed(2)}" title="${esc(label)}" aria-label="${esc(label)}">${c.taught ? "✓" : gap ? '<span class="gap-mark" aria-hidden="true">!</span>' : ""}</td>`;
  }).join("")}</tr>`).join("");
  $("#matrix").innerHTML = head + `<tbody>${body}</tbody>`;
  // the same facts as a list, for phones and projectors
  $("#gap-list").innerHTML = m.rows.map((row) => {
    const miss = row.cells.map((c, i) => ({ c, s: m.skills[i] })).filter(({ c }) => !c.taught && c.share >= 0.15).sort((a, b) => b.c.share - a.c.share);
    return `<div class="gap-row"><b>${esc(row.name)}</b>${miss.length
      ? `<div class="chips">${miss.map(({ c, s }) => `<span class="chip none">${esc(s.name)} <small>${pct(c.share)}</small></span>`).join("")}</div>`
      : '<span class="mute small">none of its most-asked skills is missing</span>'}</div>`;
  }).join("");
}

// ---- check my course --------------------------------------------------------------
function chipsFor(found) {
  const known = found.skills.length ? found.skills.map((s) => `<span class="chip have" title="matched: ${esc(s.matched.join(", "))}">${esc(s.name)}</span>`).join("") : '<span class="chip none">none yet</span>';
  const missed = found.unrecognised.length ? `<p class="small mute">Lines with no skill SkillAlign knows (not counted):</p><div class="chips">${found.unrecognised.map((u) => `<span class="chip none">${esc(u)}</span>`).join("")}</div>` : "";
  return { known, missed };
}

function renderCourse() {
  const { known, missed } = chipsFor(call("extract", $("#s-text").value));
  $("#syllabus-detected").innerHTML = `<p class="small mute">Skills found as you type:</p><div class="chips">${known}</div>${missed}`;
}
let detectTimer = null;
$("#s-text").addEventListener("input", () => {
  clearTimeout(detectTimer);
  detectTimer = setTimeout(() => api && renderCourse(), 250);
});

function pending(button, label) {
  // before the engine is ready a click is remembered and runs as soon as it is
  if (api) return false;
  button.textContent = "Getting ready…";
  button.disabled = true;
  whenReady(() => { button.textContent = label; button.disabled = false; button.click(); });
  return true;
}

$("#syllabus-form").addEventListener("submit", (e) => {
  e.preventDefault();
  if (pending($("#s-submit"), "Check this course")) return;
  const err = $("#s-error");
  err.hidden = true;
  try {
    const r = call("analyse_syllabus", $("#s-name").value, $("#s-roles").value, $("#s-text").value, $("#s-nsqf").value.trim(), $("#s-qp").value.trim());
    LAST_REPORTS.custom = r;
    $("#syllabus-result").innerHTML = reportHTML(r);
    countUp($("#syllabus-result"));
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
  if (api) renderCourse();
});
// common questions (site/faq.txt, bundled by build.py); shown once at least one is answered
fetch(`faq.json?v=${VERSION}`).then((r) => (r.ok ? r.json() : [])).then((list) => {
  if (!list.length) return;
  $("#faq").innerHTML = `<h2>Common questions</h2>${list.map((x) => `<details class="card fold"><summary><h3>${esc(x.q)}</h3></summary><p>${esc(x.a)}</p></details>`).join("")}`;
  $("#faq").hidden = false;
}).catch(() => {});

// real syllabi added by the team (data/example_syllabi/*.txt, bundled by build.py)
let EXAMPLES = [];
fetch(`examples.json?v=${VERSION}`).then((r) => (r.ok ? r.json() : [])).then((list) => {
  EXAMPLES = list;
  if (!list.length) return;
  $("#real-examples").innerHTML = `<p class="small mute">Or start from a real syllabus:</p><div class="chips">${list.map((x, i) =>
    `<button class="chip pick" type="button" data-real="${i}" title="added by ${esc(x.by)}">${esc(x.name)}</button>`).join("")}</div><p class="small mute" id="real-credit"></p>`;
  $("#real-examples").hidden = false;
}).catch(() => {});
$("#real-examples").addEventListener("click", (e) => {
  const b = e.target.closest("[data-real]");
  if (!b) return;
  const x = EXAMPLES[b.dataset.real];
  $("#s-name").value = x.name;
  $("#s-roles").value = x.roles;
  $("#s-text").value = x.text;
  $$("[data-real]").forEach((y) => y.classList.toggle("on", y === b));
  $("#real-credit").innerHTML = `Added by ${esc(x.by)} · <a href="${esc(x.source)}" rel="noopener">source</a>`;
  if (api) renderCourse();
});

$("#example-courses").addEventListener("click", (e) => {
  const b = e.target.closest("[data-example]");
  if (!b) return;
  $$("[data-example]").forEach((x) => x.classList.toggle("on", x === b));
  $("#example-result").innerHTML = reportHTML(call("program_report", b.dataset.example, "", "", ""), { example: true });
  countUp($("#example-result"));
  $("#example-result").scrollIntoView({ behavior: "smooth", block: "start" });
});

// ---- what should I learn ----------------------------------------------------------
$("#learner-form").addEventListener("submit", (e) => {
  e.preventDefault();
  if (pending($("#l-submit"), "Show what to learn")) return;
  const err = $("#l-error");
  err.hidden = true;
  const role = $("#l-role").value.trim();
  let r;
  try {
    r = call("learner", role, "[]", $("#l-text").value);
    if (!r.postings) throw new Error(`No job ads for "${role}" in this data. Start typing and pick a job from the list.`);
  } catch (ex) {
    err.textContent = ex.message;
    err.hidden = false;
    return;
  }
  const req = r.required.map((s) => `<span class="chip ${s.have ? "have" : "none"}">${s.have ? "✓" : "✗"} ${esc(s.name)} <small>${pct(s.share)}</small></span>`).join("");
  const programs = r.programs.length
    ? `<ul class="recs">${r.programs.map((p) => `<li><span class="act Add">${esc(p.duration || "")}</span><span><b>${esc(p.name)}</b> <span class="chip tiny">example course</span>${p.for_this_job ? '<span class="fit">built for this job</span>' : ""}<br>teaches ${p.covers.map(esc).join(", ")}.</span></li>`).join("")}</ul>`
    : `<p>None of the example courses teaches what you are missing.${r.next_skill ? ` Look for a short course in <b>${esc(r.next_skill.name)}</b> on <a href="https://www.skillindiadigital.gov.in/" rel="noopener">Skill India Digital</a> or at your nearest ITI.` : ""}</p>`;
  const missed = r.unrecognised.length ? `<p class="small mute">Words we could not match to a skill (if any are skills, you are more ready than this shows): ${r.unrecognised.map((u) => `<span class="chip none">${esc(u)}</span>`).join(" ")}</p>` : "";
  const next = r.next_skill
    ? `<div class="next"><span class="l">Learn next</span><b>${esc(r.next_skill.name)}</b><span>asked for in ${pct(r.next_skill.share)} of these job ads${r.next_skill.is_new || (r.next_skill.significant && r.next_skill.growth > 0) ? ", and rising" : ""}.</span></div>`
    : `<div class="next"><span class="l">Good news</span><b>You have every skill these job ads often ask for.</b></div>`;
  $("#learner-result").innerHTML = `<div class="report">
    <article class="card">${next}
      <div class="ready">${ring(r.readiness)}<div>
        <h2>${Math.round(r.readiness)}% ready for ${esc(titleCase(role))}</h2>
        <p class="mute small">Based on the skills in ${plural(r.postings, "job ad")} for this job, weighted by how often each is asked for. This is about skills on paper, not about you.</p>
      </div></div>
      ${r.low_data ? `<p class="notice">Only ${plural(r.postings, "job ad")} for this job in this data, so treat this as a rough guide.${META.source === "real" ? ' <button class="link" type="button" data-use="sample">Try the practice data</button> to see how it works with more ads.' : ""}</p>` : ""}
    </article>
    <article class="card"><h2>What employers ask for</h2><p class="mute small">Skills in 15% or more of these job ads. Green: you have it. Red: not yet.</p><div class="chips">${req}</div>
      ${r.have.length ? `<p class="small mute">Skills we read from what you wrote: ${r.have.map(esc).join(", ")}.</p>` : ""}${missed}</article>
    <article class="card"><h2>Courses that teach what you are missing</h2>${programs}</article>
  </div>`;
  $("#learner-result").scrollIntoView({ behavior: "smooth", block: "start" });
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
  document.body.classList.add("busy");
  await new Promise((r) => setTimeout(r, 30)); // let the message paint before Python runs
  try {
    META = call("load_uploaded", await file.text());
    status.innerHTML = `Loaded <b>${fmt(META.postings)}</b> job ads from ${esc(file.name)}.` +
      (META.problem_count ? ` Skipped ${META.problem_count} rows: ${META.problems.slice(0, 3).map(esc).join("; ")}${META.problem_count > 3 ? "…" : ""}` : "");
    dataChanged();
  } catch (ex) {
    status.innerHTML = `<span class="error">Nothing changed: ${esc(ex.message)}</span>`;
  } finally {
    document.body.classList.remove("busy");
  }
  e.target.value = "";
});
$("#reset-sample").addEventListener("click", () => {
  if (!api) return;
  META = call("use_sample");
  $("#upload-status").textContent = "Back on the practice data.";
  dataChanged();
});

// ---- language ------------------------------------------------------------------
// Static text marked data-i18n is translated from site/i18n/<lang>.json, where each
// key is the English text itself. A missing or empty value shows the English.
const I18N = $$("[data-i18n]").map((el) => {
  const node = [...el.childNodes].find((n) => n.nodeType === 3 && n.textContent.trim());
  return node && { node, en: node.textContent.replace(/\s+/g, " ").trim(), raw: node.textContent };
}).filter(Boolean);

async function setLang(lang) {
  let dict = {};
  if (lang !== "en") {
    try { dict = await (await fetch(`i18n/${lang}.json?v=${VERSION}`)).json(); } catch { dict = {}; }
  }
  for (const { node, en, raw } of I18N) {
    const t = (dict[en] || "").trim();
    node.textContent = t ? raw.replace(raw.trim(), t) : raw;
  }
  document.documentElement.lang = lang;
  $("#lang").value = lang;
  try { localStorage.setItem("skillalign-lang", lang); } catch {}
}
$("#lang").addEventListener("change", (e) => setLang(e.target.value));
let savedLang = "en";
try { savedLang = localStorage.getItem("skillalign-lang") || "en"; } catch {}
if (savedLang !== "en") setLang(savedLang);

route();
lastPage = document.body.dataset.page;
boot();
