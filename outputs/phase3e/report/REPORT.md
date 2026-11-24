# phase3e report (generated from outputs/phase3e/analysis)

delta = 0.005, alpha = 0.05, confirmatory b = 80 (block 0); reference = clusters >= 100.

## 1. Admissibility (label-free, before any fit)

### roman_empire

| element | n_joint_strata | acceptance | mean_overlap | mean_pairwise_overlap | mean_gen_seconds | admissible_final |
|---|---|---|---|---|---|---|
| degree | 1 | 1.000 | 0.000 | 0.000 | 0.171 | True |
| strat:block | 8 | 1.000 | 0.050 | 0.046 | 0.169 | True |
| strat:clust | 4 | 1.000 | 0.018 | 0.004 | 0.200 | True |
| strat:fsim | 16 | 1.000 | 0.021 | 0.009 | 0.835 | True |
| strat:hop2 | 4 | 1.000 | 0.012 | 0.001 | 0.213 | True |
| strat:block+clust | 32 | 1.000 | 0.065 | 0.050 | 0.203 | True |
| strat:block+fsim | 125 | 1.000 | 0.066 | 0.052 | 0.910 | True |
| strat:block+hop2 | 32 | 1.000 | 0.059 | 0.047 | 0.187 | True |
| strat:clust+fsim | 64 | 1.000 | 0.083 | 0.054 | 3.366 | True |
| strat:clust+hop2 | 16 | 1.000 | 0.050 | 0.022 | 0.413 | True |
| strat:fsim+hop2 | 64 | 0.000 | 0.130 | 0.083 | 4.169 | False |
| er | 1 | 1.000 | 0.000 | 0.000 | 0.024 | True |

### amazon_ratings

| element | n_joint_strata | acceptance | mean_overlap | mean_pairwise_overlap | mean_gen_seconds | admissible_final |
|---|---|---|---|---|---|---|
| degree | 1 | 1.000 | 0.001 | 0.001 | 0.318 | True |
| strat:block | 8 | 1.000 | 0.140 | 0.102 | 0.306 | True |
| strat:clust | 4 | 1.000 | 0.011 | 0.002 | 0.477 | True |
| strat:fsim | 16 | 1.000 | 0.034 | 0.014 | 2.601 | True |
| strat:hop2 | 4 | 1.000 | 0.027 | 0.012 | 0.444 | True |
| strat:block+clust | 32 | 1.000 | 0.125 | 0.094 | 0.612 | True |
| strat:block+fsim | 128 | 1.000 | 0.168 | 0.132 | 3.593 | True |
| strat:block+hop2 | 32 | 1.000 | 0.137 | 0.106 | 0.537 | True |
| strat:clust+fsim | 64 | 0.000 | 0.148 | 0.088 | 16.790 | False |
| strat:clust+hop2 | 16 | 1.000 | 0.084 | 0.040 | 1.294 | True |
| strat:fsim+hop2 | 64 | 0.000 | 0.143 | 0.102 | 16.283 | False |
| er | 1 | 1.000 | 0.000 | 0.000 | 0.082 | True |

## 2. Matched baselines (reference clusters; test 1 − Brier/2 and accuracy)

| dataset | model | variant | metric | mean | se | n |
|---|---|---|---|---|---|---|
| roman_empire | gcn | empty | test_score | 0.7604 | 0.0001 | 300 |
| roman_empire | gcn | empty | test_acc | 0.6457 | 0.0002 | 300 |
| roman_empire | gcn | real | test_score | 0.6337 | 0.0001 | 300 |
| roman_empire | gcn | real | test_acc | 0.4329 | 0.0003 | 300 |
| roman_empire | gcn | mlp | test_score | 0.7604 | 0.0001 | 300 |
| roman_empire | gcn | mlp | test_acc | 0.6457 | 0.0002 | 300 |
| roman_empire | sage | empty | test_score | 0.7604 | 0.0001 | 300 |
| roman_empire | sage | empty | test_acc | 0.6458 | 0.0002 | 300 |
| roman_empire | sage | real | test_score | 0.8223 | 0.0001 | 300 |
| roman_empire | sage | real | test_acc | 0.7467 | 0.0003 | 300 |
| roman_empire | sage | mlp | test_score | 0.7604 | 0.0001 | 300 |
| roman_empire | sage | mlp | test_acc | 0.6457 | 0.0002 | 300 |
| amazon_ratings | gcn | empty | test_score | 0.6437 | 0.0000 | 300 |
| amazon_ratings | gcn | empty | test_acc | 0.3887 | 0.0002 | 300 |
| amazon_ratings | gcn | real | test_score | 0.6558 | 0.0001 | 300 |
| amazon_ratings | gcn | real | test_acc | 0.4257 | 0.0003 | 300 |
| amazon_ratings | gcn | mlp | test_score | 0.6437 | 0.0000 | 300 |
| amazon_ratings | gcn | mlp | test_acc | 0.3887 | 0.0002 | 300 |
| amazon_ratings | sage | empty | test_score | 0.6436 | 0.0000 | 300 |
| amazon_ratings | sage | empty | test_acc | 0.3888 | 0.0002 | 300 |
| amazon_ratings | sage | real | test_score | 0.6618 | 0.0001 | 300 |
| amazon_ratings | sage | real | test_acc | 0.4407 | 0.0003 | 300 |
| amazon_ratings | sage | mlp | test_score | 0.6437 | 0.0000 | 300 |
| amazon_ratings | sage | mlp | test_acc | 0.3887 | 0.0002 | 300 |

## 3. Frontiers

Reference = all clusters >= block (mean over draws), Holm at alpha; simultaneous (Bonferroni) 95% intervals. Confirmatory = block 0, uniform CRAF at b_conf (primary) and adaptive CRAF (secondary).

### roman_empire / gcn

Reference:

| element | n | delta_hat | se | sim_lo | sim_hi | status | cert_min | possible_min | gap_set |
|---|---|---|---|---|---|---|---|---|---|
| degree | 300 | -0.0136 | 0.0001 | -0.0138 | -0.0133 | sufficient | True | True |  |
| strat:block | 300 | -0.0119 | 0.0001 | -0.0121 | -0.0117 | sufficient | False | False |  |
| strat:clust | 300 | -0.0131 | 0.0001 | -0.0134 | -0.0129 | sufficient | False | False |  |
| strat:fsim | 300 | -0.0159 | 0.0001 | -0.0161 | -0.0157 | sufficient | False | False |  |
| strat:hop2 | 300 | -0.0153 | 0.0001 | -0.0155 | -0.0150 | sufficient | False | False |  |
| strat:block+clust | 300 | -0.0114 | 0.0001 | -0.0116 | -0.0112 | sufficient | False | False |  |
| strat:block+fsim | 300 | -0.0146 | 0.0001 | -0.0148 | -0.0144 | sufficient | False | False |  |
| strat:block+hop2 | 300 | -0.0136 | 0.0001 | -0.0139 | -0.0134 | sufficient | False | False |  |
| strat:clust+fsim | 300 | -0.0124 | 0.0001 | -0.0126 | -0.0122 | sufficient | False | False |  |
| strat:clust+hop2 | 300 | -0.0137 | 0.0001 | -0.0139 | -0.0135 | sufficient | False | False |  |
| strat:fsim+hop2 | 0 |  |  |  |  | inconclusive | False | False |  |

Confirmatory (uniform CRAF, b = 80):

| element | delta_hat | sim_lo | sim_hi | p_adv | p_suf | status | cert_min | possible_min | min_among_cert | gap_set |
|---|---|---|---|---|---|---|---|---|---|---|
| degree | -0.0138 | -0.0144 | -0.0133 | 1.0000 | 0.0000 | sufficient | True | True | True |  |
| strat:block | -0.0120 | -0.0125 | -0.0114 | 1.0000 | 0.0000 | sufficient | False | False | False |  |
| strat:clust | -0.0130 | -0.0135 | -0.0124 | 1.0000 | 0.0000 | sufficient | False | False | False |  |
| strat:fsim | -0.0157 | -0.0162 | -0.0153 | 1.0000 | 0.0000 | sufficient | False | False | False |  |
| strat:hop2 | -0.0152 | -0.0157 | -0.0146 | 1.0000 | 0.0000 | sufficient | False | False | False |  |
| strat:block+clust | -0.0113 | -0.0119 | -0.0108 | 1.0000 | 0.0000 | sufficient | False | False | False |  |
| strat:block+fsim | -0.0147 | -0.0152 | -0.0142 | 1.0000 | 0.0000 | sufficient | False | False | False |  |
| strat:block+hop2 | -0.0139 | -0.0144 | -0.0134 | 1.0000 | 0.0000 | sufficient | False | False | False |  |
| strat:clust+fsim | -0.0126 | -0.0130 | -0.0121 | 1.0000 | 0.0000 | sufficient | False | False | False |  |
| strat:clust+hop2 | -0.0136 | -0.0142 | -0.0131 | 1.0000 | 0.0000 | sufficient | False | False | False |  |
| strat:fsim+hop2 |  |  |  | 1.0000 | 1.0000 | inconclusive | False | False | False |  |

### roman_empire / sage

Reference:

| element | n | delta_hat | se | sim_lo | sim_hi | status | cert_min | possible_min | gap_set |
|---|---|---|---|---|---|---|---|---|---|
| degree | 300 | 0.0637 | 0.0001 | 0.0635 | 0.0640 | advantage | False | False |  |
| strat:block | 300 | 0.0635 | 0.0001 | 0.0633 | 0.0638 | advantage | False | False |  |
| strat:clust | 300 | 0.0623 | 0.0001 | 0.0621 | 0.0626 | advantage | False | False |  |
| strat:fsim | 300 | 0.0284 | 0.0001 | 0.0282 | 0.0286 | advantage | False | False |  |
| strat:hop2 | 300 | 0.0629 | 0.0001 | 0.0626 | 0.0631 | advantage | False | False |  |
| strat:block+clust | 300 | 0.0621 | 0.0001 | 0.0619 | 0.0624 | advantage | False | False |  |
| strat:block+fsim | 300 | 0.0279 | 0.0001 | 0.0277 | 0.0281 | advantage | False | False |  |
| strat:block+hop2 | 300 | 0.0624 | 0.0001 | 0.0622 | 0.0627 | advantage | False | False |  |
| strat:clust+fsim | 300 | 0.0229 | 0.0001 | 0.0228 | 0.0231 | advantage | False | False |  |
| strat:clust+hop2 | 300 | 0.0608 | 0.0001 | 0.0606 | 0.0611 | advantage | False | False |  |
| strat:fsim+hop2 | 0 |  |  |  |  | inconclusive | False | True |  |

Confirmatory (uniform CRAF, b = 80):

| element | delta_hat | sim_lo | sim_hi | p_adv | p_suf | status | cert_min | possible_min | min_among_cert | gap_set |
|---|---|---|---|---|---|---|---|---|---|---|
| degree | 0.0637 | 0.0633 | 0.0642 | 0.0000 | 1.0000 | advantage | False | False | False |  |
| strat:block | 0.0636 | 0.0631 | 0.0641 | 0.0000 | 1.0000 | advantage | False | False | False |  |
| strat:clust | 0.0623 | 0.0618 | 0.0628 | 0.0000 | 1.0000 | advantage | False | False | False |  |
| strat:fsim | 0.0283 | 0.0279 | 0.0287 | 0.0000 | 1.0000 | advantage | False | False | False |  |
| strat:hop2 | 0.0629 | 0.0624 | 0.0633 | 0.0000 | 1.0000 | advantage | False | False | False |  |
| strat:block+clust | 0.0622 | 0.0617 | 0.0627 | 0.0000 | 1.0000 | advantage | False | False | False |  |
| strat:block+fsim | 0.0277 | 0.0273 | 0.0282 | 0.0000 | 1.0000 | advantage | False | False | False |  |
| strat:block+hop2 | 0.0624 | 0.0618 | 0.0629 | 0.0000 | 1.0000 | advantage | False | False | False |  |
| strat:clust+fsim | 0.0229 | 0.0225 | 0.0233 | 0.0000 | 1.0000 | advantage | False | False | False |  |
| strat:clust+hop2 | 0.0608 | 0.0603 | 0.0613 | 0.0000 | 1.0000 | advantage | False | False | False |  |
| strat:fsim+hop2 |  |  |  | 1.0000 | 1.0000 | inconclusive | False | True | False |  |

