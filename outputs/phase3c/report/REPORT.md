# phase3c report (generated from outputs/phase3c/analysis)

delta = 0.005, alpha = 0.05, confirmatory b = 80 (block 0); reference = clusters >= 100.

## 1. Admissibility (label-free, before any fit)

### citeseer

| element | n_joint_strata | acceptance | mean_overlap | mean_pairwise_overlap | mean_gen_seconds | admissible_final |
|---|---|---|---|---|---|---|
| degree | 1 | 1.000 | 0.006 | 0.005 | 0.040 | True |
| strat:block | 8 | 1.000 | 0.151 | 0.100 | 0.011 | True |
| strat:clust | 3 | 1.000 | 0.031 | 0.015 | 0.013 | True |
| strat:fsim | 16 | 1.000 | 0.139 | 0.106 | 0.055 | True |
| strat:hop2 | 4 | 1.000 | 0.081 | 0.043 | 0.012 | True |
| strat:block+clust | 24 | 1.000 | 0.266 | 0.185 | 0.016 | True |
| strat:block+fsim | 118 | 1.000 | 0.326 | 0.295 | 0.106 | True |
| strat:block+hop2 | 32 | 1.000 | 0.193 | 0.155 | 0.020 | True |
| strat:clust+fsim | 48 | 1.000 | 0.331 | 0.313 | 0.240 | True |
| strat:clust+hop2 | 12 | 1.000 | 0.091 | 0.056 | 0.022 | True |
| strat:fsim+hop2 | 64 | 1.000 | 0.430 | 0.382 | 0.124 | True |
| er | 1 | 1.000 | 0.001 | 0.001 | 0.006 | True |

## 2. Matched baselines (reference clusters; test 1 − Brier/2 and accuracy)

| dataset | model | variant | metric | mean | se | n |
|---|---|---|---|---|---|---|
| citeseer | gcn | empty | test_score | 0.6901 | 0.0004 | 300 |
| citeseer | gcn | empty | test_acc | 0.5590 | 0.0010 | 300 |
| citeseer | gcn | real | test_score | 0.7600 | 0.0004 | 300 |
| citeseer | gcn | real | test_acc | 0.6894 | 0.0008 | 300 |
| citeseer | gcn | mlp | test_score | 0.6901 | 0.0004 | 300 |
| citeseer | gcn | mlp | test_acc | 0.5590 | 0.0010 | 300 |
| citeseer | sage | empty | test_score | 0.6905 | 0.0004 | 300 |
| citeseer | sage | empty | test_acc | 0.5595 | 0.0010 | 300 |
| citeseer | sage | real | test_score | 0.7600 | 0.0004 | 300 |
| citeseer | sage | real | test_acc | 0.6754 | 0.0008 | 300 |
| citeseer | sage | mlp | test_score | 0.6901 | 0.0004 | 300 |
| citeseer | sage | mlp | test_acc | 0.5590 | 0.0010 | 300 |

## 3. Frontiers

Reference = all clusters >= block (mean over draws), Holm at alpha; simultaneous (Bonferroni) 95% intervals. Confirmatory = block 0, uniform CRAF at b_conf (primary) and adaptive CRAF (secondary).

### citeseer / gcn

Reference:

| element | n | delta_hat | se | sim_lo | sim_hi | status | cert_min | possible_min | gap_set |
|---|---|---|---|---|---|---|---|---|---|
| degree | 300 | 0.1510 | 0.0004 | 0.1498 | 0.1522 | advantage | False | False |  |
| strat:block | 300 | 0.0904 | 0.0004 | 0.0892 | 0.0915 | advantage | False | False |  |
| strat:clust | 300 | 0.1484 | 0.0004 | 0.1473 | 0.1496 | advantage | False | False |  |
| strat:fsim | 300 | 0.0447 | 0.0004 | 0.0436 | 0.0458 | advantage | False | False |  |
| strat:hop2 | 300 | 0.1374 | 0.0004 | 0.1362 | 0.1385 | advantage | False | False |  |
| strat:block+clust | 300 | 0.0891 | 0.0004 | 0.0879 | 0.0903 | advantage | False | False |  |
| strat:block+fsim | 300 | 0.0269 | 0.0004 | 0.0259 | 0.0280 | advantage | False | False |  |
| strat:block+hop2 | 300 | 0.0871 | 0.0004 | 0.0860 | 0.0882 | advantage | False | False |  |
| strat:clust+fsim | 300 | 0.0358 | 0.0004 | 0.0348 | 0.0369 | advantage | False | False |  |
| strat:clust+hop2 | 300 | 0.1364 | 0.0004 | 0.1352 | 0.1375 | advantage | False | False |  |
| strat:fsim+hop2 | 300 | 0.0256 | 0.0003 | 0.0247 | 0.0265 | advantage | False | False |  |

Confirmatory (uniform CRAF, b = 80):

| element | delta_hat | sim_lo | sim_hi | p_adv | p_suf | status | cert_min | possible_min | min_among_cert | gap_set |
|---|---|---|---|---|---|---|---|---|---|---|
| degree | 0.1505 | 0.1481 | 0.1530 | 0.0000 | 1.0000 | advantage | False | False | False |  |
| strat:block | 0.0901 | 0.0880 | 0.0922 | 0.0000 | 1.0000 | advantage | False | False | False |  |
| strat:clust | 0.1470 | 0.1447 | 0.1493 | 0.0000 | 1.0000 | advantage | False | False | False |  |
| strat:fsim | 0.0452 | 0.0428 | 0.0476 | 0.0000 | 1.0000 | advantage | False | False | False |  |
| strat:hop2 | 0.1368 | 0.1342 | 0.1393 | 0.0000 | 1.0000 | advantage | False | False | False |  |
| strat:block+clust | 0.0896 | 0.0876 | 0.0917 | 0.0000 | 1.0000 | advantage | False | False | False |  |
| strat:block+fsim | 0.0268 | 0.0246 | 0.0291 | 0.0000 | 1.0000 | advantage | False | False | False |  |
| strat:block+hop2 | 0.0877 | 0.0854 | 0.0899 | 0.0000 | 1.0000 | advantage | False | False | False |  |
| strat:clust+fsim | 0.0369 | 0.0347 | 0.0391 | 0.0000 | 1.0000 | advantage | False | False | False |  |
| strat:clust+hop2 | 0.1358 | 0.1335 | 0.1382 | 0.0000 | 1.0000 | advantage | False | False | False |  |
| strat:fsim+hop2 | 0.0259 | 0.0235 | 0.0283 | 0.0000 | 1.0000 | advantage | False | False | False |  |

