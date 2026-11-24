#!/usr/bin/env python
"""Hash-freeze a run plan (config + all source/scripts) BEFORE any output of that run exists.

  python scripts/freeze_plan.py --config configs/pilot.yaml           # write FREEZE.json
  python scripts/freeze_plan.py --config configs/pilot.yaml --verify  # exit 1 if anything changed
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rusa.evaluation.tasks import load_config  # noqa: E402
from rusa.utils.seeding import environment_info, sha256_file  # noqa: E402


def manifest(config: str) -> dict:
    cfg = load_config(config)
    files = [Path(config)] + sorted((ROOT / "src").rglob("*.py")) + sorted((ROOT / "scripts").rglob("*.py")) \
        + sorted((ROOT / "scripts").rglob("*.sbatch"))
    files += [ROOT / p for p in cfg.get("freeze_files", [])]
    return {str(Path(f).resolve().relative_to(ROOT)): sha256_file(f) for f in files}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--verify", action="store_true")
    a = ap.parse_args()
    cfg = load_config(a.config)
    path = ROOT / cfg["out_dir"] / "FREEZE.json"
    cur = manifest(a.config)
    if a.verify:
        frozen = json.loads(path.read_text())["files"]
        bad = sorted(k for k in set(frozen) | set(cur) if frozen.get(k) != cur.get(k))
        if bad:
            print("FREEZE MISMATCH:", *bad, sep="\n  ")
            sys.exit(1)
        print(f"freeze verified ({len(cur)} files)")
        return
    pool = ROOT / cfg["out_dir"] / "pool"
    if pool.exists() and any(pool.iterdir()):
        sys.exit("refusing to freeze: pool outputs already exist")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"frozen_utc": datetime.now(timezone.utc).isoformat(), "config": a.config,
                                "files": cur, "env_at_freeze": environment_info()}, indent=1))
    print(f"wrote {path} ({len(cur)} files)")


if __name__ == "__main__":
    main()