### amazon_ratings / gcn

Reference:

| element | n | delta_hat | se | sim_lo | sim_hi | status | cert_min | possible_min | gap_set |
|---|---|---|---|---|---|---|---|---|---|
| degree | 300 | 0.0190 | 0.0001 | 0.0188 | 0.0191 | advantage | False | False |  |
| strat:block | 300 | 0.0142 | 0.0000 | 0.0141 | 0.0144 | advantage | False | False |  |
| strat:clust | 300 | 0.0180 | 0.0001 | 0.0178 | 0.0181 | advantage | False | False |  |
| strat:fsim | 300 | 0.0173 | 0.0000 | 0.0172 | 0.0175 | advantage | False | False |  |
| strat:hop2 | 300 | 0.0183 | 0.0001 | 0.0181 | 0.0184 | advantage | False | False |  |
| strat:block+clust | 300 | 0.0138 | 0.0000 | 0.0136 | 0.0139 | advantage | False | False |  |
| strat:block+fsim | 300 | 0.0133 | 0.0000 | 0.0132 | 0.0134 | advantage | False | False |  |
| strat:block+hop2 | 300 | 0.0140 | 0.0000 | 0.0139 | 0.0142 | advantage | False | False |  |
| strat:clust+fsim | 0 |  |  |  |  | inconclusive | False | True |  |
| strat:clust+hop2 | 300 | 0.0173 | 0.0001 | 0.0172 | 0.0175 | advantage | False | False |  |
| strat:fsim+hop2 | 0 |  |  |  |  | inconclusive | False | True |  |

Confirmatory (uniform CRAF, b = 80):

| element | delta_hat | sim_lo | sim_hi | p_adv | p_suf | status | cert_min | possible_min | min_among_cert | gap_set |
|---|---|---|---|---|---|---|---|---|---|---|
| degree | 0.0190 | 0.0187 | 0.0193 | 0.0000 | 1.0000 | advantage | False | False | False |  |
| strat:block | 0.0142 | 0.0139 | 0.0145 | 0.0000 | 1.0000 | advantage | False | False | False |  |
| strat:clust | 0.0180 | 0.0177 | 0.0183 | 0.0000 | 1.0000 | advantage | False | False | False |  |
| strat:fsim | 0.0173 | 0.0171 | 0.0176 | 0.0000 | 1.0000 | advantage | False | False | False |  |
| strat:hop2 | 0.0183 | 0.0180 | 0.0186 | 0.0000 | 1.0000 | advantage | False | False | False |  |
| strat:block+clust | 0.0136 | 0.0134 | 0.0139 | 0.0000 | 1.0000 | advantage | False | False | False |  |
| strat:block+fsim | 0.0133 | 0.0131 | 0.0136 | 0.0000 | 1.0000 | advantage | False | False | False |  |
| strat:block+hop2 | 0.0140 | 0.0137 | 0.0143 | 0.0000 | 1.0000 | advantage | False | False | False |  |
| strat:clust+fsim |  |  |  | 1.0000 | 1.0000 | inconclusive | False | True | False |  |
| strat:clust+hop2 | 0.0173 | 0.0171 | 0.0176 | 0.0000 | 1.0000 | advantage | False | False | False |  |
| strat:fsim+hop2 |  |  |  | 1.0000 | 1.0000 | inconclusive | False | True | False |  |

### amazon_ratings / sage

Reference:

| element | n | delta_hat | se | sim_lo | sim_hi | status | cert_min | possible_min | gap_set |
|---|---|---|---|---|---|---|---|---|---|
| degree | 300 | 0.0185 | 0.0001 | 0.0184 | 0.0187 | advantage | False | False |  |
| strat:block | 300 | 0.0159 | 0.0001 | 0.0157 | 0.0161 | advantage | False | False |  |
| strat:clust | 300 | 0.0182 | 0.0001 | 0.0180 | 0.0184 | advantage | False | False |  |
| strat:fsim | 300 | 0.0172 | 0.0001 | 0.0170 | 0.0173 | advantage | False | False |  |
| strat:hop2 | 300 | 0.0181 | 0.0001 | 0.0180 | 0.0183 | advantage | False | False |  |
| strat:block+clust | 300 | 0.0157 | 0.0001 | 0.0156 | 0.0159 | advantage | False | False |  |
| strat:block+fsim | 300 | 0.0146 | 0.0001 | 0.0145 | 0.0148 | advantage | False | False |  |
| strat:block+hop2 | 300 | 0.0158 | 0.0001 | 0.0156 | 0.0160 | advantage | False | False |  |
| strat:clust+fsim | 0 |  |  |  |  | inconclusive | False | True |  |
| strat:clust+hop2 | 300 | 0.0178 | 0.0001 | 0.0177 | 0.0180 | advantage | False | False |  |
| strat:fsim+hop2 | 0 |  |  |  |  | inconclusive | False | True |  |

Confirmatory (uniform CRAF, b = 80):

| element | delta_hat | sim_lo | sim_hi | p_adv | p_suf | status | cert_min | possible_min | min_among_cert | gap_set |
|---|---|---|---|---|---|---|---|---|---|---|
| degree | 0.0185 | 0.0182 | 0.0188 | 0.0000 | 1.0000 | advantage | False | False | False |  |
| strat:block | 0.0157 | 0.0154 | 0.0160 | 0.0000 | 1.0000 | advantage | False | False | False |  |
| strat:clust | 0.0181 | 0.0178 | 0.0184 | 0.0000 | 1.0000 | advantage | False | False | False |  |
| strat:fsim | 0.0171 | 0.0168 | 0.0174 | 0.0000 | 1.0000 | advantage | False | False | False |  |
| strat:hop2 | 0.0180 | 0.0177 | 0.0183 | 0.0000 | 1.0000 | advantage | False | False | False |  |
| strat:block+clust | 0.0155 | 0.0152 | 0.0158 | 0.0000 | 1.0000 | advantage | False | False | False |  |
| strat:block+fsim | 0.0146 | 0.0143 | 0.0149 | 0.0000 | 1.0000 | advantage | False | False | False |  |
| strat:block+hop2 | 0.0157 | 0.0154 | 0.0160 | 0.0000 | 1.0000 | advantage | False | False | False |  |
| strat:clust+fsim |  |  |  | 1.0000 | 1.0000 | inconclusive | False | True | False |  |
| strat:clust+hop2 | 0.0177 | 0.0174 | 0.0180 | 0.0000 | 1.0000 | advantage | False | False | False |  |
| strat:fsim+hop2 |  |  |  | 1.0000 | 1.0000 | inconclusive | False | True | False |  |

### Frontier summary

| dataset | model | run | cert_min | possible_min | n_advantage | n_sufficient | n_inconclusive | specificity_over_L | min_among_cert | gaps |
|---|---|---|---|---|---|---|---|---|---|---|
| roman_empire | gcn | reference | {∅(degree)} | {∅(degree)} | 0 | 10 | 1 | False | {} |  |
| roman_empire | gcn | confirm craf | {∅(degree)} | {∅(degree)} | 0 | 10 | 1 | False | {∅(degree)} |  |
| roman_empire | gcn | confirm craf_adaptive | {∅(degree)} | {∅(degree)} | 0 | 10 | 1 | False | {∅(degree)} |  |
| roman_empire | sage | reference | {} | {fsim+hop2} | 10 | 0 | 1 | False | {} |  |
| roman_empire | sage | confirm craf | {} | {fsim+hop2} | 10 | 0 | 1 | False | {} |  |
| roman_empire | sage | confirm craf_adaptive | {} | {fsim+hop2} | 10 | 0 | 1 | False | {} |  |
| amazon_ratings | gcn | reference | {} | {clust+fsim, fsim+hop2} | 9 | 0 | 2 | False | {} |  |
| amazon_ratings | gcn | confirm craf | {} | {clust+fsim, fsim+hop2} | 9 | 0 | 2 | False | {} |  |
| amazon_ratings | gcn | confirm craf_adaptive | {} | {clust+fsim, fsim+hop2} | 9 | 0 | 2 | False | {} |  |
| amazon_ratings | sage | reference | {} | {clust+fsim, fsim+hop2} | 9 | 0 | 2 | False | {} |  |
| amazon_ratings | sage | confirm craf | {} | {clust+fsim, fsim+hop2} | 9 | 0 | 2 | False | {} |  |
| amazon_ratings | sage | confirm craf_adaptive | {} | {clust+fsim, fsim+hop2} | 9 | 0 | 2 | False | {} |  |

![frontiers](frontiers.png)

## 4. Confirmatory block: what each procedure reports (same data, same budget)

| dataset | model | procedure | reported | fits | n_A | n_C | n_inconclusive |
|---|---|---|---|---|---|---|---|
| roman_empire | gcn | craf | {∅(degree)} | 960 | 0 | 10 | 1 |
| roman_empire | gcn | craf_children | {∅(degree)} | 960 | 0 | 10 | 1 |
| roman_empire | gcn | factorial_unadj | {∅(degree)} | 960 | 0 | 10 | 1 |
| roman_empire | gcn | ni_holm | {∅(degree)} | 960 | 0 | 10 | 1 |
| roman_empire | gcn | naive_point | {∅(degree)} | 960 |  |  |  |
| roman_empire | gcn | craf_adaptive | {∅(degree)} | 960 | 0 | 10 | 1 |
| roman_empire | gcn | pcga_l | {∅(degree)} | 500 |  |  |  |
| roman_empire | sage | craf | {} | 960 | 10 | 0 | 1 |
| roman_empire | sage | craf_children | {} | 960 | 10 | 0 | 1 |
| roman_empire | sage | factorial_unadj | {} | 960 | 10 | 0 | 1 |
| roman_empire | sage | ni_holm | {} | 960 | 0 | 0 | 11 |
| roman_empire | sage | naive_point | {} | 960 |  |  |  |
| roman_empire | sage | craf_adaptive | {} | 960 | 10 | 0 | 1 |
| roman_empire | sage | pcga_l | {} | 500 |  |  |  |
| amazon_ratings | gcn | craf | {} | 960 | 9 | 0 | 2 |
| amazon_ratings | gcn | craf_children | {} | 960 | 9 | 0 | 2 |
| amazon_ratings | gcn | factorial_unadj | {} | 960 | 9 | 0 | 2 |
| amazon_ratings | gcn | ni_holm | {} | 960 | 0 | 0 | 11 |
| amazon_ratings | gcn | naive_point | {} | 960 |  |  |  |
| amazon_ratings | gcn | craf_adaptive | {} | 960 | 9 | 0 | 2 |
| amazon_ratings | gcn | pcga_l | {} | 500 |  |  |  |
| amazon_ratings | sage | craf | {} | 960 | 9 | 0 | 2 |
| amazon_ratings | sage | craf_children | {} | 960 | 9 | 0 | 2 |
| amazon_ratings | sage | factorial_unadj | {} | 960 | 9 | 0 | 2 |
| amazon_ratings | sage | ni_holm | {} | 960 | 0 | 0 | 11 |
| amazon_ratings | sage | naive_point | {} | 960 |  |  |  |
| amazon_ratings | sage | craf_adaptive | {} | 960 | 9 | 0 | 2 |
| amazon_ratings | sage | pcga_l | {} | 500 |  |  |  |

## 5. Resampling comparison (disjoint reference blocks; leave-block-out reference truth)

