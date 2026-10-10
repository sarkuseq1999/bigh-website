"""Make one Higgsfield picture or video for the homepage redesign, safely, and log what it cost.

Wraps Mo's bigh-website helper (~/.codex/skills/higgsfield-api/scripts/hf_api.py): it checks the
live price first, refuses anything over the per-job cap or the round budget, submits once, waits,
downloads, and appends the cost to reference/home-v2/<look>/spend.md. Receipts (which hold media
URLs) stay outside the repo, in the session scratchpad. Only one submission runs at a time.

  python -X utf8 reference/home-v2/hf_run.py image --look sunrise --name hero-v1 \
      --model higgsfield-ai/soul/v2/standard --prompt "..." [--aspect 16:9] [--resolution 2k]
  python -X utf8 reference/home-v2/hf_run.py video --look sunrise --name hero-loop-v1 \
      --image path/to/still.png --prompt "..." [--duration 5] \
      [--model kling-video/v3.0/std/image-to-video]
  python -X utf8 reference/home-v2/hf_run.py estimate ...same flags...   (free; prints the price)
  python -X utf8 reference/home-v2/hf_run.py ledger                        (spent so far)

Picture models with fixed prices (Sept 29): higgsfield-ai/soul/v2/standard ($0.004, photo-real
people; prompt + aspect_ratio only), z-image/turbo ($0.015), ideogram/v4.0 ($0.06),
alibaba/qwen-image-3/text-to-image ($0.04, $0.075 at resolution 2k), recraft/v4.1/text-to-image
($0.035; pro $0.21), xai/grok-imagine-image-2.0 ($0.06–0.08; takes --ref pictures to edit from),
alibaba/qwen-image-3/edit ($0.04; needs --ref). Video: kling-video/v3.0/std/image-to-video
(~$0.23 for 5 s, $0.46 for 10 s), kling-video/v3.0/pro/image-to-video ($0.31 for 5 s); both take
--last-image (same picture = seamless loop). GPT Image 2.5, Seedance and Wan are priced only after
the job, so the helper refuses them.
"""

import argparse
import json
import os
import shutil
import sys
import time
from datetime import datetime
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path.home() / ".codex/skills/higgsfield-api/scripts"))
import hf_api  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
STATE = Path(os.environ.get("HF_RUN_STATE", Path.home() / "AppData/Local/HiggsfieldAPI/bigh-home"))
# Round 5 (October 3): Mo gave $15 for the crane homepage's second polish round. Earlier rounds
# stay in ledger.jsonl / ledger-r3.jsonl; this round counts only ledger-r5.jsonl. Quoted jobs
# (Kling) may use up to $11; GPT Image 2.5 (hf_unquoted.py, ledger-r5-gpt.jsonl) is capped at 40
# jobs (about $2 to $2.80), so the two together stay under $15.
# Round 6 (October 4, evening): Mo gave $10 for ten more rounds on the English homepage. Quoted
# jobs (Kling) may use up to $7.20 here; GPT Image 2.5 (hf_unquoted.py, ledger-r6-gpt.jsonl) is
# capped at 40 jobs (about $2 to $2.80), so the two together stay under $10.
# Round 7 (October 9): Mo picked the painted crane (A) and approved up to three Kling takes to
# remake its wingbeat (option 1: at most $1.68, quoted $0.56 a take). Only ledger-r7.jsonl counts.
LEDGER = STATE / "ledger-r7.jsonl"
LOCK = STATE / "submit.lock"
ROUND_BUDGET = Decimal("1.68")
LOOK_BUDGET = {
    "iris": Decimal("0"),
    "everyday": Decimal("0"),
    "botanical": Decimal("0"),
    "ink": Decimal("1.68"),  # round 7 (Oct 9): the painted crane's wingbeat, three takes at most
}
JOB_CAP = {"image": Decimal("0.25"), "video": Decimal("0.60")}
LOOKS = set(LOOK_BUDGET)


