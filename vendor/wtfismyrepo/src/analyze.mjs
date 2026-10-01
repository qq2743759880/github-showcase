/**
 * The engine. Orchestrates every signal into a single analysis object that the
 * CLI renders and the Claude skill consumes.
 */
import fs from "node:fs";
import path from "node:path";
import { detectStack } from "./detect.mjs";
import { listFiles, readSources } from "./scan.mjs";
import { buildGraph } from "./graph.mjs";
import { pageRank } from "./pagerank.mjs";
import { fileChurn, isGitRepo } from "./git.mjs";
import { scoreFiles } from "./fragility.mjs";
import { detectEntryPoints } from "./entrypoints.mjs";
import { fetchHistory, hotZones } from "./history.mjs";

function readJSON(file) {
  try {
    return JSON.parse(fs.readFileSync(file, "utf8"));
  } catch {
    return {};
  }
}

function topLevelMap(files) {
  const dirs = new Map();
  for (const f of files) {
    const top = f.includes("/") ? f.split("/")[0] : "(root files)";
    dirs.set(top, (dirs.get(top) ?? 0) + 1);
  }
  return [...dirs.entries()].map(([dir, count]) => ({ dir, count })).sort((a, b) => b.count - a.count);
}

/**
 * @param {string} cwd
 * @param {object} [opts]
 * @param {boolean} [opts.history=true]  fetch GitHub PR/issue data
 * @param {number}  [opts.top=10]        how many ranked files to keep
 */
export function analyze(cwd, opts = {}) {
  const withHistory = opts.history ?? true;
  const top = opts.top ?? 10;

  const exists = (f) => fs.existsSync(path.join(cwd, f));
  const stack = detectStack(exists);
  const pkg = exists("package.json") ? readJSON(path.join(cwd, "package.json")) : {};

  const files = listFiles(cwd);
  const sources = readSources(cwd, files);
  const graph = buildGraph(sources);
  const rank = pageRank(graph);

  const git = isGitRepo(cwd);
  const churn = git ? fileChurn(cwd) : new Map();
  const { importance, fragility } = scoreFiles(rank, churn);

  const entryPoints = detectEntryPoints(files, pkg);
  const history = withHistory ? fetchHistory(cwd) : { available: false, openPRs: [], mergedPRs: [], openIssues: [], goodFirstIssues: [] };
  const hot = hotZones(history.openPRs);

  return {
    cwd,
    stack,
    pkg: { name: pkg.name, description: pkg.description, scripts: pkg.scripts ? Object.keys(pkg.scripts) : [] },
    hasReadme: ["README.md", "README.rst", "readme.md"].some(exists),
    counts: {
      files: files.length,
      sourceFiles: sources.size,
      edges: [...graph.values()].reduce((n, s) => n + s.size, 0),
      isGit: git,
    },
    topLevel: topLevelMap(files),
    entryPoints: entryPoints.slice(0, 8),
    importance: importance.slice(0, top),
    fragility: fragility.slice(0, top),
    hotZones: [...hot.entries()].map(([file, prs]) => ({ file, prs })).slice(0, top),
    history,
  };
}