| dataset | model | b | procedure | n_exp | exact | false_member | false_member_hi | class_error | class_error_hi | covered | n_inconclusive | unc_size | mean_fits | modal_report |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| amazon_ratings | gcn | 20 | craf | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 | 1.000 | 2.000 | 2.000 | 240.000 | {} |
| amazon_ratings | gcn | 20 | craf_adaptive | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 | 1.000 | 2.000 | 2.000 | 240.000 | {} |
| amazon_ratings | gcn | 20 | craf_children | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 |  | 2.000 |  | 240.000 | {} |
| amazon_ratings | gcn | 20 | ni_holm | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 |  | 11.000 |  | 240.000 | {} |
| amazon_ratings | gcn | 20 | factorial_unadj | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 |  | 2.000 |  | 240.000 | {} |
| amazon_ratings | gcn | 20 | naive_point | 3 | 1.000 | 0.000 | 0.561 |  |  |  |  |  | 240.000 | {} |
| amazon_ratings | gcn | 20 | pcga_l | 3 | 1.000 | 0.000 | 0.561 |  |  |  |  |  | 240.000 | {} |
| amazon_ratings | gcn | 40 | craf | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 | 1.000 | 2.000 | 2.000 | 480.000 | {} |
| amazon_ratings | gcn | 40 | craf_adaptive | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 | 1.000 | 2.000 | 2.000 | 480.000 | {} |
| amazon_ratings | gcn | 40 | craf_children | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 |  | 2.000 |  | 480.000 | {} |
| amazon_ratings | gcn | 40 | ni_holm | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 |  | 11.000 |  | 480.000 | {} |
| amazon_ratings | gcn | 40 | factorial_unadj | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 |  | 2.000 |  | 480.000 | {} |
| amazon_ratings | gcn | 40 | naive_point | 3 | 1.000 | 0.000 | 0.561 |  |  |  |  |  | 480.000 | {} |
| amazon_ratings | gcn | 40 | pcga_l | 3 | 1.000 | 0.000 | 0.561 |  |  |  |  |  | 480.000 | {} |
| amazon_ratings | gcn | 80 | craf | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 | 1.000 | 2.000 | 2.000 | 960.000 | {} |
| amazon_ratings | gcn | 80 | craf_adaptive | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 | 1.000 | 2.000 | 2.000 | 960.000 | {} |
| amazon_ratings | gcn | 80 | craf_children | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 |  | 2.000 |  | 960.000 | {} |
| amazon_ratings | gcn | 80 | ni_holm | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 |  | 11.000 |  | 960.000 | {} |
| amazon_ratings | gcn | 80 | factorial_unadj | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 |  | 2.000 |  | 960.000 | {} |
| amazon_ratings | gcn | 80 | naive_point | 3 | 1.000 | 0.000 | 0.561 |  |  |  |  |  | 960.000 | {} |
| amazon_ratings | gcn | 80 | pcga_l | 3 | 1.000 | 0.000 | 0.561 |  |  |  |  |  | 500.000 | {} |
| amazon_ratings | sage | 20 | craf | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 | 1.000 | 2.000 | 2.000 | 240.000 | {} |
| amazon_ratings | sage | 20 | craf_adaptive | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 | 1.000 | 2.000 | 2.000 | 240.000 | {} |
| amazon_ratings | sage | 20 | craf_children | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 |  | 2.000 |  | 240.000 | {} |
| amazon_ratings | sage | 20 | ni_holm | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 |  | 11.000 |  | 240.000 | {} |
| amazon_ratings | sage | 20 | factorial_unadj | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 |  | 2.000 |  | 240.000 | {} |
| amazon_ratings | sage | 20 | naive_point | 3 | 1.000 | 0.000 | 0.561 |  |  |  |  |  | 240.000 | {} |
| amazon_ratings | sage | 20 | pcga_l | 3 | 1.000 | 0.000 | 0.561 |  |  |  |  |  | 240.000 | {} |
| amazon_ratings | sage | 40 | craf | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 | 1.000 | 2.000 | 2.000 | 480.000 | {} |
| amazon_ratings | sage | 40 | craf_adaptive | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 | 1.000 | 2.000 | 2.000 | 480.000 | {} |
| amazon_ratings | sage | 40 | craf_children | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 |  | 2.000 |  | 480.000 | {} |
| amazon_ratings | sage | 40 | ni_holm | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 |  | 11.000 |  | 480.000 | {} |
| amazon_ratings | sage | 40 | factorial_unadj | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 |  | 2.000 |  | 480.000 | {} |
| amazon_ratings | sage | 40 | naive_point | 3 | 1.000 | 0.000 | 0.561 |  |  |  |  |  | 480.000 | {} |
| amazon_ratings | sage | 40 | pcga_l | 3 | 1.000 | 0.000 | 0.561 |  |  |  |  |  | 480.000 | {} |
| amazon_ratings | sage | 80 | craf | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 | 1.000 | 2.000 | 2.000 | 960.000 | {} |
| amazon_ratings | sage | 80 | craf_adaptive | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 | 1.000 | 2.000 | 2.000 | 960.000 | {} |
| amazon_ratings | sage | 80 | craf_children | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 |  | 2.000 |  | 960.000 | {} |
| amazon_ratings | sage | 80 | ni_holm | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 |  | 11.000 |  | 960.000 | {} |
| amazon_ratings | sage | 80 | factorial_unadj | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 |  | 2.000 |  | 960.000 | {} |
| amazon_ratings | sage | 80 | naive_point | 3 | 1.000 | 0.000 | 0.561 |  |  |  |  |  | 960.000 | {} |
| amazon_ratings | sage | 80 | pcga_l | 3 | 1.000 | 0.000 | 0.561 |  |  |  |  |  | 500.000 | {} |
| roman_empire | gcn | 20 | craf | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 | 1.000 | 1.000 | 0.000 | 240.000 | {∅(degree)} |
| roman_empire | gcn | 20 | craf_adaptive | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 | 1.000 | 1.000 | 0.000 | 240.000 | {∅(degree)} |
| roman_empire | gcn | 20 | craf_children | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 |  | 1.000 |  | 240.000 | {∅(degree)} |
| roman_empire | gcn | 20 | ni_holm | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 |  | 1.000 |  | 240.000 | {∅(degree)} |
| roman_empire | gcn | 20 | factorial_unadj | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 |  | 1.000 |  | 240.000 | {∅(degree)} |
| roman_empire | gcn | 20 | naive_point | 3 | 1.000 | 0.000 | 0.561 |  |  |  |  |  | 240.000 | {∅(degree)} |
| roman_empire | gcn | 20 | pcga_l | 3 | 1.000 | 0.000 | 0.561 |  |  |  |  |  | 240.000 | {∅(degree)} |
| roman_empire | gcn | 40 | craf | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 | 1.000 | 1.000 | 0.000 | 480.000 | {∅(degree)} |
| roman_empire | gcn | 40 | craf_adaptive | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 | 1.000 | 1.000 | 0.000 | 480.000 | {∅(degree)} |
| roman_empire | gcn | 40 | craf_children | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 |  | 1.000 |  | 480.000 | {∅(degree)} |
| roman_empire | gcn | 40 | ni_holm | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 |  | 1.000 |  | 480.000 | {∅(degree)} |
| roman_empire | gcn | 40 | factorial_unadj | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 |  | 1.000 |  | 480.000 | {∅(degree)} |
| roman_empire | gcn | 40 | naive_point | 3 | 1.000 | 0.000 | 0.561 |  |  |  |  |  | 480.000 | {∅(degree)} |
| roman_empire | gcn | 40 | pcga_l | 3 | 1.000 | 0.000 | 0.561 |  |  |  |  |  | 480.000 | {∅(degree)} |
| roman_empire | gcn | 80 | craf | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 | 1.000 | 1.000 | 0.000 | 960.000 | {∅(degree)} |
| roman_empire | gcn | 80 | craf_adaptive | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 | 1.000 | 1.000 | 0.000 | 960.000 | {∅(degree)} |
| roman_empire | gcn | 80 | craf_children | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 |  | 1.000 |  | 960.000 | {∅(degree)} |
| roman_empire | gcn | 80 | ni_holm | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 |  | 1.000 |  | 960.000 | {∅(degree)} |
| roman_empire | gcn | 80 | factorial_unadj | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 |  | 1.000 |  | 960.000 | {∅(degree)} |
| roman_empire | gcn | 80 | naive_point | 3 | 1.000 | 0.000 | 0.561 |  |  |  |  |  | 960.000 | {∅(degree)} |
| roman_empire | gcn | 80 | pcga_l | 3 | 1.000 | 0.000 | 0.561 |  |  |  |  |  | 500.000 | {∅(degree)} |
| roman_empire | sage | 20 | craf | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 | 1.000 | 1.000 | 1.000 | 240.000 | {} |
| roman_empire | sage | 20 | craf_adaptive | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 | 1.000 | 1.000 | 1.000 | 240.000 | {} |
| roman_empire | sage | 20 | craf_children | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 |  | 1.000 |  | 240.000 | {} |
| roman_empire | sage | 20 | ni_holm | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 |  | 11.000 |  | 240.000 | {} |
| roman_empire | sage | 20 | factorial_unadj | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 |  | 1.000 |  | 240.000 | {} |
| roman_empire | sage | 20 | naive_point | 3 | 1.000 | 0.000 | 0.561 |  |  |  |  |  | 240.000 | {} |
| roman_empire | sage | 20 | pcga_l | 3 | 1.000 | 0.000 | 0.561 |  |  |  |  |  | 240.000 | {} |
| roman_empire | sage | 40 | craf | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 | 1.000 | 1.000 | 1.000 | 480.000 | {} |
| roman_empire | sage | 40 | craf_adaptive | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 | 1.000 | 1.000 | 1.000 | 480.000 | {} |
| roman_empire | sage | 40 | craf_children | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 |  | 1.000 |  | 480.000 | {} |
| roman_empire | sage | 40 | ni_holm | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 |  | 11.000 |  | 480.000 | {} |
| roman_empire | sage | 40 | factorial_unadj | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 |  | 1.000 |  | 480.000 | {} |
| roman_empire | sage | 40 | naive_point | 3 | 1.000 | 0.000 | 0.561 |  |  |  |  |  | 480.000 | {} |
| roman_empire | sage | 40 | pcga_l | 3 | 1.000 | 0.000 | 0.561 |  |  |  |  |  | 480.000 | {} |
| roman_empire | sage | 80 | craf | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 | 1.000 | 1.000 | 1.000 | 960.000 | {} |
| roman_empire | sage | 80 | craf_adaptive | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 | 1.000 | 1.000 | 1.000 | 960.000 | {} |
| roman_empire | sage | 80 | craf_children | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 |  | 1.000 |  | 960.000 | {} |
| roman_empire | sage | 80 | ni_holm | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 |  | 11.000 |  | 960.000 | {} |
| roman_empire | sage | 80 | factorial_unadj | 3 | 1.000 | 0.000 | 0.561 | 0.000 | 0.561 |  | 1.000 |  | 960.000 | {} |
| roman_empire | sage | 80 | naive_point | 3 | 1.000 | 0.000 | 0.561 |  |  |  |  |  | 960.000 | {} |
| roman_empire | sage | 80 | pcga_l | 3 | 1.000 | 0.000 | 0.561 |  |  |  |  |  | 500.000 | {} |

Paired differences (experiment-paired; normal 95% CI):

