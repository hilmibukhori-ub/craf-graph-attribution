# phase2c_sage report (generated from outputs/phase2c_sage/analysis; model sage)

## Monte Carlo truths (1 - Brier units; S7 binding arm exact 0 by A/A)

| scenario | k_config | K | theta_full | argmin | delta_binding | second | delta_second | gap | delta_empty | delta_strat_block | n_within_0.002 | n_within_0.005 | sd_unit_binding | max_mc_se |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S7_hard | K18 | 18 | 0.0000 | strat:w1+w2 | 0.0000 | strat:block+w3 | 0.0143 | 0.0143 | 0.0339 | 0.0393 | 1 | 1 | 0.0093 | 0.0002 |
| S8_large_hard | K18 | 18 | 0.0118 | strat:w1+w2 | 0.0118 | strat:w1+w3 | 0.0232 | 0.0114 | 0.0386 | 0.0439 | 1 | 1 | 0.0149 | 0.0002 |
| S8_small_hard | K18 | 18 | 0.0085 | strat:w1+w2 | 0.0085 | strat:w2+w3 | 0.0207 | 0.0121 | 0.0370 | 0.0424 | 1 | 1 | 0.0133 | 0.0002 |

## eps = 0.005

### Power: claim rate in positive scenarios (S8; theta_full > eps)

| scenario | k_config | b | pcga_l | exhaustive_iut | fullset_adaptive | fullset_adaptive_fb | fullset_adaptive_s | screen_uniform | screen_random | screen_sh | oracle_select |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S8_large_hard | K18 | 6 | 1.000 | 0.183 | 0.000 | 0.183 | 0.167 | 0.683 | 0.683 | 0.633 | 0.900 |
| S8_large_hard | K18 | 9 | 1.000 | 0.300 | 0.450 | 0.450 | 0.517 | 0.833 | 0.833 | 0.817 | 0.983 |
| S8_large_hard | K18 | 12 | 1.000 | 0.367 | 0.600 | 0.600 | 0.667 | 0.900 | 0.950 | 0.900 | 1.000 |
| S8_large_hard | K18 | 24 | 1.000 | 0.717 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| S8_small_hard | K18 | 6 | 1.000 | 0.083 | 0.000 | 0.083 | 0.000 | 0.400 | 0.400 | 0.333 | 0.467 |
| S8_small_hard | K18 | 9 | 1.000 | 0.083 | 0.150 | 0.150 | 0.183 | 0.417 | 0.583 | 0.350 | 0.567 |
| S8_small_hard | K18 | 12 | 1.000 | 0.083 | 0.350 | 0.350 | 0.333 | 0.500 | 0.567 | 0.467 | 0.733 |
| S8_small_hard | K18 | 24 | 1.000 | 0.283 | 0.700 | 0.700 | 0.700 | 0.733 | 0.833 | 0.733 | 0.783 |

### Full-set false-claim rate in negative controls (S7; theta_full <= 0). A guarantee (<= alpha) exists only for scope=full procedures

| scenario | k_config | b | pcga_l | exhaustive_iut | fullset_adaptive | fullset_adaptive_fb | fullset_adaptive_s | screen_uniform | screen_random | screen_sh | oracle_select |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S7_hard | K18 | 6 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.100 | 0.100 | 0.067 | 0.000 |
| S7_hard | K18 | 9 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.050 | 0.100 | 0.017 | 0.000 |
| S7_hard | K18 | 12 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.050 | 0.100 | 0.000 | 0.000 |
| S7_hard | K18 | 24 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.100 | 0.017 | 0.000 |

### S7: Wilson 95% upper limit of the full-set claim rate (full-set procedures)

| scenario | k_config | b | exhaustive_iut | fullset_adaptive | fullset_adaptive_fb | fullset_adaptive_s |
|---|---|---|---|---|---|---|
| S7_hard | K18 | 6 | 0.060 | 0.060 | 0.060 | 0.060 |
| S7_hard | K18 | 9 | 0.060 | 0.060 | 0.060 | 0.060 |
| S7_hard | K18 | 12 | 0.060 | 0.060 | 0.060 | 0.060 |
| S7_hard | K18 | 24 | 0.060 | 0.060 | 0.060 | 0.060 |

### False claims against each procedure's OWN estimand (selected: theta_sel; PCGA-L: Delta_strat:block)

| scenario | k_config | b | pcga_l | exhaustive_iut | fullset_adaptive | fullset_adaptive_fb | fullset_adaptive_s | screen_uniform | screen_random | screen_sh | oracle_select |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S7_hard | K18 | 6 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| S7_hard | K18 | 9 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| S7_hard | K18 | 12 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| S7_hard | K18 | 24 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| S8_large_hard | K18 | 6 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| S8_large_hard | K18 | 9 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| S8_large_hard | K18 | 12 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| S8_large_hard | K18 | 24 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| S8_small_hard | K18 | 6 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| S8_small_hard | K18 | 9 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| S8_small_hard | K18 | 12 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| S8_small_hard | K18 | 24 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |

### Binding-null discovery (strat:w1+w2 in the selected set; full-set: top-allocated arm)

| scenario | k_config | b | exhaustive_iut | fullset_adaptive | fullset_adaptive_fb | fullset_adaptive_s | screen_uniform | screen_random | screen_sh | oracle_select |
|---|---|---|---|---|---|---|---|---|---|---|
| S7_hard | K18 | 6 | 0.833 |  | 0.833 | 0.300 | 0.900 | 0.900 | 0.933 | 1.000 |
| S7_hard | K18 | 9 | 0.983 | 0.317 | 0.317 | 0.300 | 0.950 | 0.900 | 0.983 | 1.000 |
| S7_hard | K18 | 12 | 1.000 | 0.317 | 0.317 | 0.350 | 0.950 | 0.900 | 1.000 | 1.000 |
| S7_hard | K18 | 24 | 1.000 | 0.400 | 0.400 | 0.417 | 1.000 | 0.900 | 0.983 | 1.000 |
| S8_large_hard | K18 | 6 | 0.833 |  | 0.833 | 0.433 | 0.883 | 0.883 | 0.900 | 1.000 |
| S8_large_hard | K18 | 9 | 0.967 | 0.500 | 0.500 | 0.483 | 0.917 | 0.883 | 0.933 | 1.000 |
| S8_large_hard | K18 | 12 | 0.983 | 0.650 | 0.650 | 0.633 | 0.933 | 0.883 | 0.983 | 1.000 |
| S8_large_hard | K18 | 24 | 1.000 | 0.672 | 0.672 | 0.672 | 1.000 | 0.883 | 1.000 | 1.000 |
| S8_small_hard | K18 | 6 | 0.800 |  | 0.800 | 0.317 | 0.883 | 0.883 | 0.967 | 1.000 |
| S8_small_hard | K18 | 9 | 0.950 | 0.567 | 0.567 | 0.517 | 0.917 | 0.883 | 0.983 | 1.000 |
| S8_small_hard | K18 | 12 | 0.967 | 0.700 | 0.700 | 0.600 | 0.967 | 0.883 | 1.000 | 1.000 |
| S8_small_hard | K18 | 24 | 1.000 | 0.729 | 0.729 | 0.729 | 1.000 | 0.883 | 1.000 | 1.000 |

### Coverage of each procedure's own estimand by its lower bound

| scenario | k_config | b | exhaustive_iut | fullset_adaptive | fullset_adaptive_fb | fullset_adaptive_s | screen_uniform | screen_random | screen_sh | oracle_select |
|---|---|---|---|---|---|---|---|---|---|---|
| S7_hard | K18 | 6 | 0.950 |  | 0.950 | 0.967 | 0.950 | 0.950 | 0.950 | 0.983 |
| S7_hard | K18 | 9 | 0.933 | 0.950 | 0.950 | 0.967 | 0.967 | 0.950 | 0.967 | 0.967 |
| S7_hard | K18 | 12 | 0.933 | 0.967 | 0.967 | 0.967 | 0.983 | 1.000 | 0.983 | 0.983 |
| S7_hard | K18 | 24 | 0.967 | 0.933 | 0.933 | 0.933 | 0.983 | 0.967 | 0.983 | 0.967 |
| S8_large_hard | K18 | 6 | 0.983 |  | 0.983 | 1.000 | 0.933 | 0.933 | 0.933 | 0.967 |
| S8_large_hard | K18 | 9 | 0.933 | 1.000 | 1.000 | 1.000 | 0.933 | 0.950 | 0.933 | 0.950 |
| S8_large_hard | K18 | 12 | 0.950 | 1.000 | 1.000 | 1.000 | 0.967 | 0.967 | 0.967 | 0.967 |
| S8_large_hard | K18 | 24 | 0.950 | 1.000 | 1.000 | 1.000 | 0.967 | 0.950 | 0.967 | 0.950 |
| S8_small_hard | K18 | 6 | 0.967 |  | 0.967 | 1.000 | 0.950 | 0.950 | 0.950 | 0.950 |
| S8_small_hard | K18 | 9 | 1.000 | 1.000 | 1.000 | 1.000 | 0.950 | 0.967 | 0.950 | 0.967 |
| S8_small_hard | K18 | 12 | 1.000 | 1.000 | 1.000 | 1.000 | 0.950 | 0.933 | 0.950 | 0.983 |
| S8_small_hard | K18 | 24 | 0.967 | 0.983 | 0.983 | 0.983 | 0.983 | 0.950 | 0.983 | 0.933 |

### Coverage of theta_full (meaningful as a guarantee for full-set procedures only)

