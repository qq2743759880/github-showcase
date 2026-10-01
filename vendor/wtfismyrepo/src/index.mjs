/**
 * Public library surface for wtfismyrepo.
 *
 *   import { analyze, renderText } from "wtfismyrepo";
 *   const report = analyze(".");
 *   console.log(renderText(report));
 */
export { analyze } from "./analyze.mjs";
export { renderText, renderJSON } from "./report.mjs";
export { pageRank } from "./pagerank.mjs";
export { buildGraph, extractImports, resolveImport } from "./graph.mjs";
export { scoreFiles } from "./fragility.mjs";
export { detectEntryPoints } from "./entrypoints.mjs";
export { installSkill } from "./install.mjs";

// ADHD engine layer (github.com/UditAkhourii/adhd, MIT) — turns the
// deterministic analysis into a divergent onboarding explanation.
export { buildADHDContext, runADHDExplain } from "./explain.mjs";
export { selectOnboardingFrames, ONBOARDING_FRAMES } from "./onboarding-frames.mjs";
