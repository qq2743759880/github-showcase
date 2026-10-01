/**
 * GitHub history signals via the `gh` CLI: open PRs (hot zones), merged PRs
 * (conventions), and open issues (pain). All calls are best-effort — if `gh`
 * is missing, unauthenticated, or the repo has no remote, we degrade
 * gracefully and the rest of the analysis still works.
 */
import { execSync } from "node:child_process";

function gh(args, cwd) {
  try {
    return execSync(`gh ${args}`, { cwd, encoding: "utf8", stdio: ["ignore", "pipe", "ignore"] });
  } catch {
    return null;
  }
}

export function ghAvailable(cwd) {
  const v = gh("--version", cwd);
  if (!v) return false;
  // Confirm this dir maps to a GitHub repo.
  return gh("repo view --json nameWithOwner", cwd) !== null;
}

function json(args, cwd, fallback = []) {
  const out = gh(args, cwd);
  if (!out) return fallback;
  try {
    return JSON.parse(out);
  } catch {
    return fallback;
  }
}

export function fetchHistory(cwd) {
  if (!ghAvailable(cwd)) {
    return { available: false, openPRs: [], mergedPRs: [], openIssues: [], goodFirstIssues: [] };
  }
  return {
    available: true,
    openPRs: json('pr list --state open --limit 20 --json number,title,author,files', cwd),
    mergedPRs: json('pr list --state merged --limit 15 --json number,title', cwd),
    openIssues: json('issue list --state open --limit 30 --json number,title,labels', cwd),
    goodFirstIssues: json('issue list --state open --label "good first issue" --limit 10 --json number,title', cwd),
  };
}

/**
 * Map files currently touched by open PRs -> the PRs touching them.
 * These are "hot zones": editing them risks conflicts and the design is in flux.
 * @returns {Map<string, number[]>} file -> PR numbers
 */
export function hotZones(openPRs) {
  const map = new Map();
  for (const pr of openPRs) {
    for (const f of pr.files ?? []) {
      const path = f.path ?? f;
      if (!path) continue;
      if (!map.has(path)) map.set(path, []);
      map.get(path).push(pr.number);
    }
  }
  return map;
}