| scenario | k_config | b | exhaustive_iut | fullset_adaptive | fullset_adaptive_fb | fullset_adaptive_s | screen_uniform | screen_random | screen_sh | oracle_select |
|---|---|---|---|---|---|---|---|---|---|---|
| S7_hard | K18 | 6 | 0.950 |  | 0.950 | 0.967 | 0.850 | 0.850 | 0.883 | 0.983 |
| S7_hard | K18 | 9 | 0.933 | 0.950 | 0.950 | 0.967 | 0.917 | 0.850 | 0.950 | 0.967 |
| S7_hard | K18 | 12 | 0.933 | 0.967 | 0.967 | 0.967 | 0.933 | 0.900 | 0.983 | 0.983 |
| S7_hard | K18 | 24 | 0.967 | 0.933 | 0.933 | 0.933 | 0.983 | 0.867 | 0.967 | 0.967 |
| S8_large_hard | K18 | 6 | 0.983 |  | 0.983 | 1.000 | 0.833 | 0.833 | 0.867 | 0.967 |
| S8_large_hard | K18 | 9 | 0.933 | 1.000 | 1.000 | 1.000 | 0.867 | 0.833 | 0.883 | 0.950 |
| S8_large_hard | K18 | 12 | 0.950 | 1.000 | 1.000 | 1.000 | 0.900 | 0.850 | 0.950 | 0.967 |
| S8_large_hard | K18 | 24 | 0.950 | 1.000 | 1.000 | 1.000 | 0.967 | 0.833 | 0.967 | 0.950 |
| S8_small_hard | K18 | 6 | 0.967 |  | 0.967 | 1.000 | 0.833 | 0.833 | 0.917 | 0.950 |
| S8_small_hard | K18 | 9 | 1.000 | 1.000 | 1.000 | 1.000 | 0.867 | 0.850 | 0.933 | 0.967 |
| S8_small_hard | K18 | 12 | 1.000 | 1.000 | 1.000 | 1.000 | 0.917 | 0.817 | 0.950 | 0.983 |
| S8_small_hard | K18 | 24 | 0.967 | 0.983 | 0.983 | 0.983 | 0.983 | 0.833 | 0.983 | 0.933 |

### Estimation bias against the procedure's own estimand

| scenario | k_config | b | pcga_l | exhaustive_iut | fullset_adaptive | fullset_adaptive_fb | fullset_adaptive_s | screen_uniform | screen_random | screen_sh | oracle_select |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S7_hard | K18 | 6 | 0.0004 | -0.0011 |  | -0.0011 | -0.0008 | -0.0002 | -0.0002 | -0.0002 | -0.0002 |
| S7_hard | K18 | 9 | 0.0004 | -0.0007 | -0.0007 | -0.0007 | -0.0003 | -0.0003 | -0.0004 | -0.0003 | -0.0001 |
| S7_hard | K18 | 12 | 0.0003 | -0.0003 | -0.0001 | -0.0001 | -0.0000 | -0.0002 | -0.0002 | -0.0002 | -0.0001 |
| S7_hard | K18 | 24 | -0.0001 | -0.0002 | -0.0002 | -0.0002 | -0.0002 | -0.0001 | -0.0002 | -0.0001 | -0.0001 |
| S8_large_hard | K18 | 6 | 0.0004 | -0.0006 |  | -0.0006 | -0.0006 | 0.0001 | 0.0001 | -0.0000 | -0.0000 |
| S8_large_hard | K18 | 9 | 0.0001 | -0.0002 | -0.0005 | -0.0005 | -0.0004 | -0.0003 | -0.0002 | -0.0003 | 0.0000 |
| S8_large_hard | K18 | 12 | -0.0000 | 0.0000 | -0.0003 | -0.0003 | -0.0002 | -0.0002 | -0.0002 | -0.0000 | 0.0000 |
| S8_large_hard | K18 | 24 | 0.0001 | 0.0001 | 0.0005 | 0.0005 | 0.0005 | 0.0000 | 0.0001 | 0.0000 | 0.0002 |
| S8_small_hard | K18 | 6 | 0.0001 | -0.0013 |  | -0.0013 | -0.0020 | -0.0004 | -0.0004 | -0.0003 | -0.0002 |
| S8_small_hard | K18 | 9 | 0.0003 | -0.0018 | -0.0009 | -0.0009 | -0.0004 | -0.0004 | -0.0003 | -0.0003 | -0.0001 |
| S8_small_hard | K18 | 12 | 0.0001 | -0.0011 | -0.0006 | -0.0006 | -0.0006 | -0.0002 | -0.0001 | -0.0002 | 0.0001 |
| S8_small_hard | K18 | 24 | 0.0002 | -0.0001 | 0.0000 | 0.0000 | 0.0000 | 0.0001 | 0.0001 | 0.0001 | 0.0001 |

### Estimation RMSE against the procedure's own estimand

| scenario | k_config | b | pcga_l | exhaustive_iut | fullset_adaptive | fullset_adaptive_fb | fullset_adaptive_s | screen_uniform | screen_random | screen_sh | oracle_select |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S7_hard | K18 | 6 | 0.0043 | 0.0045 |  | 0.0045 | 0.0041 | 0.0026 | 0.0026 | 0.0026 | 0.0016 |
| S7_hard | K18 | 9 | 0.0031 | 0.0037 | 0.0027 | 0.0027 | 0.0025 | 0.0020 | 0.0019 | 0.0020 | 0.0012 |
| S7_hard | K18 | 12 | 0.0028 | 0.0034 | 0.0019 | 0.0019 | 0.0019 | 0.0016 | 0.0014 | 0.0016 | 0.0011 |
| S7_hard | K18 | 24 | 0.0019 | 0.0022 | 0.0012 | 0.0012 | 0.0012 | 0.0011 | 0.0011 | 0.0011 | 0.0011 |
| S8_large_hard | K18 | 6 | 0.0039 | 0.0068 |  | 0.0068 | 0.0046 | 0.0038 | 0.0038 | 0.0037 | 0.0023 |
| S8_large_hard | K18 | 9 | 0.0032 | 0.0050 | 0.0046 | 0.0046 | 0.0045 | 0.0029 | 0.0026 | 0.0028 | 0.0020 |
| S8_large_hard | K18 | 12 | 0.0029 | 0.0047 | 0.0030 | 0.0030 | 0.0030 | 0.0024 | 0.0022 | 0.0023 | 0.0016 |
| S8_large_hard | K18 | 24 | 0.0019 | 0.0032 | 0.0027 | 0.0027 | 0.0027 | 0.0016 | 0.0016 | 0.0016 | 0.0015 |
| S8_small_hard | K18 | 6 | 0.0037 | 0.0060 |  | 0.0060 | 0.0058 | 0.0032 | 0.0032 | 0.0032 | 0.0023 |
| S8_small_hard | K18 | 9 | 0.0029 | 0.0050 | 0.0042 | 0.0042 | 0.0037 | 0.0025 | 0.0023 | 0.0025 | 0.0017 |
| S8_small_hard | K18 | 12 | 0.0028 | 0.0042 | 0.0027 | 0.0027 | 0.0026 | 0.0023 | 0.0021 | 0.0023 | 0.0015 |
| S8_small_hard | K18 | 24 | 0.0021 | 0.0028 | 0.0015 | 0.0015 | 0.0015 | 0.0015 | 0.0014 | 0.0015 | 0.0015 |

### Estimation RMSE against theta_full

| scenario | k_config | b | pcga_l | exhaustive_iut | fullset_adaptive | fullset_adaptive_fb | fullset_adaptive_s | screen_uniform | screen_random | screen_sh | oracle_select |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S7_hard | K18 | 6 | 0.0399 | 0.0045 |  | 0.0045 | 0.0041 | 0.0049 | 0.0050 | 0.0045 | 0.0016 |
| S7_hard | K18 | 9 | 0.0398 | 0.0037 | 0.0027 | 0.0027 | 0.0025 | 0.0036 | 0.0044 | 0.0025 | 0.0012 |
| S7_hard | K18 | 12 | 0.0397 | 0.0034 | 0.0019 | 0.0019 | 0.0019 | 0.0036 | 0.0045 | 0.0016 | 0.0011 |
| S7_hard | K18 | 24 | 0.0393 | 0.0022 | 0.0012 | 0.0012 | 0.0012 | 0.0011 | 0.0046 | 0.0022 | 0.0011 |
| S8_large_hard | K18 | 6 | 0.0327 | 0.0068 |  | 0.0068 | 0.0046 | 0.0051 | 0.0051 | 0.0048 | 0.0023 |
| S8_large_hard | K18 | 9 | 0.0324 | 0.0050 | 0.0046 | 0.0046 | 0.0045 | 0.0037 | 0.0042 | 0.0037 | 0.0020 |
| S8_large_hard | K18 | 12 | 0.0322 | 0.0047 | 0.0030 | 0.0030 | 0.0030 | 0.0034 | 0.0040 | 0.0029 | 0.0016 |
| S8_large_hard | K18 | 24 | 0.0322 | 0.0032 | 0.0027 | 0.0027 | 0.0027 | 0.0016 | 0.0039 | 0.0016 | 0.0015 |
| S8_small_hard | K18 | 6 | 0.0342 | 0.0060 |  | 0.0060 | 0.0058 | 0.0048 | 0.0048 | 0.0036 | 0.0023 |
| S8_small_hard | K18 | 9 | 0.0343 | 0.0050 | 0.0042 | 0.0042 | 0.0037 | 0.0037 | 0.0043 | 0.0027 | 0.0017 |
| S8_small_hard | K18 | 12 | 0.0340 | 0.0042 | 0.0027 | 0.0027 | 0.0026 | 0.0028 | 0.0042 | 0.0023 | 0.0015 |
| S8_small_hard | K18 | 24 | 0.0341 | 0.0028 | 0.0015 | 0.0015 | 0.0015 | 0.0015 | 0.0044 | 0.0015 | 0.0015 |

### Feasibility (fraction of experiments in which the adaptive branch ran)

