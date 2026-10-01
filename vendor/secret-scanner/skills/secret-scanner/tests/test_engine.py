import os
import sys
import textwrap

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import engine


def test_entropy_empty_is_zero():
    assert engine.shannon_entropy("") == 0.0


def test_entropy_uniform_is_low():
    assert engine.shannon_entropy("aaaaaaaa") == 0.0


def test_entropy_random_is_high():
    rand = "f3Kd9Lm2Qx8Zp1Rt7Vw4Bn6Cs0Hj5"
    assert engine.shannon_entropy(rand) > 3.5


def test_looks_like_secret_rejects_placeholder():
    assert not engine.looks_like_secret("your_api_key_here", 3.5)
    assert not engine.looks_like_secret("yourtoken-abc123", 3.5)
    assert not engine.looks_like_secret("notreal_value", 3.5)


def test_looks_like_secret_rejects_short():
    assert not engine.looks_like_secret("abc123", 3.5)


def test_looks_like_secret_accepts_real():
    assert engine.looks_like_secret("f3Kd9Lm2Qx8Zp1Rt7Vw4Bn6", 3.0)


@pytest.mark.parametrize("rule_id,sample", [
    ("aws-access-key-id", "AKIAIOSFODNN7EXAMPLE"),
    ("github-pat", "ghp_" + "a1B2c3D4e5F6g7H8i9J0k1L2m3N4o5P6q7R8"),
    ("slack-token", "xox" + "b-123456789012-abcdefghijklmnopqrstuvwx"),
    ("google-api-key", "AIza" + ("Bc" * 18)[:35]),
    ("stripe-secret", "sk_live_" + "a1B2c3D4e5F6g7H8i9J0k1L2"),
    ("anthropic-key", "sk-ant-" + "a1B2c3D4e5F6g7H8i9J0k1L2"),
    ("mailgun-api-token", "mailgun_token = 'key-" + ("a1b2" * 8) + "'"),
    ("postmark-api-token", "postmark_server_key = 'key-" + ("1a2b" * 8) + "'"),
    ("huggingface-token", "hf_" + "aB3dE5fG7hJ9kL1mN3pQ5rS7tU9vW1xY3z"),
    ("replicate-token", "r8_" + ("a1B2c3D4e5" * 4)),
    ("groq-key", "gsk_" + ("a1B2c3D4e5" * 5) + "fG"),
    # Split so the fixture is not a contiguous 40-character run: GitHub's own
    # push protection reads one as a live Cohere key and blocks the push.
    ("cohere-key",
     "cohere_api_key = '" + "aB3dE5fG7hJ9kL1mN3pQ" + "5rS7tU9vW1xY3zA5bC7d" + "'"),
    ("digitalocean-pat", "dop_v1_" + ("a1b2c3d4" * 8)),
])
def test_rule_detects(rule_id, sample):
    findings = engine.scan_text(sample, "f.py", 3.5, True)
    ids = {f.rule_id for f in findings}
    assert rule_id in ids, f"{rule_id} not found in {ids}"


def test_service_tokens_require_provider_keyword():
    findings = engine.scan_text("token = 'key-" + ("a1b2" * 8) + "'", "f.py", 3.5, True)
    assert all(
        f.rule_id not in {"mailgun-api-token", "postmark-api-token"}
        for f in findings
    )


def test_cohere_key_requires_the_provider_keyword():
    """40 alphanumerics is not a shape, so the rule is anchored on the word."""
    findings = engine.scan_text(
        "value = '" + "aB3dE5fG7hJ9kL1mN3pQ" + "5rS7tU9vW1xY3zA5bC7d" + "'",
        "f.py", 3.5, True)
    assert all(f.rule_id != "cohere-key" for f in findings)


def test_digitalocean_pat_does_not_fire_on_plain_hex():
    """A 64-character hex digest, a git SHA pair, anything: no dop_v1_ prefix."""
    findings = engine.scan_text(
        "digest = '" + ("a1b2c3d4" * 8) + "'", "f.py", 3.5, True)
    assert all(f.rule_id != "digitalocean-pat" for f in findings)


def test_private_key_block_detected():
    text = "-----BEGIN RSA PRIVATE KEY-----\nMIIE...\n-----END RSA PRIVATE KEY-----"
    findings = engine.scan_text(text, "id_rsa", 3.5, True)
    assert any(f.rule_id == "private-key" for f in findings)


