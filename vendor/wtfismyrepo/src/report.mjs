/**
 * Render an analysis object as a human-readable terminal report or as JSON
 * (for the Claude skill / other tooling to consume).
 */

const c = {
  bold: (s) => `\x1b[1m${s}\x1b[0m`,
  dim: (s) => `\x1b[2m${s}\x1b[0m`,
  cyan: (s) => `\x1b[36m${s}\x1b[0m`,
  yellow: (s) => `\x1b[33m${s}\x1b[0m`,
  red: (s) => `\x1b[31m${s}\x1b[0m`,
  green: (s) => `\x1b[32m${s}\x1b[0m`,
};

export function renderJSON(a) {
  return JSON.stringify(a, null, 2);
}

export function renderText(a, { color = true } = {}) {
  const p = color ? c : Object.fromEntries(Object.keys(c).map((k) => [k, (s) => s]));
  const L = [];
  const h = (t) => L.push("", p.bold(p.cyan(`━━ ${t} `.padEnd(60, "━"))));

  L.push(p.bold("🤯  wtfismyrepo — onboarding report"));
  L.push(p.dim(a.cwd));

  h("WHAT IS THIS");
  L.push(`Stack:        ${a.stack.languages.join(", ") || "unknown"}`);
  if (a.pkg.name) L.push(`Package:      ${a.pkg.name}`);
  if (a.pkg.description) L.push(`Purpose:      ${a.pkg.description}`);
  if (a.pkg.scripts.length) L.push(`Run scripts:  ${a.pkg.scripts.join(", ")}`);
  L.push(`README:       ${a.hasReadme ? p.green("present — read it first") : p.red("MISSING — verify claims against code")}`);
  L.push(`Size:         ${a.counts.files} files, ${a.counts.sourceFiles} source, ${a.counts.edges} internal imports`);

  h("THE MAP — top-level layout");
  for (const d of a.topLevel.slice(0, 10)) L.push(`  ${String(d.count).padStart(4)}  ${d.dir}`);

  h("START READING HERE — entry points");
  if (a.entryPoints.length === 0) L.push(p.dim("  none detected by convention"));
  for (const e of a.entryPoints) L.push(`  → ${e.file}  ${p.dim(`(${e.why})`)}`);

  h("THE SPINE — most central files (PageRank)");
  L.push(p.dim("  read these first; everything depends on them"));
  for (const f of a.importance) {
    if (f.score <= 0) continue;
    L.push(`  ${bar(f.score)} ${f.file}`);
  }

  h("HANDLE WITH CARE — most fragile files");
  L.push(p.dim("  central AND high-churn = most likely to bite you"));
  if (a.fragility.length === 0) L.push(p.dim("  (needs git history to score)"));
  for (const f of a.fragility) {
    L.push(`  ${bar(f.score)} ${f.file} ${p.dim(`(${f.churn} changes)`)}`);
  }

  h("THE HISTORY — what's happening on GitHub");
  if (!a.history.available) {
    L.push(p.dim("  gh CLI unavailable/unauthenticated — skipped. `gh auth login` to enable."));
  } else {
    L.push(p.yellow(`  🔥 ${a.history.openPRs.length} open PRs (hot zones — avoid surprising people)`));
    for (const pr of a.history.openPRs.slice(0, 5)) L.push(`     #${pr.number} ${pr.title}`);
    if (a.hotZones.length) {
      L.push(p.yellow("  files under active PRs:"));
      for (const z of a.hotZones.slice(0, 5)) L.push(`     ${z.file} ${p.dim(`(PR ${z.prs.map((n) => "#" + n).join(", ")})`)}`);
    }
    L.push(p.red(`  🩹 ${a.history.openIssues.length} open issues (where it hurts)`));
    for (const is of a.history.openIssues.slice(0, 5)) L.push(`     #${is.number} ${is.title}`);
    if (a.history.goodFirstIssues.length) {
      L.push(p.green("  🌱 good first issues — START HERE:"));
      for (const is of a.history.goodFirstIssues) L.push(`     #${is.number} ${is.title}`);
    }
  }

  h("YOUR FIRST MOVE");
  const firstRead = a.entryPoints[0]?.file ?? a.importance[0]?.file;
  if (firstRead) L.push(`  1. Open ${p.bold(firstRead)} and read top-to-bottom.`);
  if (a.importance[0]) L.push(`  2. Then trace into ${p.bold(a.importance[0].file)} — it's the spine.`);
  const start = a.history.goodFirstIssues[0];
  if (start) L.push(`  3. Pick up issue #${start.number}: "${start.title}".`);
  if (a.fragility[0]) L.push(`  ${p.red("⚠")}  Before editing ${a.fragility[0].file}, know it's the most fragile file here.`);

  L.push("");
  return L.join("\n");
}

function bar(score) {
  const n = Math.round(score * 10);
  return "█".repeat(n).padEnd(10, "░");
}
