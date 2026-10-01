#!/usr/bin/env node
/**
 * wtfismyrepo CLI — point it at a repo and it tells you what's going on.
 *
 *   wtfismyrepo [path] [--json] [--no-history] [--top N] [--no-color]
 *   wtfismyrepo explain [path] [--frames N] [--top N] [--level new-grad|mid|senior]
 *   wtfismyrepo install [--global|--project] [--force]
 *   wtfismyrepo uninstall
 */
import { analyze } from "../src/analyze.mjs";
import { renderText, renderJSON } from "../src/report.mjs";
import { installSkill, manualHelp } from "../src/install.mjs";
import { buildADHDContext, runADHDExplain } from "../src/explain.mjs";

function parseArgs(argv) {
  const opts = {
    command: "analyze",
    path: ".",
    json: false,
    history: true,
    top: 10,
    color: true,
    target: "global",
    force: false,
    frames: 5,
    level: "",
    goal: "",
  };
  const rest = [...argv];
  if (["install", "uninstall", "explain"].includes(rest[0])) {
    opts.command = rest.shift();
  }
  for (let i = 0; i < rest.length; i++) {
    const a = rest[i];
    if (a === "--json") opts.json = true;
    else if (a === "--no-history") opts.history = false;
    else if (a === "--no-color") opts.color = false;
    else if (a === "--top") opts.top = parseInt(rest[++i], 10) || 10;
    else if (a === "--frames") opts.frames = parseInt(rest[++i], 10) || 5;
    else if (a === "--level") opts.level = rest[++i] ?? "";
    else if (a === "--goal") opts.goal = rest[++i] ?? "";
    else if (a === "--project") opts.target = "project";
    else if (a === "--global") opts.target = "global";
    else if (a === "--force") opts.force = true;
    else if (a === "-h" || a === "--help") opts.help = true;
    else if (!a.startsWith("-")) opts.path = a;
  }
  return opts;
}

const c = {
  bold: (s) => `\x1b[1m${s}\x1b[0m`,
  cyan: (s) => `\x1b[36m${s}\x1b[0m`,
  yellow: (s) => `\x1b[33m${s}\x1b[0m`,
  dim: (s) => `\x1b[2m${s}\x1b[0m`,
  green: (s) => `\x1b[32m${s}\x1b[0m`,
};

const HELP = `wtfismyrepo — stop being lost in a codebase
Powered by the ADHD diverge→score→deepen engine (github.com/UditAkhourii/adhd)

Usage:
  wtfismyrepo [path]            Structural analysis: PageRank + churn + GitHub history
  wtfismyrepo explain [path]   ADHD-powered onboarding: divergent frames → best explanation
  wtfismyrepo install           Install as a Claude Code skill
  wtfismyrepo uninstall         Remove the installed skill

Analyze options:
  --json            Machine-readable JSON (what the skill and explain consume)
  --no-history      Skip GitHub PR/issue fetch (offline / faster)
  --top N           Show top N ranked files (default 10)
  --no-color        Disable ANSI colors

Explain options (requires adhd-agent: npm install -g adhd-agent):
  --level STR       Developer experience: new-grad | mid | senior | domain-expert
  --goal  STR       Developer goal: "fix a bug" | "add a feature" | "understand"
  --frames N        Number of ADHD divergent frames to generate (default 5)
  --top N           Top-K frames to deepen (default 2)
  --json            Emit raw ADHD result as JSON

Install options:
  --global          Install to ~/.claude/skills/ (all projects) [default]
  --project         Install to ./.claude/skills/ (this repo only)
  --force           Overwrite an existing install`;

function runInstall(opts) {
  const res = installSkill({ target: opts.target, force: opts.force });
  console.log(res.message);
  if (!res.installed && !res.dest) {
    console.log("\n" + manualHelp());
    process.exit(1);
  }
}

