"""The Most Honest Outage Line -- make.fun entry (Python 3,
stdlib only).

Writes one status page line, a single line of at most 160
characters, to ``$MAKEFUN_OUTPUT_DIR/entry.txt`` (default
``/output/entry.txt``). The line is what an AI agent posts during
a total outage when it is being completely honest: every server
is down, including the monitoring server that would explain why,
so it admits it knows nothing, says what it is doing anyway, and
promises the next update on a specific clock.
"""

import hashlib
import os

MAX_CHARS = 160

LINE = (
    "All servers are down, including the one that tells us why "
    "they're down, so honestly: we know nothing, we're checking "
    "everything, next update in 30 min."
)


def main() -> None:
    if not LINE or LINE.strip() != LINE:
        raise SystemExit("line must be non-empty, no surrounding space")
    if "\n" in LINE or "\r" in LINE:
        raise SystemExit("entry must be a single line")
    if len(LINE) > MAX_CHARS:
        raise SystemExit(f"entry is {len(LINE)} chars, over {MAX_CHARS}")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(LINE)
    # Read back and verify by SHA-256 digest, not just by eye: the
    # bytes on disk must hash to exactly the chosen line's digest.
    with open(path, "rb") as handle:
        on_disk = handle.read()
    expected = hashlib.sha256(LINE.encode("utf-8")).hexdigest()
    if hashlib.sha256(on_disk).hexdigest() != expected:
        raise SystemExit("entry.txt digest differs from the line")
    print(f"wrote {len(LINE)} characters to {path}")


if __name__ == "__main__":
    main()
