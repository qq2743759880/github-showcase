/**
 * Stack / project-type detection from manifest files.
 * Pure function of a file-existence predicate so it is trivially testable.
 */

const MANIFESTS = [
  { file: "package.json", lang: "JavaScript/TypeScript", ecosystem: "node" },
  { file: "pyproject.toml", lang: "Python", ecosystem: "python" },
  { file: "requirements.txt", lang: "Python", ecosystem: "python" },
  { file: "setup.py", lang: "Python", ecosystem: "python" },
  { file: "go.mod", lang: "Go", ecosystem: "go" },
  { file: "Cargo.toml", lang: "Rust", ecosystem: "rust" },
  { file: "pom.xml", lang: "Java", ecosystem: "maven" },
  { file: "build.gradle", lang: "Java/Kotlin", ecosystem: "gradle" },
  { file: "Gemfile", lang: "Ruby", ecosystem: "ruby" },
  { file: "composer.json", lang: "PHP", ecosystem: "composer" },
];

/**
 * @param {(file: string) => boolean} exists
 * @returns {{manifests: Array, languages: string[], ecosystems: string[]}}
 */
export function detectStack(exists) {
  const manifests = MANIFESTS.filter((m) => exists(m.file));
  const languages = [...new Set(manifests.map((m) => m.lang))];
  const ecosystems = [...new Set(manifests.map((m) => m.ecosystem))];
  return { manifests, languages, ecosystems };
}

/** Source-file extensions we know how to parse imports from. */
export const PARSEABLE_EXT = new Set([
  ".js", ".jsx", ".mjs", ".cjs", ".ts", ".tsx", ".py", ".go",
]);

/** Directories that are never interesting for onboarding. */
export const IGNORE_DIRS = new Set([
  "node_modules", ".git", "dist", "build", "out", "vendor", "target",
  ".next", ".nuxt", "coverage", "__pycache__", ".venv", "venv", ".idea",
  ".vscode", "bin", "obj", ".cache",
]);
