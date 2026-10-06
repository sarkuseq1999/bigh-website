"""GPT Image 2.5 (Higgsfield "Marketing Studio Image 2.5 Flare") jobs for the round-4 Ink build.

Mo approved GPT Image 2.5 on October 2, 2026 after a head-to-head with Gemini: it is the better
painter (ink wash, paper, materials) and costs about $0.05 per 2k high-quality image (billed $0.07,
$0.02 refunded on reconcile; checked on open.higgsfield.ai/billing). Higgsfield prices this model
only after the job, so the regular helper (hf_run.py) refuses it; this script is the approved
exception. Guard rails: one job at a time (hf_run.py's lock), a hard cap of MAX_JOBS jobs in this
round, and every job logged to ledger-r4-gpt.jsonl (assumed $0.05, verify on the billing page).

usage: python -X utf8 reference/home-v2/r4/hf_unquoted.py <name> <prompt.txt>
          [--aspect 16:9] [--quality high] [--resolution 2k] [--ref img.png ...] [--out <dir>]
  --ref   reference picture(s) to edit from or match (uploaded, passed as image_urls; up to 16)
  --out   where the result lands (default reference/home-v2/r4/originals); file = gpt25-<name>.png
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path.home() / ".codex/skills/higgsfield-api/scripts"))
import hf_api  # noqa: E402

MODEL = "marketing-studio/image/flare"
REPO = Path(__file__).resolve().parents[3]
STATE = Path(os.environ.get("HF_RUN_STATE", Path.home() / "AppData/Local/HiggsfieldAPI/bigh-home"))
LOCK = STATE / "submit.lock"
# Round 5 (October 3): Mo gave $15 for the crane homepage's second polish round; this round's
# GPT Image 2.5 jobs are counted on their own (round 4's 19 jobs stay in ledger-r4-gpt.jsonl).
LEDGER = STATE / "ledger-nav-rounds-gpt.jsonl"
# Menu bar, ten improvement rounds (October 5): Mo gave another $5; GPT Image 2.5 jobs capped at 40
# (about $2, $2.80 if no refund). The options round used 1 job in ledger-nav-gpt.jsonl.
MAX_JOBS = 40


def jobs_so_far():
    return len(LEDGER.read_text(encoding="utf-8").splitlines()) if LEDGER.exists() else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("name")
    ap.add_argument("prompt_file")
    ap.add_argument("--aspect", default="16:9")
    ap.add_argument("--quality", default="high")
    ap.add_argument("--resolution", default="2k")
    ap.add_argument("--ref", action="append", default=[])
    ap.add_argument("--out", default=str(REPO / "reference/home-v2/r4/originals"))
    # Legacy positional form: <name> <prompt> [aspect] [quality]
    args, extra = ap.parse_known_args()
    if extra:
        args.aspect = extra[0]
        if len(extra) > 1:
            args.quality = extra[1]

    if jobs_so_far() >= MAX_JOBS:
        raise SystemExit(f"Job cap reached ({MAX_JOBS}); ask the lead before spending more.")
    prompt = Path(args.prompt_file).read_text(encoding="utf-8").strip()
    data = {"prompt": prompt, "aspect_ratio": args.aspect, "resolution": args.resolution,
            "quality": args.quality}
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    STATE.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    job = STATE / f"r4-gpt25-{args.name}-{stamp}.json"

    for _ in range(360):
        try:
            handle = os.open(LOCK, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            break
        except FileExistsError:
            time.sleep(5)
    else:
        raise SystemExit("Another Higgsfield job has held the lock for 30 minutes.")
    try:
        if args.ref:
            data["image_urls"] = [hf_api.upload(r)["public_url"] for r in args.ref]
        record = {"model": MODEL, "input": data, "submitted_at": stamp, "approved_by": "Mo 10/5 menu bar rounds $5"}
        job.write_text(json.dumps(record, indent=2), encoding="utf-8")
        response = hf_api.api("POST", MODEL, data)
        record.update(response)
        job.write_text(json.dumps(record, indent=2), encoding="utf-8")
        with LEDGER.open("a", encoding="utf-8") as ledger:
            ledger.write(json.dumps({"name": args.name, "request_id": response.get("request_id"),
                                     "usd_assumed": "0.05", "at": stamp,
                                     "refs": len(args.ref)}) + "\n")
        print("submitted", response.get("request_id"), flush=True)
    finally:
        os.close(handle)
        LOCK.unlink(missing_ok=True)

    deadline = time.time() + 1500
    while time.time() < deadline:
        time.sleep(10)
        record.update(hf_api.api("GET", f"requests/{record['request_id']}/status"))
        job.write_text(json.dumps(record, indent=2), encoding="utf-8")
        if record.get("status") in hf_api.TERMINAL:
            break
    print("status", record.get("status"))
    if record.get("status") != "completed":
        raise SystemExit(f"not completed; receipt {job}")
    saved = hf_api.download(str(job), str(STATE / f"dl-r4-{args.name}-{stamp}"))["downloaded"]
    src = Path(saved[0]["path"])
    target = out_dir / f"gpt25-{args.name}{src.suffix}"
    if target.exists():
        target = out_dir / f"gpt25-{args.name}-{stamp}{src.suffix}"
    src.replace(target)
    (target.with_suffix(".json")).write_text(
        json.dumps({"model": MODEL, "prompt": prompt,
                    "settings": {k: v for k, v in data.items() if k not in ("prompt", "image_urls")},
                    "refs": [str(r) for r in args.ref], "made": stamp}, indent=2) + "\n",
        encoding="utf-8", newline="\n")
    print("saved", target)
    print("jobs this round:", jobs_so_far(), "of", MAX_JOBS)


if __name__ == "__main__":
    main()