### citeseer / sage

Reference:

| element | n | delta_hat | se | sim_lo | sim_hi | status | cert_min | possible_min | gap_set |
|---|---|---|---|---|---|---|---|---|---|
| degree | 300 | 0.1109 | 0.0004 | 0.1098 | 0.1121 | advantage | False | False |  |
| strat:block | 300 | 0.0794 | 0.0004 | 0.0783 | 0.0805 | advantage | False | False |  |
| strat:clust | 300 | 0.1069 | 0.0004 | 0.1058 | 0.1080 | advantage | False | False |  |
| strat:fsim | 300 | 0.0457 | 0.0004 | 0.0447 | 0.0467 | advantage | False | False |  |
| strat:hop2 | 300 | 0.1009 | 0.0004 | 0.0998 | 0.1020 | advantage | False | False |  |
| strat:block+clust | 300 | 0.0748 | 0.0004 | 0.0737 | 0.0759 | advantage | False | False |  |
| strat:block+fsim | 300 | 0.0270 | 0.0003 | 0.0260 | 0.0279 | advantage | False | False |  |
| strat:block+hop2 | 300 | 0.0707 | 0.0004 | 0.0697 | 0.0718 | advantage | False | False |  |
| strat:clust+fsim | 300 | 0.0348 | 0.0003 | 0.0338 | 0.0358 | advantage | False | False |  |
| strat:clust+hop2 | 300 | 0.1004 | 0.0004 | 0.0992 | 0.1015 | advantage | False | False |  |
| strat:fsim+hop2 | 300 | 0.0245 | 0.0003 | 0.0236 | 0.0253 | advantage | False | False |  |

Confirmatory (uniform CRAF, b = 80):

| element | delta_hat | sim_lo | sim_hi | p_adv | p_suf | status | cert_min | possible_min | min_among_cert | gap_set |
|---|---|---|---|---|---|---|---|---|---|---|
| degree | 0.1112 | 0.1086 | 0.1138 | 0.0000 | 1.0000 | advantage | False | False | False |  |
| strat:block | 0.0790 | 0.0765 | 0.0815 | 0.0000 | 1.0000 | advantage | False | False | False |  |
| strat:clust | 0.1075 | 0.1051 | 0.1100 | 0.0000 | 1.0000 | advantage | False | False | False |  |
| strat:fsim | 0.0470 | 0.0443 | 0.0496 | 0.0000 | 1.0000 | advantage | False | False | False |  |
| strat:hop2 | 0.1011 | 0.0986 | 0.1037 | 0.0000 | 1.0000 | advantage | False | False | False |  |
| strat:block+clust | 0.0759 | 0.0735 | 0.0784 | 0.0000 | 1.0000 | advantage | False | False | False |  |
| strat:block+fsim | 0.0276 | 0.0251 | 0.0302 | 0.0000 | 1.0000 | advantage | False | False | False |  |
| strat:block+hop2 | 0.0717 | 0.0693 | 0.0740 | 0.0000 | 1.0000 | advantage | False | False | False |  |
| strat:clust+fsim | 0.0354 | 0.0333 | 0.0375 | 0.0000 | 1.0000 | advantage | False | False | False |  |
| strat:clust+hop2 | 0.1000 | 0.0972 | 0.1028 | 0.0000 | 1.0000 | advantage | False | False | False |  |
| strat:fsim+hop2 | 0.0254 | 0.0231 | 0.0277 | 0.0000 | 1.0000 | advantage | False | False | False |  |

### Frontier summary

| dataset | model | run | cert_min | possible_min | n_advantage | n_sufficient | n_inconclusive | specificity_over_L | min_among_cert | gaps |
|---|---|---|---|---|---|---|---|---|---|---|
| citeseer | gcn | reference | {} | {} | 11 | 0 | 0 | True | {} |  |
| citeseer | gcn | confirm craf | {} | {} | 11 | 0 | 0 | True | {} |  |
| citeseer | gcn | confirm craf_adaptive | {} | {} | 11 | 0 | 0 | True | {} |  |
| citeseer | sage | reference | {} | {} | 11 | 0 | 0 | True | {} |  |
| citeseer | sage | confirm craf | {} | {} | 11 | 0 | 0 | True | {} |  |
| citeseer | sage | confirm craf_adaptive | {} | {} | 11 | 0 | 0 | True | {} |  |

![frontiers](frontiers.png)

## 4. Confirmatory block: what each procedure reports (same data, same budget)

| dataset | model | procedure | reported | fits | n_A | n_C | n_inconclusive |
|---|---|---|---|---|---|---|---|
| citeseer | gcn | craf | {} | 960 | 11 | 0 | 0 |
| citeseer | gcn | craf_children | {} | 960 | 11 | 0 | 0 |
| citeseer | gcn | factorial_unadj | {} | 960 | 11 | 0 | 0 |
| citeseer | gcn | ni_holm | {} | 960 | 0 | 0 | 11 |
| citeseer | gcn | naive_point | {} | 960 |  |  |  |
| citeseer | gcn | craf_adaptive | {} | 556 | 11 | 0 | 0 |
| citeseer | gcn | pcga_l | {} | 500 |  |  |  |
| citeseer | sage | craf | {} | 960 | 11 | 0 | 0 |
| citeseer | sage | craf_children | {} | 960 | 11 | 0 | 0 |
| citeseer | sage | factorial_unadj | {} | 960 | 11 | 0 | 0 |
| citeseer | sage | ni_holm | {} | 960 | 0 | 0 | 11 |
| citeseer | sage | naive_point | {} | 960 |  |  |  |
| citeseer | sage | craf_adaptive | {} | 560 | 11 | 0 | 0 |
| citeseer | sage | pcga_l | {} | 500 |  |  |  |

## 5. Resampling comparison (disjoint reference blocks; leave-block-out reference truth)