| dataset | model | b | a | b_proc | metric | diff | ci_lo | ci_hi | n_exp |
|---|---|---|---|---|---|---|---|---|---|
| roman_empire | gcn | 20 | craf_adaptive | craf | exact | 0.000 | 0.000 | 0.000 | 3 |
| roman_empire | gcn | 40 | craf_adaptive | craf | exact | 0.000 | 0.000 | 0.000 | 3 |
| roman_empire | gcn | 80 | craf_adaptive | craf | exact | 0.000 | 0.000 | 0.000 | 3 |
| roman_empire | sage | 20 | craf_adaptive | craf | exact | 0.000 | 0.000 | 0.000 | 3 |
| roman_empire | sage | 40 | craf_adaptive | craf | exact | 0.000 | 0.000 | 0.000 | 3 |
| roman_empire | sage | 80 | craf_adaptive | craf | exact | 0.000 | 0.000 | 0.000 | 3 |
| amazon_ratings | gcn | 20 | craf_adaptive | craf | exact | 0.000 | 0.000 | 0.000 | 3 |
| amazon_ratings | gcn | 40 | craf_adaptive | craf | exact | 0.000 | 0.000 | 0.000 | 3 |
| amazon_ratings | gcn | 80 | craf_adaptive | craf | exact | 0.000 | 0.000 | 0.000 | 3 |
| amazon_ratings | sage | 20 | craf_adaptive | craf | exact | 0.000 | 0.000 | 0.000 | 3 |
| amazon_ratings | sage | 40 | craf_adaptive | craf | exact | 0.000 | 0.000 | 0.000 | 3 |
| amazon_ratings | sage | 80 | craf_adaptive | craf | exact | 0.000 | 0.000 | 0.000 | 3 |
| roman_empire | gcn | 20 | craf_adaptive | craf | n_inconclusive | 0.000 | 0.000 | 0.000 | 3 |
| roman_empire | gcn | 40 | craf_adaptive | craf | n_inconclusive | 0.000 | 0.000 | 0.000 | 3 |
| roman_empire | gcn | 80 | craf_adaptive | craf | n_inconclusive | 0.000 | 0.000 | 0.000 | 3 |
| roman_empire | sage | 20 | craf_adaptive | craf | n_inconclusive | 0.000 | 0.000 | 0.000 | 3 |
| roman_empire | sage | 40 | craf_adaptive | craf | n_inconclusive | 0.000 | 0.000 | 0.000 | 3 |
| roman_empire | sage | 80 | craf_adaptive | craf | n_inconclusive | 0.000 | 0.000 | 0.000 | 3 |
| amazon_ratings | gcn | 20 | craf_adaptive | craf | n_inconclusive | 0.000 | 0.000 | 0.000 | 3 |
| amazon_ratings | gcn | 40 | craf_adaptive | craf | n_inconclusive | 0.000 | 0.000 | 0.000 | 3 |
| amazon_ratings | gcn | 80 | craf_adaptive | craf | n_inconclusive | 0.000 | 0.000 | 0.000 | 3 |
| amazon_ratings | sage | 20 | craf_adaptive | craf | n_inconclusive | 0.000 | 0.000 | 0.000 | 3 |
| amazon_ratings | sage | 40 | craf_adaptive | craf | n_inconclusive | 0.000 | 0.000 | 0.000 | 3 |
| amazon_ratings | sage | 80 | craf_adaptive | craf | n_inconclusive | 0.000 | 0.000 | 0.000 | 3 |
| roman_empire | gcn | 20 | craf | ni_holm | false_member | 0.000 | 0.000 | 0.000 | 3 |
| roman_empire | gcn | 40 | craf | ni_holm | false_member | 0.000 | 0.000 | 0.000 | 3 |
| roman_empire | gcn | 80 | craf | ni_holm | false_member | 0.000 | 0.000 | 0.000 | 3 |
| roman_empire | sage | 20 | craf | ni_holm | false_member | 0.000 | 0.000 | 0.000 | 3 |
| roman_empire | sage | 40 | craf | ni_holm | false_member | 0.000 | 0.000 | 0.000 | 3 |
| roman_empire | sage | 80 | craf | ni_holm | false_member | 0.000 | 0.000 | 0.000 | 3 |
| amazon_ratings | gcn | 20 | craf | ni_holm | false_member | 0.000 | 0.000 | 0.000 | 3 |
| amazon_ratings | gcn | 40 | craf | ni_holm | false_member | 0.000 | 0.000 | 0.000 | 3 |
| amazon_ratings | gcn | 80 | craf | ni_holm | false_member | 0.000 | 0.000 | 0.000 | 3 |
| amazon_ratings | sage | 20 | craf | ni_holm | false_member | 0.000 | 0.000 | 0.000 | 3 |
| amazon_ratings | sage | 40 | craf | ni_holm | false_member | 0.000 | 0.000 | 0.000 | 3 |
| amazon_ratings | sage | 80 | craf | ni_holm | false_member | 0.000 | 0.000 | 0.000 | 3 |
| roman_empire | gcn | 20 | craf | craf_children | false_member | 0.000 | 0.000 | 0.000 | 3 |
| roman_empire | gcn | 40 | craf | craf_children | false_member | 0.000 | 0.000 | 0.000 | 3 |
| roman_empire | gcn | 80 | craf | craf_children | false_member | 0.000 | 0.000 | 0.000 | 3 |
| roman_empire | sage | 20 | craf | craf_children | false_member | 0.000 | 0.000 | 0.000 | 3 |
| roman_empire | sage | 40 | craf | craf_children | false_member | 0.000 | 0.000 | 0.000 | 3 |
| roman_empire | sage | 80 | craf | craf_children | false_member | 0.000 | 0.000 | 0.000 | 3 |
| amazon_ratings | gcn | 20 | craf | craf_children | false_member | 0.000 | 0.000 | 0.000 | 3 |
| amazon_ratings | gcn | 40 | craf | craf_children | false_member | 0.000 | 0.000 | 0.000 | 3 |
| amazon_ratings | gcn | 80 | craf | craf_children | false_member | 0.000 | 0.000 | 0.000 | 3 |
| amazon_ratings | sage | 20 | craf | craf_children | false_member | 0.000 | 0.000 | 0.000 | 3 |
| amazon_ratings | sage | 40 | craf | craf_children | false_member | 0.000 | 0.000 | 0.000 | 3 |
| amazon_ratings | sage | 80 | craf | craf_children | false_member | 0.000 | 0.000 | 0.000 | 3 |
| roman_empire | gcn | 20 | craf | naive_point | false_member | 0.000 | 0.000 | 0.000 | 3 |
| roman_empire | gcn | 40 | craf | naive_point | false_member | 0.000 | 0.000 | 0.000 | 3 |
| roman_empire | gcn | 80 | craf | naive_point | false_member | 0.000 | 0.000 | 0.000 | 3 |
| roman_empire | sage | 20 | craf | naive_point | false_member | 0.000 | 0.000 | 0.000 | 3 |
| roman_empire | sage | 40 | craf | naive_point | false_member | 0.000 | 0.000 | 0.000 | 3 |
| roman_empire | sage | 80 | craf | naive_point | false_member | 0.000 | 0.000 | 0.000 | 3 |
| amazon_ratings | gcn | 20 | craf | naive_point | false_member | 0.000 | 0.000 | 0.000 | 3 |
| amazon_ratings | gcn | 40 | craf | naive_point | false_member | 0.000 | 0.000 | 0.000 | 3 |
| amazon_ratings | gcn | 80 | craf | naive_point | false_member | 0.000 | 0.000 | 0.000 | 3 |
| amazon_ratings | sage | 20 | craf | naive_point | false_member | 0.000 | 0.000 | 0.000 | 3 |
| amazon_ratings | sage | 40 | craf | naive_point | false_member | 0.000 | 0.000 | 0.000 | 3 |
| amazon_ratings | sage | 80 | craf | naive_point | false_member | 0.000 | 0.000 | 0.000 | 3 |
| roman_empire | gcn | 20 | craf | naive_point | exact | 0.000 | 0.000 | 0.000 | 3 |
| roman_empire | gcn | 40 | craf | naive_point | exact | 0.000 | 0.000 | 0.000 | 3 |
| roman_empire | gcn | 80 | craf | naive_point | exact | 0.000 | 0.000 | 0.000 | 3 |
| roman_empire | sage | 20 | craf | naive_point | exact | 0.000 | 0.000 | 0.000 | 3 |
| roman_empire | sage | 40 | craf | naive_point | exact | 0.000 | 0.000 | 0.000 | 3 |
| roman_empire | sage | 80 | craf | naive_point | exact | 0.000 | 0.000 | 0.000 | 3 |
| amazon_ratings | gcn | 20 | craf | naive_point | exact | 0.000 | 0.000 | 0.000 | 3 |
| amazon_ratings | gcn | 40 | craf | naive_point | exact | 0.000 | 0.000 | 0.000 | 3 |
| amazon_ratings | gcn | 80 | craf | naive_point | exact | 0.000 | 0.000 | 0.000 | 3 |
| amazon_ratings | sage | 20 | craf | naive_point | exact | 0.000 | 0.000 | 0.000 | 3 |
| amazon_ratings | sage | 40 | craf | naive_point | exact | 0.000 | 0.000 | 0.000 | 3 |
| amazon_ratings | sage | 80 | craf | naive_point | exact | 0.000 | 0.000 | 0.000 | 3 |

## 6. RUSA full-set claim (exhaustive IUT vs fullset_adaptive_fb; PCGA-L edge step for reference)

| dataset | model | b | procedure | n_exp | claim | false_vs_full | theta_full | fits | fallback |
|---|---|---|---|---|---|---|---|---|---|
| amazon_ratings | gcn | 6 | exhaustive_iut | 3 | 0.000 | 0.000 | 0.012 | 84.000 |  |
| amazon_ratings | gcn | 6 | fullset_adaptive_fb | 3 | 0.000 | 0.000 | 0.012 | 84.000 | 1.000 |
| amazon_ratings | gcn | 6 | pcga_l | 3 | 1.000 | 0.000 | 0.012 | 80.000 |  |
| amazon_ratings | gcn | 12 | exhaustive_iut | 3 | 0.000 | 0.000 | 0.012 | 168.000 |  |
| amazon_ratings | gcn | 12 | fullset_adaptive_fb | 3 | 0.000 | 0.000 | 0.012 | 296.000 | 0.000 |
| amazon_ratings | gcn | 12 | pcga_l | 3 | 1.000 | 0.000 | 0.012 | 165.000 |  |
| amazon_ratings | gcn | 24 | exhaustive_iut | 3 | 0.000 | 0.000 | 0.012 | 336.000 |  |
| amazon_ratings | gcn | 24 | fullset_adaptive_fb | 3 | 0.000 | 0.000 | 0.012 | 352.000 | 0.000 |
| amazon_ratings | gcn | 24 | pcga_l | 3 | 1.000 | 0.000 | 0.012 | 335.000 |  |
| amazon_ratings | sage | 6 | exhaustive_iut | 3 | 0.000 | 0.000 | 0.015 | 84.000 |  |
| amazon_ratings | sage | 6 | fullset_adaptive_fb | 3 | 0.000 | 0.000 | 0.015 | 84.000 | 1.000 |
| amazon_ratings | sage | 6 | pcga_l | 3 | 1.000 | 0.000 | 0.015 | 80.000 |  |
| amazon_ratings | sage | 12 | exhaustive_iut | 3 | 0.000 | 0.000 | 0.015 | 168.000 |  |
| amazon_ratings | sage | 12 | fullset_adaptive_fb | 3 | 0.000 | 0.000 | 0.015 | 296.000 | 0.000 |
| amazon_ratings | sage | 12 | pcga_l | 3 | 1.000 | 0.000 | 0.015 | 165.000 |  |
| amazon_ratings | sage | 24 | exhaustive_iut | 3 | 0.000 | 0.000 | 0.015 | 336.000 |  |
| amazon_ratings | sage | 24 | fullset_adaptive_fb | 3 | 0.000 | 0.000 | 0.015 | 352.000 | 0.000 |
| amazon_ratings | sage | 24 | pcga_l | 3 | 1.000 | 0.000 | 0.015 | 335.000 |  |
| roman_empire | gcn | 6 | exhaustive_iut | 3 | 0.000 | 0.000 | -0.127 | 84.000 |  |
| roman_empire | gcn | 6 | fullset_adaptive_fb | 3 | 0.000 | 0.000 | -0.127 | 84.000 | 1.000 |
| roman_empire | gcn | 6 | pcga_l | 3 | 0.000 | 0.000 | -0.127 | 80.000 |  |
| roman_empire | gcn | 12 | exhaustive_iut | 3 | 0.000 | 0.000 | -0.127 | 168.000 |  |
| roman_empire | gcn | 12 | fullset_adaptive_fb | 3 | 0.000 | 0.000 | -0.127 | 276.000 | 0.000 |
| roman_empire | gcn | 12 | pcga_l | 3 | 0.000 | 0.000 | -0.127 | 165.000 |  |
| roman_empire | gcn | 24 | exhaustive_iut | 3 | 0.000 | 0.000 | -0.127 | 336.000 |  |
| roman_empire | gcn | 24 | fullset_adaptive_fb | 3 | 0.000 | 0.000 | -0.127 | 336.000 | 0.000 |
| roman_empire | gcn | 24 | pcga_l | 3 | 0.000 | 0.000 | -0.127 | 335.000 |  |
| roman_empire | sage | 6 | exhaustive_iut | 3 | 0.000 | 0.000 | 0.023 | 84.000 |  |
| roman_empire | sage | 6 | fullset_adaptive_fb | 3 | 0.000 | 0.000 | 0.023 | 84.000 | 1.000 |
| roman_empire | sage | 6 | pcga_l | 3 | 1.000 | 0.000 | 0.023 | 80.000 |  |
| roman_empire | sage | 12 | exhaustive_iut | 3 | 0.000 | 0.000 | 0.023 | 168.000 |  |
| roman_empire | sage | 12 | fullset_adaptive_fb | 3 | 0.000 | 0.000 | 0.023 | 216.000 | 0.000 |
| roman_empire | sage | 12 | pcga_l | 3 | 1.000 | 0.000 | 0.023 | 165.000 |  |
| roman_empire | sage | 24 | exhaustive_iut | 3 | 0.000 | 0.000 | 0.023 | 336.000 |  |
| roman_empire | sage | 24 | fullset_adaptive_fb | 3 | 0.000 | 0.000 | 0.023 | 272.000 | 0.000 |
| roman_empire | sage | 24 | pcga_l | 3 | 1.000 | 0.000 | 0.023 | 335.000 |  |

