import numpy as np
import pytest
from scipy import stats

from rusa.inference.certificates import bonferroni_bounds, iut_certificate, nested_radius
from rusa.inference.tests import (boot_lower, eb_lower, lower_bound, rank_test, signflip_test, t_lower,
                                  wsr_lower)


def test_t_lower_matches_scipy():
    d = np.random.default_rng(0).normal(0.3, 1, 25)
    r = t_lower(d, 0.05, 0.0)
    p = stats.ttest_1samp(d, 0.0, alternative="greater").pvalue
    assert r["p"] == pytest.approx(p, rel=1e-10)
    assert (r["L"] > 0) == (r["p"] <= 0.05)


def test_t_degenerate_cases():
    assert t_lower([0.1], 0.05)["p"] == 1.0
    r = t_lower([0.2, 0.2, 0.2], 0.05, 0.0)
    assert r["p"] == 0.0 and r["L"] == pytest.approx(0.2)
    with pytest.raises(ValueError):
        t_lower([0.1, np.nan])


@pytest.mark.parametrize("method", ["t", "boot", "eb", "wsr"])
def test_p_and_bound_agree(method):
    rng = np.random.default_rng(1)
    for eps in (0.0, 0.05):
        for _ in range(5):
            d = np.clip(rng.normal(0.08, 0.1, 30), -1, 1)
            r = lower_bound(d, method, 0.05, eps)
            assert (r["L"] > eps) == (r["p"] <= 0.05 + 1e-6), (method, r)


def test_bounded_methods_reject_out_of_range():
    with pytest.raises(ValueError):
        eb_lower([0.5, 1.5])
    with pytest.raises(ValueError):
        wsr_lower([-1.2, 0.1])


@pytest.mark.parametrize("method", ["eb", "wsr"])
def test_bounded_methods_cover_skewed_bounded_data(method):
    # skewed bounded variable where t-intervals can undercover; finite-sample methods must not
    rng = np.random.default_rng(2)
    mu = 0.9 * 0.05 + (-0.1) * 0.95  # Bernoulli mixture mean
    miss = 0
    reps = 300
    for _ in range(reps):
        d = np.where(rng.random(20) < 0.05, 0.9, -0.1)
        miss += lower_bound(d, method, 0.1)["L"] > mu
    assert miss / reps <= 0.1 + 3 * np.sqrt(0.1 * 0.9 / reps)


def test_signflip_exact_small_n():
    d = np.array([0.1, 0.2, -0.05, 0.3])
    r = signflip_test(d, 0.05, 0.0)
    signs = np.array([[1 if (k >> i) & 1 else -1 for i in range(4)] for k in range(16)])
    null = (signs * np.abs(d)).mean(1)
    assert r["p"] == pytest.approx(np.mean(null >= d.mean() - 1e-15))


def test_rank_test_formula_and_ties():
    assert rank_test(1.0, [0.1, 0.2, 0.3])["p"] == pytest.approx(0.25)
    assert rank_test(0.2, [0.1, 0.2, 0.3])["p"] == pytest.approx(0.75)  # tie counts against
    assert rank_test(0.1, [0.2, 0.3], larger_is_better=False)["p"] == pytest.approx(1 / 3)


def test_iut_is_max_p_and_min_L():
    rng = np.random.default_rng(3)
    D = {"a": rng.normal(0.5, 1, 30), "b": rng.normal(0.1, 1, 30), "c": rng.normal(1.0, 1, 30)}
    cert = iut_certificate(D, "t", 0.05, 0.0)
    marg = {k: t_lower(v) for k, v in D.items()}
    assert cert.p_iut == pytest.approx(max(m["p"] for m in marg.values()))
    assert cert.L_robust == pytest.approx(min(m["L"] for m in marg.values()))
    assert cert.argmin_L == "b"
    assert cert.certified == (cert.L_robust > 0)


def test_iut_type_one_error_at_boundary():
    # one comparator exactly at the boundary, the others far above: rejection ~ alpha, never more
    rng = np.random.default_rng(4)
    rej = 0
    reps = 2000
    for _ in range(reps):
        D = {"zero": rng.normal(0, 1, 15), "big": rng.normal(3, 1, 15)}
        rej += iut_certificate(D, "t", 0.05).certified
    rate = rej / reps
    assert abs(rate - 0.05) < 3 * np.sqrt(0.05 * 0.95 / reps)


def test_bonferroni_is_more_conservative():
    rng = np.random.default_rng(5)
    D = {k: rng.normal(0.4, 1, 40) for k in "abc"}
    b = bonferroni_bounds(D, "t", 0.05)
    for k in D:
        assert b[k]["L"] < t_lower(D[k], 0.05)["L"]


def test_nested_radius_and_validation():
    rng = np.random.default_rng(6)
    D = {"e": rng.normal(1, 0.1, 30), "q1": rng.normal(0.8, 0.1, 30), "q2": rng.normal(-0.2, 0.1, 30)}
    out = nested_radius(D, [["e"], ["e", "q1"], ["e", "q1", "q2"]], "t", 0.05, 0.0)
    assert out["rho_hat"] == 2
    curve = out["curve"]
    assert all(c["L_simultaneous_min"] <= c["L_marginal_min"] for c in curve)
    with pytest.raises(ValueError):
        nested_radius(D, [["e", "q1"], ["e"]])


def test_nested_radius_not_overstated_mc():
    # Prop. 3: P(rho_hat > rho*) <= alpha with marginal bounds; here rho* = 1
    rng = np.random.default_rng(7)
    over, reps = 0, 1500
    for _ in range(reps):
        D = {"e": rng.normal(1, 1, 12), "q1": rng.normal(0.0, 1, 12), "q2": rng.normal(-0.5, 1, 12)}
        over += nested_radius(D, [["e"], ["e", "q1"], ["e", "q1", "q2"]])["rho_hat"] > 1
    assert over / reps <= 0.05 + 3 * np.sqrt(0.05 * 0.95 / reps)


def test_bootstrap_reproducible():
    d = np.random.default_rng(8).normal(size=20)
    assert boot_lower(d, seed=3) == boot_lower(d, seed=3)