def spent(look=None):
    total = Decimal("0")
    if LEDGER.exists():
        for line in LEDGER.read_text(encoding="utf-8").splitlines():
            row = json.loads(line)
            if look is None or row["look"] == look:
                total += Decimal(row["usd"])
    return total


def build_input(args, upload=True):
    extra = json.loads(args.extra) if args.extra else {}
    if args.kind == "image":
        data = {"prompt": args.prompt}
        if args.aspect:
            data["aspect_ratio"] = args.aspect
        if args.resolution:
            data["resolution"] = args.resolution
        # Reference pictures for edit models (qwen-image-3/edit, grok-imagine-image-2.0):
        # uploaded and passed as image_urls.
        if args.ref:
            data["image_urls"] = [
                hf_api.upload(r)["public_url"] if upload else "https://example.com/ref.png"
                for r in args.ref
            ]
        return {**data, **extra}
    image = hf_api.upload(args.image)["public_url"] if upload else "https://example.com/a.png"
    data = {
        "prompt": args.prompt,
        "image_url": image,
        "duration": args.duration,
        "sound": "off",
    }
    if "kling" in (args.model or "kling"):
        data.update({"multi_shots": False, "cfg_scale": 0.5})
    if args.last_image:
        data["last_image_url"] = hf_api.upload(args.last_image)["public_url"] if upload else image
    return {**data, **extra}