| dataset | model | b | procedure | n_exp | exact | false_member | false_member_hi | class_error | class_error_hi | covered | n_inconclusive | unc_size | mean_fits | modal_report |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| citeseer | gcn | 20 | craf | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 | 1.000 | 0.000 | 0.000 | 240.000 | {} |
| citeseer | gcn | 20 | craf_adaptive | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 | 1.000 | 0.000 | 0.000 | 239.667 | {} |
| citeseer | gcn | 20 | craf_children | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 |  | 0.000 |  | 240.000 | {} |
| citeseer | gcn | 20 | ni_holm | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 |  | 11.000 |  | 240.000 | {} |
| citeseer | gcn | 20 | factorial_unadj | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 |  | 0.000 |  | 240.000 | {} |
| citeseer | gcn | 20 | naive_point | 3 | 1.000 | 0.000 | 0.561 |  |  |  |  |  | 240.000 | {} |
| citeseer | gcn | 20 | pcga_l | 3 | 1.000 | 0.000 | 0.561 |  |  |  |  |  | 240.000 | {} |
| citeseer | gcn | 40 | craf | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 | 1.000 | 0.000 | 0.000 | 480.000 | {} |
| citeseer | gcn | 40 | craf_adaptive | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 | 1.000 | 0.000 | 0.000 | 413.333 | {} |
| citeseer | gcn | 40 | craf_children | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 |  | 0.000 |  | 480.000 | {} |
| citeseer | gcn | 40 | ni_holm | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 |  | 11.000 |  | 480.000 | {} |
| citeseer | gcn | 40 | factorial_unadj | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 |  | 0.000 |  | 480.000 | {} |
| citeseer | gcn | 40 | naive_point | 3 | 1.000 | 0.000 | 0.561 |  |  |  |  |  | 480.000 | {} |
| citeseer | gcn | 40 | pcga_l | 3 | 1.000 | 0.000 | 0.561 |  |  |  |  |  | 480.000 | {} |
| citeseer | gcn | 80 | craf | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 | 1.000 | 0.000 | 0.000 | 960.000 | {} |
| citeseer | gcn | 80 | craf_adaptive | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 | 1.000 | 0.000 | 0.000 | 550.667 | {} |
| citeseer | gcn | 80 | craf_children | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 |  | 0.000 |  | 960.000 | {} |
| citeseer | gcn | 80 | ni_holm | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 |  | 11.000 |  | 960.000 | {} |
| citeseer | gcn | 80 | factorial_unadj | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 |  | 0.000 |  | 960.000 | {} |
| citeseer | gcn | 80 | naive_point | 3 | 1.000 | 0.000 | 0.561 |  |  |  |  |  | 960.000 | {} |
| citeseer | gcn | 80 | pcga_l | 3 | 1.000 | 0.000 | 0.561 |  |  |  |  |  | 500.000 | {} |
| citeseer | sage | 20 | craf | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 | 1.000 | 0.000 | 0.000 | 240.000 | {} |
| citeseer | sage | 20 | craf_adaptive | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 | 1.000 | 0.000 | 0.000 | 239.667 | {} |
| citeseer | sage | 20 | craf_children | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 |  | 0.000 |  | 240.000 | {} |
| citeseer | sage | 20 | ni_holm | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 |  | 11.000 |  | 240.000 | {} |
| citeseer | sage | 20 | factorial_unadj | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 |  | 0.000 |  | 240.000 | {} |
| citeseer | sage | 20 | naive_point | 3 | 1.000 | 0.000 | 0.561 |  |  |  |  |  | 240.000 | {} |
| citeseer | sage | 20 | pcga_l | 3 | 1.000 | 0.000 | 0.561 |  |  |  |  |  | 240.000 | {} |
| citeseer | sage | 40 | craf | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 | 1.000 | 0.000 | 0.000 | 480.000 | {} |
| citeseer | sage | 40 | craf_adaptive | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 | 1.000 | 0.000 | 0.000 | 404.333 | {} |
| citeseer | sage | 40 | craf_children | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 |  | 0.000 |  | 480.000 | {} |
| citeseer | sage | 40 | ni_holm | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 |  | 11.000 |  | 480.000 | {} |
| citeseer | sage | 40 | factorial_unadj | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 |  | 0.000 |  | 480.000 | {} |
| citeseer | sage | 40 | naive_point | 3 | 1.000 | 0.000 | 0.561 |  |  |  |  |  | 480.000 | {} |
| citeseer | sage | 40 | pcga_l | 3 | 1.000 | 0.000 | 0.561 |  |  |  |  |  | 480.000 | {} |
| citeseer | sage | 80 | craf | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 | 1.000 | 0.000 | 0.000 | 960.000 | {} |
| citeseer | sage | 80 | craf_adaptive | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 | 1.000 | 0.000 | 0.000 | 544.000 | {} |
| citeseer | sage | 80 | craf_children | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 |  | 0.000 |  | 960.000 | {} |
| citeseer | sage | 80 | ni_holm | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 |  | 11.000 |  | 960.000 | {} |
| citeseer | sage | 80 | factorial_unadj | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 |  | 0.000 |  | 960.000 | {} |
| citeseer | sage | 80 | naive_point | 3 | 1.000 | 0.000 | 0.561 |  |  |  |  |  | 960.000 | {} |
| citeseer | sage | 80 | pcga_l | 3 | 1.000 | 0.000 | 0.561 |  |  |  |  |  | 500.000 | {} |

Paired differences (experiment-paired; normal 95% CI):