| scenario | k_config | b | fullset_adaptive | fullset_adaptive_fb | fullset_adaptive_s |
|---|---|---|---|---|---|
| S7_hard | K18 | 6 | 0.00 | 0.00 | 1.00 |
| S7_hard | K18 | 9 | 1.00 | 1.00 | 1.00 |
| S7_hard | K18 | 12 | 1.00 | 1.00 | 1.00 |
| S7_hard | K18 | 24 | 1.00 | 1.00 | 1.00 |
| S8_large_hard | K18 | 6 | 0.00 | 0.00 | 1.00 |
| S8_large_hard | K18 | 9 | 1.00 | 1.00 | 1.00 |
| S8_large_hard | K18 | 12 | 1.00 | 1.00 | 1.00 |
| S8_large_hard | K18 | 24 | 1.00 | 1.00 | 1.00 |
| S8_small_hard | K18 | 6 | 0.00 | 0.00 | 1.00 |
| S8_small_hard | K18 | 9 | 1.00 | 1.00 | 1.00 |
| S8_small_hard | K18 | 12 | 1.00 | 1.00 | 1.00 |
| S8_small_hard | K18 | 24 | 1.00 | 1.00 | 1.00 |

### Compute: mean fits used (budget = b (2 + K))

| scenario | k_config | b | pcga_l | exhaustive_iut | fullset_adaptive | fullset_adaptive_fb | fullset_adaptive_s | screen_uniform | screen_random | screen_sh | oracle_select |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S7_hard | K18 | 6 | 120 | 120 | 0 | 120 | 120 | 120 | 118 | 120 | 120 |
| S7_hard | K18 | 9 | 180 | 180 | 180 | 180 | 180 | 180 | 178 | 180 | 180 |
| S7_hard | K18 | 12 | 240 | 240 | 240 | 240 | 240 | 240 | 238 | 240 | 240 |
| S7_hard | K18 | 24 | 480 | 480 | 473 | 473 | 473 | 480 | 438 | 480 | 300 |
| S8_large_hard | K18 | 6 | 120 | 120 | 0 | 120 | 120 | 120 | 118 | 120 | 120 |
| S8_large_hard | K18 | 9 | 180 | 180 | 180 | 180 | 180 | 180 | 178 | 180 | 180 |
| S8_large_hard | K18 | 12 | 240 | 240 | 240 | 240 | 240 | 240 | 238 | 240 | 240 |
| S8_large_hard | K18 | 24 | 480 | 480 | 437 | 437 | 437 | 480 | 438 | 480 | 300 |
| S8_small_hard | K18 | 6 | 120 | 120 | 0 | 120 | 120 | 120 | 118 | 120 | 120 |
| S8_small_hard | K18 | 9 | 180 | 180 | 180 | 180 | 180 | 180 | 178 | 180 | 180 |
| S8_small_hard | K18 | 12 | 240 | 240 | 240 | 240 | 240 | 240 | 238 | 240 | 240 |
| S8_small_hard | K18 | 24 | 480 | 480 | 447 | 447 | 447 | 480 | 438 | 480 | 300 |

### Compute: mean measured wall-clock seconds (fits + placebo generation)

| scenario | k_config | b | pcga_l | exhaustive_iut | fullset_adaptive | fullset_adaptive_fb | fullset_adaptive_s | screen_uniform | screen_random | screen_sh | oracle_select |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S7_hard | K18 | 6 | 10.8 | 10.6 | 0.0 | 10.6 | 10.7 | 10.8 | 10.6 | 10.9 | 11.1 |
| S7_hard | K18 | 9 | 16.1 | 15.9 | 16.0 | 16.0 | 16.1 | 16.3 | 16.1 | 16.4 | 16.6 |
| S7_hard | K18 | 12 | 21.5 | 21.2 | 21.7 | 21.7 | 21.7 | 21.7 | 21.5 | 21.9 | 22.2 |
| S7_hard | K18 | 24 | 43.1 | 42.4 | 43.3 | 43.3 | 43.3 | 43.3 | 39.7 | 43.6 | 27.7 |
| S8_large_hard | K18 | 6 | 10.7 | 10.1 | 0.0 | 10.1 | 10.3 | 10.5 | 10.3 | 10.5 | 11.0 |
| S8_large_hard | K18 | 9 | 16.1 | 15.1 | 15.5 | 15.5 | 15.7 | 15.8 | 15.6 | 16.0 | 16.5 |
| S8_large_hard | K18 | 12 | 21.4 | 20.1 | 21.3 | 21.3 | 21.4 | 21.0 | 21.0 | 21.3 | 22.0 |
| S8_large_hard | K18 | 24 | 42.8 | 40.3 | 39.6 | 39.6 | 39.6 | 42.0 | 38.7 | 42.2 | 27.5 |
| S8_small_hard | K18 | 6 | 11.0 | 10.5 | 0.0 | 10.5 | 10.6 | 10.8 | 10.6 | 10.9 | 11.2 |
| S8_small_hard | K18 | 9 | 16.5 | 15.7 | 16.0 | 16.0 | 16.2 | 16.3 | 16.1 | 16.4 | 16.9 |
| S8_small_hard | K18 | 12 | 22.1 | 20.9 | 21.9 | 21.9 | 22.0 | 21.7 | 21.6 | 21.9 | 22.5 |
| S8_small_hard | K18 | 24 | 44.1 | 41.9 | 41.7 | 41.7 | 41.7 | 43.3 | 39.8 | 43.6 | 28.1 |

## eps = 0.0

### Power: claim rate in positive scenarios (S8; theta_full > eps)

| scenario | k_config | b | pcga_l | exhaustive_iut | fullset_adaptive | fullset_adaptive_fb | fullset_adaptive_s | screen_uniform | screen_random | screen_sh | oracle_select |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S8_large_hard | K18 | 6 | 1.000 | 0.633 | 0.000 | 0.633 | 0.567 | 0.967 | 0.967 | 0.967 | 1.000 |
| S8_large_hard | K18 | 9 | 1.000 | 0.733 | 0.817 | 0.817 | 0.817 | 1.000 | 1.000 | 1.000 | 1.000 |
| S8_large_hard | K18 | 12 | 1.000 | 0.833 | 0.933 | 0.933 | 0.950 | 1.000 | 1.000 | 1.000 | 1.000 |
| S8_large_hard | K18 | 24 | 1.000 | 0.983 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| S8_small_hard | K18 | 6 | 1.000 | 0.333 | 0.000 | 0.333 | 0.300 | 0.883 | 0.883 | 0.867 | 0.983 |
| S8_small_hard | K18 | 9 | 1.000 | 0.417 | 0.750 | 0.750 | 0.833 | 0.950 | 0.967 | 0.950 | 1.000 |
| S8_small_hard | K18 | 12 | 1.000 | 0.550 | 0.883 | 0.883 | 0.883 | 0.983 | 1.000 | 0.983 | 1.000 |
| S8_small_hard | K18 | 24 | 1.000 | 0.900 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |

### Full-set false-claim rate in negative controls (S7; theta_full <= 0). A guarantee (<= alpha) exists only for scope=full procedures

| scenario | k_config | b | pcga_l | exhaustive_iut | fullset_adaptive | fullset_adaptive_fb | fullset_adaptive_s | screen_uniform | screen_random | screen_sh | oracle_select |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S7_hard | K18 | 6 | 1.000 | 0.050 | 0.000 | 0.050 | 0.050 | 0.150 | 0.150 | 0.117 | 0.017 |
| S7_hard | K18 | 9 | 1.000 | 0.067 | 0.050 | 0.050 | 0.050 | 0.083 | 0.150 | 0.050 | 0.033 |
| S7_hard | K18 | 12 | 1.000 | 0.067 | 0.050 | 0.050 | 0.033 | 0.067 | 0.100 | 0.017 | 0.017 |
| S7_hard | K18 | 24 | 1.000 | 0.033 | 0.083 | 0.083 | 0.083 | 0.017 | 0.133 | 0.033 | 0.033 |

### S7: Wilson 95% upper limit of the full-set claim rate (full-set procedures)

| scenario | k_config | b | exhaustive_iut | fullset_adaptive | fullset_adaptive_fb | fullset_adaptive_s |
|---|---|---|---|---|---|---|
| S7_hard | K18 | 6 | 0.137 | 0.060 | 0.137 | 0.137 |
| S7_hard | K18 | 9 | 0.159 | 0.137 | 0.137 | 0.137 |
| S7_hard | K18 | 12 | 0.159 | 0.137 | 0.137 | 0.114 |
| S7_hard | K18 | 24 | 0.114 | 0.181 | 0.181 | 0.181 |

### False claims against each procedure's OWN estimand (selected: theta_sel; PCGA-L: Delta_strat:block)

| scenario | k_config | b | pcga_l | exhaustive_iut | fullset_adaptive | fullset_adaptive_fb | fullset_adaptive_s | screen_uniform | screen_random | screen_sh | oracle_select |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S7_hard | K18 | 6 | 0.000 | 0.050 | 0.000 | 0.050 | 0.050 | 0.050 | 0.050 | 0.050 | 0.017 |
| S7_hard | K18 | 9 | 0.000 | 0.067 | 0.050 | 0.050 | 0.050 | 0.033 | 0.050 | 0.033 | 0.033 |
| S7_hard | K18 | 12 | 0.000 | 0.067 | 0.050 | 0.050 | 0.033 | 0.017 | 0.000 | 0.017 | 0.017 |
| S7_hard | K18 | 24 | 0.000 | 0.033 | 0.083 | 0.083 | 0.083 | 0.017 | 0.033 | 0.017 | 0.033 |
| S8_large_hard | K18 | 6 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| S8_large_hard | K18 | 9 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| S8_large_hard | K18 | 12 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| S8_large_hard | K18 | 24 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| S8_small_hard | K18 | 6 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| S8_small_hard | K18 | 9 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| S8_small_hard | K18 | 12 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| S8_small_hard | K18 | 24 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |

### Binding-null discovery (strat:w1+w2 in the selected set; full-set: top-allocated arm)

