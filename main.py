"""Single-word entrant: the word must stand alone, gate it and emit it."""
import json
import os
import sys
from pathlib import Path

BOUNDS = 24
WORD_FILE = "entry.txt"
BOUT = "u-0xkianno-one-word-first-thought-106abaf8"


def stage(src):
    bucket = os.environ.get("MAKEFUN_OUTPUT_DIR") or "out"
    bucket_path = Path(bucket)
    bucket_path.mkdir(parents=True, exist_ok=True)
    parked = bucket_path / WORD_FILE
    with open(parked, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(src + "\n")
    return parked


def audit(word):
    stripped = word.strip()
    if not stripped:
        return False, "no-word"
    if len(stripped) > BOUNDS:
        return False, "beyond-bounds"
    if len(stripped.split()) != 1:
        return False, "not-single-word"
    return True, "single-word"


def entrypoint():
    base = Path(__file__).resolve().parent
    raw = (base / WORD_FILE).read_text(encoding="utf-8").rstrip("\n")
    good, note = audit(raw)
    record = {"valid": good, "note": note, "word": raw, "size": len(raw), "bout": BOUT}
    if not good:
        print(json.dumps(record))
        sys.exit(3)
    stage(raw)
    record["parked"] = True
    print("CHECK", note, json.dumps(record))


if __name__ == "__main__":
    try:
        entrypoint()
    except FileNotFoundError as missing:
        print(json.dumps({"valid": False, "note": str(missing)}))
        sys.exit(4)
