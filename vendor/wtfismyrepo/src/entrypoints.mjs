/**
 * Heuristic entry-point detection: where execution begins. Combines manifest
 * declarations (package.json main/bin, go module main) with conventional
 * filename patterns, ranked so the CLI can show "start reading here".
 */
import path from "node:path";

const NAME_PATTERNS = [
  { re: /(^|\/)main\.(js|mjs|ts|py|go)$/, weight: 5, why: "conventional main entry" },
  { re: /(^|\/)index\.(js|mjs|ts|tsx)$/, weight: 4, why: "package/module index" },
  { re: /(^|\/)app\.(js|mjs|ts|py)$/, weight: 4, why: "application bootstrap" },
  { re: /(^|\/)server\.(js|mjs|ts|py)$/, weight: 4, why: "server bootstrap" },
  { re: /(^|\/)cli\.(js|mjs|ts|py)$/, weight: 3, why: "CLI entry" },
  { re: /(^|\/)__main__\.py$/, weight: 5, why: "python module entry" },
  { re: /(^|\/)cmd\/.+\.go$/, weight: 4, why: "go command entry" },
  { re: /(^|\/)wsgi\.py$/, weight: 3, why: "wsgi app" },
  { re: /(^|\/)manage\.py$/, weight: 3, why: "django manage" },
];

/**
 * @param {string[]} files
 * @param {object} pkg  parsed package.json (or {})
 * @returns {Array<{file:string, weight:number, why:string}>}
 */
export function detectEntryPoints(files, pkg = {}) {
  const fileSet = new Set(files);
  const found = new Map();
  const add = (file, weight, why) => {
    if (!file || !fileSet.has(file)) return;
    const cur = found.get(file);
    if (!cur || weight > cur.weight) found.set(file, { file, weight, why });
  };

  // Manifest-declared entries are the strongest signal.
  if (pkg.main) add(norm(pkg.main), 6, "package.json main");
  if (pkg.module) add(norm(pkg.module), 6, "package.json module");
  if (pkg.bin) {
    const bins = typeof pkg.bin === "string" ? [pkg.bin] : Object.values(pkg.bin);
    for (const b of bins) add(norm(b), 6, "package.json bin");
  }

  for (const f of files) {
    for (const p of NAME_PATTERNS) {
      if (p.re.test(f)) add(f, p.weight, p.why);
    }
  }

  return [...found.values()].sort((a, b) => b.weight - a.weight);
}

function norm(p) {
  return path.posix.normalize(String(p).replace(/^\.\//, "").replace(/\\/g, "/"));
}