Confirmatory block:

| dataset | model | b | procedure | claim | L | theta_hat | fits |
|---|---|---|---|---|---|---|---|
| roman_empire | gcn | 6 | pcga_l | False |  | -0.0118 | 80 |
| roman_empire | gcn | 6 | exhaustive_iut | False | -inf | -0.1253 | 84 |
| roman_empire | gcn | 6 | fullset_adaptive_fb | False | -inf | -0.1253 | 84 |
| roman_empire | gcn | 12 | pcga_l | False |  | -0.0117 | 165 |
| roman_empire | gcn | 12 | exhaustive_iut | False | -inf | -0.1260 | 168 |
| roman_empire | gcn | 12 | fullset_adaptive_fb | False | -inf | -0.1262 | 276 |
| roman_empire | gcn | 24 | pcga_l | False |  | -0.0119 | 335 |
| roman_empire | gcn | 24 | exhaustive_iut | False | -inf | -0.1261 | 336 |
| roman_empire | gcn | 24 | fullset_adaptive_fb | False | -inf | -0.1263 | 336 |
| roman_empire | sage | 6 | pcga_l | True |  | 0.0637 | 80 |
| roman_empire | sage | 6 | exhaustive_iut | False | -inf | 0.0238 | 84 |
| roman_empire | sage | 6 | fullset_adaptive_fb | False | -inf | 0.0238 | 84 |
| roman_empire | sage | 12 | pcga_l | True |  | 0.0637 | 165 |
| roman_empire | sage | 12 | exhaustive_iut | False | -inf | 0.0233 | 168 |
| roman_empire | sage | 12 | fullset_adaptive_fb | False | -inf | 0.0233 | 216 |
| roman_empire | sage | 24 | pcga_l | True |  | 0.0636 | 335 |
| roman_empire | sage | 24 | exhaustive_iut | False | -inf | 0.0229 | 336 |
| roman_empire | sage | 24 | fullset_adaptive_fb | False | -inf | 0.0226 | 272 |
| amazon_ratings | gcn | 6 | pcga_l | True |  | 0.0145 | 80 |
| amazon_ratings | gcn | 6 | exhaustive_iut | False | -inf | 0.0119 | 84 |
| amazon_ratings | gcn | 6 | fullset_adaptive_fb | False | -inf | 0.0119 | 84 |
| amazon_ratings | gcn | 12 | pcga_l | True |  | 0.0143 | 165 |
| amazon_ratings | gcn | 12 | exhaustive_iut | False | -inf | 0.0120 | 168 |
| amazon_ratings | gcn | 12 | fullset_adaptive_fb | False | -inf | 0.0121 | 296 |
| amazon_ratings | gcn | 24 | pcga_l | True |  | 0.0143 | 335 |
| amazon_ratings | gcn | 24 | exhaustive_iut | False | -inf | 0.0122 | 336 |
| amazon_ratings | gcn | 24 | fullset_adaptive_fb | False | -inf | 0.0122 | 352 |
| amazon_ratings | sage | 6 | pcga_l | True |  | 0.0159 | 80 |
| amazon_ratings | sage | 6 | exhaustive_iut | False | -inf | 0.0147 | 84 |
| amazon_ratings | sage | 6 | fullset_adaptive_fb | False | -inf | 0.0147 | 84 |
| amazon_ratings | sage | 12 | pcga_l | True |  | 0.0157 | 165 |
| amazon_ratings | sage | 12 | exhaustive_iut | False | -inf | 0.0148 | 168 |
| amazon_ratings | sage | 12 | fullset_adaptive_fb | False | -inf | 0.0147 | 296 |
| amazon_ratings | sage | 24 | pcga_l | True |  | 0.0158 | 335 |
| amazon_ratings | sage | 24 | exhaustive_iut | False | -inf | 0.0148 | 336 |
| amazon_ratings | sage | 24 | fullset_adaptive_fb | False | -inf | 0.0146 | 352 |

| dataset | model | b | diff_claim(fb − exhaustive) | ci_lo | ci_hi | n_exp |
|---|---|---|---|---|---|---|
| amazon_ratings | gcn | 6 | 0.000 | 0.000 | 0.000 | 3 |
| amazon_ratings | gcn | 12 | 0.000 | 0.000 | 0.000 | 3 |
| amazon_ratings | gcn | 24 | 0.000 | 0.000 | 0.000 | 3 |
| amazon_ratings | sage | 6 | 0.000 | 0.000 | 0.000 | 3 |
| amazon_ratings | sage | 12 | 0.000 | 0.000 | 0.000 | 3 |
| amazon_ratings | sage | 24 | 0.000 | 0.000 | 0.000 | 3 |
| roman_empire | gcn | 6 | 0.000 | 0.000 | 0.000 | 3 |
| roman_empire | gcn | 12 | 0.000 | 0.000 | 0.000 | 3 |
| roman_empire | gcn | 24 | 0.000 | 0.000 | 0.000 | 3 |
| roman_empire | sage | 6 | 0.000 | 0.000 | 0.000 | 3 |
| roman_empire | sage | 12 | 0.000 | 0.000 | 0.000 | 3 |
| roman_empire | sage | 24 | 0.000 | 0.000 | 0.000 | 3 |

## 7. Calibration on fresh clusters (exact A/A contrasts; centred real contrasts secondary)

Marginal one-sided t size (pooled over elements):

