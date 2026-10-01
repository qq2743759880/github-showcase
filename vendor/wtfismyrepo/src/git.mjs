/**
 * Git-derived signals: per-file churn (how often a file changes).
 * High churn = actively edited = either important or fragile (often both).
 */
import { execSync } from "node:child_process";

function sh(cmd, cwd) {
  try {
    return execSync(cmd, { cwd, encoding: "utf8", stdio: ["ignore", "pipe", "ignore"] });
  } catch {
    return null;
  }
}

export function isGitRepo(cwd) {
  return sh("git rev-parse --is-inside-work-tree", cwd)?.trim() === "true";
}

/**
 * @returns {Map<string, number>} repo-relative file -> commit-touch count
 */
export function fileChurn(cwd, { since = "" } = {}) {
  const range = since ? `--since="${since}"` : "";
  const out = sh(`git log ${range} --pretty=format: --name-only`, cwd);
  const churn = new Map();
  if (!out) return churn;
  for (const line of out.split("\n")) {
    const f = line.trim();
    if (!f) continue;
    churn.set(f, (churn.get(f) ?? 0) + 1);
  }
  return churn;
}

/** Files tracked by git (respects .gitignore). */
export function trackedFiles(cwd) {
  const out = sh("git ls-files", cwd);
  return out ? out.split("\n").map((l) => l.trim()).filter(Boolean) : [];
}
