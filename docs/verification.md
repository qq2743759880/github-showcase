# Verification — 2026-10-01

Status: **SELF_CONTAINED_ORCHESTRATION_VERIFIED**, for the local Hello CLI fixture.
This is a bounded acceptance run, not a promise that every optional phase or host backend works everywhere.

## Published baseline

Preview main: `4ddaef50143d3298ffe53918794eaae7ba2cdc4b`; 14 files read back exactly.
Self-contained branch: `codex/self-contained-release`. Fresh Agent tested runtime commit
`546eeb13e4011404efc8f64ea2561863c0f97abd` from GitHub. It had only the clone, its fixture and the main SKILL entry;
no mother repository, author research or previous conversation was available.

## Results

| Check | Result |
|---|---|
| Runtime closure | 20 vendored entities, pinned external packages, explicit host/optional capabilities |
| License closure | Selected license files, per-file CC-BY-SA override, notices and local changes preserved; unlicensed F03 fallback removed |
| Vendor integrity | Exact file/hash lock PASS |
| Primary dispatch | Actual F01, F02, F03 + compose, F06 + compose, F08, F09 and F10 local calls PASS |
| Fallback dispatch | F04 GUI primary lacked CLI coverage; real pretty-mermaid SVG/PNG renderer PASS |
| Visual validation | C4 context/container, workflow and Snap-X card rendered and viewed; labels corrected |
| STOP gate | Dummy secret, private literal, unknown license, missing authorization each blocked actual packaging; no probe archive |
| Fixture preservation | Original five files unchanged |
| Generated project | Fresh clone runtime install, startup, sample/error paths and 4 behavior tests PASS |
| Project ZIP | 18 files exactly match committed export bytes |
| Product tests | 16 PASS |
| Fixed external dependencies | npm audit: 0 vulnerabilities at verification time |

Generated export commit: `61354457470739b3afe5aee582ba981b54ed951c`.
ZIP SHA256: `af4f0bf5137970f2ef62512f969a8e264f023aa07840dd93409b6986e8c15f29`.

F05 and F07 were skipped because the fixture has no metrics or footage. Optional ffmpeg/record availability
does not become a fabricated demo. The fixture package is **PACKAGE_PASS / READY_FOR_APPROVAL**;
no remote publication was authorized or attempted for that generated project.

## Host limits

The maintenance host's GitHub Connector authenticated reads worked, but actual write probes returned
403 `Resource not accessible by integration`; owner push permission does not prove integration access.
gh was absent. Product remote publication correctly remains blocked on this host. Preview and development
branch publication used separately authorized saved Git authentication and non-force pushes, then remote readback.
This does not claim the Connector write backend passed.

Rendering needs Node >=24, pinned npm dependencies and Chrome/Edge or the project-local Puppeteer browser.
Font/network and sandbox process restrictions may require normal host permission handling.
Full private trace is excluded from the public repository; this page records reproducible scope and outcomes.
The release branch remains available for owner review before stable promotion.
