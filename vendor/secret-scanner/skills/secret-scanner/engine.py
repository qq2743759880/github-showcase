from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
from dataclasses import dataclass, asdict
from typing import Iterable, Iterator


SKIP_DIRS = {
    ".git", ".hg", ".svn", "node_modules", "venv", ".venv", "env",
    "__pycache__", "dist", "build", ".mypy_cache", ".pytest_cache",
    "vendor", ".idea", ".vscode", "site-packages",
}

BINARY_EXT = {
    ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".ico", ".pdf", ".zip",
    ".gz", ".tar", ".7z", ".rar", ".exe", ".dll", ".so", ".dylib",
    ".class", ".jar", ".woff", ".woff2", ".ttf", ".eot", ".mp3", ".mp4",
    ".mov", ".avi", ".mkv", ".flac", ".pyc", ".o", ".a", ".wasm",
    ".webp", ".heic", ".avif",
}

MAX_FILE_BYTES = 5 * 1024 * 1024
MAX_LINE_LEN = 4096

PLACEHOLDER_RE = re.compile(
    r"(?i)(example|sample|dummy|placeholder|your[_-]?key|xxx+|00000+|"
    r"123456|changeme|redacted|test[_-]?key|testvalue|donotuse|"
    r"mykey|yourtoken|notreal|fake|<[^>]+>|\$\{[^}]+\})"
)


@dataclass
class Rule:
    id: str
    description: str
    severity: str
    pattern: re.Pattern
    secret_group: int = 0
    keywords: tuple = ()


def _c(pattern: str) -> re.Pattern:
    return re.compile(pattern)


