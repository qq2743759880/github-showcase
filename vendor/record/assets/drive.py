#!/usr/bin/env python3
"""drive.py — run record.sh (or any command) inside a pty and feed it a
timed key script, so a terminal demo can be recorded unattended.

The recorder is interactive by design: it preloads the demo command into
the prompt buffer, waits for Enter, and ends on Ctrl-D. This driver plays
the operator. Same pattern as a pty smoke harness, plus a long tail wait
for the sed/awk/agg post-processing.

    assets/drive.py --record ./record.sh --dir ~/git/proj \
        --basename demo --cols 120 --rows 30 --font-size 16 \
        --script "6:ENTER 3.5:v 2.5:j 1.5:/ 0.6:scan 0.8:ENTER 3:q 1.5:CTRL_D"

Script grammar: whitespace-separated `delay:keys` pairs. `delay` is seconds
to drain output before sending; `keys` is literal text, or a named key in
caps. Multi-key literals are sent as one write ("scan" types four chars).

    ENTER \r   TAB \t   SPACE ' '   ESC \x1b   CTRL_D \x04   CTRL_C \x03
    UP/DOWN/LEFT/RIGHT: arrow escape sequences

`--smoke CMD...` skips the recorder entirely and drives CMD directly —
Phase 2's rehearsal: confirm exit 0 and no traceback before spending a take.

Stdlib only, POSIX only.
"""
from __future__ import annotations

import argparse
import fcntl
import os
import pty
import select
import struct
import sys
import termios
import time

NAMED = {
    "ENTER": b"\r", "TAB": b"\t", "SPACE": b" ", "ESC": b"\x1b",
    "CTRL_D": b"\x04", "CTRL_C": b"\x03",
    "UP": b"\x1b[A", "DOWN": b"\x1b[B", "RIGHT": b"\x1b[C", "LEFT": b"\x1b[D",
}


def parse_script(text):
    """[(delay, bytes)] from 'delay:keys' tokens; raises on a bad token."""
    steps = []
    for tok in text.split():
        delay, sep, keys = tok.partition(":")
        if not sep or not keys:
            raise ValueError(f"bad script token (want delay:keys): {tok!r}")
        steps.append((float(delay), NAMED.get(keys, keys.encode())))
    return steps


def drive(cmd, rows, cols, steps, tail_timeout):
    """Run cmd in a rows x cols pty, play steps, wait for exit.
    Returns (exit_code, captured_output)."""
    pid, fd = pty.fork()
    if pid == 0:
        os.environ["TERM"] = "xterm-256color"
        os.execvp(cmd[0], cmd)

    fcntl.ioctl(fd, termios.TIOCSWINSZ, struct.pack("HHHH", rows, cols, 0, 0))
    out = []

    def drain(duration):
        end = time.time() + duration
        while time.time() < end:
            r, _, _ = select.select([fd], [], [], 0.05)
            if r:
                try:
                    out.append(os.read(fd, 65536))
                except OSError:
                    return False
        return True

    for delay, keys in steps:
        if not drain(delay):
            break
        try:
            os.write(fd, keys)
        except OSError:
            break

    # agg renders after the shell exits; give the whole pipeline time.
    deadline = time.time() + tail_timeout
    status = None
    while time.time() < deadline:
        done, st = os.waitpid(pid, os.WNOHANG)
        if done:
            status = st
            break
        drain(0.25)

    text = b"".join(out).decode("utf-8", "replace")
    if status is None:
        os.kill(pid, 9)
        os.waitpid(pid, 0)
        return 124, text
    return os.waitstatus_to_exitcode(status), text


def main():
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--script", required=True,
                   help="timed keys: 'delay:keys ...' (see module docstring)")
    p.add_argument("--size", default="120x30", help="pty COLSxROWS (default 120x30)")
    p.add_argument("--tail-timeout", type=float, default=240,
                   help="seconds to wait for post-processing after the script (default 240)")

    mode = p.add_mutually_exclusive_group(required=True)
    mode.add_argument("--record", metavar="RECORD_SH",
                      help="path to record.sh; recorder flags are built from the options below")
    mode.add_argument("--smoke", action="store_true",
                      help="drive CMD directly (after --) without recording")

    p.add_argument("--dir", help="directory to record (required with --record)")
    p.add_argument("--basename", help="output basename (required with --record)")
    p.add_argument("--out-dir", help="recordings output dir (default: <dir-repo>/recordings)")
    p.add_argument("--title")
    p.add_argument("--prompt-label")
    p.add_argument("--cols", type=int)
    p.add_argument("--rows", type=int)
    p.add_argument("--font-size", type=int)
    p.add_argument("--idle-time-limit", default="1.5")
    p.add_argument("--last-frame-duration", default="3")
    p.add_argument("cmd", nargs="*",
                   help="demo command (after --): preloaded by record.sh, or run directly with --smoke")
    args = p.parse_args()

    cols, rows = (int(v) for v in args.size.split("x"))
    if args.cols:
        cols = args.cols
    if args.rows:
        rows = args.rows

    if args.smoke:
        if not args.cmd:
            p.error("--smoke needs a command after --")
        cmd = args.cmd
    else:
        if not (args.dir and args.basename):
            p.error("--record needs --dir and --basename")
        cmd = [args.record, args.dir, "--no-env-file",
               "--basename", args.basename,
               "--cols", str(cols), "--rows", str(rows),
               "--idle-time-limit", args.idle_time_limit,
               "--last-frame-duration", args.last_frame_duration]
        if args.out_dir:
            cmd += ["--out-dir", args.out_dir]
        if args.title:
            cmd += ["--title", args.title, "--demo-name", args.title]
        if args.prompt_label:
            cmd += ["--prompt-label", args.prompt_label]
        if args.font_size:
            cmd += ["--font-size", str(args.font_size)]
        cmd += args.cmd

    steps = parse_script(args.script)
    code, text = drive(cmd, rows, cols, steps, args.tail_timeout)

    ok = code == 0 and "Traceback" not in text
    print(f"drive {'ok' if ok else 'FAIL'} exit={code} steps={len(steps)} size={cols}x{rows}")
    if not ok:
        sys.stdout.write(text[-3000:])
        sys.exit(1)
    # On success surface the recorder's closing lines (output paths).
    tail = [ln for ln in text.splitlines() if ln.strip()][-3:]
    print("\n".join(tail))


if __name__ == "__main__":
    main()
