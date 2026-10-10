"""GPT Image 2.5 (Higgsfield "Marketing Studio Image 2.5 Flare") jobs: the flying crane repainted.

Mo, October 9, 2026: make the homepage's flying crane look more like a painting than a picture;
three samples, up to $0.50 (cap 7 jobs = $0.49 at the $0.07 billed before refunds). Ledger:
%LOCALAPPDATA%/HiggsfieldAPI/bigh-crane-paint. One job at a time; never retried automatically.

usage: python -X utf8 reference/home-v2/ink/hf_crane_paint.py <name> <prompt.txt>
          [--aspect 3:2] [--quality high] [--resolution 2k] [--ref img.png ...]
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
STATE = Path(os.environ.get("HF_RUN_STATE", Path.home() / "AppData/Local/HiggsfieldAPI/bigh-crane-paint"))
LOCK = STATE / "submit.lock"
LEDGER = STATE / "ledger-crane-paint.jsonl"
MAX_JOBS = 7  # crane painting samples, Mo 10/9: up to $0.50 (7 jobs = $0.49 at $0.07 billed, the worst case)


def jobs_so_far():
    return len(LEDGER.read_text(encoding="utf-8").splitlines()) if LEDGER.exists() else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("name")
    ap.add_argument("prompt_file")
    ap.add_argument("--aspect", default="3:2")
    ap.add_argument("--quality", default="high")
    ap.add_argument("--resolution", default="2k")
    ap.add_argument("--ref", action="append", default=[])
    ap.add_argument("--out", default=str(Path(__file__).parent / "originals"))
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
    job = STATE / f"crane-gpt25-{args.name}-{stamp}.json"

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
        # A free price check. This model quotes per token ("type": "description", no dollar figure);
        # NuriCell's 70 jobs at these settings billed $0.05-0.07 each, so the job cap is the limit.
        # If a dollar figure ever comes back, never more than 8 cents a picture.
        quote = hf_api.estimate(MODEL, data)
        if "usd" in quote and float(quote["usd"]) > 0.08:
            raise SystemExit(f"Quote {quote['usd']} is over 8 cents; not submitted.")
        record = {"model": MODEL, "input": data, "submitted_at": stamp, "approved_by": "Mo 10/9 crane painting samples, up to $0.50"}
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
    saved = hf_api.download(str(job), str(STATE / f"dl-crane-{args.name}-{stamp}"))["downloaded"]
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
