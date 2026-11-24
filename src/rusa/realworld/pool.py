"""Replicate-cluster pools on a fixed real graph.

One replicate cluster r of dataset D consists of:
* a fresh class-stratified split (key: master, D, r, 'split');
* one training seed shared by every variant in the cluster (key: master, D, r, 'model');
* fresh, independent null draws for every lattice element and for ER
  (key: master, D, r, 'null', element, draw). These are label-free and arch-independent, so GCN
  and SAGE see the **same** null graphs (paired across architectures).

Variants fitted per architecture: real (G0), empty (matched no-graph), er (1 draw), and every
lattice element (``draws`` draws; draw 1 provides exact A/A contrasts for calibration). The
feature-only MLP is fitted once per cluster. Each null sample is audited (hard constraints
exactly; swap completion and edge overlap against pre-declared thresholds) before fitting.
Failed samples are logged with valid = False and not fitted.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
import pandas as pd
from ..craf.core import element_of
from ..nulls.admissibility import AdmissibilityPolicy, audit_sample
from ..nulls.generators import NullSpec, erdos_renyi_gnm, stratum_codes, swap_null
from ..utils.seeding import environment_info, int_seed_for, rng_for
from .data import make_split
from .models import fit_score, to_sparse_input


def lattice_names(attrs, max_order: int = 2) -> list[str]:
    from itertools import combinations

    out = ["degree"]
    for k in range(1, max_order + 1):
        out += ["strat:" + "+".join(sorted(c)) for c in combinations(sorted(attrs), k)]
    return out


def sample_null(name: str, g, node_attrs: dict, rng, swap_factor: float = 5.0, attempt_factor: float = 200.0):
    """Label-free null sample: inputs are G0, label-free node attributes and an rng only."""
    if name == "er":
        return erdos_renyi_gnm(g, rng)
    S = element_of(name)
    if S is None:
        raise ValueError(name)
    strata = stratum_codes(node_attrs, tuple(sorted(S)), g.n) if S else None
    return swap_null(g, rng, strata=strata, swap_factor=swap_factor, attempt_factor=attempt_factor)


def audit_null(name: str, g0, gp, node_attrs, info, key, policy=AdmissibilityPolicy()):
    spec = NullSpec("er") if name == "er" else NullSpec.parse(name)
    # Report every declared label-free attribute.  This is diagnostic only; the hard
    # constraint checks are determined by ``name`` and remain unchanged.
    return audit_sample(g0, gp, spec, node_attrs, info, key, policy,
                        report_attrs=tuple(sorted(node_attrs)))


def run_chunk_3b(ds, node_attrs: dict, start: int, count: int, out_dir: str | Path, *, archs, elements, draws: int,
                 master_seed: int, swap_factor: float, attempt_factor: float, split_kw: dict | None = None,
                 hp: dict | None = None) -> list[Path]:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    tag = f"{start:06d}_{start + count:06d}"
    paths = {a: out_dir / f"{ds.name}__{a}__{tag}.csv.gz" for a in list(archs) + ["mlp"]}
    meta_path = out_dir / f"{ds.name}__{tag}.meta.json"
    if meta_path.exists() and all(p.exists() for p in paths.values()):
        return list(paths.values())  # checkpoint
    # exact sparse first layer for sparse bag-of-words inputs; dense inputs (Phase 3E) stay dense
    x_t = to_sparse_input(ds.X) if float((ds.X != 0).mean()) < 0.5 else None
    rows = {a: [] for a in paths}
    t_all = time.time()
    for r in range(start, start + count):
        split = make_split(ds.y, rng_for(master_seed, ds.name, r, "split"), **(split_kw or {}))
        mseed = int_seed_for(master_seed, ds.name, r, "model")
        base = {"scenario": ds.name, "instance": r, "m": ds.graph.m}
        nulls = []
        for name in ["er"] + list(elements):
            for d in range(1 if name == "er" else draws):
                key = (master_seed, ds.name, r, "null", name, d)
                t0 = time.perf_counter()
                gp, info = sample_null(name, ds.graph, node_attrs, rng_for(*key), swap_factor, attempt_factor)
                gen_s = time.perf_counter() - t0
                au = audit_null(name, ds.graph, gp, node_attrs, info, key)
                extra = {"valid": au.valid, "violated_hard": ";".join(au.violated_hard),
                         "violated_soft": ";".join(au.violated_soft), "gen_seconds": gen_s,
                         **{f"diag_{k}": v for k, v in au.diagnostics.items()
                            if k in ("edge_overlap", "swap_completion", "swap_acceptance_rate")
                            or k.startswith("mixing_l1_")}}
                nulls.append((name, d, gp, extra))

        def fit(arch, variant, draw, g, extra):
            t0 = time.perf_counter()
            res = fit_score(arch, ds.X, ds.y, g, split, mseed, hp, x_t)
            rows[arch].append({**base, "variant": variant, "draw": draw, **res,
                               "fit_seconds": time.perf_counter() - t0, **extra})

        fit("mlp", "mlp", 0, None, {"valid": True})
        for arch in archs:
            fit(arch, "real", 0, ds.graph, {"valid": True})
            fit(arch, "empty", 0, None, {"valid": True})
            for name, d, gp, extra in nulls:
                if extra["valid"]:
                    fit(arch, name, d, gp, extra)
                else:
                    rows[arch].append({**base, "variant": name, "draw": d, "val_score": np.nan,
                                       "test_score": np.nan, **extra})
    for a, p in paths.items():
        tmp = p.with_name(p.name + ".tmp")
        pd.DataFrame(rows[a]).to_csv(tmp, index=False, compression="gzip")
        tmp.rename(p)
    meta_path.write_text(json.dumps({"dataset": ds.name, "start": start, "count": count, "archs": list(archs),
                                     "elements": list(elements), "draws": draws, "master_seed": master_seed,
                                     "seconds": time.time() - t_all, "env": environment_info()}, indent=1, default=str))
    return list(paths.values())
