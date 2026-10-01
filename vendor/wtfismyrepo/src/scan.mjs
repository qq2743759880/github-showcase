/**
 * Walk a repo directory and read parseable source files.
 * Prefers git-tracked files (respects .gitignore); falls back to a manual
 * walk that skips known-noise directories.
 */
import fs from "node:fs";
import path from "node:path";
import { PARSEABLE_EXT, IGNORE_DIRS } from "./detect.mjs";
import { trackedFiles, isGitRepo } from "./git.mjs";

const MAX_FILE_BYTES = 1_000_000; // skip giant generated/minified files

function walk(dir, root, acc) {
  let entries;
  try {
    entries = fs.readdirSync(dir, { withFileTypes: true });
  } catch {
    return;
  }
  for (const e of entries) {
    if (e.name.startsWith(".") && e.name !== ".") {
      if (IGNORE_DIRS.has(e.name)) continue;
    }
    const full = path.join(dir, e.name);
    if (e.isDirectory()) {
      if (IGNORE_DIRS.has(e.name)) continue;
      walk(full, root, acc);
    } else if (e.isFile()) {
      acc.push(path.relative(root, full).split(path.sep).join("/"));
    }
  }
}

/** @returns {string[]} repo-relative paths of all candidate files */
export function listFiles(cwd) {
  if (isGitRepo(cwd)) {
    const tracked = trackedFiles(cwd);
    if (tracked.length) return tracked;
  }
  const acc = [];
  walk(cwd, cwd, acc);
  return acc;
}

/**
 * @returns {Map<string,string>} repo-relative path -> source text,
 *          for parseable source files only.
 */
export function readSources(cwd, files) {
  const out = new Map();
  for (const rel of files) {
    if (!PARSEABLE_EXT.has(path.extname(rel))) continue;
    const full = path.join(cwd, rel);
    try {
      const stat = fs.statSync(full);
      if (stat.size > MAX_FILE_BYTES) continue;
      out.set(rel, fs.readFileSync(full, "utf8"));
    } catch {
      /* unreadable file — skip */
    }
  }
  return out;
}