RULES: list[Rule] = [
    Rule("aws-access-key-id", "AWS Access Key ID", "high",
         _c(r"\b((?:AKIA|ASIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA)[A-Z0-9]{16})\b"), 1),
    Rule("aws-secret-access-key", "AWS Secret Access Key", "critical",
         _c(r"(?i)aws[_-]?secret[_-]?access[_-]?key\s*[:=]\s*['\"]?([A-Za-z0-9/+=]{40})['\"]?"), 1),
    Rule("github-pat", "GitHub Personal Access Token", "critical",
         _c(r"\b(ghp_[A-Za-z0-9]{36})\b"), 1),
    Rule("github-oauth", "GitHub OAuth / App token", "critical",
         _c(r"\b(gh[osu]_[A-Za-z0-9]{36})\b"), 1),
    Rule("github-fine-grained", "GitHub fine-grained PAT", "critical",
         _c(r"\b(github_pat_[A-Za-z0-9_]{82})\b"), 1),
    Rule("gitlab-pat", "GitLab Personal Access Token", "critical",
         _c(r"\b(glpat-[A-Za-z0-9_-]{20})\b"), 1),
    Rule("slack-token", "Slack token", "high",
         _c(r"\b(xox[baprs]-[A-Za-z0-9-]{10,48})\b"), 1),
    Rule("slack-webhook", "Slack webhook URL", "medium",
         _c(r"(https://hooks\.slack\.com/services/T[A-Za-z0-9_]+/B[A-Za-z0-9_]+/[A-Za-z0-9_]+)"), 1),
    Rule("google-api-key", "Google API key", "high",
         _c(r"\b(AIza[0-9A-Za-z_-]{35})\b"), 1),
    Rule("gcp-service-account", "GCP service account key", "critical",
         _c(r'"type"\s*:\s*"service_account"'), 0),
    Rule("stripe-secret", "Stripe secret key", "critical",
         _c(r"\b(sk_(?:live|test)_[A-Za-z0-9]{24,})\b"), 1),
    Rule("stripe-restricted", "Stripe restricted key", "high",
         _c(r"\b(rk_(?:live|test)_[A-Za-z0-9]{24,})\b"), 1),
    Rule("sendgrid-key", "SendGrid API key", "high",
         _c(r"\b(SG\.[A-Za-z0-9_-]{22}\.[A-Za-z0-9_-]{43})\b"), 1),
    Rule("twilio-key", "Twilio API key", "high",
         _c(r"\b(SK[0-9a-fA-F]{32})\b"), 1),
    Rule("openai-key", "OpenAI API key", "critical",
         _c(r"\b(sk-(?:proj-)?[A-Za-z0-9_-]{20,})\b"), 1,
         keywords=("openai", "sk-")),
    Rule("anthropic-key", "Anthropic API key", "critical",
         _c(r"\b(sk-ant-[A-Za-z0-9_-]{20,})\b"), 1),
    Rule("huggingface-token", "Hugging Face access token", "high",
         _c(r"\b(hf_[A-Za-z0-9]{34})\b"), 1),
    Rule("replicate-token", "Replicate API token", "high",
         _c(r"\b(r8_[A-Za-z0-9]{40})\b"), 1),
    Rule("groq-key", "Groq API key", "critical",
         _c(r"\b(gsk_[A-Za-z0-9]{52})\b"), 1),
    Rule("cohere-key", "Cohere API key", "high",
         _c(r"(?i)^(?=.*cohere).*\b([A-Za-z0-9]{40})\b"), 1,
         keywords=("cohere",)),
    Rule("digitalocean-pat", "DigitalOcean PAT", "high",
         _c(r"\b(dop_v1_[a-f0-9]{64})\b"), 1),
    Rule("npm-token", "npm access token", "high",
         _c(r"\b(npm_[A-Za-z0-9]{36})\b"), 1),
    Rule("pypi-token", "PyPI upload token", "critical",
         _c(r"\b(pypi-AgEIcHlwaS5vcmc[A-Za-z0-9_-]{50,})\b"), 1),
    Rule("mailgun-api-token", "Mailgun API token", "high",
         _c(r"(?i)^(?=.*mailgun).*\b(key-[A-Fa-f0-9]{32})\b"), 1,
         keywords=("mailgun",)),
    Rule("postmark-api-token", "Postmark server token", "high",
         _c(r"(?i)^(?=.*postmark).*\b(key-[A-Fa-f0-9]{32})\b"), 1,
         keywords=("postmark",)),
    Rule("jwt", "JSON Web Token", "low",
         _c(r"\b(eyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,})\b"), 1),
    Rule("private-key", "Private key block", "critical",
         _c(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP )?PRIVATE KEY-----"), 0),
    Rule("generic-password", "Hardcoded password assignment", "medium",
         _c(r"""(?i)(?:password|passwd|pwd)\s*[:=]\s*['"]([^'"\s]{6,})['"]"""), 1,
         keywords=("password", "passwd", "pwd")),
    Rule("generic-secret", "Generic secret/token assignment", "medium",
         _c(r"""(?i)(?:secret|token|api[_-]?key|apikey|auth)\s*[:=]\s*['"]([A-Za-z0-9_\-./+=]{16,})['"]"""), 1,
         keywords=("secret", "token", "key", "auth")),
    Rule("basic-auth-url", "Credentials in URL", "high",
         _c(r"\b([a-z][a-z0-9+.-]*://[^/\s:@]+:[^/\s:@]+@[^/\s]+)"), 1),
]

NO_ENTROPY_RULES = {
    "private-key", "gcp-service-account", "github-pat", "github-oauth",
    "github-fine-grained", "gitlab-pat", "stripe-secret", "stripe-restricted",
    "anthropic-key", "openai-key", "slack-token", "slack-webhook",
    "aws-access-key-id", "google-api-key", "sendgrid-key", "twilio-key",
    "npm-token", "pypi-token", "basic-auth-url", "jwt",
    "huggingface-token", "replicate-token", "groq-key", "digitalocean-pat",
    "mailgun-api-token", "postmark-api-token",
}


def shannon_entropy(data: str) -> float:
    if not data:
        return 0.0
    freq: dict[str, int] = {}
    for ch in data:
        freq[ch] = freq.get(ch, 0) + 1
    n = len(data)
    entropy = 0.0
    for count in freq.values():
        p = count / n
        entropy -= p * math.log2(p)
    return entropy


def looks_like_secret(value: str, min_entropy: float) -> bool:
    if len(value) < 12:
        return False
    if PLACEHOLDER_RE.search(value):
        return False
    if len(set(value)) <= 4:
        return False
    return shannon_entropy(value) >= min_entropy


@dataclass
class Finding:
    rule_id: str
    description: str
    severity: str
    path: str
    line: int
    column: int
    secret: str
    entropy: float

    def to_dict(self) -> dict:
        return asdict(self)


def _redact(secret: str) -> str:
    if len(secret) <= 8:
        return secret[0] + "*" * (len(secret) - 1)
    return f"{secret[:4]}...{secret[-4:]} (len={len(secret)})"


def iter_files(paths: Iterable[str], include_tests: bool) -> Iterator[str]:
    for root_path in paths:
        if os.path.isfile(root_path):
            yield root_path
            continue
        for dirpath, dirnames, filenames in os.walk(root_path):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            if not include_tests:
                dirnames[:] = [d for d in dirnames
                               if d not in ("test", "tests", "__tests__")]
            for name in filenames:
                ext = os.path.splitext(name)[1].lower()
                if ext in BINARY_EXT:
                    continue
                yield os.path.join(dirpath, name)


def scan_text(text: str, path: str, min_entropy: float,
              use_entropy: bool) -> list[Finding]:
    findings: list[Finding] = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        if len(line) > MAX_LINE_LEN:
            continue
        lower = line.lower()
        for rule in RULES:
            if rule.keywords and not any(k in lower for k in rule.keywords):
                continue
            for m in rule.pattern.finditer(line):
                value = m.group(rule.secret_group) if rule.secret_group else m.group(0)
                ent = shannon_entropy(value)
                if use_entropy and rule.id not in NO_ENTROPY_RULES:
                    if not looks_like_secret(value, min_entropy):
                        continue
                if PLACEHOLDER_RE.search(value) and rule.id not in NO_ENTROPY_RULES:
                    continue
                findings.append(Finding(
                    rule_id=rule.id,
                    description=rule.description,
                    severity=rule.severity,
                    path=path,
                    line=lineno,
                    column=m.start(rule.secret_group) + 1 if rule.secret_group else m.start() + 1,
                    secret=_redact(value),
                    entropy=round(ent, 2),
                ))
    return findings


def scan_file(path: str, min_entropy: float, use_entropy: bool) -> list[Finding]:
    try:
        if os.path.getsize(path) > MAX_FILE_BYTES:
            return []
        with open(path, "r", encoding="utf-8", errors="ignore") as fh:
            text = fh.read()
    except (OSError, ValueError):
        return []
    if "\x00" in text[:1024]:
        return []
    return scan_text(text, path, min_entropy, use_entropy)


def scan_paths(paths: Iterable[str], min_entropy: float = 3.5,
               use_entropy: bool = True,
               include_tests: bool = False) -> list[Finding]:
    results: list[Finding] = []
    for path in iter_files(paths, include_tests):
        results.extend(scan_file(path, min_entropy, use_entropy))
    sev_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    results.sort(key=lambda f: (sev_order.get(f.severity, 9), f.path, f.line))
    return results


_SEV_COLOR = {
    "critical": "\033[1;91m", "high": "\033[91m",
    "medium": "\033[93m", "low": "\033[90m",
}
_RESET = "\033[0m"


def _supports_color() -> bool:
    return sys.stdout.isatty() and os.environ.get("NO_COLOR") is None


def render_pretty(findings: list[Finding]) -> str:
    if not findings:
        return "[secret-scanner] No secrets detected. [OK]"
    color = _supports_color()
    lines = [f"[secret-scanner] {len(findings)} potential secret(s) found:\n"]
    for f in findings:
        tag = f.severity.upper()
        if color:
            tag = f"{_SEV_COLOR.get(f.severity, '')}{tag}{_RESET}"
        lines.append(f"  {tag:<10} {f.path}:{f.line}:{f.column}")
        lines.append(f"             {f.description} [{f.rule_id}]  "
                     f"value={f.secret}  entropy={f.entropy}")
    counts: dict[str, int] = {}
    for f in findings:
        counts[f.severity] = counts.get(f.severity, 0) + 1
    summary = ", ".join(f"{k}={v}" for k, v in sorted(counts.items()))
    lines.append(f"\nSummary: {summary}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="secret-scanner",
        description="Detect hardcoded secrets via regex rules + entropy analysis.")
    parser.add_argument("paths", nargs="+", help="files or directories to scan")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    parser.add_argument("--min-entropy", type=float, default=3.5,
                        help="entropy threshold for generic rules (default 3.5)")
    parser.add_argument("--no-entropy", action="store_true",
                        help="disable entropy gating (more findings, more FPs)")
    parser.add_argument("--include-tests", action="store_true",
                        help="also scan test directories")
    args = parser.parse_args(argv)

    for p in args.paths:
        if not os.path.exists(p):
            print(f"error: path not found: {p}", file=sys.stderr)
            return 2

    findings = scan_paths(
        args.paths,
        min_entropy=args.min_entropy,
        use_entropy=not args.no_entropy,
        include_tests=args.include_tests,
    )

    if args.json:
        print(json.dumps([f.to_dict() for f in findings], indent=2))
    else:
        print(render_pretty(findings))

    return 1 if findings else 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    raise SystemExit(main())