| scenario | k_config | b | exhaustive_iut | fullset_adaptive | fullset_adaptive_fb | fullset_adaptive_s | screen_uniform | screen_random | screen_sh | oracle_select |
|---|---|---|---|---|---|---|---|---|---|---|
| S7_hard | K18 | 6 | 0.833 |  | 0.833 | 0.467 | 0.900 | 0.900 | 0.933 | 1.000 |
| S7_hard | K18 | 9 | 0.983 | 0.367 | 0.367 | 0.450 | 0.950 | 0.900 | 0.983 | 1.000 |
| S7_hard | K18 | 12 | 1.000 | 0.650 | 0.650 | 0.683 | 0.950 | 0.900 | 1.000 | 1.000 |
| S7_hard | K18 | 24 | 1.000 | 0.661 | 0.661 | 0.661 | 1.000 | 0.900 | 0.983 | 1.000 |
| S8_large_hard | K18 | 6 | 0.833 |  | 0.833 | 0.533 | 0.883 | 0.883 | 0.900 | 1.000 |
| S8_large_hard | K18 | 9 | 0.967 | 0.600 | 0.600 | 0.550 | 0.917 | 0.883 | 0.933 | 1.000 |
| S8_large_hard | K18 | 12 | 0.983 | 0.683 | 0.683 | 0.683 | 0.933 | 0.883 | 0.983 | 1.000 |
| S8_large_hard | K18 | 24 | 1.000 | 0.809 | 0.809 | 0.809 | 1.000 | 0.883 | 1.000 | 1.000 |
| S8_small_hard | K18 | 6 | 0.800 |  | 0.800 | 0.500 | 0.883 | 0.883 | 0.967 | 1.000 |
| S8_small_hard | K18 | 9 | 0.950 | 0.633 | 0.633 | 0.600 | 0.917 | 0.883 | 0.983 | 1.000 |
| S8_small_hard | K18 | 12 | 0.967 | 0.717 | 0.717 | 0.733 | 0.967 | 0.883 | 1.000 | 1.000 |
| S8_small_hard | K18 | 24 | 1.000 | 0.765 | 0.765 | 0.765 | 1.000 | 0.883 | 1.000 | 1.000 |

### Coverage of each procedure's own estimand by its lower bound

| scenario | k_config | b | exhaustive_iut | fullset_adaptive | fullset_adaptive_fb | fullset_adaptive_s | screen_uniform | screen_random | screen_sh | oracle_select |
|---|---|---|---|---|---|---|---|---|---|---|
| S7_hard | K18 | 6 | 0.950 |  | 0.950 | 0.950 | 0.950 | 0.950 | 0.950 | 0.983 |
| S7_hard | K18 | 9 | 0.933 | 0.950 | 0.950 | 0.950 | 0.967 | 0.950 | 0.967 | 0.967 |
| S7_hard | K18 | 12 | 0.933 | 0.950 | 0.950 | 0.967 | 0.983 | 1.000 | 0.983 | 0.983 |
| S7_hard | K18 | 24 | 0.967 | 0.917 | 0.917 | 0.917 | 0.983 | 0.967 | 0.983 | 0.967 |
| S8_large_hard | K18 | 6 | 0.983 |  | 0.983 | 1.000 | 0.933 | 0.933 | 0.933 | 0.967 |
| S8_large_hard | K18 | 9 | 0.933 | 1.000 | 1.000 | 1.000 | 0.933 | 0.950 | 0.933 | 0.950 |
| S8_large_hard | K18 | 12 | 0.950 | 1.000 | 1.000 | 1.000 | 0.967 | 0.967 | 0.967 | 0.967 |
| S8_large_hard | K18 | 24 | 0.950 | 1.000 | 1.000 | 1.000 | 0.967 | 0.950 | 0.967 | 0.950 |
| S8_small_hard | K18 | 6 | 0.967 |  | 0.967 | 1.000 | 0.950 | 0.950 | 0.950 | 0.950 |
| S8_small_hard | K18 | 9 | 1.000 | 1.000 | 1.000 | 1.000 | 0.950 | 0.967 | 0.950 | 0.967 |
| S8_small_hard | K18 | 12 | 1.000 | 1.000 | 1.000 | 1.000 | 0.950 | 0.933 | 0.950 | 0.983 |
| S8_small_hard | K18 | 24 | 0.967 | 0.983 | 0.983 | 0.983 | 0.983 | 0.950 | 0.983 | 0.933 |

### Coverage of theta_full (meaningful as a guarantee for full-set procedures only)

| scenario | k_config | b | exhaustive_iut | fullset_adaptive | fullset_adaptive_fb | fullset_adaptive_s | screen_uniform | screen_random | screen_sh | oracle_select |
|---|---|---|---|---|---|---|---|---|---|---|
| S7_hard | K18 | 6 | 0.950 |  | 0.950 | 0.950 | 0.850 | 0.850 | 0.883 | 0.983 |
| S7_hard | K18 | 9 | 0.933 | 0.950 | 0.950 | 0.950 | 0.917 | 0.850 | 0.950 | 0.967 |
| S7_hard | K18 | 12 | 0.933 | 0.950 | 0.950 | 0.967 | 0.933 | 0.900 | 0.983 | 0.983 |
| S7_hard | K18 | 24 | 0.967 | 0.917 | 0.917 | 0.917 | 0.983 | 0.867 | 0.967 | 0.967 |
| S8_large_hard | K18 | 6 | 0.983 |  | 0.983 | 1.000 | 0.833 | 0.833 | 0.867 | 0.967 |
| S8_large_hard | K18 | 9 | 0.933 | 1.000 | 1.000 | 1.000 | 0.867 | 0.833 | 0.883 | 0.950 |
| S8_large_hard | K18 | 12 | 0.950 | 1.000 | 1.000 | 1.000 | 0.900 | 0.850 | 0.950 | 0.967 |
| S8_large_hard | K18 | 24 | 0.950 | 1.000 | 1.000 | 1.000 | 0.967 | 0.833 | 0.967 | 0.950 |
| S8_small_hard | K18 | 6 | 0.967 |  | 0.967 | 1.000 | 0.833 | 0.833 | 0.917 | 0.950 |
| S8_small_hard | K18 | 9 | 1.000 | 1.000 | 1.000 | 1.000 | 0.867 | 0.850 | 0.933 | 0.967 |
| S8_small_hard | K18 | 12 | 1.000 | 1.000 | 1.000 | 1.000 | 0.917 | 0.817 | 0.950 | 0.983 |
| S8_small_hard | K18 | 24 | 0.967 | 0.983 | 0.983 | 0.983 | 0.983 | 0.833 | 0.983 | 0.933 |

### Estimation bias against the procedure's own estimand

| scenario | k_config | b | pcga_l | exhaustive_iut | fullset_adaptive | fullset_adaptive_fb | fullset_adaptive_s | screen_uniform | screen_random | screen_sh | oracle_select |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S7_hard | K18 | 6 | 0.0004 | -0.0011 |  | -0.0011 | -0.0010 | -0.0002 | -0.0002 | -0.0002 | -0.0002 |
| S7_hard | K18 | 9 | 0.0004 | -0.0007 | -0.0002 | -0.0002 | -0.0002 | -0.0003 | -0.0004 | -0.0003 | -0.0001 |
| S7_hard | K18 | 12 | 0.0003 | -0.0003 | -0.0001 | -0.0001 | 0.0001 | -0.0002 | -0.0002 | -0.0002 | -0.0001 |
| S7_hard | K18 | 24 | -0.0001 | -0.0002 | -0.0000 | -0.0000 | -0.0000 | -0.0001 | -0.0002 | -0.0001 | -0.0001 |
| S8_large_hard | K18 | 6 | 0.0004 | -0.0006 |  | -0.0006 | -0.0003 | 0.0001 | 0.0001 | -0.0000 | -0.0000 |
| S8_large_hard | K18 | 9 | 0.0001 | -0.0002 | -0.0003 | -0.0003 | -0.0004 | -0.0003 | -0.0002 | -0.0003 | 0.0000 |
| S8_large_hard | K18 | 12 | -0.0000 | 0.0000 | 0.0001 | 0.0001 | 0.0001 | -0.0002 | -0.0002 | -0.0000 | 0.0000 |
| S8_large_hard | K18 | 24 | 0.0001 | 0.0001 | 0.0011 | 0.0011 | 0.0011 | 0.0000 | 0.0001 | 0.0000 | 0.0002 |
| S8_small_hard | K18 | 6 | 0.0001 | -0.0013 |  | -0.0013 | -0.0018 | -0.0004 | -0.0004 | -0.0003 | -0.0002 |
| S8_small_hard | K18 | 9 | 0.0003 | -0.0018 | -0.0004 | -0.0004 | -0.0002 | -0.0004 | -0.0003 | -0.0003 | -0.0001 |
| S8_small_hard | K18 | 12 | 0.0001 | -0.0011 | -0.0002 | -0.0002 | -0.0001 | -0.0002 | -0.0001 | -0.0002 | 0.0001 |
| S8_small_hard | K18 | 24 | 0.0002 | -0.0001 | 0.0005 | 0.0005 | 0.0005 | 0.0001 | 0.0001 | 0.0001 | 0.0001 |

### Estimation RMSE against the procedure's own estimand