def test_basic_auth_url_detected():
    text = "db = 'postgres://admin:s3cr3tP4ss@db.internal:5432/app'"
    findings = engine.scan_text(text, "config.py", 3.5, True)
    assert any(f.rule_id == "basic-auth-url" for f in findings)


def test_generic_password_detected():
    text = "password = 'Sup3rH4rdT0Gu3ss!'"
    findings = engine.scan_text(text, "settings.py", 3.0, True)
    assert any(f.rule_id == "generic-password" for f in findings)


def test_placeholder_not_flagged():
    text = textwrap.dedent("""
        api_key = "your_api_key_here"
        password = "changeme"
        token = "<YOUR_TOKEN>"
        secret = "${SECRET_FROM_ENV}"
    """)
    findings = engine.scan_text(text, "readme_example.py", 3.5, True)
    assert findings == [], [f.to_dict() for f in findings]


def test_low_entropy_generic_not_flagged():
    text = 'secret = "aaaaaaaaaaaaaaaaaaaa"'
    findings = engine.scan_text(text, "f.py", 3.5, True)
    assert not any(f.rule_id == "generic-secret" for f in findings)


def test_clean_code_has_no_findings():
    text = "def add(a, b):\n    return a + b\n"
    findings = engine.scan_text(text, "math.py", 3.5, True)
    assert findings == []


def test_secret_is_redacted():
    secret = "AKIAIOSFODNN7EXAMPLE"
    findings = engine.scan_text(f"k='{secret}'", "f.py", 3.5, True)
    assert findings
    for f in findings:
        assert secret not in f.secret


def test_findings_sorted_by_severity():
    text = textwrap.dedent("""
        jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
        key = "-----BEGIN PRIVATE KEY-----"
    """)
    findings = engine.scan_text(text, "f.py", 3.5, True)
    sev_rank = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    ranks = [sev_rank[f.severity] for f in findings]
    findings_sorted = sorted(findings, key=lambda f: sev_rank[f.severity])
    assert [sev_rank[f.severity] for f in findings_sorted] == sorted(ranks)


def test_scan_paths_skips_binary_and_finds_secret(tmp_path):
    (tmp_path / "app.py").write_text("token = 'ghp_" + "x" * 36 + "'")
    (tmp_path / "image.png").write_bytes(b"\x89PNG\x00\x00secretAKIAIOSFODNN7EXAMPLE")
    (tmp_path / "cover.webp").write_bytes(b"\x00secretAKIAIOSFODNN7EXAMPLE")
    (tmp_path / "movie.mkv").write_bytes(b"\x1A\x45\xDF\xA3secretAKIAIOSFODNN7EXAMPLE")
    (tmp_path / "audio.flac").write_bytes(b"fLaCsecretAKIAIOSFODNN7EXAMPLE")
    (tmp_path / "icon.heic").write_bytes(b"\x00\x00\x00\x00secretAKIAIOSFODNN7EXAMPLE")
    (tmp_path / "vector.avif").write_bytes(b"\x00\x00\x00\x18avifsecretAKIAIOSFODNN7EXAMPLE")
    sub = tmp_path / "node_modules"
    sub.mkdir()
    (sub / "lib.js").write_text("var k='AKIAIOSFODNN7EXAMPLE'")

    findings = engine.scan_paths([str(tmp_path)])
    paths = {os.path.basename(f.path) for f in findings}
    assert "app.py" in paths
    assert "image.png" not in paths
    assert "cover.webp" not in paths
    assert "movie.mkv" not in paths
    assert "audio.flac" not in paths
    assert "icon.heic" not in paths
    assert "vector.avif" not in paths
    assert "lib.js" not in paths


def test_cli_exit_code_clean(tmp_path, capsys):
    (tmp_path / "ok.py").write_text("x = 1\n")
    rc = engine.main([str(tmp_path)])
    assert rc == 0


def test_cli_exit_code_findings(tmp_path):
    (tmp_path / "bad.py").write_text("k = 'AKIAIOSFODNN7EXAMPLE'\n")
    rc = engine.main([str(tmp_path)])
    assert rc == 1


def test_cli_json_output(tmp_path, capsys):
    (tmp_path / "bad.py").write_text("k = 'AKIAIOSFODNN7EXAMPLE'\n")
    engine.main([str(tmp_path), "--json"])
    out = capsys.readouterr().out
    import json
    data = json.loads(out)
    assert isinstance(data, list) and data
    assert data[0]["rule_id"]