| dataset | model | b | a | b_proc | metric | diff | ci_lo | ci_hi | n_exp |
|---|---|---|---|---|---|---|---|---|---|
| citeseer | gcn | 20 | craf_adaptive | craf | exact | 0.000 | 0.000 | 0.000 | 3 |
| citeseer | gcn | 40 | craf_adaptive | craf | exact | 0.000 | 0.000 | 0.000 | 3 |
| citeseer | gcn | 80 | craf_adaptive | craf | exact | 0.000 | 0.000 | 0.000 | 3 |
| citeseer | sage | 20 | craf_adaptive | craf | exact | 0.000 | 0.000 | 0.000 | 3 |
| citeseer | sage | 40 | craf_adaptive | craf | exact | 0.000 | 0.000 | 0.000 | 3 |
| citeseer | sage | 80 | craf_adaptive | craf | exact | 0.000 | 0.000 | 0.000 | 3 |
| citeseer | gcn | 20 | craf_adaptive | craf | n_inconclusive | 0.000 | 0.000 | 0.000 | 3 |
| citeseer | gcn | 40 | craf_adaptive | craf | n_inconclusive | 0.000 | 0.000 | 0.000 | 3 |
| citeseer | gcn | 80 | craf_adaptive | craf | n_inconclusive | 0.000 | 0.000 | 0.000 | 3 |
| citeseer | sage | 20 | craf_adaptive | craf | n_inconclusive | 0.000 | 0.000 | 0.000 | 3 |
| citeseer | sage | 40 | craf_adaptive | craf | n_inconclusive | 0.000 | 0.000 | 0.000 | 3 |
| citeseer | sage | 80 | craf_adaptive | craf | n_inconclusive | 0.000 | 0.000 | 0.000 | 3 |
| citeseer | gcn | 20 | craf | ni_holm | false_member | 0.000 | 0.000 | 0.000 | 3 |
| citeseer | gcn | 40 | craf | ni_holm | false_member | 0.000 | 0.000 | 0.000 | 3 |
| citeseer | gcn | 80 | craf | ni_holm | false_member | 0.000 | 0.000 | 0.000 | 3 |
| citeseer | sage | 20 | craf | ni_holm | false_member | 0.000 | 0.000 | 0.000 | 3 |
| citeseer | sage | 40 | craf | ni_holm | false_member | 0.000 | 0.000 | 0.000 | 3 |
| citeseer | sage | 80 | craf | ni_holm | false_member | 0.000 | 0.000 | 0.000 | 3 |
| citeseer | gcn | 20 | craf | craf_children | false_member | 0.000 | 0.000 | 0.000 | 3 |
| citeseer | gcn | 40 | craf | craf_children | false_member | 0.000 | 0.000 | 0.000 | 3 |
| citeseer | gcn | 80 | craf | craf_children | false_member | 0.000 | 0.000 | 0.000 | 3 |
| citeseer | sage | 20 | craf | craf_children | false_member | 0.000 | 0.000 | 0.000 | 3 |
| citeseer | sage | 40 | craf | craf_children | false_member | 0.000 | 0.000 | 0.000 | 3 |
| citeseer | sage | 80 | craf | craf_children | false_member | 0.000 | 0.000 | 0.000 | 3 |
| citeseer | gcn | 20 | craf | naive_point | false_member | 0.000 | 0.000 | 0.000 | 3 |
| citeseer | gcn | 40 | craf | naive_point | false_member | 0.000 | 0.000 | 0.000 | 3 |
| citeseer | gcn | 80 | craf | naive_point | false_member | 0.000 | 0.000 | 0.000 | 3 |
| citeseer | sage | 20 | craf | naive_point | false_member | 0.000 | 0.000 | 0.000 | 3 |
| citeseer | sage | 40 | craf | naive_point | false_member | 0.000 | 0.000 | 0.000 | 3 |
| citeseer | sage | 80 | craf | naive_point | false_member | 0.000 | 0.000 | 0.000 | 3 |
| citeseer | gcn | 20 | craf | naive_point | exact | 0.000 | 0.000 | 0.000 | 3 |
| citeseer | gcn | 40 | craf | naive_point | exact | 0.000 | 0.000 | 0.000 | 3 |
| citeseer | gcn | 80 | craf | naive_point | exact | 0.000 | 0.000 | 0.000 | 3 |
| citeseer | sage | 20 | craf | naive_point | exact | 0.000 | 0.000 | 0.000 | 3 |
| citeseer | sage | 40 | craf | naive_point | exact | 0.000 | 0.000 | 0.000 | 3 |
| citeseer | sage | 80 | craf | naive_point | exact | 0.000 | 0.000 | 0.000 | 3 |

## 6. RUSA full-set claim (exhaustive IUT vs fullset_adaptive_fb; PCGA-L edge step for reference)

| dataset | model | b | procedure | n_exp | claim | false_vs_full | theta_full | fits | fallback |
|---|---|---|---|---|---|---|---|---|---|
| citeseer | gcn | 6 | exhaustive_iut | 3 | 1.000 | 0.000 | 0.026 | 84.000 |  |
| citeseer | gcn | 6 | fullset_adaptive_fb | 3 | 1.000 | 0.000 | 0.026 | 84.000 | 1.000 |
| citeseer | gcn | 6 | pcga_l | 3 | 1.000 | 0.000 | 0.026 | 80.000 |  |
| citeseer | gcn | 12 | exhaustive_iut | 3 | 1.000 | 0.000 | 0.026 | 168.000 |  |
| citeseer | gcn | 12 | fullset_adaptive_fb | 3 | 1.000 | 0.000 | 0.026 | 93.333 | 0.000 |
| citeseer | gcn | 12 | pcga_l | 3 | 1.000 | 0.000 | 0.026 | 165.000 |  |
| citeseer | gcn | 24 | exhaustive_iut | 3 | 1.000 | 0.000 | 0.026 | 336.000 |  |
| citeseer | gcn | 24 | fullset_adaptive_fb | 3 | 1.000 | 0.000 | 0.026 | 112.000 | 0.000 |
| citeseer | gcn | 24 | pcga_l | 3 | 1.000 | 0.000 | 0.026 | 335.000 |  |
| citeseer | sage | 6 | exhaustive_iut | 3 | 1.000 | 0.000 | 0.024 | 84.000 |  |
| citeseer | sage | 6 | fullset_adaptive_fb | 3 | 1.000 | 0.000 | 0.024 | 84.000 | 1.000 |
| citeseer | sage | 6 | pcga_l | 3 | 1.000 | 0.000 | 0.024 | 80.000 |  |
| citeseer | sage | 12 | exhaustive_iut | 3 | 1.000 | 0.000 | 0.024 | 168.000 |  |
| citeseer | sage | 12 | fullset_adaptive_fb | 3 | 1.000 | 0.000 | 0.024 | 93.333 | 0.000 |
| citeseer | sage | 12 | pcga_l | 3 | 1.000 | 0.000 | 0.024 | 165.000 |  |
| citeseer | sage | 24 | exhaustive_iut | 3 | 1.000 | 0.000 | 0.024 | 336.000 |  |
| citeseer | sage | 24 | fullset_adaptive_fb | 3 | 1.000 | 0.000 | 0.024 | 112.000 | 0.000 |
| citeseer | sage | 24 | pcga_l | 3 | 1.000 | 0.000 | 0.024 | 335.000 |  |