| dataset | model | n | direction | alpha | tests | size | wilson_lo | wilson_hi | flag |
|---|---|---|---|---|---|---|---|---|---|
| roman_empire | gcn | 5 | adv | 0.0023 | 600 | 0.0033 | 0.0009 | 0.0121 | False |
| roman_empire | gcn | 5 | adv | 0.0100 | 600 | 0.0167 | 0.0091 | 0.0304 | False |
| roman_empire | gcn | 5 | adv | 0.0500 | 600 | 0.0550 | 0.0394 | 0.0762 | False |
| roman_empire | gcn | 5 | suf | 0.0023 | 600 | 0.0000 | 0.0000 | 0.0064 | False |
| roman_empire | gcn | 5 | suf | 0.0100 | 600 | 0.0017 | 0.0003 | 0.0094 | False |
| roman_empire | gcn | 5 | suf | 0.0500 | 600 | 0.0400 | 0.0270 | 0.0588 | False |
| roman_empire | gcn | 10 | adv | 0.0023 | 300 | 0.0000 | 0.0000 | 0.0126 | False |
| roman_empire | gcn | 10 | adv | 0.0100 | 300 | 0.0167 | 0.0071 | 0.0384 | False |
| roman_empire | gcn | 10 | adv | 0.0500 | 300 | 0.0667 | 0.0436 | 0.1007 | False |
| roman_empire | gcn | 10 | suf | 0.0023 | 300 | 0.0000 | 0.0000 | 0.0126 | False |
| roman_empire | gcn | 10 | suf | 0.0100 | 300 | 0.0133 | 0.0052 | 0.0338 | False |
| roman_empire | gcn | 10 | suf | 0.0500 | 300 | 0.0533 | 0.0331 | 0.0849 | False |
| roman_empire | gcn | 20 | adv | 0.0023 | 150 | 0.0000 | 0.0000 | 0.0250 | False |
| roman_empire | gcn | 20 | adv | 0.0100 | 150 | 0.0067 | 0.0012 | 0.0368 | False |
| roman_empire | gcn | 20 | adv | 0.0500 | 150 | 0.0667 | 0.0366 | 0.1184 | False |
| roman_empire | gcn | 20 | suf | 0.0023 | 150 | 0.0000 | 0.0000 | 0.0250 | False |
| roman_empire | gcn | 20 | suf | 0.0100 | 150 | 0.0133 | 0.0037 | 0.0473 | False |
| roman_empire | gcn | 20 | suf | 0.0500 | 150 | 0.0467 | 0.0228 | 0.0932 | False |
| roman_empire | gcn | 40 | adv | 0.0023 | 70 | 0.0000 | 0.0000 | 0.0520 | False |
| roman_empire | gcn | 40 | adv | 0.0100 | 70 | 0.0000 | 0.0000 | 0.0520 | False |
| roman_empire | gcn | 40 | adv | 0.0500 | 70 | 0.1000 | 0.0493 | 0.1923 | False |
| roman_empire | gcn | 40 | suf | 0.0023 | 70 | 0.0143 | 0.0025 | 0.0766 | True |
| roman_empire | gcn | 40 | suf | 0.0100 | 70 | 0.0143 | 0.0025 | 0.0766 | False |
| roman_empire | gcn | 40 | suf | 0.0500 | 70 | 0.0857 | 0.0399 | 0.1747 | False |
| roman_empire | gcn | 80 | adv | 0.0023 | 30 | 0.0000 | 0.0000 | 0.1135 | False |
| roman_empire | gcn | 80 | adv | 0.0100 | 30 | 0.0000 | 0.0000 | 0.1135 | False |
| roman_empire | gcn | 80 | adv | 0.0500 | 30 | 0.0667 | 0.0185 | 0.2132 | False |
| roman_empire | gcn | 80 | suf | 0.0023 | 30 | 0.0000 | 0.0000 | 0.1135 | False |
| roman_empire | gcn | 80 | suf | 0.0100 | 30 | 0.0667 | 0.0185 | 0.2132 | True |
| roman_empire | gcn | 80 | suf | 0.0500 | 30 | 0.1333 | 0.0531 | 0.2968 | True |
| roman_empire | sage | 5 | adv | 0.0023 | 600 | 0.0000 | 0.0000 | 0.0064 | False |
| roman_empire | sage | 5 | adv | 0.0100 | 600 | 0.0067 | 0.0026 | 0.0170 | False |
| roman_empire | sage | 5 | adv | 0.0500 | 600 | 0.0450 | 0.0311 | 0.0647 | False |
| roman_empire | sage | 5 | suf | 0.0023 | 600 | 0.0033 | 0.0009 | 0.0121 | False |
| roman_empire | sage | 5 | suf | 0.0100 | 600 | 0.0050 | 0.0017 | 0.0146 | False |
| roman_empire | sage | 5 | suf | 0.0500 | 600 | 0.0567 | 0.0408 | 0.0781 | False |
| roman_empire | sage | 10 | adv | 0.0023 | 300 | 0.0000 | 0.0000 | 0.0126 | False |
| roman_empire | sage | 10 | adv | 0.0100 | 300 | 0.0000 | 0.0000 | 0.0126 | False |
| roman_empire | sage | 10 | adv | 0.0500 | 300 | 0.0333 | 0.0182 | 0.0603 | False |
| roman_empire | sage | 10 | suf | 0.0023 | 300 | 0.0033 | 0.0006 | 0.0186 | False |
| roman_empire | sage | 10 | suf | 0.0100 | 300 | 0.0133 | 0.0052 | 0.0338 | False |
| roman_empire | sage | 10 | suf | 0.0500 | 300 | 0.0467 | 0.0280 | 0.0768 | False |
| roman_empire | sage | 20 | adv | 0.0023 | 150 | 0.0000 | 0.0000 | 0.0250 | False |
| roman_empire | sage | 20 | adv | 0.0100 | 150 | 0.0000 | 0.0000 | 0.0250 | False |
| roman_empire | sage | 20 | adv | 0.0500 | 150 | 0.0667 | 0.0366 | 0.1184 | False |
| roman_empire | sage | 20 | suf | 0.0023 | 150 | 0.0000 | 0.0000 | 0.0250 | False |
| roman_empire | sage | 20 | suf | 0.0100 | 150 | 0.0000 | 0.0000 | 0.0250 | False |
| roman_empire | sage | 20 | suf | 0.0500 | 150 | 0.0467 | 0.0228 | 0.0932 | False |
| roman_empire | sage | 40 | adv | 0.0023 | 70 | 0.0000 | 0.0000 | 0.0520 | False |
| roman_empire | sage | 40 | adv | 0.0100 | 70 | 0.0000 | 0.0000 | 0.0520 | False |
| roman_empire | sage | 40 | adv | 0.0500 | 70 | 0.0571 | 0.0224 | 0.1379 | False |
| roman_empire | sage | 40 | suf | 0.0023 | 70 | 0.0000 | 0.0000 | 0.0520 | False |
| roman_empire | sage | 40 | suf | 0.0100 | 70 | 0.0143 | 0.0025 | 0.0766 | False |
| roman_empire | sage | 40 | suf | 0.0500 | 70 | 0.0286 | 0.0079 | 0.0983 | False |
| roman_empire | sage | 80 | adv | 0.0023 | 30 | 0.0000 | 0.0000 | 0.1135 | False |
| roman_empire | sage | 80 | adv | 0.0100 | 30 | 0.0000 | 0.0000 | 0.1135 | False |
| roman_empire | sage | 80 | adv | 0.0500 | 30 | 0.0000 | 0.0000 | 0.1135 | False |
| roman_empire | sage | 80 | suf | 0.0023 | 30 | 0.0000 | 0.0000 | 0.1135 | False |
| roman_empire | sage | 80 | suf | 0.0100 | 30 | 0.0000 | 0.0000 | 0.1135 | False |
| roman_empire | sage | 80 | suf | 0.0500 | 30 | 0.0667 | 0.0185 | 0.2132 | False |
| amazon_ratings | gcn | 5 | adv | 0.0023 | 540 | 0.0019 | 0.0003 | 0.0104 | False |
| amazon_ratings | gcn | 5 | adv | 0.0100 | 540 | 0.0130 | 0.0063 | 0.0265 | False |
| amazon_ratings | gcn | 5 | adv | 0.0500 | 540 | 0.0593 | 0.0423 | 0.0825 | False |
| amazon_ratings | gcn | 5 | suf | 0.0023 | 540 | 0.0019 | 0.0003 | 0.0104 | False |
| amazon_ratings | gcn | 5 | suf | 0.0100 | 540 | 0.0074 | 0.0029 | 0.0189 | False |
| amazon_ratings | gcn | 5 | suf | 0.0500 | 540 | 0.0426 | 0.0285 | 0.0631 | False |
| amazon_ratings | gcn | 10 | adv | 0.0023 | 270 | 0.0000 | 0.0000 | 0.0140 | False |
| amazon_ratings | gcn | 10 | adv | 0.0100 | 270 | 0.0148 | 0.0058 | 0.0375 | False |
| amazon_ratings | gcn | 10 | adv | 0.0500 | 270 | 0.0667 | 0.0426 | 0.1029 | False |
| amazon_ratings | gcn | 10 | suf | 0.0023 | 270 | 0.0000 | 0.0000 | 0.0140 | False |
| amazon_ratings | gcn | 10 | suf | 0.0100 | 270 | 0.0074 | 0.0020 | 0.0266 | False |
| amazon_ratings | gcn | 10 | suf | 0.0500 | 270 | 0.0296 | 0.0151 | 0.0574 | False |
| amazon_ratings | gcn | 20 | adv | 0.0023 | 135 | 0.0000 | 0.0000 | 0.0277 | False |
| amazon_ratings | gcn | 20 | adv | 0.0100 | 135 | 0.0074 | 0.0013 | 0.0408 | False |
| amazon_ratings | gcn | 20 | adv | 0.0500 | 135 | 0.0519 | 0.0253 | 0.1032 | False |
| amazon_ratings | gcn | 20 | suf | 0.0023 | 135 | 0.0000 | 0.0000 | 0.0277 | False |
| amazon_ratings | gcn | 20 | suf | 0.0100 | 135 | 0.0000 | 0.0000 | 0.0277 | False |
| amazon_ratings | gcn | 20 | suf | 0.0500 | 135 | 0.0296 | 0.0116 | 0.0737 | False |
| amazon_ratings | gcn | 40 | adv | 0.0023 | 63 | 0.0000 | 0.0000 | 0.0575 | False |
| amazon_ratings | gcn | 40 | adv | 0.0100 | 63 | 0.0000 | 0.0000 | 0.0575 | False |
| amazon_ratings | gcn | 40 | adv | 0.0500 | 63 | 0.0317 | 0.0087 | 0.1086 | False |
| amazon_ratings | gcn | 40 | suf | 0.0023 | 63 | 0.0000 | 0.0000 | 0.0575 | False |
| amazon_ratings | gcn | 40 | suf | 0.0100 | 63 | 0.0000 | 0.0000 | 0.0575 | False |
| amazon_ratings | gcn | 40 | suf | 0.0500 | 63 | 0.0159 | 0.0028 | 0.0846 | False |
| amazon_ratings | gcn | 80 | adv | 0.0023 | 27 | 0.0000 | 0.0000 | 0.1246 | False |
| amazon_ratings | gcn | 80 | adv | 0.0100 | 27 | 0.0000 | 0.0000 | 0.1246 | False |
| amazon_ratings | gcn | 80 | adv | 0.0500 | 27 | 0.0741 | 0.0206 | 0.2337 | False |
| amazon_ratings | gcn | 80 | suf | 0.0023 | 27 | 0.0000 | 0.0000 | 0.1246 | False |
| amazon_ratings | gcn | 80 | suf | 0.0100 | 27 | 0.0000 | 0.0000 | 0.1246 | False |
| amazon_ratings | gcn | 80 | suf | 0.0500 | 27 | 0.0000 | 0.0000 | 0.1246 | False |
| amazon_ratings | sage | 5 | adv | 0.0023 | 540 | 0.0000 | 0.0000 | 0.0071 | False |
| amazon_ratings | sage | 5 | adv | 0.0100 | 540 | 0.0093 | 0.0040 | 0.0215 | False |
| amazon_ratings | sage | 5 | adv | 0.0500 | 540 | 0.0463 | 0.0316 | 0.0674 | False |
| amazon_ratings | sage | 5 | suf | 0.0023 | 540 | 0.0019 | 0.0003 | 0.0104 | False |
| amazon_ratings | sage | 5 | suf | 0.0100 | 540 | 0.0074 | 0.0029 | 0.0189 | False |
| amazon_ratings | sage | 5 | suf | 0.0500 | 540 | 0.0481 | 0.0331 | 0.0696 | False |
| amazon_ratings | sage | 10 | adv | 0.0023 | 270 | 0.0000 | 0.0000 | 0.0140 | False |
| amazon_ratings | sage | 10 | adv | 0.0100 | 270 | 0.0074 | 0.0020 | 0.0266 | False |
| amazon_ratings | sage | 10 | adv | 0.0500 | 270 | 0.0481 | 0.0284 | 0.0806 | False |
| amazon_ratings | sage | 10 | suf | 0.0023 | 270 | 0.0037 | 0.0007 | 0.0207 | False |
| amazon_ratings | sage | 10 | suf | 0.0100 | 270 | 0.0074 | 0.0020 | 0.0266 | False |
| amazon_ratings | sage | 10 | suf | 0.0500 | 270 | 0.0556 | 0.0340 | 0.0896 | False |
| amazon_ratings | sage | 20 | adv | 0.0023 | 135 | 0.0000 | 0.0000 | 0.0277 | False |
| amazon_ratings | sage | 20 | adv | 0.0100 | 135 | 0.0000 | 0.0000 | 0.0277 | False |
| amazon_ratings | sage | 20 | adv | 0.0500 | 135 | 0.0444 | 0.0205 | 0.0936 | False |
| amazon_ratings | sage | 20 | suf | 0.0023 | 135 | 0.0000 | 0.0000 | 0.0277 | False |
| amazon_ratings | sage | 20 | suf | 0.0100 | 135 | 0.0000 | 0.0000 | 0.0277 | False |
| amazon_ratings | sage | 20 | suf | 0.0500 | 135 | 0.0296 | 0.0116 | 0.0737 | False |
| amazon_ratings | sage | 40 | adv | 0.0023 | 63 | 0.0000 | 0.0000 | 0.0575 | False |
| amazon_ratings | sage | 40 | adv | 0.0100 | 63 | 0.0000 | 0.0000 | 0.0575 | False |
| amazon_ratings | sage | 40 | adv | 0.0500 | 63 | 0.0159 | 0.0028 | 0.0846 | False |
| amazon_ratings | sage | 40 | suf | 0.0023 | 63 | 0.0000 | 0.0000 | 0.0575 | False |
| amazon_ratings | sage | 40 | suf | 0.0100 | 63 | 0.0000 | 0.0000 | 0.0575 | False |
| amazon_ratings | sage | 40 | suf | 0.0500 | 63 | 0.0476 | 0.0163 | 0.1309 | False |
| amazon_ratings | sage | 80 | adv | 0.0023 | 27 | 0.0000 | 0.0000 | 0.1246 | False |
| amazon_ratings | sage | 80 | adv | 0.0100 | 27 | 0.0000 | 0.0000 | 0.1246 | False |
| amazon_ratings | sage | 80 | adv | 0.0500 | 27 | 0.0370 | 0.0066 | 0.1828 | False |
| amazon_ratings | sage | 80 | suf | 0.0023 | 27 | 0.0000 | 0.0000 | 0.1246 | False |
| amazon_ratings | sage | 80 | suf | 0.0100 | 27 | 0.0000 | 0.0000 | 0.1246 | False |
| amazon_ratings | sage | 80 | suf | 0.0500 | 27 | 0.0370 | 0.0066 | 0.1828 | False |

Worst-case FWER of certifications (all elements at Delta = delta):

