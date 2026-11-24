"""Hierarchical, collision-free seeding and provenance helpers.

All randomness in RUSA flows from ``numpy.random.SeedSequence`` keyed by a tuple of
non-negative integers, e.g. ``(master, scenario_id, instance, purpose, candidate, draw)``.
Two different key tuples give statistically independent streams; the same tuple always
gives the same stream.  String components are mapped to integers by a stable hash.
"""

from __future__ import annotations

import hashlib
import json
import platform
import random
import sys
from pathlib import Path
from typing import Any, Iterable

import numpy as np

PURPOSE = {
    "dgp": 1,
    "split": 2,
    "null": 3,
    "model": 4,
    "search": 5,
    "aa": 6,
    "bootstrap": 7,
    "experiment": 8,
}


def stable_int(token: Any) -> int:
    """Map an int or str to a stable non-negative int (independent of PYTHONHASHSEED)."""
    if isinstance(token, (int, np.integer)):
        if token < 0:
            raise ValueError("seed components must be non-negative")
        return int(token)
    digest = hashlib.sha256(str(token).encode()).hexdigest()
    return int(digest[:12], 16)


def seed_key(*parts: Any) -> tuple[int, ...]:
    return tuple(stable_int(p) for p in parts)


def rng_for(*parts: Any) -> np.random.Generator:
    """Independent generator for a key tuple."""
    return np.random.default_rng(np.random.SeedSequence(list(seed_key(*parts))))


def int_seed_for(*parts: Any) -> int:
    """A 31-bit integer seed (for torch) derived from the key tuple."""
    ss = np.random.SeedSequence(list(seed_key(*parts)))
    return int(ss.generate_state(1, dtype=np.uint32)[0] & 0x7FFFFFFF)


def set_global_determinism(seed: int) -> None:
    """Seed python/numpy/torch global RNGs and request deterministic torch kernels."""
    random.seed(seed)
    np.random.seed(seed % (2**32))
    try:
        import torch

        torch.manual_seed(seed)
        torch.use_deterministic_algorithms(True, warn_only=True)
        torch.set_num_threads(1)
    except ImportError:  # pragma: no cover
        pass


def sha256_file(path: str | Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_obj(obj: Any) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, default=str).encode()).hexdigest()


def environment_info() -> dict:
    info = {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "numpy": np.__version__,
    }
    for mod in ("scipy", "pandas", "torch", "torch_geometric", "networkx", "yaml"):
        try:
            info[mod] = __import__(mod).__version__
        except Exception:  # pragma: no cover
            info[mod] = "unavailable"
    return info


def hash_tree(paths: Iterable[str | Path]) -> dict[str, str]:
    out = {}
    for p in paths:
        p = Path(p)
        files = sorted(p.rglob("*.py")) if p.is_dir() else [p]
        for f in files:
            out[str(f)] = sha256_file(f)
    return out