function runUninstall(opts) {
  import("node:fs").then(({ default: fs }) =>
    import("node:os").then(({ default: os }) =>
      import("node:path").then(({ default: path }) => {
        const base =
          opts.target === "project"
            ? path.join(process.cwd(), ".claude", "skills", "wtfismyrepo")
            : path.join(os.homedir(), ".claude", "skills", "wtfismyrepo");
        if (fs.existsSync(base)) {
          fs.rmSync(base, { recursive: true, force: true });
          console.log(`🗑️  Removed wtfismyrepo skill from ${base}`);
        } else {
          console.log(`Nothing to remove at ${base}`);
        }
      }),
    ),
  );
}

async function runExplain(opts) {
  let analysis;
  try {
    analysis = analyze(opts.path, { history: opts.history, top: opts.top });
  } catch (err) {
    console.error("wtfismyrepo: analysis failed —", err.message);
    process.exit(1);
  }

  const dev = {
    experience: opts.level || undefined,
    goal: opts.goal || undefined,
  };

  // Show the structural analysis first regardless.
  if (!opts.json) {
    console.log(renderText(analysis, { color: opts.color }));
    console.log(
      c.bold(c.cyan("\n━━ ADHD EXPLAIN ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")),
    );
    console.log(
      c.dim(
        "  Running the ADHD diverge→score→cluster→deepen engine on the analysis…\n" +
        "  (github.com/UditAkhourii/adhd — parallel frames, no cross-talk)\n",
      ),
    );
  }

  const res = await runADHDExplain(analysis, {
    dev,
    framesPerRun: opts.frames,
    topK: opts.top,
    onEvent: opts.json
      ? undefined
      : (e) => {
          if (e.kind === "frame:start") process.stdout.write(c.dim(`  ↳ frame: ${e.frameLabel}\n`));
          if (e.kind === "score:done") process.stdout.write(c.dim(`  ✓ scored ${e.total} ideas\n`));
          if (e.kind === "deepen:start") process.stdout.write(c.dim(`  ↳ deepening: ${e.text.slice(0, 60)}…\n`));
        },
  });

  if (opts.json) {
    console.log(JSON.stringify(res, null, 2));
    return;
  }

  if (!res.available) {
    console.log(c.yellow("  adhd-agent not installed — printing the ADHD context prompt instead."));
    console.log(c.dim("  Install: npm install -g adhd-agent\n"));
    console.log(c.bold("  PROBLEM:\n"), res.problem);
    console.log(c.bold("\n  CONTEXT (paste this into your ADHD session):\n"), res.context);
    return;
  }

  const r = res.result;
  if (r.nonObviousPick) {
    console.log(c.bold("  🎯 Best onboarding angle (non-obvious pick):"));
    console.log(`     ${r.nonObviousPick.text}`);
    console.log();
  }
  if (r.shortlist?.length) {
    console.log(c.bold("  Shortlist:"));
    for (const i of r.shortlist) console.log(`  • ${i.text}`);
    console.log();
  }
  if (r.traps?.length) {
    console.log(c.yellow("  ⚠  Traps (onboarding angles that look helpful but aren't):"));
    for (const t of r.traps) console.log(c.dim(`  ✗ ${t.text} — ${t.score?.trap}`));
    console.log();
  }
  if (r.deepened?.length) {
    console.log(c.bold("  Deepened:"));
    for (const d of r.deepened) {
      const idea = r.shortlist.find((i) => i.id === d.ideaId);
      if (idea) console.log(c.bold(`\n  ▶ ${idea.text}`));
      console.log(`  ${d.sketch}`);
    }
  }
  if (r.provocation) {
    console.log(c.yellow(`\n  💡 ${r.provocation}`));
  }
}

async function main() {
  const opts = parseArgs(process.argv.slice(2));
  if (opts.help) { console.log(HELP); return; }
  if (opts.command === "install") { runInstall(opts); return; }
  if (opts.command === "uninstall") { runUninstall(opts); return; }
  if (opts.command === "explain") { await runExplain(opts); return; }

  let analysis;
  try {
    analysis = analyze(opts.path, { history: opts.history, top: opts.top });
  } catch (err) {
    console.error("wtfismyrepo: analysis failed —", err.message);
    process.exit(1);
  }
  console.log(opts.json ? renderJSON(analysis) : renderText(analysis, { color: opts.color }));
}

main().catch((err) => { console.error(err.message); process.exit(1); });