| dataset | model | procedure | n_or_b | scheme | source | groups | fwer | false_adv | false_suf | wilson_lo | wilson_hi | flag |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| roman_empire | gcn | craf | 20 | disjoint | aa | 15 | 0.000 | 0.000 | 0.000 | 0.000 | 0.204 | False |
| roman_empire | gcn | craf | 40 | disjoint | aa | 7 | 0.143 | 0.000 | 0.143 | 0.026 | 0.513 | False |
| roman_empire | gcn | craf | 80 | disjoint | aa | 3 | 0.000 | 0.000 | 0.000 | 0.000 | 0.561 | False |
| roman_empire | gcn | craf_adaptive | 20 | disjoint | aa | 3 | 0.000 | 0.000 | 0.000 | 0.000 | 0.561 | False |
| roman_empire | gcn | craf_adaptive | 40 | disjoint | aa | 3 | 0.000 | 0.000 | 0.000 | 0.000 | 0.561 | False |
| roman_empire | gcn | craf_adaptive | 80 | disjoint | aa | 3 | 0.333 | 0.000 | 0.333 | 0.061 | 0.792 | True |
| roman_empire | gcn | craf | 20 | disjoint | centred | 15 | 0.000 | 0.000 | 0.000 | 0.000 | 0.204 | False |
| roman_empire | gcn | craf | 40 | disjoint | centred | 7 | 0.000 | 0.000 | 0.000 | 0.000 | 0.354 | False |
| roman_empire | gcn | craf | 80 | disjoint | centred | 3 | 0.000 | 0.000 | 0.000 | 0.000 | 0.561 | False |
| roman_empire | gcn | craf_adaptive | 20 | disjoint | centred | 3 | 0.000 | 0.000 | 0.000 | 0.000 | 0.561 | False |
| roman_empire | gcn | craf_adaptive | 40 | disjoint | centred | 3 | 0.000 | 0.000 | 0.000 | 0.000 | 0.561 | False |
| roman_empire | gcn | craf_adaptive | 80 | disjoint | centred | 3 | 0.000 | 0.000 | 0.000 | 0.000 | 0.561 | False |
| roman_empire | sage | craf | 20 | disjoint | aa | 15 | 0.000 | 0.000 | 0.000 | 0.000 | 0.204 | False |
| roman_empire | sage | craf | 40 | disjoint | aa | 7 | 0.000 | 0.000 | 0.000 | 0.000 | 0.354 | False |
| roman_empire | sage | craf | 80 | disjoint | aa | 3 | 0.000 | 0.000 | 0.000 | 0.000 | 0.561 | False |
| roman_empire | sage | craf_adaptive | 20 | disjoint | aa | 3 | 0.000 | 0.000 | 0.000 | 0.000 | 0.561 | False |
| roman_empire | sage | craf_adaptive | 40 | disjoint | aa | 3 | 0.000 | 0.000 | 0.000 | 0.000 | 0.561 | False |
| roman_empire | sage | craf_adaptive | 80 | disjoint | aa | 3 | 0.000 | 0.000 | 0.000 | 0.000 | 0.561 | False |
| roman_empire | sage | craf | 20 | disjoint | centred | 15 | 0.000 | 0.000 | 0.000 | 0.000 | 0.204 | False |
| roman_empire | sage | craf | 40 | disjoint | centred | 7 | 0.000 | 0.000 | 0.000 | 0.000 | 0.354 | False |
| roman_empire | sage | craf | 80 | disjoint | centred | 3 | 0.000 | 0.000 | 0.000 | 0.000 | 0.561 | False |
| roman_empire | sage | craf_adaptive | 20 | disjoint | centred | 3 | 0.000 | 0.000 | 0.000 | 0.000 | 0.561 | False |
| roman_empire | sage | craf_adaptive | 40 | disjoint | centred | 3 | 0.000 | 0.000 | 0.000 | 0.000 | 0.561 | False |
| roman_empire | sage | craf_adaptive | 80 | disjoint | centred | 3 | 0.000 | 0.000 | 0.000 | 0.000 | 0.561 | False |
| amazon_ratings | gcn | craf | 20 | disjoint | aa | 15 | 0.000 | 0.000 | 0.000 | 0.000 | 0.204 | False |
| amazon_ratings | gcn | craf | 40 | disjoint | aa | 7 | 0.000 | 0.000 | 0.000 | 0.000 | 0.354 | False |
| amazon_ratings | gcn | craf | 80 | disjoint | aa | 3 | 0.000 | 0.000 | 0.000 | 0.000 | 0.561 | False |
| amazon_ratings | gcn | craf_adaptive | 20 | disjoint | aa | 3 | 0.000 | 0.000 | 0.000 | 0.000 | 0.561 | False |
| amazon_ratings | gcn | craf_adaptive | 40 | disjoint | aa | 3 | 0.000 | 0.000 | 0.000 | 0.000 | 0.561 | False |
| amazon_ratings | gcn | craf_adaptive | 80 | disjoint | aa | 3 | 0.000 | 0.000 | 0.000 | 0.000 | 0.561 | False |
| amazon_ratings | gcn | craf | 20 | disjoint | centred | 15 | 0.000 | 0.000 | 0.000 | 0.000 | 0.204 | False |
| amazon_ratings | gcn | craf | 40 | disjoint | centred | 7 | 0.000 | 0.000 | 0.000 | 0.000 | 0.354 | False |
| amazon_ratings | gcn | craf | 80 | disjoint | centred | 3 | 0.000 | 0.000 | 0.000 | 0.000 | 0.561 | False |
| amazon_ratings | gcn | craf_adaptive | 20 | disjoint | centred | 3 | 0.000 | 0.000 | 0.000 | 0.000 | 0.561 | False |
| amazon_ratings | gcn | craf_adaptive | 40 | disjoint | centred | 3 | 0.000 | 0.000 | 0.000 | 0.000 | 0.561 | False |
| amazon_ratings | gcn | craf_adaptive | 80 | disjoint | centred | 3 | 0.000 | 0.000 | 0.000 | 0.000 | 0.561 | False |
| amazon_ratings | sage | craf | 20 | disjoint | aa | 15 | 0.000 | 0.000 | 0.000 | 0.000 | 0.204 | False |
| amazon_ratings | sage | craf | 40 | disjoint | aa | 7 | 0.000 | 0.000 | 0.000 | 0.000 | 0.354 | False |
| amazon_ratings | sage | craf | 80 | disjoint | aa | 3 | 0.000 | 0.000 | 0.000 | 0.000 | 0.561 | False |
| amazon_ratings | sage | craf_adaptive | 20 | disjoint | aa | 3 | 0.000 | 0.000 | 0.000 | 0.000 | 0.561 | False |
| amazon_ratings | sage | craf_adaptive | 40 | disjoint | aa | 3 | 0.000 | 0.000 | 0.000 | 0.000 | 0.561 | False |
| amazon_ratings | sage | craf_adaptive | 80 | disjoint | aa | 3 | 0.000 | 0.000 | 0.000 | 0.000 | 0.561 | False |
| amazon_ratings | sage | craf | 20 | disjoint | centred | 15 | 0.000 | 0.000 | 0.000 | 0.000 | 0.204 | False |
| amazon_ratings | sage | craf | 40 | disjoint | centred | 7 | 0.000 | 0.000 | 0.000 | 0.000 | 0.354 | False |
| amazon_ratings | sage | craf | 80 | disjoint | centred | 3 | 0.000 | 0.000 | 0.000 | 0.000 | 0.561 | False |
| amazon_ratings | sage | craf_adaptive | 20 | disjoint | centred | 3 | 0.000 | 0.000 | 0.000 | 0.000 | 0.561 | False |
| amazon_ratings | sage | craf_adaptive | 40 | disjoint | centred | 3 | 0.000 | 0.000 | 0.000 | 0.000 | 0.561 | False |
| amazon_ratings | sage | craf_adaptive | 80 | disjoint | centred | 3 | 0.000 | 0.000 | 0.000 | 0.000 | 0.561 | False |

## 8. Natural structure (reference clusters)

Certified non-monotone pairs (Delta_T > Delta_S for S ⊊ T; Holm over pairs): 11; with margin delta: 0.

| dataset | model | S | T | diff | se | p_nonmono_holm | certified_nonmono_delta |
|---|---|---|---|---|---|---|---|
| roman_empire | gcn | degree | strat:block | 0.0017 | 0.0001 | 0.0000 | False |
| roman_empire | gcn | degree | strat:clust | 0.0004 | 0.0001 | 0.0000 | False |
| roman_empire | gcn | degree | strat:block+clust | 0.0022 | 0.0001 | 0.0000 | False |
| roman_empire | gcn | strat:block | strat:block+clust | 0.0005 | 0.0001 | 0.0000 | False |
| roman_empire | gcn | strat:clust | strat:block+clust | 0.0017 | 0.0001 | 0.0000 | False |
| roman_empire | gcn | strat:fsim | strat:block+fsim | 0.0013 | 0.0001 | 0.0000 | False |
| roman_empire | gcn | strat:hop2 | strat:block+hop2 | 0.0016 | 0.0001 | 0.0000 | False |
| roman_empire | gcn | degree | strat:clust+fsim | 0.0012 | 0.0001 | 0.0000 | False |
| roman_empire | gcn | strat:clust | strat:clust+fsim | 0.0007 | 0.0001 | 0.0000 | False |
| roman_empire | gcn | strat:fsim | strat:clust+fsim | 0.0034 | 0.0001 | 0.0000 | False |
| roman_empire | gcn | strat:hop2 | strat:clust+hop2 | 0.0016 | 0.0001 | 0.0000 | False |

Largest estimated violations of monotonicity per cell:

| dataset | model | S | T | diff | se | p_nonmono_holm |
|---|---|---|---|---|---|---|
| roman_empire | gcn | strat:fsim | strat:clust+fsim | 0.0034 | 0.0001 | 0.0000 |
| roman_empire | gcn | degree | strat:block+clust | 0.0022 | 0.0001 | 0.0000 |
| roman_empire | gcn | strat:clust | strat:block+clust | 0.0017 | 0.0001 | 0.0000 |
| amazon_ratings | sage | strat:block | strat:block+hop2 | -0.0001 | 0.0000 | 1.0000 |
| amazon_ratings | sage | strat:block | strat:block+clust | -0.0002 | 0.0000 | 1.0000 |
| roman_empire | sage | degree | strat:block | -0.0002 | 0.0000 | 1.0000 |
| amazon_ratings | gcn | strat:block | strat:block+hop2 | -0.0002 | 0.0000 | 1.0000 |
| roman_empire | sage | strat:clust | strat:block+clust | -0.0002 | 0.0000 | 1.0000 |
| amazon_ratings | sage | strat:hop2 | strat:clust+hop2 | -0.0003 | 0.0000 | 1.0000 |
| roman_empire | sage | strat:hop2 | strat:block+hop2 | -0.0004 | 0.0000 | 1.0000 |
| amazon_ratings | gcn | strat:block | strat:block+clust | -0.0005 | 0.0000 | 1.0000 |
| amazon_ratings | gcn | strat:clust | strat:clust+hop2 | -0.0006 | 0.0000 | 1.0000 |

Pairwise interactions I_ab = Delta_∅ − Delta_a − Delta_b + Delta_ab (two-sided, Holm):

| dataset | model | element | interaction | se | p_holm | significant |
|---|---|---|---|---|---|---|
| roman_empire | gcn | strat:block+clust | 0.0001 | 0.0001 | 1.0000 | False |
| roman_empire | gcn | strat:block+fsim | -0.0004 | 0.0001 | 0.0001 | True |
| roman_empire | gcn | strat:block+hop2 | -0.0000 | 0.0001 | 1.0000 | False |
| roman_empire | gcn | strat:clust+fsim | 0.0030 | 0.0001 | 0.0000 | True |
| roman_empire | gcn | strat:clust+hop2 | 0.0011 | 0.0001 | 0.0000 | True |
| roman_empire | gcn | strat:fsim+hop2 |  |  | 1.0000 | False |
| roman_empire | sage | strat:block+clust | -0.0001 | 0.0000 | 0.2888 | False |
| roman_empire | sage | strat:block+fsim | -0.0003 | 0.0000 | 0.0000 | True |
| roman_empire | sage | strat:block+hop2 | -0.0003 | 0.0000 | 0.0000 | True |
| roman_empire | sage | strat:clust+fsim | -0.0041 | 0.0000 | 0.0000 | True |
| roman_empire | sage | strat:clust+hop2 | -0.0007 | 0.0000 | 0.0000 | True |
| roman_empire | sage | strat:fsim+hop2 |  |  | 1.0000 | False |
| amazon_ratings | gcn | strat:block+clust | 0.0006 | 0.0000 | 0.0000 | True |
| amazon_ratings | gcn | strat:block+fsim | 0.0007 | 0.0000 | 0.0000 | True |
| amazon_ratings | gcn | strat:block+hop2 | 0.0005 | 0.0000 | 0.0000 | True |
| amazon_ratings | gcn | strat:clust+fsim |  |  | 1.0000 | False |
| amazon_ratings | gcn | strat:clust+hop2 | 0.0001 | 0.0000 | 0.0017 | True |
| amazon_ratings | gcn | strat:fsim+hop2 |  |  | 1.0000 | False |
| amazon_ratings | sage | strat:block+clust | 0.0002 | 0.0000 | 0.0000 | True |
| amazon_ratings | sage | strat:block+fsim | 0.0001 | 0.0000 | 0.0159 | True |
| amazon_ratings | sage | strat:block+hop2 | 0.0003 | 0.0000 | 0.0000 | True |
| amazon_ratings | sage | strat:clust+fsim |  |  | 1.0000 | False |
| amazon_ratings | sage | strat:clust+hop2 | 0.0000 | 0.0000 | 1.0000 | False |
| amazon_ratings | sage | strat:fsim+hop2 |  |  | 1.0000 | False |