Confirmatory block:

| dataset | model | b | procedure | claim | L | theta_hat | fits |
|---|---|---|---|---|---|---|---|
| citeseer | gcn | 6 | pcga_l | True |  | 0.0898 | 80 |
| citeseer | gcn | 6 | exhaustive_iut | True | 0.0158 | 0.0214 | 84 |
| citeseer | gcn | 6 | fullset_adaptive_fb | True | 0.0158 | 0.0214 | 84 |
| citeseer | gcn | 12 | pcga_l | True |  | 0.0894 | 165 |
| citeseer | gcn | 12 | exhaustive_iut | True | 0.0196 | 0.0231 | 168 |
| citeseer | gcn | 12 | fullset_adaptive_fb | True | 0.0135 | 0.0243 | 56 |
| citeseer | gcn | 24 | pcga_l | True |  | 0.0901 | 335 |
| citeseer | gcn | 24 | exhaustive_iut | True | 0.0225 | 0.0255 | 336 |
| citeseer | gcn | 24 | fullset_adaptive_fb | True | 0.0171 | 0.0222 | 112 |
| citeseer | sage | 6 | pcga_l | True |  | 0.0806 | 80 |
| citeseer | sage | 6 | exhaustive_iut | True | 0.0169 | 0.0243 | 84 |
| citeseer | sage | 6 | fullset_adaptive_fb | True | 0.0169 | 0.0243 | 84 |
| citeseer | sage | 12 | pcga_l | True |  | 0.0791 | 165 |
| citeseer | sage | 12 | exhaustive_iut | True | 0.0199 | 0.0242 | 168 |
| citeseer | sage | 12 | fullset_adaptive_fb | True | 0.0073 | 0.0207 | 56 |
| citeseer | sage | 24 | pcga_l | True |  | 0.0790 | 335 |
| citeseer | sage | 24 | exhaustive_iut | True | 0.0226 | 0.0252 | 336 |
| citeseer | sage | 24 | fullset_adaptive_fb | True | 0.0157 | 0.0229 | 112 |

| dataset | model | b | diff_claim(fb − exhaustive) | ci_lo | ci_hi | n_exp |
|---|---|---|---|---|---|---|
| citeseer | gcn | 6 | 0.000 | 0.000 | 0.000 | 3 |
| citeseer | gcn | 12 | 0.000 | 0.000 | 0.000 | 3 |
| citeseer | gcn | 24 | 0.000 | 0.000 | 0.000 | 3 |
| citeseer | sage | 6 | 0.000 | 0.000 | 0.000 | 3 |
| citeseer | sage | 12 | 0.000 | 0.000 | 0.000 | 3 |
| citeseer | sage | 24 | 0.000 | 0.000 | 0.000 | 3 |

## 7. Calibration on fresh clusters (exact A/A contrasts; centred real contrasts secondary)

Marginal one-sided t size (pooled over elements):

