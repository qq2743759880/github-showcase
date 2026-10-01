/**
 * explain.mjs — format a wtfismyrepo analysis as an ADHD problem statement.
 *
 * ADHD (github.com/UditAkhourii/adhd, MIT) takes a `problem` string and an
 * optional `context` string, then fans out across cognitive frames to generate
 * diverse approaches. This module formats wtfismyrepo's deterministic analysis
 * output into exactly those two things:
 *
 *   problem  = "How should I explain and onboard a developer onto <repo>?"
 *   context  = the full structural intelligence: entry points, spine, fragility,
 *               hot zones, GitHub signals — everything ADHD needs to generate
 *               onboarding angles that are grounded in *this* codebase.
 *
 * Usage (Claude Code skill layer — ADHD handles the LLM calls):
 *   const { problem, context } = buildADHDContext(analysis, developerProfile);
 *   // pass to ADHD's run() or embed in the SKILL.md prompt
 *
 * Usage (programmatic — requires adhd-agent installed):
 *   const result = await runADHDExplain(analysis, { framesPerRun: 5, topK: 2 });
 */

/**
 * Build the ADHD `problem` + `context` for a codebase onboarding task.
 *
 * @param {object} analysis  output of analyze()
 * @param {object} [dev]     optional developer profile
 * @param {string} [dev.experience]  "new-grad" | "mid" | "senior" | "domain-expert"
 * @param {string} [dev.goal]        "fix a bug" | "add a feature" | "understand" | "review"
 * @returns {{ problem: string, context: string }}
 */
export function buildADHDContext(analysis, dev = {}) {
  const repoName = analysis.pkg?.name ?? analysis.cwd.split(/[\\/]/).pop() ?? "this repo";
  const devDesc = dev.experience
    ? `The developer is ${dev.experience} level. Their goal: ${dev.goal ?? "understand the codebase"}.`
    : "No developer profile provided — optimize for someone new to the codebase.";

  const problem = `How should I explain and onboard a developer onto "${repoName}"? ${devDesc}`;

  const spineList = (analysis.importance ?? [])
    .slice(0, 6)
    .map((f, i) => `  ${i + 1}. ${f.file}`)
    .join("\n");

  const fragilityList = (analysis.fragility ?? [])
    .slice(0, 5)
    .map((f) => `  ${f.file} (${f.churn} changes)`)
    .join("\n") || "  (not enough git history yet)";

  const entryList = (analysis.entryPoints ?? [])
    .slice(0, 4)
    .map((e) => `  ${e.file}  [${e.why}]`)
    .join("\n") || "  none detected";

  const hotList = (analysis.hotZones ?? [])
    .slice(0, 5)
    .map((z) => `  ${z.file}  [PR ${z.prs.map((n) => "#" + n).join(", ")}]`)
    .join("\n") || "  none";

  const openIssues = (analysis.history?.openIssues ?? [])
    .slice(0, 5)
    .map((i) => `  #${i.number} ${i.title}`)
    .join("\n") || "  none";

  const goodFirst = (analysis.history?.goodFirstIssues ?? [])
    .slice(0, 3)
    .map((i) => `  #${i.number} ${i.title}`)
    .join("\n") || "  none";

  const context = `
## Codebase intelligence (from wtfismyrepo analysis)

**Stack:** ${analysis.stack?.languages?.join(", ") || "unknown"}
**Size:** ${analysis.counts?.files ?? "?"} files, ${analysis.counts?.sourceFiles ?? "?"} source files, ${analysis.counts?.edges ?? 0} internal import edges
**README present:** ${analysis.hasReadme ? "yes" : "no"}
**Run scripts:** ${analysis.pkg?.scripts?.join(", ") || "none detected"}

**Entry points (where execution starts):**
${entryList}

**THE SPINE — structurally central files (PageRank):**
Read these first; everything else depends on them.
${spineList || "  (not enough source to rank)"}

**HANDLE WITH CARE — most fragile (central × git churn):**
${fragilityList}

**HOT ZONES — files under active open PRs (touching these risks conflicts):**
${hotList}

**Open issues (where it hurts):**
${openIssues}

**Good first issues (where a newcomer should start):**
${goodFirst}

**Top-level layout:**
${(analysis.topLevel ?? []).slice(0, 8).map((d) => `  ${d.dir}  (${d.count} files)`).join("\n")}
`.trim();

  return { problem, context };
}

/**
 * If adhd-agent is installed in the user's environment, run it
 * programmatically on the formatted context. Falls back gracefully with a
 * human-readable message if the package is not available.
 *
 * @param {object} analysis  from analyze()
 * @param {object} [opts]
 * @param {object} [opts.dev]          developer profile
 * @param {number} [opts.framesPerRun] default 5
 * @param {number} [opts.topK]         default 2
 * @returns {Promise<{available:boolean, result?:object, context:string, problem:string}>}
 */
export async function runADHDExplain(analysis, opts = {}) {
  const { problem, context } = buildADHDContext(analysis, opts.dev ?? {});

  let adhdRun;
  try {
    const adhd = await import("adhd-agent");
    adhdRun = adhd.run;
  } catch {
    return {
      available: false,
      problem,
      context,
      message: [
        "adhd-agent is not installed — the ADHD diverge→score→deepen engine is unavailable.",
        "Install it with: npm install -g adhd-agent",
        "",
        "Without it, the wtfismyrepo skill still uses the ADHD method manually:",
        "the SKILL.md instructs Claude to run the diverge→score→deepen loop itself.",
      ].join("\n"),
    };
  }

  const result = await adhdRun({
    problem,
    context,
    framesPerRun: opts.framesPerRun ?? 5,
    topK: opts.topK ?? 2,
    codeMode: true,
    onEvent: opts.onEvent,
  });

  return { available: true, problem, context, result };
}
