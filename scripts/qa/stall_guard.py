"""A freeze alarm for the page checks.

The checks drive real browsers for many minutes, and a browser can stop answering without an
error: page.evaluate and some waits have no time limit of their own. On November 4, 2026 qa_nav
sat idle on the public demo for 55 minutes after 259 passes and no fails, and nobody could tell a
slow run from a stuck one.

Importing this module watches the check's own output. If no new line is printed for
QA_STALL_MINUTES (default 10), it prints one FAIL line naming the last line that was printed and
ends the run at once with exit code 3, so a freeze reads as a failure instead of a run that never
ends. It also makes the output line-buffered, so a log file shows each check as it finishes.

Import it after any sys.stdout.reconfigure(...) call:

    import stall_guard  # noqa: F401  (ends a frozen run; see stall_guard.py)
"""

import os
import sys
import threading
import time

LIMIT = float(os.environ.get("QA_STALL_MINUTES", "10")) * 60


class _Watched:
    """sys.stdout that notes when it was last written to."""

    def __init__(self, stream):
        self._stream = stream
        self.beat = time.monotonic()
        self.last = "(nothing printed yet)"

    def write(self, text):
        self.beat = time.monotonic()
        if text.strip():
            self.last = text.strip().splitlines()[-1]
        return self._stream.write(text)

    def __getattr__(self, name):
        return getattr(self._stream, name)


def _watch(out):
    while True:
        time.sleep(min(15, LIMIT / 4))
        quiet = time.monotonic() - out.beat
        if quiet > LIMIT:
            minutes = quiet / 60
            out._stream.write(
                f"FAIL frozen: nothing printed for {minutes:.1f} minutes, so the run was stopped."
                f" The last line was: {out.last[:200]}\n"
            )
            out._stream.flush()
            os._exit(3)


if not isinstance(sys.stdout, _Watched):
    sys.stdout.reconfigure(line_buffering=True)
    sys.stdout = _Watched(sys.stdout)
    threading.Thread(target=_watch, args=(sys.stdout,), daemon=True).start()