| dataset | model | n | direction | alpha | tests | size | wilson_lo | wilson_hi | flag |
|---|---|---|---|---|---|---|---|---|---|
| citeseer | gcn | 5 | adv | 0.0023 | 660 | 0.0015 | 0.0003 | 0.0085 | False |
| citeseer | gcn | 5 | adv | 0.0100 | 660 | 0.0106 | 0.0051 | 0.0217 | False |
| citeseer | gcn | 5 | adv | 0.0500 | 660 | 0.0561 | 0.0409 | 0.0763 | False |
| citeseer | gcn | 5 | suf | 0.0023 | 660 | 0.0015 | 0.0003 | 0.0085 | False |
| citeseer | gcn | 5 | suf | 0.0100 | 660 | 0.0061 | 0.0024 | 0.0155 | False |
| citeseer | gcn | 5 | suf | 0.0500 | 660 | 0.0515 | 0.0371 | 0.0711 | False |
| citeseer | gcn | 10 | adv | 0.0023 | 330 | 0.0030 | 0.0005 | 0.0170 | False |
| citeseer | gcn | 10 | adv | 0.0100 | 330 | 0.0152 | 0.0065 | 0.0350 | False |
| citeseer | gcn | 10 | adv | 0.0500 | 330 | 0.0576 | 0.0372 | 0.0882 | False |
| citeseer | gcn | 10 | suf | 0.0023 | 330 | 0.0000 | 0.0000 | 0.0115 | False |
| citeseer | gcn | 10 | suf | 0.0100 | 330 | 0.0091 | 0.0031 | 0.0264 | False |
| citeseer | gcn | 10 | suf | 0.0500 | 330 | 0.0455 | 0.0277 | 0.0736 | False |
| citeseer | gcn | 20 | adv | 0.0023 | 165 | 0.0121 | 0.0033 | 0.0431 | True |
| citeseer | gcn | 20 | adv | 0.0100 | 165 | 0.0182 | 0.0062 | 0.0521 | False |
| citeseer | gcn | 20 | adv | 0.0500 | 165 | 0.0485 | 0.0248 | 0.0927 | False |
| citeseer | gcn | 20 | suf | 0.0023 | 165 | 0.0000 | 0.0000 | 0.0228 | False |
| citeseer | gcn | 20 | suf | 0.0100 | 165 | 0.0000 | 0.0000 | 0.0228 | False |
| citeseer | gcn | 20 | suf | 0.0500 | 165 | 0.0545 | 0.0290 | 0.1004 | False |
| citeseer | gcn | 40 | adv | 0.0023 | 77 | 0.0130 | 0.0023 | 0.0700 | True |
| citeseer | gcn | 40 | adv | 0.0100 | 77 | 0.0260 | 0.0072 | 0.0898 | False |
| citeseer | gcn | 40 | adv | 0.0500 | 77 | 0.0519 | 0.0204 | 0.1261 | False |
| citeseer | gcn | 40 | suf | 0.0023 | 77 | 0.0000 | 0.0000 | 0.0475 | False |
| citeseer | gcn | 40 | suf | 0.0100 | 77 | 0.0000 | 0.0000 | 0.0475 | False |
| citeseer | gcn | 40 | suf | 0.0500 | 77 | 0.0519 | 0.0204 | 0.1261 | False |
| citeseer | gcn | 80 | adv | 0.0023 | 33 | 0.0000 | 0.0000 | 0.1043 | False |
| citeseer | gcn | 80 | adv | 0.0100 | 33 | 0.0303 | 0.0054 | 0.1532 | False |
| citeseer | gcn | 80 | adv | 0.0500 | 33 | 0.0909 | 0.0314 | 0.2357 | False |
| citeseer | gcn | 80 | suf | 0.0023 | 33 | 0.0000 | 0.0000 | 0.1043 | False |
| citeseer | gcn | 80 | suf | 0.0100 | 33 | 0.0000 | 0.0000 | 0.1043 | False |
| citeseer | gcn | 80 | suf | 0.0500 | 33 | 0.0303 | 0.0054 | 0.1532 | False |
| citeseer | sage | 5 | adv | 0.0023 | 660 | 0.0030 | 0.0008 | 0.0110 | False |
| citeseer | sage | 5 | adv | 0.0100 | 660 | 0.0106 | 0.0051 | 0.0217 | False |
| citeseer | sage | 5 | adv | 0.0500 | 660 | 0.0485 | 0.0346 | 0.0676 | False |
| citeseer | sage | 5 | suf | 0.0023 | 660 | 0.0076 | 0.0032 | 0.0176 | True |
| citeseer | sage | 5 | suf | 0.0100 | 660 | 0.0167 | 0.0093 | 0.0296 | False |
| citeseer | sage | 5 | suf | 0.0500 | 660 | 0.0576 | 0.0422 | 0.0780 | False |
| citeseer | sage | 10 | adv | 0.0023 | 330 | 0.0030 | 0.0005 | 0.0170 | False |
| citeseer | sage | 10 | adv | 0.0100 | 330 | 0.0242 | 0.0123 | 0.0471 | True |
| citeseer | sage | 10 | adv | 0.0500 | 330 | 0.0697 | 0.0469 | 0.1024 | False |
| citeseer | sage | 10 | suf | 0.0023 | 330 | 0.0030 | 0.0005 | 0.0170 | False |
| citeseer | sage | 10 | suf | 0.0100 | 330 | 0.0121 | 0.0047 | 0.0307 | False |
| citeseer | sage | 10 | suf | 0.0500 | 330 | 0.0545 | 0.0348 | 0.0846 | False |
| citeseer | sage | 20 | adv | 0.0023 | 165 | 0.0182 | 0.0062 | 0.0521 | True |
| citeseer | sage | 20 | adv | 0.0100 | 165 | 0.0424 | 0.0207 | 0.0850 | True |
| citeseer | sage | 20 | adv | 0.0500 | 165 | 0.0848 | 0.0512 | 0.1374 | True |
| citeseer | sage | 20 | suf | 0.0023 | 165 | 0.0000 | 0.0000 | 0.0228 | False |
| citeseer | sage | 20 | suf | 0.0100 | 165 | 0.0061 | 0.0011 | 0.0335 | False |
| citeseer | sage | 20 | suf | 0.0500 | 165 | 0.0606 | 0.0332 | 0.1080 | False |
| citeseer | sage | 40 | adv | 0.0023 | 77 | 0.0390 | 0.0133 | 0.1084 | True |
| citeseer | sage | 40 | adv | 0.0100 | 77 | 0.0390 | 0.0133 | 0.1084 | True |
| citeseer | sage | 40 | adv | 0.0500 | 77 | 0.1039 | 0.0536 | 0.1918 | True |
| citeseer | sage | 40 | suf | 0.0023 | 77 | 0.0000 | 0.0000 | 0.0475 | False |
| citeseer | sage | 40 | suf | 0.0100 | 77 | 0.0130 | 0.0023 | 0.0700 | False |
| citeseer | sage | 40 | suf | 0.0500 | 77 | 0.0649 | 0.0281 | 0.1432 | False |
| citeseer | sage | 80 | adv | 0.0023 | 33 | 0.0000 | 0.0000 | 0.1043 | False |
| citeseer | sage | 80 | adv | 0.0100 | 33 | 0.0000 | 0.0000 | 0.1043 | False |
| citeseer | sage | 80 | adv | 0.0500 | 33 | 0.0909 | 0.0314 | 0.2357 | False |
| citeseer | sage | 80 | suf | 0.0023 | 33 | 0.0000 | 0.0000 | 0.1043 | False |
| citeseer | sage | 80 | suf | 0.0100 | 33 | 0.0000 | 0.0000 | 0.1043 | False |
| citeseer | sage | 80 | suf | 0.0500 | 33 | 0.0000 | 0.0000 | 0.1043 | False |

Worst-case FWER of certifications (all elements at Delta = delta):