Architecture differences Delta^gcn − Delta^sage (paired; Holm):

| dataset | element | diff | se | p_holm | significant |
|---|---|---|---|---|---|
| roman_empire | empty | -0.1886 | 0.0001 | 0.0000 | True |
| roman_empire | degree | -0.0773 | 0.0001 | 0.0000 | True |
| roman_empire | strat:block | -0.0755 | 0.0001 | 0.0000 | True |
| roman_empire | strat:clust | -0.0755 | 0.0001 | 0.0000 | True |
| roman_empire | strat:fsim | -0.0443 | 0.0001 | 0.0000 | True |
| roman_empire | strat:hop2 | -0.0781 | 0.0001 | 0.0000 | True |
| roman_empire | strat:block+clust | -0.0735 | 0.0001 | 0.0000 | True |
| roman_empire | strat:block+fsim | -0.0425 | 0.0001 | 0.0000 | True |
| roman_empire | strat:block+hop2 | -0.0761 | 0.0001 | 0.0000 | True |
| roman_empire | strat:clust+fsim | -0.0354 | 0.0001 | 0.0000 | True |
| roman_empire | strat:clust+hop2 | -0.0745 | 0.0001 | 0.0000 | True |
| roman_empire | strat:fsim+hop2 |  |  | 1.0000 | False |
| amazon_ratings | empty | -0.0060 | 0.0001 | 0.0000 | True |
| amazon_ratings | degree | 0.0004 | 0.0001 | 0.0000 | True |
| amazon_ratings | strat:block | -0.0017 | 0.0000 | 0.0000 | True |
| amazon_ratings | strat:clust | -0.0003 | 0.0001 | 0.0000 | True |
| amazon_ratings | strat:fsim | 0.0001 | 0.0000 | 0.0137 | True |
| amazon_ratings | strat:hop2 | 0.0002 | 0.0001 | 0.0137 | True |
| amazon_ratings | strat:block+clust | -0.0020 | 0.0000 | 0.0000 | True |
| amazon_ratings | strat:block+fsim | -0.0013 | 0.0000 | 0.0000 | True |
| amazon_ratings | strat:block+hop2 | -0.0018 | 0.0000 | 0.0000 | True |
| amazon_ratings | strat:clust+fsim |  |  | 1.0000 | False |
| amazon_ratings | strat:clust+hop2 | -0.0005 | 0.0001 | 0.0000 | True |
| amazon_ratings | strat:fsim+hop2 |  |  | 1.0000 | False |

Attribute–label association, roman_empire (descriptive, post hoc; never used upstream):

| attribute | nmi_with_labels | edge_homophily_attr |
|---|---|---|
| block | 0.004 | 1.000 |
| fsim | 0.384 | 0.109 |
| clust | 0.157 | 0.416 |
| hop2 | 0.067 | 0.413 |
| LABEL (reference) | 1.000 | 0.047 |

Attribute–label association, amazon_ratings (descriptive, post hoc; never used upstream):

| attribute | nmi_with_labels | edge_homophily_attr |
|---|---|---|
| block | 0.026 | 0.985 |
| fsim | 0.003 | 0.203 |
| clust | 0.003 | 0.368 |
| hop2 | 0.003 | 0.588 |
| LABEL (reference) | 1.000 | 0.380 |

## 9. Computational cost (CPU seconds per fit / per null draw, single thread)

| variant | fit_seconds | gen_seconds | n_rows | valid_rate | dataset | model |
|---|---|---|---|---|---|---|
| degree | 69.496 | 0.534 | 800.000 | 1.000 | roman_empire | gcn |
| empty | 60.206 | 0.000 | 400.000 | 1.000 | roman_empire | gcn |
| er | 68.554 | 0.024 | 400.000 | 1.000 | roman_empire | gcn |
| real | 62.570 | 0.000 | 400.000 | 1.000 | roman_empire | gcn |
| strat:block | 69.332 | 0.185 | 800.000 | 1.000 | roman_empire | gcn |
| strat:block+clust | 69.061 | 0.199 | 800.000 | 1.000 | roman_empire | gcn |
| strat:block+fsim | 69.012 | 0.770 | 800.000 | 1.000 | roman_empire | gcn |
| strat:block+hop2 | 69.536 | 0.207 | 800.000 | 1.000 | roman_empire | gcn |
| strat:clust | 69.672 | 0.211 | 800.000 | 1.000 | roman_empire | gcn |
| strat:clust+fsim | 69.256 | 2.822 | 800.000 | 1.000 | roman_empire | gcn |
| strat:clust+hop2 | 69.828 | 0.360 | 800.000 | 1.000 | roman_empire | gcn |
| strat:fsim | 69.596 | 0.726 | 800.000 | 1.000 | roman_empire | gcn |
| strat:fsim+hop2 |  | 3.415 | 800.000 | 0.000 | roman_empire | gcn |
| strat:hop2 | 69.504 | 0.212 | 800.000 | 1.000 | roman_empire | gcn |
| mlp | 55.968 | 0.000 | 400.000 | 1.000 | roman_empire | gcn |
| degree | 89.794 | 0.534 | 800.000 | 1.000 | roman_empire | sage |
| empty | 76.010 | 0.000 | 400.000 | 1.000 | roman_empire | sage |
| er | 88.956 | 0.024 | 400.000 | 1.000 | roman_empire | sage |
| real | 80.697 | 0.000 | 400.000 | 1.000 | roman_empire | sage |
| strat:block | 89.221 | 0.185 | 800.000 | 1.000 | roman_empire | sage |
| strat:block+clust | 88.731 | 0.199 | 800.000 | 1.000 | roman_empire | sage |
| strat:block+fsim | 88.450 | 0.770 | 800.000 | 1.000 | roman_empire | sage |
| strat:block+hop2 | 88.349 | 0.207 | 800.000 | 1.000 | roman_empire | sage |
| strat:clust | 89.731 | 0.211 | 800.000 | 1.000 | roman_empire | sage |
| strat:clust+fsim | 88.489 | 2.822 | 800.000 | 1.000 | roman_empire | sage |
| strat:clust+hop2 | 87.046 | 0.360 | 800.000 | 1.000 | roman_empire | sage |
| strat:fsim | 89.094 | 0.726 | 800.000 | 1.000 | roman_empire | sage |
| strat:fsim+hop2 |  | 3.415 | 800.000 | 0.000 | roman_empire | sage |
| strat:hop2 | 89.246 | 0.212 | 800.000 | 1.000 | roman_empire | sage |
| mlp | 55.968 | 0.000 | 400.000 | 1.000 | roman_empire | sage |
| degree | 83.578 | 0.692 | 800.000 | 1.000 | amazon_ratings | gcn |
| empty | 62.301 | 0.000 | 400.000 | 1.000 | amazon_ratings | gcn |
| er | 83.406 | 0.073 | 400.000 | 1.000 | amazon_ratings | gcn |
| real | 84.493 | 0.000 | 400.000 | 1.000 | amazon_ratings | gcn |
| strat:block | 85.786 | 0.338 | 800.000 | 1.000 | amazon_ratings | gcn |
| strat:block+clust | 85.785 | 0.493 | 800.000 | 1.000 | amazon_ratings | gcn |
| strat:block+fsim | 86.113 | 2.431 | 800.000 | 1.000 | amazon_ratings | gcn |
| strat:block+hop2 | 86.730 | 0.435 | 800.000 | 1.000 | amazon_ratings | gcn |
| strat:clust | 84.567 | 0.429 | 800.000 | 1.000 | amazon_ratings | gcn |
| strat:clust+fsim |  | 11.347 | 800.000 | 0.000 | amazon_ratings | gcn |
| strat:clust+hop2 | 86.994 | 0.959 | 800.000 | 1.000 | amazon_ratings | gcn |
| strat:fsim | 84.733 | 1.770 | 800.000 | 1.000 | amazon_ratings | gcn |
| strat:fsim+hop2 |  | 11.303 | 800.000 | 0.000 | amazon_ratings | gcn |
| strat:hop2 | 84.169 | 0.385 | 800.000 | 1.000 | amazon_ratings | gcn |
| mlp | 59.302 | 0.000 | 400.000 | 1.000 | amazon_ratings | gcn |
| degree | 107.150 | 0.692 | 800.000 | 1.000 | amazon_ratings | sage |
| empty | 77.692 | 0.000 | 400.000 | 1.000 | amazon_ratings | sage |
| er | 107.372 | 0.073 | 400.000 | 1.000 | amazon_ratings | sage |
| real | 111.326 | 0.000 | 400.000 | 1.000 | amazon_ratings | sage |
| strat:block | 110.190 | 0.338 | 800.000 | 1.000 | amazon_ratings | sage |
| strat:block+clust | 109.384 | 0.493 | 800.000 | 1.000 | amazon_ratings | sage |
| strat:block+fsim | 108.708 | 2.431 | 800.000 | 1.000 | amazon_ratings | sage |
| strat:block+hop2 | 101.663 | 0.435 | 800.000 | 1.000 | amazon_ratings | sage |
| strat:clust | 106.292 | 0.429 | 800.000 | 1.000 | amazon_ratings | sage |
| strat:clust+fsim |  | 11.347 | 800.000 | 0.000 | amazon_ratings | sage |
| strat:clust+hop2 | 92.293 | 0.959 | 800.000 | 1.000 | amazon_ratings | sage |
| strat:fsim | 110.108 | 1.770 | 800.000 | 1.000 | amazon_ratings | sage |
| strat:fsim+hop2 |  | 11.303 | 800.000 | 0.000 | amazon_ratings | sage |
| strat:hop2 | 106.753 | 0.385 | 800.000 | 1.000 | amazon_ratings | sage |
| mlp | 59.302 | 0.000 | 400.000 | 1.000 | amazon_ratings | sage |

| dataset | model | cpu_s_per_replicate(real+|L| nulls) | craf_b80_cpu_hours | craf_b20_cpu_hours |
|---|---|---|---|---|
| amazon_ratings | gcn |  |  |  |
| amazon_ratings | sage |  |  |  |
| roman_empire | gcn |  |  |  |
| roman_empire | sage |  |  |  |

## 10. Decision inputs (rules R1–R4 of the protocol)

```
{
 "R2": {
  "roman_empire": true,
  "amazon_ratings": true
 },
 "R1": {
  "no_fwer_flag_primary": false,
  "no_marginal_flag_alpha05": false
 },
 "R4": {
  "amazon_ratings/gcn": false,
  "amazon_ratings/sage": false,
  "roman_empire/gcn": false,
  "roman_empire/sage": false
 },
 "R3": {
  "amazon_ratings/gcn": {
   "certified_member_outside_pcga_ladder": false,
   "ni_holm_differs_from_craf": false,
   "certified_specificity_over_L": false
  },
  "amazon_ratings/sage": {
   "certified_member_outside_pcga_ladder": false,
   "ni_holm_differs_from_craf": false,
   "certified_specificity_over_L": false
  },
  "roman_empire/gcn": {
   "certified_member_outside_pcga_ladder": false,
   "ni_holm_differs_from_craf": false,
   "certified_specificity_over_L": false
  },
  "roman_empire/sage": {
   "certified_member_outside_pcga_ladder": false,
   "ni_holm_differs_from_craf": false,
   "certified_specificity_over_L": false
  }
 },
 "natural_nonmonotonicity_certified": true
}
```