| scenario | k_config | b | pcga_l | exhaustive_iut | fullset_adaptive | fullset_adaptive_fb | fullset_adaptive_s | screen_uniform | screen_random | screen_sh | oracle_select |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S7_hard | K18 | 6 | 0.0043 | 0.0045 |  | 0.0045 | 0.0038 | 0.0026 | 0.0026 | 0.0026 | 0.0016 |
| S7_hard | K18 | 9 | 0.0031 | 0.0037 | 0.0027 | 0.0027 | 0.0024 | 0.0020 | 0.0019 | 0.0020 | 0.0012 |
| S7_hard | K18 | 12 | 0.0028 | 0.0034 | 0.0017 | 0.0017 | 0.0016 | 0.0016 | 0.0014 | 0.0016 | 0.0011 |
| S7_hard | K18 | 24 | 0.0019 | 0.0022 | 0.0011 | 0.0011 | 0.0011 | 0.0011 | 0.0011 | 0.0011 | 0.0011 |
| S8_large_hard | K18 | 6 | 0.0039 | 0.0068 |  | 0.0068 | 0.0049 | 0.0038 | 0.0038 | 0.0037 | 0.0023 |
| S8_large_hard | K18 | 9 | 0.0032 | 0.0050 | 0.0046 | 0.0046 | 0.0045 | 0.0029 | 0.0026 | 0.0028 | 0.0020 |
| S8_large_hard | K18 | 12 | 0.0029 | 0.0047 | 0.0030 | 0.0030 | 0.0029 | 0.0024 | 0.0022 | 0.0023 | 0.0016 |
| S8_large_hard | K18 | 24 | 0.0019 | 0.0032 | 0.0033 | 0.0033 | 0.0033 | 0.0016 | 0.0016 | 0.0016 | 0.0015 |
| S8_small_hard | K18 | 6 | 0.0037 | 0.0060 |  | 0.0060 | 0.0053 | 0.0032 | 0.0032 | 0.0032 | 0.0023 |
| S8_small_hard | K18 | 9 | 0.0029 | 0.0050 | 0.0037 | 0.0037 | 0.0034 | 0.0025 | 0.0023 | 0.0025 | 0.0017 |
| S8_small_hard | K18 | 12 | 0.0028 | 0.0042 | 0.0024 | 0.0024 | 0.0025 | 0.0023 | 0.0021 | 0.0023 | 0.0015 |
| S8_small_hard | K18 | 24 | 0.0021 | 0.0028 | 0.0018 | 0.0018 | 0.0018 | 0.0015 | 0.0014 | 0.0015 | 0.0015 |

### Estimation RMSE against theta_full

| scenario | k_config | b | pcga_l | exhaustive_iut | fullset_adaptive | fullset_adaptive_fb | fullset_adaptive_s | screen_uniform | screen_random | screen_sh | oracle_select |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S7_hard | K18 | 6 | 0.0399 | 0.0045 |  | 0.0045 | 0.0038 | 0.0049 | 0.0050 | 0.0045 | 0.0016 |
| S7_hard | K18 | 9 | 0.0398 | 0.0037 | 0.0027 | 0.0027 | 0.0024 | 0.0036 | 0.0044 | 0.0025 | 0.0012 |
| S7_hard | K18 | 12 | 0.0397 | 0.0034 | 0.0017 | 0.0017 | 0.0016 | 0.0036 | 0.0045 | 0.0016 | 0.0011 |
| S7_hard | K18 | 24 | 0.0393 | 0.0022 | 0.0011 | 0.0011 | 0.0011 | 0.0011 | 0.0046 | 0.0022 | 0.0011 |
| S8_large_hard | K18 | 6 | 0.0327 | 0.0068 |  | 0.0068 | 0.0049 | 0.0051 | 0.0051 | 0.0048 | 0.0023 |
| S8_large_hard | K18 | 9 | 0.0324 | 0.0050 | 0.0046 | 0.0046 | 0.0045 | 0.0037 | 0.0042 | 0.0037 | 0.0020 |
| S8_large_hard | K18 | 12 | 0.0322 | 0.0047 | 0.0030 | 0.0030 | 0.0029 | 0.0034 | 0.0040 | 0.0029 | 0.0016 |
| S8_large_hard | K18 | 24 | 0.0322 | 0.0032 | 0.0033 | 0.0033 | 0.0033 | 0.0016 | 0.0039 | 0.0016 | 0.0015 |
| S8_small_hard | K18 | 6 | 0.0342 | 0.0060 |  | 0.0060 | 0.0053 | 0.0048 | 0.0048 | 0.0036 | 0.0023 |
| S8_small_hard | K18 | 9 | 0.0343 | 0.0050 | 0.0037 | 0.0037 | 0.0034 | 0.0037 | 0.0043 | 0.0027 | 0.0017 |
| S8_small_hard | K18 | 12 | 0.0340 | 0.0042 | 0.0024 | 0.0024 | 0.0025 | 0.0028 | 0.0042 | 0.0023 | 0.0015 |
| S8_small_hard | K18 | 24 | 0.0341 | 0.0028 | 0.0018 | 0.0018 | 0.0018 | 0.0015 | 0.0044 | 0.0015 | 0.0015 |

### Feasibility (fraction of experiments in which the adaptive branch ran)

| scenario | k_config | b | fullset_adaptive | fullset_adaptive_fb | fullset_adaptive_s |
|---|---|---|---|---|---|
| S7_hard | K18 | 6 | 0.00 | 0.00 | 1.00 |
| S7_hard | K18 | 9 | 1.00 | 1.00 | 1.00 |
| S7_hard | K18 | 12 | 1.00 | 1.00 | 1.00 |
| S7_hard | K18 | 24 | 1.00 | 1.00 | 1.00 |
| S8_large_hard | K18 | 6 | 0.00 | 0.00 | 1.00 |
| S8_large_hard | K18 | 9 | 1.00 | 1.00 | 1.00 |
| S8_large_hard | K18 | 12 | 1.00 | 1.00 | 1.00 |
| S8_large_hard | K18 | 24 | 1.00 | 1.00 | 1.00 |
| S8_small_hard | K18 | 6 | 0.00 | 0.00 | 1.00 |
| S8_small_hard | K18 | 9 | 1.00 | 1.00 | 1.00 |
| S8_small_hard | K18 | 12 | 1.00 | 1.00 | 1.00 |
| S8_small_hard | K18 | 24 | 1.00 | 1.00 | 1.00 |

### Compute: mean fits used (budget = b (2 + K))

| scenario | k_config | b | pcga_l | exhaustive_iut | fullset_adaptive | fullset_adaptive_fb | fullset_adaptive_s | screen_uniform | screen_random | screen_sh | oracle_select |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S7_hard | K18 | 6 | 120 | 120 | 0 | 120 | 120 | 120 | 118 | 120 | 120 |
| S7_hard | K18 | 9 | 180 | 180 | 180 | 180 | 180 | 180 | 178 | 180 | 180 |
| S7_hard | K18 | 12 | 240 | 240 | 240 | 240 | 240 | 240 | 238 | 240 | 240 |
| S7_hard | K18 | 24 | 480 | 480 | 450 | 450 | 450 | 480 | 438 | 480 | 300 |
| S8_large_hard | K18 | 6 | 120 | 120 | 0 | 120 | 120 | 120 | 118 | 120 | 120 |
| S8_large_hard | K18 | 9 | 180 | 180 | 180 | 180 | 180 | 180 | 178 | 180 | 180 |
| S8_large_hard | K18 | 12 | 240 | 240 | 240 | 240 | 240 | 240 | 238 | 240 | 240 |
| S8_large_hard | K18 | 24 | 480 | 480 | 373 | 373 | 373 | 480 | 438 | 480 | 300 |
| S8_small_hard | K18 | 6 | 120 | 120 | 0 | 120 | 120 | 120 | 118 | 120 | 120 |
| S8_small_hard | K18 | 9 | 180 | 180 | 180 | 180 | 180 | 180 | 178 | 180 | 180 |
| S8_small_hard | K18 | 12 | 240 | 240 | 240 | 240 | 240 | 240 | 238 | 240 | 240 |
| S8_small_hard | K18 | 24 | 480 | 480 | 380 | 380 | 380 | 480 | 438 | 480 | 300 |

### Compute: mean measured wall-clock seconds (fits + placebo generation)

| scenario | k_config | b | pcga_l | exhaustive_iut | fullset_adaptive | fullset_adaptive_fb | fullset_adaptive_s | screen_uniform | screen_random | screen_sh | oracle_select |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S7_hard | K18 | 6 | 10.8 | 10.6 | 0.0 | 10.6 | 10.7 | 10.8 | 10.6 | 10.9 | 11.1 |
| S7_hard | K18 | 9 | 16.1 | 15.9 | 16.2 | 16.2 | 16.3 | 16.3 | 16.1 | 16.4 | 16.6 |
| S7_hard | K18 | 12 | 21.5 | 21.2 | 22.0 | 22.0 | 22.1 | 21.7 | 21.5 | 21.9 | 22.2 |
| S7_hard | K18 | 24 | 43.1 | 42.4 | 41.9 | 41.9 | 41.9 | 43.3 | 39.7 | 43.6 | 27.7 |
| S8_large_hard | K18 | 6 | 10.7 | 10.1 | 0.0 | 10.1 | 10.3 | 10.5 | 10.3 | 10.5 | 11.0 |
| S8_large_hard | K18 | 9 | 16.1 | 15.1 | 15.6 | 15.6 | 15.8 | 15.8 | 15.6 | 16.0 | 16.5 |
| S8_large_hard | K18 | 12 | 21.4 | 20.1 | 21.5 | 21.5 | 21.6 | 21.0 | 21.0 | 21.3 | 22.0 |
| S8_large_hard | K18 | 24 | 42.8 | 40.3 | 34.0 | 34.0 | 34.0 | 42.0 | 38.7 | 42.2 | 27.5 |
| S8_small_hard | K18 | 6 | 11.0 | 10.5 | 0.0 | 10.5 | 10.6 | 10.8 | 10.6 | 10.9 | 11.2 |
| S8_small_hard | K18 | 9 | 16.5 | 15.7 | 16.2 | 16.2 | 16.4 | 16.3 | 16.1 | 16.4 | 16.9 |
| S8_small_hard | K18 | 12 | 22.1 | 20.9 | 22.2 | 22.2 | 22.3 | 21.7 | 21.6 | 21.9 | 22.5 |
| S8_small_hard | K18 | 24 | 44.1 | 41.9 | 35.8 | 35.8 | 35.8 | 43.3 | 39.8 | 43.6 | 28.1 |

## Paired differences (experiment-paired; 95% normal CI), eps = 0.005; full table in paired_differences.csv