| dataset | model | procedure | n_or_b | scheme | source | groups | fwer | false_adv | false_suf | wilson_lo | wilson_hi | flag |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| citeseer | gcn | craf | 20 | disjoint | aa | 15 | 0.133 | 0.133 | 0.000 | 0.037 | 0.379 | False |
| citeseer | gcn | craf | 40 | disjoint | aa | 7 | 0.143 | 0.143 | 0.000 | 0.026 | 0.513 | False |
| citeseer | gcn | craf | 80 | disjoint | aa | 3 | 0.000 | 0.000 | 0.000 | 0.000 | 0.561 | False |
| citeseer | gcn | craf_adaptive | 20 | disjoint | aa | 3 | 0.000 | 0.000 | 0.000 | 0.000 | 0.561 | False |
| citeseer | gcn | craf_adaptive | 20 | bootstrap | aa | 2000 | 0.045 | 0.025 | 0.019 | 0.037 | 0.055 | False |
| citeseer | gcn | craf_adaptive | 40 | disjoint | aa | 3 | 0.000 | 0.000 | 0.000 | 0.000 | 0.561 | False |
| citeseer | gcn | craf_adaptive | 40 | bootstrap | aa | 2000 | 0.041 | 0.022 | 0.019 | 0.033 | 0.051 | False |
| citeseer | gcn | craf_adaptive | 80 | disjoint | aa | 3 | 0.000 | 0.000 | 0.000 | 0.000 | 0.561 | False |
| citeseer | gcn | craf_adaptive | 80 | bootstrap | aa | 2000 | 0.044 | 0.025 | 0.020 | 0.036 | 0.054 | False |
| citeseer | gcn | craf | 20 | disjoint | centred | 15 | 0.000 | 0.000 | 0.000 | 0.000 | 0.204 | False |
| citeseer | gcn | craf | 40 | disjoint | centred | 7 | 0.000 | 0.000 | 0.000 | 0.000 | 0.354 | False |
| citeseer | gcn | craf | 80 | disjoint | centred | 3 | 0.000 | 0.000 | 0.000 | 0.000 | 0.561 | False |
| citeseer | gcn | craf_adaptive | 20 | disjoint | centred | 3 | 0.000 | 0.000 | 0.000 | 0.000 | 0.561 | False |
| citeseer | gcn | craf_adaptive | 40 | disjoint | centred | 3 | 0.000 | 0.000 | 0.000 | 0.000 | 0.561 | False |
| citeseer | gcn | craf_adaptive | 80 | disjoint | centred | 3 | 0.000 | 0.000 | 0.000 | 0.000 | 0.561 | False |
| citeseer | sage | craf | 20 | disjoint | aa | 15 | 0.200 | 0.200 | 0.000 | 0.070 | 0.452 | True |
| citeseer | sage | craf | 40 | disjoint | aa | 7 | 0.429 | 0.429 | 0.000 | 0.158 | 0.750 | True |
| citeseer | sage | craf | 80 | disjoint | aa | 3 | 0.000 | 0.000 | 0.000 | 0.000 | 0.561 | False |
| citeseer | sage | craf_adaptive | 20 | disjoint | aa | 3 | 0.000 | 0.000 | 0.000 | 0.000 | 0.561 | False |
| citeseer | sage | craf_adaptive | 20 | bootstrap | aa | 2000 | 0.057 | 0.031 | 0.027 | 0.048 | 0.068 | False |
| citeseer | sage | craf_adaptive | 40 | disjoint | aa | 3 | 0.000 | 0.000 | 0.000 | 0.000 | 0.561 | False |
| citeseer | sage | craf_adaptive | 40 | bootstrap | aa | 2000 | 0.046 | 0.028 | 0.020 | 0.038 | 0.056 | False |
| citeseer | sage | craf_adaptive | 80 | disjoint | aa | 3 | 0.000 | 0.000 | 0.000 | 0.000 | 0.561 | False |
| citeseer | sage | craf_adaptive | 80 | bootstrap | aa | 2000 | 0.038 | 0.020 | 0.018 | 0.031 | 0.048 | False |
| citeseer | sage | craf | 20 | disjoint | centred | 15 | 0.000 | 0.000 | 0.000 | 0.000 | 0.204 | False |
| citeseer | sage | craf | 40 | disjoint | centred | 7 | 0.000 | 0.000 | 0.000 | 0.000 | 0.354 | False |
| citeseer | sage | craf | 80 | disjoint | centred | 3 | 0.000 | 0.000 | 0.000 | 0.000 | 0.561 | False |
| citeseer | sage | craf_adaptive | 20 | disjoint | centred | 3 | 0.000 | 0.000 | 0.000 | 0.000 | 0.561 | False |
| citeseer | sage | craf_adaptive | 40 | disjoint | centred | 3 | 0.000 | 0.000 | 0.000 | 0.000 | 0.561 | False |
| citeseer | sage | craf_adaptive | 80 | disjoint | centred | 3 | 0.000 | 0.000 | 0.000 | 0.000 | 0.561 | False |

## 8. Natural structure (reference clusters)

Certified non-monotone pairs (Delta_T > Delta_S for S ⊊ T; Holm over pairs): 0; with margin delta: 0.

Largest estimated violations of monotonicity per cell:

| dataset | model | S | T | diff | se | p_nonmono_holm |
|---|---|---|---|---|---|---|
| citeseer | sage | strat:hop2 | strat:clust+hop2 | -0.0005 | 0.0002 | 1.0000 |
| citeseer | gcn | strat:hop2 | strat:clust+hop2 | -0.0010 | 0.0002 | 1.0000 |
| citeseer | gcn | strat:block | strat:block+clust | -0.0012 | 0.0003 | 1.0000 |
| citeseer | gcn | degree | strat:clust | -0.0026 | 0.0002 | 1.0000 |
| citeseer | sage | degree | strat:clust | -0.0041 | 0.0002 | 1.0000 |
| citeseer | sage | strat:block | strat:block+clust | -0.0046 | 0.0002 | 1.0000 |

Pairwise interactions I_ab = Delta_∅ − Delta_a − Delta_b + Delta_ab (two-sided, Holm):

| dataset | model | element | interaction | se | p_holm | significant |
|---|---|---|---|---|---|---|
| citeseer | gcn | strat:block+clust | 0.0013 | 0.0003 | 0.0001 | True |
| citeseer | gcn | strat:block+fsim | 0.0429 | 0.0004 | 0.0000 | True |
| citeseer | gcn | strat:block+hop2 | 0.0103 | 0.0003 | 0.0000 | True |
| citeseer | gcn | strat:clust+fsim | -0.0063 | 0.0003 | 0.0000 | True |
| citeseer | gcn | strat:clust+hop2 | 0.0016 | 0.0003 | 0.0000 | True |
| citeseer | gcn | strat:fsim+hop2 | -0.0055 | 0.0004 | 0.0000 | True |
| citeseer | sage | strat:block+clust | -0.0005 | 0.0003 | 0.1194 | False |
| citeseer | sage | strat:block+fsim | 0.0128 | 0.0004 | 0.0000 | True |
| citeseer | sage | strat:block+hop2 | 0.0014 | 0.0003 | 0.0001 | True |
| citeseer | sage | strat:clust+fsim | -0.0068 | 0.0004 | 0.0000 | True |
| citeseer | sage | strat:clust+hop2 | 0.0036 | 0.0003 | 0.0000 | True |
| citeseer | sage | strat:fsim+hop2 | -0.0112 | 0.0004 | 0.0000 | True |

