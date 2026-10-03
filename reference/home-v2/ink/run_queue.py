"""Run the Ink look's GPT Image 2.5 plate jobs one after another (round 4, October 2, 2026).

Jobs are lines in queue.jsonl: {"name", "prompt", "aspect", "refs": [...]}. Each job runs through
reference/home-v2/r4/hf_unquoted.py (its lock, ledger and job cap) and lands in originals/.
Finished names go to queue-done.txt, so jobs can be appended while the runner works. The runner
exits after 20 idle minutes.

usage: python -X utf8 reference/home-v2/ink/run_queue.py
"""

import json
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
QUEUE = HERE / "queue.jsonl"
DONE = HERE / "queue-done.txt"
LOG = HERE / "queue.log"


def log(text):
    with LOG.open("a", encoding="utf-8", newline="\n") as f:
        f.write(time.strftime("%H:%M:%S ") + text + "\n")


def pending():
    done = set(DONE.read_text(encoding="utf-8").split()) if DONE.exists() else set()
    if not QUEUE.exists():
        return []
    jobs = [json.loads(line) for line in QUEUE.read_text(encoding="utf-8").splitlines() if line]
    return [j for j in jobs if j["name"] not in done]


def main():
    idle_since = time.time()
    while True:
        jobs = pending()
        if not jobs:
            if time.time() - idle_since > 1200:
                log("idle, exit")
                return
            time.sleep(15)
            continue
        job = jobs[0]
        cmd = [sys.executable, "-X", "utf8", str(REPO / "reference/home-v2/r4/hf_unquoted.py"),
               job["name"], str(HERE / "prompts" / job["prompt"]), "--aspect", job["aspect"],
               "--out", str(HERE / "originals")]
        for ref in job.get("refs", []):
            cmd += ["--ref", str(REPO / ref)]
        log("start " + job["name"])
        result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
        tail = (result.stdout + result.stderr).strip().splitlines()[-4:]
        log(f"end {job['name']} rc={result.returncode} :: " + " | ".join(tail))
        with DONE.open("a", encoding="utf-8", newline="\n") as f:
            f.write(job["name"] + "\n")
        if "Job cap reached" in " ".join(tail):
            log("cap reached, exit")
            return
        idle_since = time.time()


if __name__ == "__main__":
    main()