| scenario | k_config | b | eps | a | b_proc | metric | diff | ci_lo | ci_hi | n_exp |
|---|---|---|---|---|---|---|---|---|---|---|
| S7_hard | K18 | 6 | 0.005 | fullset_adaptive_s | exhaustive_iut | claim | 0.000 | 0.000 | 0.000 | 60 |
| S7_hard | K18 | 9 | 0.005 | fullset_adaptive_s | exhaustive_iut | claim | 0.000 | 0.000 | 0.000 | 60 |
| S7_hard | K18 | 12 | 0.005 | fullset_adaptive_s | exhaustive_iut | claim | 0.000 | 0.000 | 0.000 | 60 |
| S7_hard | K18 | 24 | 0.005 | fullset_adaptive_s | exhaustive_iut | claim | 0.000 | 0.000 | 0.000 | 60 |
| S8_large_hard | K18 | 6 | 0.005 | fullset_adaptive_s | exhaustive_iut | claim | -0.017 | -0.115 | 0.082 | 60 |
| S8_large_hard | K18 | 9 | 0.005 | fullset_adaptive_s | exhaustive_iut | claim | 0.217 | 0.102 | 0.332 | 60 |
| S8_large_hard | K18 | 12 | 0.005 | fullset_adaptive_s | exhaustive_iut | claim | 0.300 | 0.166 | 0.434 | 60 |
| S8_large_hard | K18 | 24 | 0.005 | fullset_adaptive_s | exhaustive_iut | claim | 0.283 | 0.168 | 0.398 | 60 |
| S8_small_hard | K18 | 6 | 0.005 | fullset_adaptive_s | exhaustive_iut | claim | -0.083 | -0.154 | -0.013 | 60 |
| S8_small_hard | K18 | 9 | 0.005 | fullset_adaptive_s | exhaustive_iut | claim | 0.100 | -0.011 | 0.211 | 60 |
| S8_small_hard | K18 | 12 | 0.005 | fullset_adaptive_s | exhaustive_iut | claim | 0.250 | 0.121 | 0.379 | 60 |
| S8_small_hard | K18 | 24 | 0.005 | fullset_adaptive_s | exhaustive_iut | claim | 0.417 | 0.283 | 0.551 | 60 |
| S7_hard | K18 | 6 | 0.005 | fullset_adaptive_fb | exhaustive_iut | claim | 0.000 | 0.000 | 0.000 | 60 |
| S7_hard | K18 | 9 | 0.005 | fullset_adaptive_fb | exhaustive_iut | claim | 0.000 | 0.000 | 0.000 | 60 |
| S7_hard | K18 | 12 | 0.005 | fullset_adaptive_fb | exhaustive_iut | claim | 0.000 | 0.000 | 0.000 | 60 |
| S7_hard | K18 | 24 | 0.005 | fullset_adaptive_fb | exhaustive_iut | claim | 0.000 | 0.000 | 0.000 | 60 |
| S8_large_hard | K18 | 6 | 0.005 | fullset_adaptive_fb | exhaustive_iut | claim | 0.000 | 0.000 | 0.000 | 60 |
| S8_large_hard | K18 | 9 | 0.005 | fullset_adaptive_fb | exhaustive_iut | claim | 0.150 | 0.038 | 0.262 | 60 |
| S8_large_hard | K18 | 12 | 0.005 | fullset_adaptive_fb | exhaustive_iut | claim | 0.233 | 0.099 | 0.368 | 60 |
| S8_large_hard | K18 | 24 | 0.005 | fullset_adaptive_fb | exhaustive_iut | claim | 0.283 | 0.168 | 0.398 | 60 |
| S8_small_hard | K18 | 6 | 0.005 | fullset_adaptive_fb | exhaustive_iut | claim | 0.000 | 0.000 | 0.000 | 60 |
| S8_small_hard | K18 | 9 | 0.005 | fullset_adaptive_fb | exhaustive_iut | claim | 0.067 | -0.036 | 0.169 | 60 |
| S8_small_hard | K18 | 12 | 0.005 | fullset_adaptive_fb | exhaustive_iut | claim | 0.267 | 0.136 | 0.397 | 60 |
| S8_small_hard | K18 | 24 | 0.005 | fullset_adaptive_fb | exhaustive_iut | claim | 0.417 | 0.283 | 0.551 | 60 |
| S7_hard | K18 | 6 | 0.005 | fullset_adaptive | exhaustive_iut | claim | 0.000 | 0.000 | 0.000 | 60 |
| S7_hard | K18 | 9 | 0.005 | fullset_adaptive | exhaustive_iut | claim | 0.000 | 0.000 | 0.000 | 60 |
| S7_hard | K18 | 12 | 0.005 | fullset_adaptive | exhaustive_iut | claim | 0.000 | 0.000 | 0.000 | 60 |
| S7_hard | K18 | 24 | 0.005 | fullset_adaptive | exhaustive_iut | claim | 0.000 | 0.000 | 0.000 | 60 |
| S8_large_hard | K18 | 6 | 0.005 | fullset_adaptive | exhaustive_iut | claim | -0.183 | -0.282 | -0.085 | 60 |
| S8_large_hard | K18 | 9 | 0.005 | fullset_adaptive | exhaustive_iut | claim | 0.150 | 0.038 | 0.262 | 60 |
| S8_large_hard | K18 | 12 | 0.005 | fullset_adaptive | exhaustive_iut | claim | 0.233 | 0.099 | 0.368 | 60 |
| S8_large_hard | K18 | 24 | 0.005 | fullset_adaptive | exhaustive_iut | claim | 0.283 | 0.168 | 0.398 | 60 |
| S8_small_hard | K18 | 6 | 0.005 | fullset_adaptive | exhaustive_iut | claim | -0.083 | -0.154 | -0.013 | 60 |
| S8_small_hard | K18 | 9 | 0.005 | fullset_adaptive | exhaustive_iut | claim | 0.067 | -0.036 | 0.169 | 60 |
| S8_small_hard | K18 | 12 | 0.005 | fullset_adaptive | exhaustive_iut | claim | 0.267 | 0.136 | 0.397 | 60 |
| S8_small_hard | K18 | 24 | 0.005 | fullset_adaptive | exhaustive_iut | claim | 0.417 | 0.283 | 0.551 | 60 |
| S7_hard | K18 | 6 | 0.005 | fullset_adaptive_s | fullset_adaptive_fb | claim | 0.000 | 0.000 | 0.000 | 60 |
| S7_hard | K18 | 9 | 0.005 | fullset_adaptive_s | fullset_adaptive_fb | claim | 0.000 | 0.000 | 0.000 | 60 |
| S7_hard | K18 | 12 | 0.005 | fullset_adaptive_s | fullset_adaptive_fb | claim | 0.000 | 0.000 | 0.000 | 60 |
| S7_hard | K18 | 24 | 0.005 | fullset_adaptive_s | fullset_adaptive_fb | claim | 0.000 | 0.000 | 0.000 | 60 |
| S8_large_hard | K18 | 6 | 0.005 | fullset_adaptive_s | fullset_adaptive_fb | claim | -0.017 | -0.115 | 0.082 | 60 |
| S8_large_hard | K18 | 9 | 0.005 | fullset_adaptive_s | fullset_adaptive_fb | claim | 0.067 | -0.025 | 0.158 | 60 |
| S8_large_hard | K18 | 12 | 0.005 | fullset_adaptive_s | fullset_adaptive_fb | claim | 0.067 | 0.003 | 0.130 | 60 |
| S8_large_hard | K18 | 24 | 0.005 | fullset_adaptive_s | fullset_adaptive_fb | claim | 0.000 | 0.000 | 0.000 | 60 |
| S8_small_hard | K18 | 6 | 0.005 | fullset_adaptive_s | fullset_adaptive_fb | claim | -0.083 | -0.154 | -0.013 | 60 |
| S8_small_hard | K18 | 9 | 0.005 | fullset_adaptive_s | fullset_adaptive_fb | claim | 0.033 | -0.047 | 0.114 | 60 |
| S8_small_hard | K18 | 12 | 0.005 | fullset_adaptive_s | fullset_adaptive_fb | claim | -0.017 | -0.049 | 0.016 | 60 |
| S8_small_hard | K18 | 24 | 0.005 | fullset_adaptive_s | fullset_adaptive_fb | claim | 0.000 | 0.000 | 0.000 | 60 |
| S7_hard | K18 | 6 | 0.005 | screen_sh | screen_uniform | claim | -0.033 | -0.099 | 0.032 | 60 |
| S7_hard | K18 | 9 | 0.005 | screen_sh | screen_uniform | claim | -0.033 | -0.079 | 0.012 | 60 |
| S7_hard | K18 | 12 | 0.005 | screen_sh | screen_uniform | claim | -0.050 | -0.106 | 0.006 | 60 |
| S7_hard | K18 | 24 | 0.005 | screen_sh | screen_uniform | claim | 0.017 | -0.016 | 0.049 | 60 |
| S8_large_hard | K18 | 6 | 0.005 | screen_sh | screen_uniform | claim | -0.050 | -0.106 | 0.006 | 60 |
| S8_large_hard | K18 | 9 | 0.005 | screen_sh | screen_uniform | claim | -0.017 | -0.049 | 0.016 | 60 |
| S8_large_hard | K18 | 12 | 0.005 | screen_sh | screen_uniform | claim | 0.000 | 0.000 | 0.000 | 60 |
| S8_large_hard | K18 | 24 | 0.005 | screen_sh | screen_uniform | claim | 0.000 | 0.000 | 0.000 | 60 |
| S8_small_hard | K18 | 6 | 0.005 | screen_sh | screen_uniform | claim | -0.067 | -0.130 | -0.003 | 60 |
| S8_small_hard | K18 | 9 | 0.005 | screen_sh | screen_uniform | claim | -0.067 | -0.130 | -0.003 | 60 |
| S8_small_hard | K18 | 12 | 0.005 | screen_sh | screen_uniform | claim | -0.033 | -0.079 | 0.012 | 60 |
| S8_small_hard | K18 | 24 | 0.005 | screen_sh | screen_uniform | claim | 0.000 | 0.000 | 0.000 | 60 |
| S7_hard | K18 | 6 | 0.005 | screen_sh | screen_random | claim | -0.033 | -0.099 | 0.032 | 60 |
| S7_hard | K18 | 9 | 0.005 | screen_sh | screen_random | claim | -0.083 | -0.154 | -0.013 | 60 |
| S7_hard | K18 | 12 | 0.005 | screen_sh | screen_random | claim | -0.100 | -0.177 | -0.023 | 60 |
| S7_hard | K18 | 24 | 0.005 | screen_sh | screen_random | claim | -0.083 | -0.154 | -0.013 | 60 |
| S8_large_hard | K18 | 6 | 0.005 | screen_sh | screen_random | claim | -0.050 | -0.106 | 0.006 | 60 |
| S8_large_hard | K18 | 9 | 0.005 | screen_sh | screen_random | claim | -0.017 | -0.090 | 0.057 | 60 |
| S8_large_hard | K18 | 12 | 0.005 | screen_sh | screen_random | claim | -0.050 | -0.106 | 0.006 | 60 |
| S8_large_hard | K18 | 24 | 0.005 | screen_sh | screen_random | claim | 0.000 | 0.000 | 0.000 | 60 |
| S8_small_hard | K18 | 6 | 0.005 | screen_sh | screen_random | claim | -0.067 | -0.130 | -0.003 | 60 |
| S8_small_hard | K18 | 9 | 0.005 | screen_sh | screen_random | claim | -0.233 | -0.351 | -0.116 | 60 |
| S8_small_hard | K18 | 12 | 0.005 | screen_sh | screen_random | claim | -0.100 | -0.211 | 0.011 | 60 |
| S8_small_hard | K18 | 24 | 0.005 | screen_sh | screen_random | claim | -0.100 | -0.201 | 0.001 | 60 |
| S7_hard | K18 | 6 | 0.005 | screen_sh | screen_uniform | discovered | 0.033 | -0.032 | 0.099 | 60 |
| S7_hard | K18 | 9 | 0.005 | screen_sh | screen_uniform | discovered | 0.033 | -0.012 | 0.079 | 60 |
| S7_hard | K18 | 12 | 0.005 | screen_sh | screen_uniform | discovered | 0.050 | -0.006 | 0.106 | 60 |
| S7_hard | K18 | 24 | 0.005 | screen_sh | screen_uniform | discovered | -0.017 | -0.049 | 0.016 | 60 |
| S8_large_hard | K18 | 6 | 0.005 | screen_sh | screen_uniform | discovered | 0.017 | -0.082 | 0.115 | 60 |
| S8_large_hard | K18 | 9 | 0.005 | screen_sh | screen_uniform | discovered | 0.017 | -0.057 | 0.090 | 60 |
| S8_large_hard | K18 | 12 | 0.005 | screen_sh | screen_uniform | discovered | 0.050 | -0.023 | 0.123 | 60 |
| S8_large_hard | K18 | 24 | 0.005 | screen_sh | screen_uniform | discovered | 0.000 | 0.000 | 0.000 | 60 |
| S8_small_hard | K18 | 6 | 0.005 | screen_sh | screen_uniform | discovered | 0.083 | 0.013 | 0.154 | 60 |
| S8_small_hard | K18 | 9 | 0.005 | screen_sh | screen_uniform | discovered | 0.067 | 0.003 | 0.130 | 60 |
| S8_small_hard | K18 | 12 | 0.005 | screen_sh | screen_uniform | discovered | 0.033 | -0.012 | 0.079 | 60 |
| S8_small_hard | K18 | 24 | 0.005 | screen_sh | screen_uniform | discovered | 0.000 | 0.000 | 0.000 | 60 |
| S7_hard | K18 | 6 | 0.005 | screen_sh | screen_random | discovered | 0.033 | -0.032 | 0.099 | 60 |
| S7_hard | K18 | 9 | 0.005 | screen_sh | screen_random | discovered | 0.083 | 0.013 | 0.154 | 60 |
| S7_hard | K18 | 12 | 0.005 | screen_sh | screen_random | discovered | 0.100 | 0.023 | 0.177 | 60 |
| S7_hard | K18 | 24 | 0.005 | screen_sh | screen_random | discovered | 0.083 | 0.013 | 0.154 | 60 |
| S8_large_hard | K18 | 6 | 0.005 | screen_sh | screen_random | discovered | 0.017 | -0.082 | 0.115 | 60 |
| S8_large_hard | K18 | 9 | 0.005 | screen_sh | screen_random | discovered | 0.050 | -0.036 | 0.136 | 60 |
| S8_large_hard | K18 | 12 | 0.005 | screen_sh | screen_random | discovered | 0.100 | 0.010 | 0.190 | 60 |
| S8_large_hard | K18 | 24 | 0.005 | screen_sh | screen_random | discovered | 0.117 | 0.035 | 0.199 | 60 |
| S8_small_hard | K18 | 6 | 0.005 | screen_sh | screen_random | discovered | 0.083 | 0.013 | 0.154 | 60 |
| S8_small_hard | K18 | 9 | 0.005 | screen_sh | screen_random | discovered | 0.100 | 0.023 | 0.177 | 60 |
| S8_small_hard | K18 | 12 | 0.005 | screen_sh | screen_random | discovered | 0.117 | 0.035 | 0.199 | 60 |
| S8_small_hard | K18 | 24 | 0.005 | screen_sh | screen_random | discovered | 0.117 | 0.035 | 0.199 | 60 |
| S7_hard | K18 | 6 | 0.005 | screen_uniform | screen_random | discovered | 0.000 | 0.000 | 0.000 | 60 |
| S7_hard | K18 | 9 | 0.005 | screen_uniform | screen_random | discovered | 0.050 | -0.023 | 0.123 | 60 |
| S7_hard | K18 | 12 | 0.005 | screen_uniform | screen_random | discovered | 0.050 | -0.023 | 0.123 | 60 |
| S7_hard | K18 | 24 | 0.005 | screen_uniform | screen_random | discovered | 0.100 | 0.023 | 0.177 | 60 |
| S8_large_hard | K18 | 6 | 0.005 | screen_uniform | screen_random | discovered | 0.000 | 0.000 | 0.000 | 60 |
| S8_large_hard | K18 | 9 | 0.005 | screen_uniform | screen_random | discovered | 0.033 | -0.070 | 0.137 | 60 |
| S8_large_hard | K18 | 12 | 0.005 | screen_uniform | screen_random | discovered | 0.050 | -0.048 | 0.148 | 60 |
| S8_large_hard | K18 | 24 | 0.005 | screen_uniform | screen_random | discovered | 0.117 | 0.035 | 0.199 | 60 |
| S8_small_hard | K18 | 6 | 0.005 | screen_uniform | screen_random | discovered | 0.000 | 0.000 | 0.000 | 60 |
| S8_small_hard | K18 | 9 | 0.005 | screen_uniform | screen_random | discovered | 0.033 | -0.012 | 0.079 | 60 |
| S8_small_hard | K18 | 12 | 0.005 | screen_uniform | screen_random | discovered | 0.083 | 0.013 | 0.154 | 60 |
| S8_small_hard | K18 | 24 | 0.005 | screen_uniform | screen_random | discovered | 0.117 | 0.035 | 0.199 | 60 |
| S7_hard | K18 | 6 | 0.005 | screen_uniform | exhaustive_iut | claim | 0.100 | 0.023 | 0.177 | 60 |
| S7_hard | K18 | 9 | 0.005 | screen_uniform | exhaustive_iut | claim | 0.050 | -0.006 | 0.106 | 60 |
| S7_hard | K18 | 12 | 0.005 | screen_uniform | exhaustive_iut | claim | 0.050 | -0.006 | 0.106 | 60 |
| S7_hard | K18 | 24 | 0.005 | screen_uniform | exhaustive_iut | claim | 0.000 | 0.000 | 0.000 | 60 |
| S8_large_hard | K18 | 6 | 0.005 | screen_uniform | exhaustive_iut | claim | 0.500 | 0.356 | 0.644 | 60 |
| S8_large_hard | K18 | 9 | 0.005 | screen_uniform | exhaustive_iut | claim | 0.533 | 0.406 | 0.661 | 60 |
| S8_large_hard | K18 | 12 | 0.005 | screen_uniform | exhaustive_iut | claim | 0.533 | 0.398 | 0.669 | 60 |
| S8_large_hard | K18 | 24 | 0.005 | screen_uniform | exhaustive_iut | claim | 0.283 | 0.168 | 0.398 | 60 |
| S8_small_hard | K18 | 6 | 0.005 | screen_uniform | exhaustive_iut | claim | 0.317 | 0.189 | 0.444 | 60 |
| S8_small_hard | K18 | 9 | 0.005 | screen_uniform | exhaustive_iut | claim | 0.333 | 0.204 | 0.462 | 60 |
| S8_small_hard | K18 | 12 | 0.005 | screen_uniform | exhaustive_iut | claim | 0.417 | 0.283 | 0.551 | 60 |
| S8_small_hard | K18 | 24 | 0.005 | screen_uniform | exhaustive_iut | claim | 0.450 | 0.323 | 0.577 | 60 |
| S7_hard | K18 | 6 | 0.005 | screen_uniform | exhaustive_iut | false_vs_full | 0.100 | 0.023 | 0.177 | 60 |
| S7_hard | K18 | 9 | 0.005 | screen_uniform | exhaustive_iut | false_vs_full | 0.050 | -0.006 | 0.106 | 60 |
| S7_hard | K18 | 12 | 0.005 | screen_uniform | exhaustive_iut | false_vs_full | 0.050 | -0.006 | 0.106 | 60 |
| S7_hard | K18 | 24 | 0.005 | screen_uniform | exhaustive_iut | false_vs_full | 0.000 | 0.000 | 0.000 | 60 |
| S8_large_hard | K18 | 6 | 0.005 | screen_uniform | exhaustive_iut | false_vs_full | 0.000 | 0.000 | 0.000 | 60 |
| S8_large_hard | K18 | 9 | 0.005 | screen_uniform | exhaustive_iut | false_vs_full | 0.000 | 0.000 | 0.000 | 60 |
| S8_large_hard | K18 | 12 | 0.005 | screen_uniform | exhaustive_iut | false_vs_full | 0.000 | 0.000 | 0.000 | 60 |
| S8_large_hard | K18 | 24 | 0.005 | screen_uniform | exhaustive_iut | false_vs_full | 0.000 | 0.000 | 0.000 | 60 |
| S8_small_hard | K18 | 6 | 0.005 | screen_uniform | exhaustive_iut | false_vs_full | 0.000 | 0.000 | 0.000 | 60 |
| S8_small_hard | K18 | 9 | 0.005 | screen_uniform | exhaustive_iut | false_vs_full | 0.000 | 0.000 | 0.000 | 60 |
| S8_small_hard | K18 | 12 | 0.005 | screen_uniform | exhaustive_iut | false_vs_full | 0.000 | 0.000 | 0.000 | 60 |
| S8_small_hard | K18 | 24 | 0.005 | screen_uniform | exhaustive_iut | false_vs_full | 0.000 | 0.000 | 0.000 | 60 |
| S7_hard | K18 | 6 | 0.005 | fullset_adaptive_s | exhaustive_iut | covered_full | 0.017 | -0.016 | 0.049 | 60 |
| S7_hard | K18 | 9 | 0.005 | fullset_adaptive_s | exhaustive_iut | covered_full | 0.033 | -0.032 | 0.099 | 60 |
| S7_hard | K18 | 12 | 0.005 | fullset_adaptive_s | exhaustive_iut | covered_full | 0.033 | -0.032 | 0.099 | 60 |
| S7_hard | K18 | 24 | 0.005 | fullset_adaptive_s | exhaustive_iut | covered_full | -0.033 | -0.114 | 0.047 | 60 |
| S8_large_hard | K18 | 6 | 0.005 | fullset_adaptive_s | exhaustive_iut | covered_full | 0.017 | -0.016 | 0.049 | 60 |
| S8_large_hard | K18 | 9 | 0.005 | fullset_adaptive_s | exhaustive_iut | covered_full | 0.067 | 0.003 | 0.130 | 60 |
| S8_large_hard | K18 | 12 | 0.005 | fullset_adaptive_s | exhaustive_iut | covered_full | 0.050 | -0.006 | 0.106 | 60 |
| S8_large_hard | K18 | 24 | 0.005 | fullset_adaptive_s | exhaustive_iut | covered_full | 0.050 | -0.006 | 0.106 | 60 |
| S8_small_hard | K18 | 6 | 0.005 | fullset_adaptive_s | exhaustive_iut | covered_full | 0.033 | -0.012 | 0.079 | 60 |
| S8_small_hard | K18 | 9 | 0.005 | fullset_adaptive_s | exhaustive_iut | covered_full | 0.000 | 0.000 | 0.000 | 60 |
| S8_small_hard | K18 | 12 | 0.005 | fullset_adaptive_s | exhaustive_iut | covered_full | 0.000 | 0.000 | 0.000 | 60 |
| S8_small_hard | K18 | 24 | 0.005 | fullset_adaptive_s | exhaustive_iut | covered_full | 0.017 | -0.040 | 0.074 | 60 |

