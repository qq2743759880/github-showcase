/**
 * Build a directed import graph from a set of source files.
 *
 * Edge A -> B means file A imports/depends on file B (both internal repo
 * files). External/library imports are ignored — we only care about the
 * internal coupling structure, which is what PageRank ranks.
 */
import path from "node:path";

/** Extract raw import specifiers from a source string, per language. */
export function extractImports(content, ext) {
  const specs = [];
  const push = (re) => {
    let m;
    while ((m = re.exec(content)) !== null) {
      const spec = m[1] ?? m[2];
      if (spec) specs.push(spec);
    }
  };

  if ([".js", ".jsx", ".mjs", ".cjs", ".ts", ".tsx"].includes(ext)) {
    // import ... from 'x' ; import 'x' ; export ... from 'x'
    push(/(?:import|export)[^'"]*?from\s*['"]([^'"]+)['"]/g);
    push(/import\s*['"]([^'"]+)['"]/g);
    // require('x') and dynamic import('x')
    push(/require\(\s*['"]([^'"]+)['"]\s*\)/g);
    push(/import\(\s*['"]([^'"]+)['"]\s*\)/g);
  } else if (ext === ".py") {
    // from .pkg.mod import x   |   import pkg.mod
    push(/^\s*from\s+([.\w]+)\s+import\s+/gm);
    push(/^\s*import\s+([.\w]+)/gm);
  } else if (ext === ".go") {
    // single import "x"  and  grouped import ( "x" \n "y" )
    push(/import\s+"([^"]+)"/g);
    push(/^\s*"([^"]+)"\s*$/gm); // lines inside an import ( ... ) block
  }
  return specs;
}

/**
 * Resolve an import specifier to an actual repo file, if it is internal.
 * Returns the normalized repo-relative path, or null for external deps.
 *
 * @param {string} spec        the raw import string
 * @param {string} fromFile    repo-relative path of the importing file
 * @param {Set<string>} fileSet  set of all repo-relative source files
 * @param {string} ext         extension of the importing file
 */
export function resolveImport(spec, fromFile, fileSet, ext) {
  // Only relative specs are unambiguously internal for JS/TS/Python.
  const isRelative = spec.startsWith(".") || spec.startsWith("/");

  if ([".py"].includes(ext)) {
    // Python: leading dots = relative package. Convert dotted path to slashes.
    if (!spec.startsWith(".")) return null; // absolute import: usually external/stdlib
    const dots = spec.match(/^\.+/)[0].length;
    const rest = spec.slice(dots).replace(/\./g, "/");
    const baseDir = path.posix.dirname(fromFile);
    const up = baseDir.split("/").slice(0, baseDir.split("/").length - (dots - 1)).join("/");
    const target = path.posix.join(up, rest);
    return firstExisting([`${target}.py`, `${target}/__init__.py`], fileSet);
  }

  if (ext === ".go") {
    // Go imports are module paths; map by suffix match to an internal dir.
    const hit = [...fileSet].find((f) => f.endsWith(".go") && path.posix.dirname(f).endsWith(spec.split("/").pop()));
    return hit ?? null;
  }

  // JS/TS
  if (!isRelative) return null; // bare specifier = npm package
  const baseDir = path.posix.dirname(fromFile);
  const target = path.posix.normalize(path.posix.join(baseDir, spec)).replace(/\\/g, "/");
  const candidates = [
    target,
    `${target}.ts`, `${target}.tsx`, `${target}.js`, `${target}.jsx`, `${target}.mjs`, `${target}.cjs`,
    `${target}/index.ts`, `${target}/index.tsx`, `${target}/index.js`, `${target}/index.mjs`,
  ];
  return firstExisting(candidates, fileSet);
}

function firstExisting(candidates, fileSet) {
  for (const c of candidates) {
    const norm = c.replace(/^\.\//, "");
    if (fileSet.has(norm)) return norm;
  }
  return null;
}

/**
 * @param {Map<string,string>} fileContents  repo-relative path -> source text
 * @returns {Map<string, Set<string>>} import graph
 */
export function buildGraph(fileContents) {
  const fileSet = new Set(fileContents.keys());
  const graph = new Map();
  for (const [file, content] of fileContents) {
    const ext = path.extname(file);
    const edges = new Set();
    for (const spec of extractImports(content, ext)) {
      const resolved = resolveImport(spec, file, fileSet, ext);
      if (resolved && resolved !== file) edges.add(resolved);
    }
    graph.set(file, edges);
  }
  return graph;
}