Architecture differences Delta^gcn − Delta^sage (paired; Holm):

| dataset | element | diff | se | p_holm | significant |
|---|---|---|---|---|---|
| citeseer | empty | 0.0004 | 0.0003 | 0.5854 | False |
| citeseer | degree | 0.0400 | 0.0004 | 0.0000 | True |
| citeseer | strat:block | 0.0110 | 0.0003 | 0.0000 | True |
| citeseer | strat:clust | 0.0416 | 0.0004 | 0.0000 | True |
| citeseer | strat:fsim | -0.0010 | 0.0003 | 0.0057 | True |
| citeseer | strat:hop2 | 0.0364 | 0.0004 | 0.0000 | True |
| citeseer | strat:block+clust | 0.0143 | 0.0003 | 0.0000 | True |
| citeseer | strat:block+fsim | -0.0000 | 0.0003 | 0.9290 | False |
| citeseer | strat:block+hop2 | 0.0163 | 0.0003 | 0.0000 | True |
| citeseer | strat:clust+fsim | 0.0010 | 0.0003 | 0.0056 | True |
| citeseer | strat:clust+hop2 | 0.0360 | 0.0004 | 0.0000 | True |
| citeseer | strat:fsim+hop2 | 0.0011 | 0.0003 | 0.0009 | True |

Attribute–label association, citeseer (descriptive, post hoc; never used upstream):

| attribute | nmi_with_labels | edge_homophily_attr |
|---|---|---|
| block | 0.210 | 0.941 |
| fsim | 0.205 | 0.308 |
| clust | 0.010 | 0.594 |
| hop2 | 0.038 | 0.675 |
| LABEL (reference) | 1.000 | 0.738 |

## 9. Computational cost (CPU seconds per fit / per null draw, single thread)

| variant | fit_seconds | gen_seconds | n_rows | valid_rate | dataset | model |
|---|---|---|---|---|---|---|
| degree | 6.534 | 0.078 | 800.000 | 1.000 | citeseer | gcn |
| empty | 7.975 | 0.000 | 400.000 | 1.000 | citeseer | gcn |
| er | 6.092 | 0.003 | 400.000 | 1.000 | citeseer | gcn |
| real | 9.051 | 0.000 | 400.000 | 1.000 | citeseer | gcn |
| strat:block | 7.631 | 0.009 | 800.000 | 1.000 | citeseer | gcn |
| strat:block+clust | 7.514 | 0.013 | 800.000 | 1.000 | citeseer | gcn |
| strat:block+fsim | 8.713 | 0.088 | 800.000 | 1.000 | citeseer | gcn |
| strat:block+hop2 | 7.489 | 0.017 | 800.000 | 1.000 | citeseer | gcn |
| strat:clust | 6.392 | 0.010 | 800.000 | 1.000 | citeseer | gcn |
| strat:clust+fsim | 8.637 | 0.201 | 800.000 | 1.000 | citeseer | gcn |
| strat:clust+hop2 | 6.811 | 0.018 | 800.000 | 1.000 | citeseer | gcn |
| strat:fsim | 8.562 | 0.045 | 800.000 | 1.000 | citeseer | gcn |
| strat:fsim+hop2 | 8.866 | 0.102 | 800.000 | 1.000 | citeseer | gcn |
| strat:hop2 | 6.656 | 0.009 | 800.000 | 1.000 | citeseer | gcn |
| mlp | 7.726 | 0.000 | 400.000 | 1.000 | citeseer | gcn |
| degree | 14.130 | 0.078 | 800.000 | 1.000 | citeseer | sage |
| empty | 14.246 | 0.000 | 400.000 | 1.000 | citeseer | sage |
| er | 15.017 | 0.003 | 400.000 | 1.000 | citeseer | sage |
| real | 11.643 | 0.000 | 400.000 | 1.000 | citeseer | sage |
| strat:block | 12.610 | 0.009 | 800.000 | 1.000 | citeseer | sage |
| strat:block+clust | 12.465 | 0.013 | 800.000 | 1.000 | citeseer | sage |
| strat:block+fsim | 12.167 | 0.088 | 800.000 | 1.000 | citeseer | sage |
| strat:block+hop2 | 12.363 | 0.017 | 800.000 | 1.000 | citeseer | sage |
| strat:clust | 13.900 | 0.010 | 800.000 | 1.000 | citeseer | sage |
| strat:clust+fsim | 12.331 | 0.201 | 800.000 | 1.000 | citeseer | sage |
| strat:clust+hop2 | 13.558 | 0.018 | 800.000 | 1.000 | citeseer | sage |
| strat:fsim | 12.344 | 0.045 | 800.000 | 1.000 | citeseer | sage |
| strat:fsim+hop2 | 12.134 | 0.102 | 800.000 | 1.000 | citeseer | sage |
| strat:hop2 | 13.732 | 0.009 | 800.000 | 1.000 | citeseer | sage |
| mlp | 7.726 | 0.000 | 400.000 | 1.000 | citeseer | sage |

| dataset | model | cpu_s_per_replicate(real+|L| nulls) | craf_b80_cpu_hours | craf_b20_cpu_hours |
|---|---|---|---|---|
| citeseer | gcn | 93.448 | 2.077 | 0.519 |
| citeseer | sage | 153.968 | 3.422 | 0.855 |

## 10. Decision inputs (rules R1–R4 of the protocol)

```
{
 "R2": {
  "citeseer": true
 },
 "R1": {
  "no_fwer_flag_primary": false,
  "no_marginal_flag_alpha05": false
 },
 "R4": {
  "citeseer/gcn": true,
  "citeseer/sage": true
 },
 "R3": {
  "citeseer/gcn": {
   "certified_member_outside_pcga_ladder": false,
   "ni_holm_differs_from_craf": false,
   "certified_specificity_over_L": true
  },
  "citeseer/sage": {
   "certified_member_outside_pcga_ladder": false,
   "ni_holm_differs_from_craf": false,
   "certified_specificity_over_L": true
  }
 },
 "natural_nonmonotonicity_certified": false
}
```