## Size of the one-sided t-test on exact-null (A/A) contrasts, disjoint groups

| scenario | n | groups | 0.01 | 0.025 | 0.04 | 0.05 | 0.1 |
|---|---|---|---|---|---|---|---|
| S7_hard | 2 | 3600 | 0.0092 | 0.0217 | 0.0350 | 0.0439 | 0.0903 |
| S7_hard | 3 | 2400 | 0.0092 | 0.0208 | 0.0329 | 0.0404 | 0.0929 |
| S7_hard | 4 | 1800 | 0.0106 | 0.0200 | 0.0361 | 0.0444 | 0.0939 |
| S7_hard | 5 | 1440 | 0.0076 | 0.0264 | 0.0382 | 0.0528 | 0.1007 |
| S7_hard | 8 | 900 | 0.0078 | 0.0244 | 0.0411 | 0.0478 | 0.1056 |
| S7_hard | 12 | 600 | 0.0050 | 0.0233 | 0.0417 | 0.0533 | 0.0950 |
| S7_hard | 20 | 360 | 0.0056 | 0.0222 | 0.0389 | 0.0472 | 0.1028 |

## Interim (alpha1 = 0.01) + inverse-normal combination (alpha2 = 0.04), data-dependent stage-2 size, exact-null arm

| R1 | rule | replicates | source | interim_rate | combination_rate | total_type1 | nominal | scenario |
|---|---|---|---|---|---|---|---|---|
| 2 | fixed5 | 1028 | disjoint_blocks | 0.0068 | 0.0331 | 0.0399 | 0.0500 | S7_hard |
| 2 | fixed20 | 327 | disjoint_blocks | 0.0214 | 0.0367 | 0.0581 | 0.0500 | S7_hard |
| 2 | promising_more | 225 | disjoint_blocks | 0.0133 | 0.0222 | 0.0356 | 0.0500 | S7_hard |
| 2 | promising_less | 225 | disjoint_blocks | 0.0133 | 0.0222 | 0.0356 | 0.0500 | S7_hard |
| 3 | fixed5 | 900 | disjoint_blocks | 0.0156 | 0.0322 | 0.0478 | 0.0500 | S7_hard |
| 3 | fixed20 | 313 | disjoint_blocks | 0.0064 | 0.0224 | 0.0288 | 0.0500 | S7_hard |
| 3 | promising_more | 218 | disjoint_blocks | 0.0138 | 0.0413 | 0.0550 | 0.0500 | S7_hard |
| 3 | promising_less | 218 | disjoint_blocks | 0.0138 | 0.0505 | 0.0642 | 0.0500 | S7_hard |
| 4 | fixed5 | 800 | disjoint_blocks | 0.0138 | 0.0338 | 0.0475 | 0.0500 | S7_hard |
| 4 | fixed20 | 300 | disjoint_blocks | 0.0133 | 0.0167 | 0.0300 | 0.0500 | S7_hard |
| 4 | promising_more | 211 | disjoint_blocks | 0.0142 | 0.0427 | 0.0569 | 0.0500 | S7_hard |
| 4 | promising_less | 211 | disjoint_blocks | 0.0142 | 0.0237 | 0.0379 | 0.0500 | S7_hard |
| 7 | fixed5 | 600 | disjoint_blocks | 0.0183 | 0.0367 | 0.0550 | 0.0500 | S7_hard |
| 7 | fixed20 | 266 | disjoint_blocks | 0.0075 | 0.0301 | 0.0376 | 0.0500 | S7_hard |
| 7 | promising_more | 194 | disjoint_blocks | 0.0052 | 0.0155 | 0.0206 | 0.0500 | S7_hard |
| 7 | promising_less | 194 | disjoint_blocks | 0.0052 | 0.0464 | 0.0515 | 0.0500 | S7_hard |
| 2 | fixed5 | 20000 | bootstrap_centred | 0.0090 | 0.0312 | 0.0403 | 0.0500 | S7_hard |
| 2 | fixed20 | 20000 | bootstrap_centred | 0.0089 | 0.0359 | 0.0448 | 0.0500 | S7_hard |
| 2 | promising_more | 20000 | bootstrap_centred | 0.0089 | 0.0340 | 0.0428 | 0.0500 | S7_hard |
| 2 | promising_less | 20000 | bootstrap_centred | 0.0089 | 0.0300 | 0.0389 | 0.0500 | S7_hard |
| 3 | fixed5 | 20000 | bootstrap_centred | 0.0086 | 0.0323 | 0.0410 | 0.0500 | S7_hard |
| 3 | fixed20 | 20000 | bootstrap_centred | 0.0078 | 0.0347 | 0.0425 | 0.0500 | S7_hard |
| 3 | promising_more | 20000 | bootstrap_centred | 0.0068 | 0.0351 | 0.0419 | 0.0500 | S7_hard |
| 3 | promising_less | 20000 | bootstrap_centred | 0.0075 | 0.0332 | 0.0407 | 0.0500 | S7_hard |
| 4 | fixed5 | 20000 | bootstrap_centred | 0.0073 | 0.0331 | 0.0403 | 0.0500 | S7_hard |
| 4 | fixed20 | 20000 | bootstrap_centred | 0.0073 | 0.0348 | 0.0422 | 0.0500 | S7_hard |
| 4 | promising_more | 20000 | bootstrap_centred | 0.0078 | 0.0349 | 0.0427 | 0.0500 | S7_hard |
| 4 | promising_less | 20000 | bootstrap_centred | 0.0077 | 0.0321 | 0.0399 | 0.0500 | S7_hard |
| 7 | fixed5 | 20000 | bootstrap_centred | 0.0066 | 0.0333 | 0.0399 | 0.0500 | S7_hard |
| 7 | fixed20 | 20000 | bootstrap_centred | 0.0067 | 0.0362 | 0.0428 | 0.0500 | S7_hard |
| 7 | promising_more | 20000 | bootstrap_centred | 0.0068 | 0.0350 | 0.0418 | 0.0500 | S7_hard |
| 7 | promising_less | 20000 | bootstrap_centred | 0.0070 | 0.0311 | 0.0381 | 0.0500 | S7_hard |

## Exact-null contrast distribution

| Unnamed: 0 | value | scenario |
|---|---|---|
| n | 7200.0000 | S7_hard |
| mean | 0.0000 | S7_hard |
| sd | 0.0106 | S7_hard |
| skew | 0.0512 | S7_hard |
| excess_kurtosis | 2.7478 | S7_hard |
| q01 | -0.0284 | S7_hard |
| q99 | 0.0280 | S7_hard |
