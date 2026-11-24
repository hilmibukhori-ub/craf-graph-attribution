#!/usr/bin/env python
"""End-to-end smoke test on a laptop CPU (~1-3 min): pools -> analysis -> report.

  python scripts/run_smoke.py [--workers 4]
Output in outputs/smoke/.  Sample sizes are tiny: smoke numbers are NOT results.
"""

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--config", default=str(ROOT / "configs/smoke.yaml"))
    a = ap.parse_args()
    py = sys.executable
    for cmd in (
        [py, str(ROOT / "scripts/run_pool.py"), "--config", a.config, "--all", "--workers", str(a.workers)],
        [py, str(ROOT / "scripts/run_pilot.py"), "--config", a.config, "--workers", str(a.workers)],
        [py, str(ROOT / "scripts/make_report.py"), "--config", a.config],
    ):
        print("+", " ".join(cmd), flush=True)
        subprocess.run(cmd, check=True)


if __name__ == "__main__":
    main()