def lock():
    STATE.mkdir(parents=True, exist_ok=True)
    for _ in range(360):
        try:
            return os.open(LOCK, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError:
            time.sleep(5)
    raise SystemExit("Another Higgsfield job has held the lock for 30 minutes; check on it first.")


def run(args):
    if args.look not in LOOKS:
        raise SystemExit(f"--look must be one of {sorted(LOOKS)}")
    model = args.model or ("kling-video/v3.0/std/image-to-video" if args.kind == "video" else None)
    if not model:
        raise SystemExit("--model is required for images")
    if args.aspect == "":
        args.aspect = None
    if args.kind == "video" and not args.image:
        raise SystemExit("--image is required for video")

    if args.command == "estimate":
        print(json.dumps(hf_api.estimate(model, build_input(args, upload=False)), indent=2))
        return

    out_dir = REPO / "reference/home-v2" / args.look / "originals"
    out_dir.mkdir(parents=True, exist_ok=True)
    handle = lock()
    try:
        data = build_input(args)
        quote = Decimal(str(hf_api.estimate(model, data)["usd"]))
        cap = min(JOB_CAP[args.kind], Decimal(args.max_usd) if args.max_usd else JOB_CAP[args.kind])
        if quote > cap:
            raise SystemExit(f"Price ${quote} is over the per-job cap ${cap}; not submitted.")
        if spent() + quote > ROUND_BUDGET:
            raise SystemExit(f"Round budget reached (${spent()} of ${ROUND_BUDGET}); not submitted.")
        if spent(args.look) + quote > LOOK_BUDGET[args.look]:
            raise SystemExit(
                f"{args.look} budget reached (${spent(args.look)} of ${LOOK_BUDGET[args.look]})."
            )
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        job = STATE / f"{args.look}-{args.name}-{stamp}.json"
        result = hf_api.submit(model, data, str(cap), str(job))
        with LEDGER.open("a", encoding="utf-8") as ledger:
            ledger.write(json.dumps({"look": args.look, "name": args.name, "model": model,
                                     "usd": str(quote), "at": stamp,
                                     "request_id": result["request_id"]}) + "\n")
        spend = REPO / "reference/home-v2" / args.look / "spend.md"
        with spend.open("a", encoding="utf-8", newline="\n") as log:
            log.write(f"- {stamp} Higgsfield {model} `{args.name}` ${quote}\n")
    finally:
        os.close(handle)
        LOCK.unlink(missing_ok=True)

    wait(job, 900 if args.kind == "video" else 600, 8 if args.kind == "image" else 15)
    fetch(job, args, out_dir, model, quote, stamp)


def wait(job, seconds, every):
    # The receipt's status_url points at platform.higgsfield.ai, where the helper (rightly) won't
    # send the key; the same status lives at api.higgsfield.ai/requests/<id>/status.
    record = hf_api.read_json(job)
    deadline = time.time() + seconds
    while time.time() < deadline:
        time.sleep(every)
        record.update(hf_api.api("GET", f"requests/{record['request_id']}/status"))
        hf_api.write_json(job, record)
        if record.get("status") in hf_api.TERMINAL:
            break
    if record.get("status") != "completed":
        raise SystemExit(
            f"Job is {record.get('status')!r}; receipt {job}. Resume with: hf_run.py resume "
            f"--receipt {job} (never resubmit blindly)."
        )


def fetch(job, args, out_dir, model, quote, stamp):
    tmp = STATE / f"dl-{args.look}-{args.name}-{stamp}"
    saved = hf_api.download(str(job), str(tmp))["downloaded"]
    outputs = []
    for number, item in enumerate(saved, 1):
        source = Path(item["path"])
        suffix = "" if len(saved) == 1 else f"-{number}"
        target = out_dir / f"{args.name}{suffix}{source.suffix}"
        if target.exists():
            target = out_dir / f"{args.name}{suffix}-{stamp}{source.suffix}"
        shutil.move(str(source), target)
        outputs.append(str(target))
    sidecar = out_dir / f"{args.name}.json"
    sidecar.write_text(json.dumps({"model": model, "prompt": args.prompt, "usd": str(quote),
                                   "made": stamp, "files": [Path(o).name for o in outputs],
                                   **({"from_image": str(args.image)} if args.image else {})},
                                  indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"usd": str(quote), "files": outputs, "round_spent": str(spent())}, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", choices=["image", "video", "estimate", "ledger", "resume"])
    parser.add_argument("--receipt", help="resume: a receipt JSON from an earlier run")
    parser.add_argument("--kind", choices=["image", "video"])
    parser.add_argument("--look")
    parser.add_argument("--name")
    parser.add_argument("--model")
    parser.add_argument("--prompt")
    parser.add_argument("--aspect", default="16:9", help="'' to omit")
    parser.add_argument("--resolution")
    parser.add_argument("--image")
    parser.add_argument("--duration", type=int, default=5)
    parser.add_argument("--ref", action="append", help="image models: a reference picture (repeat)")
    parser.add_argument("--last-image", help="video models that take an end frame (seamless loops)")
    parser.add_argument("--extra", help="JSON object merged into the model input")
    parser.add_argument("--max-usd")
    args = parser.parse_args()
    if args.command == "ledger":
        rows = LEDGER.read_text(encoding="utf-8").splitlines() if LEDGER.exists() else []
        for look in sorted(LOOKS):
            print(f"{look}: ${spent(look)}")
        print(f"total: ${spent()} of ${ROUND_BUDGET} ({len(rows)} jobs)")
        return
    if args.command == "resume":
        # Finish a job that timed out or was interrupted: wait for it, then download (no new spend).
        job = Path(args.receipt)
        record = hf_api.read_json(job)
        look, rest = job.stem.split("-", 1)
        args.look, args.name, stamp = look, rest.rsplit("-", 2)[0], "-".join(rest.rsplit("-", 2)[1:])
        args.kind = "video" if "video" in record["model"] else "image"
        args.prompt, args.image = record["input"].get("prompt", ""), None
        out_dir = REPO / "reference/home-v2" / look / "originals"
        out_dir.mkdir(parents=True, exist_ok=True)
        if record.get("status") != "completed":
            wait(job, 900, 10)
        fetch(job, args, out_dir, record["model"], Decimal(record["estimate"]["usd"]), stamp)
        return
    args.kind = args.kind or ("video" if args.command == "video" else "image")
    if not (args.look and args.name and args.prompt):
        raise SystemExit("--look, --name and --prompt are required")
    run(args)


if __name__ == "__main__":
    main()
