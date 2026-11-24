# phase3a report (generated from outputs/phase3a/analysis)

## True frontiers (Monte Carlo truths; A/A elements exact 0)

| pool | |L| | F_true | n_sufficient | min_delta | closest_to_margin | nonmonotone_pairs |
|---|---|---|---|---|---|---|
| N6_hard__sgc_ridge | 16 | strat:w3 | 5 | -0.0000 | strat:w2+w3=0.0001; strat:w1+w3=0.0001; strat:block+w3=0.0000 | 0 |
| P3_multi__sgc_ridge | 16 | strat:w1+w2|strat:w3 | 6 | -0.0001 | strat:block+w3=0.0001; strat:w1+w2=0.0000; strat:w2+w3=-0.0000 | 0 |
| S7_easy__sgc_ridge | 16 | strat:w1+w2 | 1 | 0.0000 | strat:w1+w2=0.0000; strat:block+w2=0.0260; strat:block+w1=0.0261 | 0 |
| S7_hard__sage | 16 | strat:w1+w2 | 1 | 0.0000 | strat:w1+w2=0.0000; strat:block+w3=0.0143; strat:w2+w3=0.0147 | 0 |
| S7_hard__sgc_ridge | 16 | strat:w1+w2 | 1 | 0.0000 | strat:w1+w2=0.0000; strat:block+w3=0.0109; strat:w2+w3=0.0112 | 0 |
| S8_small_hard__sgc_ridge | 16 | ∅ (none sufficient) | 0 | 0.0106 | strat:w1+w2=0.0106; strat:block+w3=0.0205; strat:w1+w3=0.0208 | 0 |
| SS_boundary__semisynthetic | 7 | ∅ (none sufficient) | 0 | 0.0050 | degree=0.0050; strat:a=0.0050; strat:b=0.0050 | 0 |
| SS_near__semisynthetic | 7 | strat:a+b|strat:c | 4 | 0.0000 | strat:a=0.0080; strat:c=0.0020; strat:a+c=0.0020 | 0 |
| SS_nonmono_A__semisynthetic | 7 | degree | 2 | 0.0000 | degree=0.0000; strat:a+b=0.0000; strat:a=0.0200 | 5 |
| SS_nonmono_B__semisynthetic | 7 | strat:a|strat:b+c | 3 | 0.0000 | strat:a=0.0000; strat:a+c=0.0000; strat:b+c=0.0000 | 1 |

## Exact frontier recovery: reported frontier == true frontier

| role | scenario | model | b | craf | craf_adaptive | craf_children | ni_holm | factorial_unadj | naive_point | pcga_l |
|---|---|---|---|---|---|---|---|---|---|---|
| interaction_easy | S7_easy | sgc_ridge | 20 | 0.097 | 0.229 | 0.097 | 0.111 | 0.472 | 0.951 | 0.000 |
| interaction_easy | S7_easy | sgc_ridge | 40 | 0.375 | 0.771 | 0.375 | 0.389 | 0.757 | 0.993 | 0.000 |
| interaction_easy | S7_easy | sgc_ridge | 80 | 0.708 | 0.854 | 0.708 | 0.715 | 0.958 | 1.000 | 0.000 |
| interaction_isolated | S7_hard | sgc_ridge | 20 | 0.097 | 0.167 | 0.097 | 0.125 | 0.535 | 0.861 | 0.000 |
| interaction_isolated | S7_hard | sgc_ridge | 40 | 0.375 | 0.660 | 0.375 | 0.410 | 0.806 | 0.986 | 0.000 |
| interaction_isolated | S7_hard | sgc_ridge | 80 | 0.792 | 0.924 | 0.792 | 0.792 | 0.986 | 1.000 | 0.000 |
| many_sufficient_one_minimal | N6_hard | sgc_ridge | 20 | 0.118 | 0.167 | 0.118 | 0.167 | 0.611 | 0.910 | 0.000 |
| many_sufficient_one_minimal | N6_hard | sgc_ridge | 40 | 0.389 | 0.535 | 0.389 | 0.410 | 0.785 | 0.972 | 0.000 |
| many_sufficient_one_minimal | N6_hard | sgc_ridge | 80 | 0.736 | 0.896 | 0.736 | 0.806 | 0.979 | 1.000 | 0.000 |
| multiple_minimal | P3_multi | sgc_ridge | 20 | 0.125 | 0.111 | 0.125 | 0.167 | 0.556 | 0.944 | 0.000 |
| multiple_minimal | P3_multi | sgc_ridge | 40 | 0.292 | 0.778 | 0.292 | 0.417 | 0.778 | 1.000 | 0.000 |
| multiple_minimal | P3_multi | sgc_ridge | 80 | 0.875 | 0.944 | 0.875 | 0.903 | 1.000 | 1.000 | 0.000 |
| near_boundary | SS_near | semisynthetic | 20 | 0.002 | 0.002 | 0.002 | 0.030 | 0.053 | 0.735 |  |
| near_boundary | SS_near | semisynthetic | 40 | 0.011 | 0.029 | 0.011 | 0.123 | 0.197 | 0.895 |  |
| near_boundary | SS_near | semisynthetic | 80 | 0.126 | 0.200 | 0.126 | 0.408 | 0.500 | 0.979 |  |
| neural_interaction | S7_hard | sage | 20 | 0.250 | 0.458 | 0.250 | 0.292 | 0.611 | 0.958 | 0.000 |
| neural_interaction | S7_hard | sage | 40 | 0.611 | 0.861 | 0.611 | 0.625 | 0.847 | 1.000 | 0.000 |
| neural_interaction | S7_hard | sage | 80 | 0.806 | 0.958 | 0.806 | 0.806 | 0.986 | 1.000 | 0.000 |
| no_sufficient | S8_small_hard | sgc_ridge | 20 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.958 | 1.000 |
| no_sufficient | S8_small_hard | sgc_ridge | 40 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| no_sufficient | S8_small_hard | sgc_ridge | 80 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| nonmonotone_empty_sufficient | SS_nonmono_A | semisynthetic | 20 | 0.232 | 0.403 | 0.168 | 0.271 | 0.584 | 0.978 |  |
| nonmonotone_empty_sufficient | SS_nonmono_A | semisynthetic | 40 | 0.530 | 0.834 | 0.237 | 0.570 | 0.840 | 0.994 |  |
| nonmonotone_empty_sufficient | SS_nonmono_A | semisynthetic | 80 | 0.880 | 0.944 | 0.106 | 0.898 | 0.981 | 1.000 |  |
| nonmonotone_two_minimal | SS_nonmono_B | semisynthetic | 20 | 0.052 | 0.093 | 0.052 | 0.083 | 0.346 | 0.938 |  |
| nonmonotone_two_minimal | SS_nonmono_B | semisynthetic | 40 | 0.273 | 0.542 | 0.273 | 0.347 | 0.688 | 0.995 |  |
| nonmonotone_two_minimal | SS_nonmono_B | semisynthetic | 80 | 0.756 | 0.888 | 0.756 | 0.813 | 0.957 | 1.000 |  |
| worst_case_fwer | SS_boundary | semisynthetic | 20 | 0.999 | 0.997 | 0.999 | 0.959 | 0.943 | 0.007 |  |
| worst_case_fwer | SS_boundary | semisynthetic | 40 | 0.996 | 0.997 | 0.996 | 0.952 | 0.938 | 0.008 |  |
| worst_case_fwer | SS_boundary | semisynthetic | 80 | 0.996 | 0.997 | 0.996 | 0.953 | 0.938 | 0.011 |  |

## False frontier member: some reported element is not truly minimal sufficient

| role | scenario | model | b | craf | craf_adaptive | craf_children | ni_holm | factorial_unadj | naive_point | pcga_l |
|---|---|---|---|---|---|---|---|---|---|---|
| interaction_easy | S7_easy | sgc_ridge | 20 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| interaction_easy | S7_easy | sgc_ridge | 40 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| interaction_easy | S7_easy | sgc_ridge | 80 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| interaction_isolated | S7_hard | sgc_ridge | 20 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.097 | 0.000 |
| interaction_isolated | S7_hard | sgc_ridge | 40 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.007 | 0.000 |
| interaction_isolated | S7_hard | sgc_ridge | 80 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| many_sufficient_one_minimal | N6_hard | sgc_ridge | 20 | 0.000 | 0.000 | 0.000 | 0.306 | 0.000 | 0.090 | 0.000 |
| many_sufficient_one_minimal | N6_hard | sgc_ridge | 40 | 0.000 | 0.000 | 0.000 | 0.382 | 0.000 | 0.028 | 0.000 |
| many_sufficient_one_minimal | N6_hard | sgc_ridge | 80 | 0.000 | 0.000 | 0.000 | 0.188 | 0.000 | 0.000 | 0.000 |
| multiple_minimal | P3_multi | sgc_ridge | 20 | 0.000 | 0.000 | 0.000 | 0.264 | 0.000 | 0.042 | 0.000 |
| multiple_minimal | P3_multi | sgc_ridge | 40 | 0.000 | 0.000 | 0.000 | 0.333 | 0.000 | 0.000 | 0.000 |
| multiple_minimal | P3_multi | sgc_ridge | 80 | 0.000 | 0.000 | 0.000 | 0.056 | 0.000 | 0.000 | 0.000 |
| near_boundary | SS_near | semisynthetic | 20 | 0.000 | 0.000 | 0.000 | 0.154 | 0.002 | 0.237 |  |
| near_boundary | SS_near | semisynthetic | 40 | 0.000 | 0.000 | 0.000 | 0.278 | 0.001 | 0.102 |  |
| near_boundary | SS_near | semisynthetic | 80 | 0.000 | 0.000 | 0.000 | 0.368 | 0.000 | 0.021 |  |
| neural_interaction | S7_hard | sage | 20 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.028 | 0.000 |
| neural_interaction | S7_hard | sage | 40 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| neural_interaction | S7_hard | sage | 80 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| no_sufficient | S8_small_hard | sgc_ridge | 20 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.042 | 0.000 |
| no_sufficient | S8_small_hard | sgc_ridge | 40 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| no_sufficient | S8_small_hard | sgc_ridge | 80 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| nonmonotone_empty_sufficient | SS_nonmono_A | semisynthetic | 20 | 0.000 | 0.000 | 0.252 | 0.209 | 0.000 | 0.021 |  |
| nonmonotone_empty_sufficient | SS_nonmono_A | semisynthetic | 40 | 0.000 | 0.000 | 0.536 | 0.235 | 0.000 | 0.006 |  |
| nonmonotone_empty_sufficient | SS_nonmono_A | semisynthetic | 80 | 0.000 | 0.000 | 0.875 | 0.087 | 0.000 | 0.001 |  |
| nonmonotone_two_minimal | SS_nonmono_B | semisynthetic | 20 | 0.000 | 0.000 | 0.000 | 0.195 | 0.000 | 0.029 |  |
| nonmonotone_two_minimal | SS_nonmono_B | semisynthetic | 40 | 0.000 | 0.000 | 0.000 | 0.228 | 0.000 | 0.003 |  |
| nonmonotone_two_minimal | SS_nonmono_B | semisynthetic | 80 | 0.000 | 0.000 | 0.000 | 0.079 | 0.000 | 0.000 |  |
| worst_case_fwer | SS_boundary | semisynthetic | 20 | 0.001 | 0.003 | 0.001 | 0.041 | 0.057 | 0.993 |  |
| worst_case_fwer | SS_boundary | semisynthetic | 40 | 0.004 | 0.004 | 0.004 | 0.049 | 0.062 | 0.992 |  |
| worst_case_fwer | SS_boundary | semisynthetic | 80 | 0.004 | 0.003 | 0.004 | 0.047 | 0.062 | 0.989 |  |

## FWER of certifications (any false advantage or false sufficiency)

| role | scenario | model | b | craf | craf_adaptive | craf_children | ni_holm | factorial_unadj |
|---|---|---|---|---|---|---|---|---|
| interaction_easy | S7_easy | sgc_ridge | 20 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| interaction_easy | S7_easy | sgc_ridge | 40 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| interaction_easy | S7_easy | sgc_ridge | 80 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| interaction_isolated | S7_hard | sgc_ridge | 20 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| interaction_isolated | S7_hard | sgc_ridge | 40 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| interaction_isolated | S7_hard | sgc_ridge | 80 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| many_sufficient_one_minimal | N6_hard | sgc_ridge | 20 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| many_sufficient_one_minimal | N6_hard | sgc_ridge | 40 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| many_sufficient_one_minimal | N6_hard | sgc_ridge | 80 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| multiple_minimal | P3_multi | sgc_ridge | 20 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| multiple_minimal | P3_multi | sgc_ridge | 40 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| multiple_minimal | P3_multi | sgc_ridge | 80 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| near_boundary | SS_near | semisynthetic | 20 | 0.001 | 0.000 | 0.001 | 0.000 | 0.007 |
| near_boundary | SS_near | semisynthetic | 40 | 0.000 | 0.000 | 0.000 | 0.000 | 0.003 |
| near_boundary | SS_near | semisynthetic | 80 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| neural_interaction | S7_hard | sage | 20 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| neural_interaction | S7_hard | sage | 40 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| neural_interaction | S7_hard | sage | 80 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| no_sufficient | S8_small_hard | sgc_ridge | 20 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| no_sufficient | S8_small_hard | sgc_ridge | 40 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| no_sufficient | S8_small_hard | sgc_ridge | 80 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| nonmonotone_empty_sufficient | SS_nonmono_A | semisynthetic | 20 | 0.000 | 0.000 | 0.000 | 0.000 | 0.001 |
| nonmonotone_empty_sufficient | SS_nonmono_A | semisynthetic | 40 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| nonmonotone_empty_sufficient | SS_nonmono_A | semisynthetic | 80 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| nonmonotone_two_minimal | SS_nonmono_B | semisynthetic | 20 | 0.000 | 0.001 | 0.000 | 0.000 | 0.001 |
| nonmonotone_two_minimal | SS_nonmono_B | semisynthetic | 40 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| nonmonotone_two_minimal | SS_nonmono_B | semisynthetic | 80 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| worst_case_fwer | SS_boundary | semisynthetic | 20 | 0.040 | 0.040 | 0.040 | 0.041 | 0.516 |
| worst_case_fwer | SS_boundary | semisynthetic | 40 | 0.046 | 0.043 | 0.046 | 0.049 | 0.535 |
| worst_case_fwer | SS_boundary | semisynthetic | 80 | 0.051 | 0.048 | 0.051 | 0.047 | 0.540 |

## Uncertainty-set coverage: true frontier ⊆ possible_min (CRAF)

| role | scenario | model | b | craf | craf_adaptive |
|---|---|---|---|---|---|
| interaction_easy | S7_easy | sgc_ridge | 20 | 1.000 | 1.000 |
| interaction_easy | S7_easy | sgc_ridge | 40 | 1.000 | 1.000 |
| interaction_easy | S7_easy | sgc_ridge | 80 | 1.000 | 1.000 |
| interaction_isolated | S7_hard | sgc_ridge | 20 | 1.000 | 1.000 |
| interaction_isolated | S7_hard | sgc_ridge | 40 | 1.000 | 1.000 |
| interaction_isolated | S7_hard | sgc_ridge | 80 | 1.000 | 1.000 |
| many_sufficient_one_minimal | N6_hard | sgc_ridge | 20 | 1.000 | 1.000 |
| many_sufficient_one_minimal | N6_hard | sgc_ridge | 40 | 1.000 | 1.000 |
| many_sufficient_one_minimal | N6_hard | sgc_ridge | 80 | 1.000 | 1.000 |
| multiple_minimal | P3_multi | sgc_ridge | 20 | 1.000 | 1.000 |
| multiple_minimal | P3_multi | sgc_ridge | 40 | 1.000 | 1.000 |
| multiple_minimal | P3_multi | sgc_ridge | 80 | 1.000 | 1.000 |
| near_boundary | SS_near | semisynthetic | 20 | 1.000 | 1.000 |
| near_boundary | SS_near | semisynthetic | 40 | 1.000 | 1.000 |
| near_boundary | SS_near | semisynthetic | 80 | 1.000 | 1.000 |
| neural_interaction | S7_hard | sage | 20 | 1.000 | 1.000 |
| neural_interaction | S7_hard | sage | 40 | 1.000 | 1.000 |
| neural_interaction | S7_hard | sage | 80 | 1.000 | 1.000 |
| no_sufficient | S8_small_hard | sgc_ridge | 20 | 1.000 | 1.000 |
| no_sufficient | S8_small_hard | sgc_ridge | 40 | 1.000 | 1.000 |
| no_sufficient | S8_small_hard | sgc_ridge | 80 | 1.000 | 1.000 |
| nonmonotone_empty_sufficient | SS_nonmono_A | semisynthetic | 20 | 1.000 | 1.000 |
| nonmonotone_empty_sufficient | SS_nonmono_A | semisynthetic | 40 | 1.000 | 1.000 |
| nonmonotone_empty_sufficient | SS_nonmono_A | semisynthetic | 80 | 1.000 | 1.000 |
| nonmonotone_two_minimal | SS_nonmono_B | semisynthetic | 20 | 1.000 | 1.000 |
| nonmonotone_two_minimal | SS_nonmono_B | semisynthetic | 40 | 1.000 | 1.000 |
| nonmonotone_two_minimal | SS_nonmono_B | semisynthetic | 80 | 1.000 | 1.000 |
| worst_case_fwer | SS_boundary | semisynthetic | 20 | 1.000 | 1.000 |
| worst_case_fwer | SS_boundary | semisynthetic | 40 | 1.000 | 1.000 |
| worst_case_fwer | SS_boundary | semisynthetic | 80 | 1.000 | 1.000 |

## Size of the uncertainty region |possible_min − cert_min| (CRAF)

| role | scenario | model | b | craf | craf_adaptive |
|---|---|---|---|---|---|
| interaction_easy | S7_easy | sgc_ridge | 20 | 1.278 | 2.090 |
| interaction_easy | S7_easy | sgc_ridge | 40 | 0.625 | 0.236 |
| interaction_easy | S7_easy | sgc_ridge | 80 | 0.292 | 0.146 |
| interaction_isolated | S7_hard | sgc_ridge | 20 | 5.403 | 5.632 |
| interaction_isolated | S7_hard | sgc_ridge | 40 | 3.472 | 1.597 |
| interaction_isolated | S7_hard | sgc_ridge | 80 | 0.778 | 0.278 |
| many_sufficient_one_minimal | N6_hard | sgc_ridge | 20 | 7.861 | 7.729 |
| many_sufficient_one_minimal | N6_hard | sgc_ridge | 40 | 5.104 | 3.562 |
| many_sufficient_one_minimal | N6_hard | sgc_ridge | 80 | 1.604 | 0.646 |
| multiple_minimal | P3_multi | sgc_ridge | 20 | 4.750 | 5.472 |
| multiple_minimal | P3_multi | sgc_ridge | 40 | 2.875 | 0.986 |
| multiple_minimal | P3_multi | sgc_ridge | 80 | 0.431 | 0.222 |
| near_boundary | SS_near | semisynthetic | 20 | 4.790 | 4.869 |
| near_boundary | SS_near | semisynthetic | 40 | 4.338 | 4.148 |
| near_boundary | SS_near | semisynthetic | 80 | 3.213 | 2.746 |
| neural_interaction | S7_hard | sage | 20 | 2.958 | 1.917 |
| neural_interaction | S7_hard | sage | 40 | 0.597 | 0.153 |
| neural_interaction | S7_hard | sage | 80 | 0.194 | 0.042 |
| no_sufficient | S8_small_hard | sgc_ridge | 20 | 1.583 | 1.417 |
| no_sufficient | S8_small_hard | sgc_ridge | 40 | 0.694 | 0.167 |
| no_sufficient | S8_small_hard | sgc_ridge | 80 | 0.306 | 0.125 |
| nonmonotone_empty_sufficient | SS_nonmono_A | semisynthetic | 20 | 1.615 | 1.387 |
| nonmonotone_empty_sufficient | SS_nonmono_A | semisynthetic | 40 | 0.942 | 0.340 |
| nonmonotone_empty_sufficient | SS_nonmono_A | semisynthetic | 80 | 0.240 | 0.114 |
| nonmonotone_two_minimal | SS_nonmono_B | semisynthetic | 20 | 2.433 | 2.397 |
| nonmonotone_two_minimal | SS_nonmono_B | semisynthetic | 40 | 1.422 | 0.833 |
| nonmonotone_two_minimal | SS_nonmono_B | semisynthetic | 80 | 0.386 | 0.170 |
| worst_case_fwer | SS_boundary | semisynthetic | 20 | 6.954 | 6.939 |
| worst_case_fwer | SS_boundary | semisynthetic | 40 | 6.928 | 6.936 |
| worst_case_fwer | SS_boundary | semisynthetic | 80 | 6.924 | 6.935 |

## Mean number of inconclusive lattice elements

| role | scenario | model | b | craf | craf_adaptive | craf_children | ni_holm | factorial_unadj |
|---|---|---|---|---|---|---|---|---|
| interaction_easy | S7_easy | sgc_ridge | 20 | 1.278 | 2.042 | 1.278 | 15.889 | 0.535 |
| interaction_easy | S7_easy | sgc_ridge | 40 | 0.625 | 0.236 | 0.625 | 15.611 | 0.243 |
| interaction_easy | S7_easy | sgc_ridge | 80 | 0.292 | 0.146 | 0.292 | 15.285 | 0.042 |
| interaction_isolated | S7_hard | sgc_ridge | 20 | 5.396 | 5.590 | 5.396 | 15.875 | 2.340 |
| interaction_isolated | S7_hard | sgc_ridge | 40 | 3.472 | 1.576 | 3.472 | 15.590 | 0.833 |
| interaction_isolated | S7_hard | sgc_ridge | 80 | 0.778 | 0.278 | 0.778 | 15.208 | 0.042 |
| many_sufficient_one_minimal | N6_hard | sgc_ridge | 20 | 7.854 | 8.028 | 7.854 | 15.215 | 3.597 |
| many_sufficient_one_minimal | N6_hard | sgc_ridge | 40 | 5.222 | 4.215 | 5.222 | 13.924 | 1.361 |
| many_sufficient_one_minimal | N6_hard | sgc_ridge | 80 | 1.451 | 2.333 | 1.451 | 11.951 | 0.167 |
| multiple_minimal | P3_multi | sgc_ridge | 20 | 5.028 | 5.903 | 5.028 | 14.333 | 2.167 |
| multiple_minimal | P3_multi | sgc_ridge | 40 | 3.042 | 2.292 | 3.042 | 12.611 | 0.722 |
| multiple_minimal | P3_multi | sgc_ridge | 80 | 0.583 | 2.069 | 0.583 | 10.486 | 0.014 |
| near_boundary | SS_near | semisynthetic | 20 | 4.606 | 4.668 | 4.606 | 6.460 | 3.182 |
| near_boundary | SS_near | semisynthetic | 40 | 3.897 | 3.774 | 3.897 | 5.798 | 2.237 |
| near_boundary | SS_near | semisynthetic | 80 | 2.671 | 2.461 | 2.671 | 4.721 | 1.134 |
| neural_interaction | S7_hard | sage | 20 | 2.958 | 1.903 | 2.958 | 15.708 | 0.778 |
| neural_interaction | S7_hard | sage | 40 | 0.597 | 0.153 | 0.597 | 15.375 | 0.167 |
| neural_interaction | S7_hard | sage | 80 | 0.194 | 0.042 | 0.194 | 15.194 | 0.014 |
| no_sufficient | S8_small_hard | sgc_ridge | 20 | 1.583 | 1.417 | 1.583 | 16.000 | 0.597 |
| no_sufficient | S8_small_hard | sgc_ridge | 40 | 0.694 | 0.167 | 0.694 | 16.000 | 0.236 |
| no_sufficient | S8_small_hard | sgc_ridge | 80 | 0.306 | 0.125 | 0.306 | 16.000 | 0.014 |
| nonmonotone_empty_sufficient | SS_nonmono_A | semisynthetic | 20 | 1.607 | 1.728 | 1.607 | 6.434 | 0.840 |
| nonmonotone_empty_sufficient | SS_nonmono_A | semisynthetic | 40 | 0.937 | 0.751 | 0.937 | 5.854 | 0.341 |
| nonmonotone_empty_sufficient | SS_nonmono_A | semisynthetic | 80 | 0.245 | 0.522 | 0.245 | 5.208 | 0.046 |
| nonmonotone_two_minimal | SS_nonmono_B | semisynthetic | 20 | 2.420 | 2.434 | 2.420 | 6.178 | 1.254 |
| nonmonotone_two_minimal | SS_nonmono_B | semisynthetic | 40 | 1.441 | 1.109 | 1.441 | 5.257 | 0.515 |
| nonmonotone_two_minimal | SS_nonmono_B | semisynthetic | 80 | 0.409 | 0.578 | 0.409 | 4.311 | 0.072 |
| worst_case_fwer | SS_boundary | semisynthetic | 20 | 6.960 | 6.959 | 6.960 | 6.957 | 6.307 |
| worst_case_fwer | SS_boundary | semisynthetic | 40 | 6.954 | 6.957 | 6.954 | 6.950 | 6.269 |
| worst_case_fwer | SS_boundary | semisynthetic | 80 | 6.947 | 6.952 | 6.947 | 6.952 | 6.277 |

## Elements minimal among certified-sufficient but NOT certified minimal (mean count)

| role | scenario | model | b | craf | craf_adaptive |
|---|---|---|---|---|---|
| interaction_easy | S7_easy | sgc_ridge | 20 | 0.000 | 0.049 |
| interaction_easy | S7_easy | sgc_ridge | 40 | 0.000 | 0.000 |
| interaction_easy | S7_easy | sgc_ridge | 80 | 0.000 | 0.000 |
| interaction_isolated | S7_hard | sgc_ridge | 20 | 0.007 | 0.042 |
| interaction_isolated | S7_hard | sgc_ridge | 40 | 0.000 | 0.021 |
| interaction_isolated | S7_hard | sgc_ridge | 80 | 0.000 | 0.000 |
| many_sufficient_one_minimal | N6_hard | sgc_ridge | 20 | 0.389 | 0.319 |
| many_sufficient_one_minimal | N6_hard | sgc_ridge | 40 | 0.583 | 0.597 |
| many_sufficient_one_minimal | N6_hard | sgc_ridge | 80 | 0.660 | 0.174 |
| multiple_minimal | P3_multi | sgc_ridge | 20 | 0.472 | 0.569 |
| multiple_minimal | P3_multi | sgc_ridge | 40 | 0.708 | 0.319 |
| multiple_minimal | P3_multi | sgc_ridge | 80 | 0.194 | 0.125 |
| near_boundary | SS_near | semisynthetic | 20 | 0.299 | 0.327 |
| near_boundary | SS_near | semisynthetic | 40 | 0.673 | 0.687 |
| near_boundary | SS_near | semisynthetic | 80 | 0.977 | 0.910 |
| neural_interaction | S7_hard | sage | 20 | 0.000 | 0.014 |
| neural_interaction | S7_hard | sage | 40 | 0.000 | 0.000 |
| neural_interaction | S7_hard | sage | 80 | 0.000 | 0.000 |
| no_sufficient | S8_small_hard | sgc_ridge | 20 | 0.000 | 0.000 |
| no_sufficient | S8_small_hard | sgc_ridge | 40 | 0.000 | 0.000 |
| no_sufficient | S8_small_hard | sgc_ridge | 80 | 0.000 | 0.000 |
| nonmonotone_empty_sufficient | SS_nonmono_A | semisynthetic | 20 | 0.197 | 0.179 |
| nonmonotone_empty_sufficient | SS_nonmono_A | semisynthetic | 40 | 0.243 | 0.118 |
| nonmonotone_empty_sufficient | SS_nonmono_A | semisynthetic | 80 | 0.102 | 0.042 |
| nonmonotone_two_minimal | SS_nonmono_B | semisynthetic | 20 | 0.186 | 0.213 |
| nonmonotone_two_minimal | SS_nonmono_B | semisynthetic | 40 | 0.234 | 0.151 |
| nonmonotone_two_minimal | SS_nonmono_B | semisynthetic | 80 | 0.101 | 0.043 |
| worst_case_fwer | SS_boundary | semisynthetic | 20 | 0.018 | 0.018 |
| worst_case_fwer | SS_boundary | semisynthetic | 40 | 0.020 | 0.019 |
| worst_case_fwer | SS_boundary | semisynthetic | 80 | 0.021 | 0.019 |

## Certified relational specificity over L (all elements certified advantage)

| role | scenario | model | b | craf | craf_adaptive | craf_children | ni_holm | factorial_unadj |
|---|---|---|---|---|---|---|---|---|
| interaction_easy | S7_easy | sgc_ridge | 20 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| interaction_easy | S7_easy | sgc_ridge | 40 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| interaction_easy | S7_easy | sgc_ridge | 80 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| interaction_isolated | S7_hard | sgc_ridge | 20 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| interaction_isolated | S7_hard | sgc_ridge | 40 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| interaction_isolated | S7_hard | sgc_ridge | 80 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| many_sufficient_one_minimal | N6_hard | sgc_ridge | 20 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| many_sufficient_one_minimal | N6_hard | sgc_ridge | 40 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| many_sufficient_one_minimal | N6_hard | sgc_ridge | 80 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| multiple_minimal | P3_multi | sgc_ridge | 20 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| multiple_minimal | P3_multi | sgc_ridge | 40 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| multiple_minimal | P3_multi | sgc_ridge | 80 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| near_boundary | SS_near | semisynthetic | 20 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| near_boundary | SS_near | semisynthetic | 40 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| near_boundary | SS_near | semisynthetic | 80 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| neural_interaction | S7_hard | sage | 20 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| neural_interaction | S7_hard | sage | 40 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| neural_interaction | S7_hard | sage | 80 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| no_sufficient | S8_small_hard | sgc_ridge | 20 | 0.069 | 0.264 | 0.069 | 0.000 | 0.458 |
| no_sufficient | S8_small_hard | sgc_ridge | 40 | 0.333 | 0.833 | 0.333 | 0.000 | 0.764 |
| no_sufficient | S8_small_hard | sgc_ridge | 80 | 0.694 | 0.875 | 0.694 | 0.000 | 0.986 |
| nonmonotone_empty_sufficient | SS_nonmono_A | semisynthetic | 20 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| nonmonotone_empty_sufficient | SS_nonmono_A | semisynthetic | 40 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| nonmonotone_empty_sufficient | SS_nonmono_A | semisynthetic | 80 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| nonmonotone_two_minimal | SS_nonmono_B | semisynthetic | 20 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| nonmonotone_two_minimal | SS_nonmono_B | semisynthetic | 40 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| nonmonotone_two_minimal | SS_nonmono_B | semisynthetic | 80 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| worst_case_fwer | SS_boundary | semisynthetic | 20 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| worst_case_fwer | SS_boundary | semisynthetic | 40 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| worst_case_fwer | SS_boundary | semisynthetic | 80 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |

## Mean fits used (budget B = b (1 + |L|))

| role | scenario | model | b | craf | craf_adaptive | craf_children | ni_holm | factorial_unadj | naive_point | pcga_l |
|---|---|---|---|---|---|---|---|---|---|---|
| interaction_easy | S7_easy | sgc_ridge | 20 | 340.000 | 339.715 | 340.000 | 340.000 | 340.000 | 340.000 | 340.000 |
| interaction_easy | S7_easy | sgc_ridge | 40 | 680.000 | 679.958 | 680.000 | 680.000 | 680.000 | 680.000 | 500.000 |
| interaction_easy | S7_easy | sgc_ridge | 80 | 1360.000 | 1360.000 | 1360.000 | 1360.000 | 1360.000 | 1360.000 | 500.000 |
| interaction_isolated | S7_hard | sgc_ridge | 20 | 340.000 | 339.757 | 340.000 | 340.000 | 340.000 | 340.000 | 340.000 |
| interaction_isolated | S7_hard | sgc_ridge | 40 | 680.000 | 679.826 | 680.000 | 680.000 | 680.000 | 680.000 | 500.000 |
| interaction_isolated | S7_hard | sgc_ridge | 80 | 1360.000 | 1359.181 | 1360.000 | 1360.000 | 1360.000 | 1360.000 | 500.000 |
| many_sufficient_one_minimal | N6_hard | sgc_ridge | 20 | 340.000 | 339.896 | 340.000 | 340.000 | 340.000 | 340.000 | 340.000 |
| many_sufficient_one_minimal | N6_hard | sgc_ridge | 40 | 680.000 | 679.861 | 680.000 | 680.000 | 680.000 | 680.000 | 500.000 |
| many_sufficient_one_minimal | N6_hard | sgc_ridge | 80 | 1360.000 | 1330.028 | 1360.000 | 1360.000 | 1360.000 | 1360.000 | 500.000 |
| multiple_minimal | P3_multi | sgc_ridge | 20 | 340.000 | 339.875 | 340.000 | 340.000 | 340.000 | 340.000 | 340.000 |
| multiple_minimal | P3_multi | sgc_ridge | 40 | 680.000 | 679.889 | 680.000 | 680.000 | 680.000 | 680.000 | 500.000 |
| multiple_minimal | P3_multi | sgc_ridge | 80 | 1360.000 | 1344.500 | 1360.000 | 1360.000 | 1360.000 | 1360.000 | 500.000 |
| near_boundary | SS_near | semisynthetic | 20 | 160.000 | 159.799 | 160.000 | 160.000 | 160.000 | 160.000 |  |
| near_boundary | SS_near | semisynthetic | 40 | 320.000 | 319.820 | 320.000 | 320.000 | 320.000 | 320.000 |  |
| near_boundary | SS_near | semisynthetic | 80 | 640.000 | 639.237 | 640.000 | 640.000 | 640.000 | 640.000 |  |
| neural_interaction | S7_hard | sage | 20 | 340.000 | 339.778 | 340.000 | 340.000 | 340.000 | 340.000 | 340.000 |
| neural_interaction | S7_hard | sage | 40 | 680.000 | 679.931 | 680.000 | 680.000 | 680.000 | 680.000 | 500.000 |
| neural_interaction | S7_hard | sage | 80 | 1360.000 | 1265.931 | 1360.000 | 1360.000 | 1360.000 | 1360.000 | 500.000 |
| no_sufficient | S8_small_hard | sgc_ridge | 20 | 340.000 | 339.778 | 340.000 | 340.000 | 340.000 | 340.000 | 340.000 |
| no_sufficient | S8_small_hard | sgc_ridge | 40 | 680.000 | 679.986 | 680.000 | 680.000 | 680.000 | 680.000 | 500.000 |
| no_sufficient | S8_small_hard | sgc_ridge | 80 | 1360.000 | 1338.389 | 1360.000 | 1360.000 | 1360.000 | 1360.000 | 500.000 |
| nonmonotone_empty_sufficient | SS_nonmono_A | semisynthetic | 20 | 160.000 | 159.788 | 160.000 | 160.000 | 160.000 | 160.000 |  |
| nonmonotone_empty_sufficient | SS_nonmono_A | semisynthetic | 40 | 320.000 | 315.322 | 320.000 | 320.000 | 320.000 | 320.000 |  |
| nonmonotone_empty_sufficient | SS_nonmono_A | semisynthetic | 80 | 640.000 | 490.084 | 640.000 | 640.000 | 640.000 | 640.000 |  |
| nonmonotone_two_minimal | SS_nonmono_B | semisynthetic | 20 | 160.000 | 159.732 | 160.000 | 160.000 | 160.000 | 160.000 |  |
| nonmonotone_two_minimal | SS_nonmono_B | semisynthetic | 40 | 320.000 | 319.704 | 320.000 | 320.000 | 320.000 | 320.000 |  |
| nonmonotone_two_minimal | SS_nonmono_B | semisynthetic | 80 | 640.000 | 636.856 | 640.000 | 640.000 | 640.000 | 640.000 |  |
| worst_case_fwer | SS_boundary | semisynthetic | 20 | 160.000 | 159.915 | 160.000 | 160.000 | 160.000 | 160.000 |  |
| worst_case_fwer | SS_boundary | semisynthetic | 40 | 320.000 | 319.579 | 320.000 | 320.000 | 320.000 | 320.000 |  |
| worst_case_fwer | SS_boundary | semisynthetic | 80 | 640.000 | 633.244 | 640.000 | 640.000 | 640.000 | 640.000 |  |

## Most frequent reported frontier

| role | scenario | model | b |
|---|---|---|---|
| interaction_easy | S7_easy | sgc_ridge | 20 |
| interaction_easy | S7_easy | sgc_ridge | 40 |
| interaction_easy | S7_easy | sgc_ridge | 80 |
| interaction_isolated | S7_hard | sgc_ridge | 20 |
| interaction_isolated | S7_hard | sgc_ridge | 40 |
| interaction_isolated | S7_hard | sgc_ridge | 80 |
| many_sufficient_one_minimal | N6_hard | sgc_ridge | 20 |
| many_sufficient_one_minimal | N6_hard | sgc_ridge | 40 |
| many_sufficient_one_minimal | N6_hard | sgc_ridge | 80 |
| multiple_minimal | P3_multi | sgc_ridge | 20 |
| multiple_minimal | P3_multi | sgc_ridge | 40 |
| multiple_minimal | P3_multi | sgc_ridge | 80 |
| near_boundary | SS_near | semisynthetic | 20 |
| near_boundary | SS_near | semisynthetic | 40 |
| near_boundary | SS_near | semisynthetic | 80 |
| neural_interaction | S7_hard | sage | 20 |
| neural_interaction | S7_hard | sage | 40 |
| neural_interaction | S7_hard | sage | 80 |
| no_sufficient | S8_small_hard | sgc_ridge | 20 |
| no_sufficient | S8_small_hard | sgc_ridge | 40 |
| no_sufficient | S8_small_hard | sgc_ridge | 80 |
| nonmonotone_empty_sufficient | SS_nonmono_A | semisynthetic | 20 |
| nonmonotone_empty_sufficient | SS_nonmono_A | semisynthetic | 40 |
| nonmonotone_empty_sufficient | SS_nonmono_A | semisynthetic | 80 |
| nonmonotone_two_minimal | SS_nonmono_B | semisynthetic | 20 |
| nonmonotone_two_minimal | SS_nonmono_B | semisynthetic | 40 |
| nonmonotone_two_minimal | SS_nonmono_B | semisynthetic | 80 |
| worst_case_fwer | SS_boundary | semisynthetic | 20 |
| worst_case_fwer | SS_boundary | semisynthetic | 40 |
| worst_case_fwer | SS_boundary | semisynthetic | 80 |

## Paired differences (experiment-paired; 95% normal CI)

| scenario | model | b | a | b_proc | metric | diff | ci_lo | ci_hi | n_exp |
|---|---|---|---|---|---|---|---|---|---|
| N6_hard | sgc_ridge | 20 | craf_adaptive | craf | exact | 0.049 | -0.016 | 0.114 | 144 |
| N6_hard | sgc_ridge | 40 | craf_adaptive | craf | exact | 0.146 | 0.069 | 0.223 | 144 |
| N6_hard | sgc_ridge | 80 | craf_adaptive | craf | exact | 0.160 | 0.097 | 0.223 | 144 |
| P3_multi | sgc_ridge | 20 | craf_adaptive | craf | exact | -0.014 | -0.105 | 0.077 | 72 |
| P3_multi | sgc_ridge | 40 | craf_adaptive | craf | exact | 0.486 | 0.370 | 0.602 | 72 |
| P3_multi | sgc_ridge | 80 | craf_adaptive | craf | exact | 0.069 | -0.011 | 0.150 | 72 |
| S7_easy | sgc_ridge | 20 | craf_adaptive | craf | exact | 0.132 | 0.057 | 0.207 | 144 |
| S7_easy | sgc_ridge | 40 | craf_adaptive | craf | exact | 0.396 | 0.311 | 0.481 | 144 |
| S7_easy | sgc_ridge | 80 | craf_adaptive | craf | exact | 0.146 | 0.082 | 0.210 | 144 |
| S7_hard | sage | 20 | craf_adaptive | craf | exact | 0.208 | 0.080 | 0.337 | 72 |
| S7_hard | sage | 40 | craf_adaptive | craf | exact | 0.250 | 0.129 | 0.371 | 72 |
| S7_hard | sage | 80 | craf_adaptive | craf | exact | 0.153 | 0.069 | 0.236 | 72 |
| S7_hard | sgc_ridge | 20 | craf_adaptive | craf | exact | 0.069 | 0.013 | 0.126 | 144 |
| S7_hard | sgc_ridge | 40 | craf_adaptive | craf | exact | 0.285 | 0.191 | 0.379 | 144 |
| S7_hard | sgc_ridge | 80 | craf_adaptive | craf | exact | 0.132 | 0.067 | 0.197 | 144 |
| S8_small_hard | sgc_ridge | 20 | craf_adaptive | craf | exact | 0.000 | 0.000 | 0.000 | 72 |
| S8_small_hard | sgc_ridge | 40 | craf_adaptive | craf | exact | 0.000 | 0.000 | 0.000 | 72 |
| S8_small_hard | sgc_ridge | 80 | craf_adaptive | craf | exact | 0.000 | 0.000 | 0.000 | 72 |
| SS_boundary | semisynthetic | 20 | craf_adaptive | craf | exact | -0.002 | -0.004 | 0.000 | 2000 |
| SS_boundary | semisynthetic | 40 | craf_adaptive | craf | exact | 0.001 | -0.002 | 0.003 | 2000 |
| SS_boundary | semisynthetic | 80 | craf_adaptive | craf | exact | 0.001 | -0.001 | 0.003 | 2000 |
| SS_near | semisynthetic | 20 | craf_adaptive | craf | exact | 0.000 | -0.002 | 0.002 | 2000 |
| SS_near | semisynthetic | 40 | craf_adaptive | craf | exact | 0.018 | 0.011 | 0.025 | 2000 |
| SS_near | semisynthetic | 80 | craf_adaptive | craf | exact | 0.074 | 0.059 | 0.089 | 2000 |
| SS_nonmono_A | semisynthetic | 20 | craf_adaptive | craf | exact | 0.171 | 0.151 | 0.191 | 2000 |
| SS_nonmono_A | semisynthetic | 40 | craf_adaptive | craf | exact | 0.303 | 0.282 | 0.324 | 2000 |
| SS_nonmono_A | semisynthetic | 80 | craf_adaptive | craf | exact | 0.064 | 0.051 | 0.076 | 2000 |
| SS_nonmono_B | semisynthetic | 20 | craf_adaptive | craf | exact | 0.042 | 0.029 | 0.054 | 2000 |
| SS_nonmono_B | semisynthetic | 40 | craf_adaptive | craf | exact | 0.270 | 0.248 | 0.292 | 2000 |
| SS_nonmono_B | semisynthetic | 80 | craf_adaptive | craf | exact | 0.132 | 0.115 | 0.149 | 2000 |
| N6_hard | sgc_ridge | 20 | craf | ni_holm | exact | -0.049 | -0.084 | -0.013 | 144 |
| N6_hard | sgc_ridge | 40 | craf | ni_holm | exact | -0.021 | -0.044 | 0.003 | 144 |
| N6_hard | sgc_ridge | 80 | craf | ni_holm | exact | -0.069 | -0.111 | -0.028 | 144 |
| P3_multi | sgc_ridge | 20 | craf | ni_holm | exact | -0.042 | -0.088 | 0.005 | 72 |
| P3_multi | sgc_ridge | 40 | craf | ni_holm | exact | -0.125 | -0.202 | -0.048 | 72 |
| P3_multi | sgc_ridge | 80 | craf | ni_holm | exact | -0.028 | -0.066 | 0.010 | 72 |
| S7_easy | sgc_ridge | 20 | craf | ni_holm | exact | -0.014 | -0.033 | 0.005 | 144 |
| S7_easy | sgc_ridge | 40 | craf | ni_holm | exact | -0.014 | -0.033 | 0.005 | 144 |
| S7_easy | sgc_ridge | 80 | craf | ni_holm | exact | -0.007 | -0.021 | 0.007 | 144 |
| S7_hard | sage | 20 | craf | ni_holm | exact | -0.042 | -0.088 | 0.005 | 72 |
| S7_hard | sage | 40 | craf | ni_holm | exact | -0.014 | -0.041 | 0.013 | 72 |
| S7_hard | sage | 80 | craf | ni_holm | exact | 0.000 | 0.000 | 0.000 | 72 |
| S7_hard | sgc_ridge | 20 | craf | ni_holm | exact | -0.028 | -0.055 | -0.001 | 144 |
| S7_hard | sgc_ridge | 40 | craf | ni_holm | exact | -0.035 | -0.065 | -0.005 | 144 |
| S7_hard | sgc_ridge | 80 | craf | ni_holm | exact | 0.000 | 0.000 | 0.000 | 144 |
| S8_small_hard | sgc_ridge | 20 | craf | ni_holm | exact | 0.000 | 0.000 | 0.000 | 72 |
| S8_small_hard | sgc_ridge | 40 | craf | ni_holm | exact | 0.000 | 0.000 | 0.000 | 72 |
| S8_small_hard | sgc_ridge | 80 | craf | ni_holm | exact | 0.000 | 0.000 | 0.000 | 72 |
| SS_boundary | semisynthetic | 20 | craf | ni_holm | exact | 0.040 | 0.031 | 0.049 | 2000 |
| SS_boundary | semisynthetic | 40 | craf | ni_holm | exact | 0.044 | 0.035 | 0.054 | 2000 |
| SS_boundary | semisynthetic | 80 | craf | ni_holm | exact | 0.043 | 0.034 | 0.052 | 2000 |
| SS_near | semisynthetic | 20 | craf | ni_holm | exact | -0.029 | -0.036 | -0.022 | 2000 |
| SS_near | semisynthetic | 40 | craf | ni_holm | exact | -0.112 | -0.126 | -0.098 | 2000 |
| SS_near | semisynthetic | 80 | craf | ni_holm | exact | -0.282 | -0.302 | -0.262 | 2000 |
| SS_nonmono_A | semisynthetic | 20 | craf | ni_holm | exact | -0.039 | -0.047 | -0.031 | 2000 |
| SS_nonmono_A | semisynthetic | 40 | craf | ni_holm | exact | -0.040 | -0.048 | -0.031 | 2000 |
| SS_nonmono_A | semisynthetic | 80 | craf | ni_holm | exact | -0.018 | -0.024 | -0.012 | 2000 |
| SS_nonmono_B | semisynthetic | 20 | craf | ni_holm | exact | -0.030 | -0.038 | -0.023 | 2000 |
| SS_nonmono_B | semisynthetic | 40 | craf | ni_holm | exact | -0.075 | -0.087 | -0.063 | 2000 |
| SS_nonmono_B | semisynthetic | 80 | craf | ni_holm | exact | -0.057 | -0.067 | -0.047 | 2000 |
| N6_hard | sgc_ridge | 20 | craf | naive_point | exact | -0.792 | -0.861 | -0.722 | 144 |
| N6_hard | sgc_ridge | 40 | craf | naive_point | exact | -0.583 | -0.669 | -0.498 | 144 |
| N6_hard | sgc_ridge | 80 | craf | naive_point | exact | -0.264 | -0.336 | -0.192 | 144 |
| P3_multi | sgc_ridge | 20 | craf | naive_point | exact | -0.819 | -0.909 | -0.730 | 72 |
| P3_multi | sgc_ridge | 40 | craf | naive_point | exact | -0.708 | -0.814 | -0.603 | 72 |
| P3_multi | sgc_ridge | 80 | craf | naive_point | exact | -0.125 | -0.202 | -0.048 | 72 |
| S7_easy | sgc_ridge | 20 | craf | naive_point | exact | -0.854 | -0.912 | -0.796 | 144 |
| S7_easy | sgc_ridge | 40 | craf | naive_point | exact | -0.618 | -0.698 | -0.538 | 144 |
| S7_easy | sgc_ridge | 80 | craf | naive_point | exact | -0.292 | -0.366 | -0.217 | 144 |
| S7_hard | sage | 20 | craf | naive_point | exact | -0.708 | -0.821 | -0.596 | 72 |
| S7_hard | sage | 40 | craf | naive_point | exact | -0.389 | -0.502 | -0.275 | 72 |
| S7_hard | sage | 80 | craf | naive_point | exact | -0.194 | -0.287 | -0.102 | 72 |
| S7_hard | sgc_ridge | 20 | craf | naive_point | exact | -0.764 | -0.841 | -0.687 | 144 |
| S7_hard | sgc_ridge | 40 | craf | naive_point | exact | -0.611 | -0.693 | -0.529 | 144 |
| S7_hard | sgc_ridge | 80 | craf | naive_point | exact | -0.208 | -0.275 | -0.142 | 144 |
| S8_small_hard | sgc_ridge | 20 | craf | naive_point | exact | 0.042 | -0.005 | 0.088 | 72 |
| S8_small_hard | sgc_ridge | 40 | craf | naive_point | exact | 0.000 | 0.000 | 0.000 | 72 |
| S8_small_hard | sgc_ridge | 80 | craf | naive_point | exact | 0.000 | 0.000 | 0.000 | 72 |
| SS_boundary | semisynthetic | 20 | craf | naive_point | exact | 0.992 | 0.988 | 0.996 | 2000 |
| SS_boundary | semisynthetic | 40 | craf | naive_point | exact | 0.988 | 0.983 | 0.993 | 2000 |
| SS_boundary | semisynthetic | 80 | craf | naive_point | exact | 0.985 | 0.979 | 0.990 | 2000 |
| SS_near | semisynthetic | 20 | craf | naive_point | exact | -0.733 | -0.752 | -0.714 | 2000 |
| SS_near | semisynthetic | 40 | craf | naive_point | exact | -0.883 | -0.898 | -0.869 | 2000 |
| SS_near | semisynthetic | 80 | craf | naive_point | exact | -0.853 | -0.868 | -0.837 | 2000 |
| SS_nonmono_A | semisynthetic | 20 | craf | naive_point | exact | -0.746 | -0.765 | -0.727 | 2000 |
| SS_nonmono_A | semisynthetic | 40 | craf | naive_point | exact | -0.464 | -0.485 | -0.442 | 2000 |
| SS_nonmono_A | semisynthetic | 80 | craf | naive_point | exact | -0.119 | -0.134 | -0.105 | 2000 |
| SS_nonmono_B | semisynthetic | 20 | craf | naive_point | exact | -0.886 | -0.900 | -0.872 | 2000 |
| SS_nonmono_B | semisynthetic | 40 | craf | naive_point | exact | -0.722 | -0.742 | -0.702 | 2000 |
| SS_nonmono_B | semisynthetic | 80 | craf | naive_point | exact | -0.244 | -0.263 | -0.225 | 2000 |
| N6_hard | sgc_ridge | 20 | craf | factorial_unadj | exact | -0.493 | -0.575 | -0.411 | 144 |
| N6_hard | sgc_ridge | 40 | craf | factorial_unadj | exact | -0.396 | -0.476 | -0.316 | 144 |
| N6_hard | sgc_ridge | 80 | craf | factorial_unadj | exact | -0.243 | -0.313 | -0.173 | 144 |
| P3_multi | sgc_ridge | 20 | craf | factorial_unadj | exact | -0.431 | -0.546 | -0.315 | 72 |
| P3_multi | sgc_ridge | 40 | craf | factorial_unadj | exact | -0.486 | -0.602 | -0.370 | 72 |
| P3_multi | sgc_ridge | 80 | craf | factorial_unadj | exact | -0.125 | -0.202 | -0.048 | 72 |
| S7_easy | sgc_ridge | 20 | craf | factorial_unadj | exact | -0.375 | -0.454 | -0.296 | 144 |
| S7_easy | sgc_ridge | 40 | craf | factorial_unadj | exact | -0.382 | -0.462 | -0.302 | 144 |
| S7_easy | sgc_ridge | 80 | craf | factorial_unadj | exact | -0.250 | -0.321 | -0.179 | 144 |
| S7_hard | sage | 20 | craf | factorial_unadj | exact | -0.361 | -0.473 | -0.249 | 72 |
| S7_hard | sage | 40 | craf | factorial_unadj | exact | -0.236 | -0.335 | -0.137 | 72 |
| S7_hard | sage | 80 | craf | factorial_unadj | exact | -0.181 | -0.270 | -0.091 | 72 |
| S7_hard | sgc_ridge | 20 | craf | factorial_unadj | exact | -0.438 | -0.519 | -0.356 | 144 |
| S7_hard | sgc_ridge | 40 | craf | factorial_unadj | exact | -0.431 | -0.512 | -0.349 | 144 |
| S7_hard | sgc_ridge | 80 | craf | factorial_unadj | exact | -0.194 | -0.259 | -0.130 | 144 |
| S8_small_hard | sgc_ridge | 20 | craf | factorial_unadj | exact | 0.000 | 0.000 | 0.000 | 72 |
| S8_small_hard | sgc_ridge | 40 | craf | factorial_unadj | exact | 0.000 | 0.000 | 0.000 | 72 |
| S8_small_hard | sgc_ridge | 80 | craf | factorial_unadj | exact | 0.000 | 0.000 | 0.000 | 72 |
| SS_boundary | semisynthetic | 20 | craf | factorial_unadj | exact | 0.056 | 0.046 | 0.066 | 2000 |
| SS_boundary | semisynthetic | 40 | craf | factorial_unadj | exact | 0.059 | 0.048 | 0.069 | 2000 |
| SS_boundary | semisynthetic | 80 | craf | factorial_unadj | exact | 0.059 | 0.048 | 0.069 | 2000 |
| SS_near | semisynthetic | 20 | craf | factorial_unadj | exact | -0.052 | -0.062 | -0.042 | 2000 |
| SS_near | semisynthetic | 40 | craf | factorial_unadj | exact | -0.185 | -0.203 | -0.168 | 2000 |
| SS_near | semisynthetic | 80 | craf | factorial_unadj | exact | -0.374 | -0.396 | -0.353 | 2000 |
| SS_nonmono_A | semisynthetic | 20 | craf | factorial_unadj | exact | -0.352 | -0.373 | -0.331 | 2000 |
| SS_nonmono_A | semisynthetic | 40 | craf | factorial_unadj | exact | -0.309 | -0.330 | -0.289 | 2000 |
| SS_nonmono_A | semisynthetic | 80 | craf | factorial_unadj | exact | -0.101 | -0.114 | -0.087 | 2000 |
| SS_nonmono_B | semisynthetic | 20 | craf | factorial_unadj | exact | -0.294 | -0.314 | -0.275 | 2000 |
| SS_nonmono_B | semisynthetic | 40 | craf | factorial_unadj | exact | -0.415 | -0.437 | -0.394 | 2000 |
| SS_nonmono_B | semisynthetic | 80 | craf | factorial_unadj | exact | -0.201 | -0.218 | -0.183 | 2000 |
| N6_hard | sgc_ridge | 20 | craf | pcga_l | exact | 0.118 | 0.065 | 0.171 | 144 |
| N6_hard | sgc_ridge | 40 | craf | pcga_l | exact | 0.389 | 0.309 | 0.469 | 144 |
| N6_hard | sgc_ridge | 80 | craf | pcga_l | exact | 0.736 | 0.664 | 0.808 | 144 |
| P3_multi | sgc_ridge | 20 | craf | pcga_l | exact | 0.125 | 0.048 | 0.202 | 72 |
| P3_multi | sgc_ridge | 40 | craf | pcga_l | exact | 0.292 | 0.186 | 0.397 | 72 |
| P3_multi | sgc_ridge | 80 | craf | pcga_l | exact | 0.875 | 0.798 | 0.952 | 72 |
| S7_easy | sgc_ridge | 20 | craf | pcga_l | exact | 0.097 | 0.049 | 0.146 | 144 |
| S7_easy | sgc_ridge | 40 | craf | pcga_l | exact | 0.375 | 0.296 | 0.454 | 144 |
| S7_easy | sgc_ridge | 80 | craf | pcga_l | exact | 0.708 | 0.634 | 0.783 | 144 |
| S7_hard | sage | 20 | craf | pcga_l | exact | 0.250 | 0.149 | 0.351 | 72 |
| S7_hard | sage | 40 | craf | pcga_l | exact | 0.611 | 0.498 | 0.725 | 72 |
| S7_hard | sage | 80 | craf | pcga_l | exact | 0.806 | 0.713 | 0.898 | 72 |
| S7_hard | sgc_ridge | 20 | craf | pcga_l | exact | 0.097 | 0.049 | 0.146 | 144 |
| S7_hard | sgc_ridge | 40 | craf | pcga_l | exact | 0.375 | 0.296 | 0.454 | 144 |
| S7_hard | sgc_ridge | 80 | craf | pcga_l | exact | 0.792 | 0.725 | 0.858 | 144 |
| S8_small_hard | sgc_ridge | 20 | craf | pcga_l | exact | 0.000 | 0.000 | 0.000 | 72 |
| S8_small_hard | sgc_ridge | 40 | craf | pcga_l | exact | 0.000 | 0.000 | 0.000 | 72 |
| S8_small_hard | sgc_ridge | 80 | craf | pcga_l | exact | 0.000 | 0.000 | 0.000 | 72 |
| N6_hard | sgc_ridge | 20 | craf_adaptive | craf | n_inconclusive | 0.174 | -0.076 | 0.423 | 144 |
| N6_hard | sgc_ridge | 40 | craf_adaptive | craf | n_inconclusive | -1.007 | -1.291 | -0.723 | 144 |
| N6_hard | sgc_ridge | 80 | craf_adaptive | craf | n_inconclusive | 0.882 | 0.561 | 1.203 | 144 |
| P3_multi | sgc_ridge | 20 | craf_adaptive | craf | n_inconclusive | 0.875 | 0.402 | 1.348 | 72 |
| P3_multi | sgc_ridge | 40 | craf_adaptive | craf | n_inconclusive | -0.750 | -1.192 | -0.308 | 72 |
| P3_multi | sgc_ridge | 80 | craf_adaptive | craf | n_inconclusive | 1.486 | 1.058 | 1.914 | 72 |
| S7_easy | sgc_ridge | 20 | craf_adaptive | craf | n_inconclusive | 0.764 | 0.372 | 1.155 | 144 |
| S7_easy | sgc_ridge | 40 | craf_adaptive | craf | n_inconclusive | -0.389 | -0.476 | -0.302 | 144 |
| S7_easy | sgc_ridge | 80 | craf_adaptive | craf | n_inconclusive | -0.146 | -0.210 | -0.082 | 144 |
| S7_hard | sage | 20 | craf_adaptive | craf | n_inconclusive | -1.056 | -1.433 | -0.678 | 72 |
| S7_hard | sage | 40 | craf_adaptive | craf | n_inconclusive | -0.444 | -0.604 | -0.285 | 72 |
| S7_hard | sage | 80 | craf_adaptive | craf | n_inconclusive | -0.153 | -0.236 | -0.069 | 72 |
| S7_hard | sgc_ridge | 20 | craf_adaptive | craf | n_inconclusive | 0.194 | -0.104 | 0.493 | 144 |
| S7_hard | sgc_ridge | 40 | craf_adaptive | craf | n_inconclusive | -1.896 | -2.151 | -1.641 | 144 |
| S7_hard | sgc_ridge | 80 | craf_adaptive | craf | n_inconclusive | -0.500 | -0.655 | -0.345 | 144 |
| S8_small_hard | sgc_ridge | 20 | craf_adaptive | craf | n_inconclusive | -0.167 | -0.454 | 0.121 | 72 |
| S8_small_hard | sgc_ridge | 40 | craf_adaptive | craf | n_inconclusive | -0.528 | -0.650 | -0.405 | 72 |
| S8_small_hard | sgc_ridge | 80 | craf_adaptive | craf | n_inconclusive | -0.181 | -0.278 | -0.083 | 72 |
| SS_boundary | semisynthetic | 20 | craf_adaptive | craf | n_inconclusive | -0.001 | -0.009 | 0.008 | 2000 |
| SS_boundary | semisynthetic | 40 | craf_adaptive | craf | n_inconclusive | 0.003 | -0.006 | 0.012 | 2000 |
| SS_boundary | semisynthetic | 80 | craf_adaptive | craf | n_inconclusive | 0.004 | -0.003 | 0.011 | 2000 |
| SS_near | semisynthetic | 20 | craf_adaptive | craf | n_inconclusive | 0.062 | 0.033 | 0.091 | 2000 |
| SS_near | semisynthetic | 40 | craf_adaptive | craf | n_inconclusive | -0.123 | -0.158 | -0.088 | 2000 |
| SS_near | semisynthetic | 80 | craf_adaptive | craf | n_inconclusive | -0.210 | -0.252 | -0.168 | 2000 |
| SS_nonmono_A | semisynthetic | 20 | craf_adaptive | craf | n_inconclusive | 0.121 | 0.081 | 0.162 | 2000 |
| SS_nonmono_A | semisynthetic | 40 | craf_adaptive | craf | n_inconclusive | -0.185 | -0.226 | -0.145 | 2000 |
| SS_nonmono_A | semisynthetic | 80 | craf_adaptive | craf | n_inconclusive | 0.278 | 0.249 | 0.306 | 2000 |
| SS_nonmono_B | semisynthetic | 20 | craf_adaptive | craf | n_inconclusive | 0.015 | -0.024 | 0.053 | 2000 |
| SS_nonmono_B | semisynthetic | 40 | craf_adaptive | craf | n_inconclusive | -0.332 | -0.370 | -0.294 | 2000 |
| SS_nonmono_B | semisynthetic | 80 | craf_adaptive | craf | n_inconclusive | 0.168 | 0.137 | 0.199 | 2000 |
| N6_hard | sgc_ridge | 20 | craf | ni_holm | false_member | -0.306 | -0.381 | -0.230 | 144 |
| N6_hard | sgc_ridge | 40 | craf | ni_holm | false_member | -0.382 | -0.462 | -0.302 | 144 |
| N6_hard | sgc_ridge | 80 | craf | ni_holm | false_member | -0.188 | -0.251 | -0.124 | 144 |
| P3_multi | sgc_ridge | 20 | craf | ni_holm | false_member | -0.264 | -0.366 | -0.161 | 72 |
| P3_multi | sgc_ridge | 40 | craf | ni_holm | false_member | -0.333 | -0.443 | -0.224 | 72 |
| P3_multi | sgc_ridge | 80 | craf | ni_holm | false_member | -0.056 | -0.109 | -0.002 | 72 |
| S7_easy | sgc_ridge | 20 | craf | ni_holm | false_member | 0.000 | 0.000 | 0.000 | 144 |
| S7_easy | sgc_ridge | 40 | craf | ni_holm | false_member | 0.000 | 0.000 | 0.000 | 144 |
| S7_easy | sgc_ridge | 80 | craf | ni_holm | false_member | 0.000 | 0.000 | 0.000 | 144 |
| S7_hard | sage | 20 | craf | ni_holm | false_member | 0.000 | 0.000 | 0.000 | 72 |
| S7_hard | sage | 40 | craf | ni_holm | false_member | 0.000 | 0.000 | 0.000 | 72 |
| S7_hard | sage | 80 | craf | ni_holm | false_member | 0.000 | 0.000 | 0.000 | 72 |
| S7_hard | sgc_ridge | 20 | craf | ni_holm | false_member | 0.000 | 0.000 | 0.000 | 144 |
| S7_hard | sgc_ridge | 40 | craf | ni_holm | false_member | 0.000 | 0.000 | 0.000 | 144 |
| S7_hard | sgc_ridge | 80 | craf | ni_holm | false_member | 0.000 | 0.000 | 0.000 | 144 |
| S8_small_hard | sgc_ridge | 20 | craf | ni_holm | false_member | 0.000 | 0.000 | 0.000 | 72 |
| S8_small_hard | sgc_ridge | 40 | craf | ni_holm | false_member | 0.000 | 0.000 | 0.000 | 72 |
| S8_small_hard | sgc_ridge | 80 | craf | ni_holm | false_member | 0.000 | 0.000 | 0.000 | 72 |
| SS_boundary | semisynthetic | 20 | craf | ni_holm | false_member | -0.040 | -0.049 | -0.031 | 2000 |
| SS_boundary | semisynthetic | 40 | craf | ni_holm | false_member | -0.044 | -0.054 | -0.035 | 2000 |
| SS_boundary | semisynthetic | 80 | craf | ni_holm | false_member | -0.043 | -0.052 | -0.034 | 2000 |
| SS_near | semisynthetic | 20 | craf | ni_holm | false_member | -0.154 | -0.170 | -0.138 | 2000 |
| SS_near | semisynthetic | 40 | craf | ni_holm | false_member | -0.278 | -0.297 | -0.258 | 2000 |
| SS_near | semisynthetic | 80 | craf | ni_holm | false_member | -0.368 | -0.389 | -0.347 | 2000 |
| SS_nonmono_A | semisynthetic | 20 | craf | ni_holm | false_member | -0.209 | -0.227 | -0.191 | 2000 |
| SS_nonmono_A | semisynthetic | 40 | craf | ni_holm | false_member | -0.235 | -0.254 | -0.217 | 2000 |
| SS_nonmono_A | semisynthetic | 80 | craf | ni_holm | false_member | -0.087 | -0.100 | -0.075 | 2000 |
| SS_nonmono_B | semisynthetic | 20 | craf | ni_holm | false_member | -0.195 | -0.212 | -0.178 | 2000 |
| SS_nonmono_B | semisynthetic | 40 | craf | ni_holm | false_member | -0.228 | -0.246 | -0.209 | 2000 |
| SS_nonmono_B | semisynthetic | 80 | craf | ni_holm | false_member | -0.079 | -0.090 | -0.067 | 2000 |
| N6_hard | sgc_ridge | 20 | craf | naive_point | false_member | -0.090 | -0.137 | -0.043 | 144 |
| N6_hard | sgc_ridge | 40 | craf | naive_point | false_member | -0.028 | -0.055 | -0.001 | 144 |
| N6_hard | sgc_ridge | 80 | craf | naive_point | false_member | 0.000 | 0.000 | 0.000 | 144 |
| P3_multi | sgc_ridge | 20 | craf | naive_point | false_member | -0.042 | -0.088 | 0.005 | 72 |
| P3_multi | sgc_ridge | 40 | craf | naive_point | false_member | 0.000 | 0.000 | 0.000 | 72 |
| P3_multi | sgc_ridge | 80 | craf | naive_point | false_member | 0.000 | 0.000 | 0.000 | 72 |
| S7_easy | sgc_ridge | 20 | craf | naive_point | false_member | 0.000 | 0.000 | 0.000 | 144 |
| S7_easy | sgc_ridge | 40 | craf | naive_point | false_member | 0.000 | 0.000 | 0.000 | 144 |
| S7_easy | sgc_ridge | 80 | craf | naive_point | false_member | 0.000 | 0.000 | 0.000 | 144 |
| S7_hard | sage | 20 | craf | naive_point | false_member | -0.028 | -0.066 | 0.010 | 72 |
| S7_hard | sage | 40 | craf | naive_point | false_member | 0.000 | 0.000 | 0.000 | 72 |
| S7_hard | sage | 80 | craf | naive_point | false_member | 0.000 | 0.000 | 0.000 | 72 |
| S7_hard | sgc_ridge | 20 | craf | naive_point | false_member | -0.097 | -0.146 | -0.049 | 144 |
| S7_hard | sgc_ridge | 40 | craf | naive_point | false_member | -0.007 | -0.021 | 0.007 | 144 |
| S7_hard | sgc_ridge | 80 | craf | naive_point | false_member | 0.000 | 0.000 | 0.000 | 144 |
| S8_small_hard | sgc_ridge | 20 | craf | naive_point | false_member | -0.042 | -0.088 | 0.005 | 72 |
| S8_small_hard | sgc_ridge | 40 | craf | naive_point | false_member | 0.000 | 0.000 | 0.000 | 72 |
| S8_small_hard | sgc_ridge | 80 | craf | naive_point | false_member | 0.000 | 0.000 | 0.000 | 72 |
| SS_boundary | semisynthetic | 20 | craf | naive_point | false_member | -0.992 | -0.996 | -0.988 | 2000 |
| SS_boundary | semisynthetic | 40 | craf | naive_point | false_member | -0.988 | -0.993 | -0.983 | 2000 |
| SS_boundary | semisynthetic | 80 | craf | naive_point | false_member | -0.985 | -0.990 | -0.979 | 2000 |
| SS_near | semisynthetic | 20 | craf | naive_point | false_member | -0.237 | -0.256 | -0.218 | 2000 |
| SS_near | semisynthetic | 40 | craf | naive_point | false_member | -0.102 | -0.115 | -0.088 | 2000 |
| SS_near | semisynthetic | 80 | craf | naive_point | false_member | -0.021 | -0.028 | -0.015 | 2000 |
| SS_nonmono_A | semisynthetic | 20 | craf | naive_point | false_member | -0.021 | -0.028 | -0.015 | 2000 |
| SS_nonmono_A | semisynthetic | 40 | craf | naive_point | false_member | -0.006 | -0.009 | -0.003 | 2000 |
| SS_nonmono_A | semisynthetic | 80 | craf | naive_point | false_member | -0.001 | -0.001 | 0.000 | 2000 |
| SS_nonmono_B | semisynthetic | 20 | craf | naive_point | false_member | -0.029 | -0.036 | -0.021 | 2000 |
| SS_nonmono_B | semisynthetic | 40 | craf | naive_point | false_member | -0.003 | -0.005 | -0.000 | 2000 |
| SS_nonmono_B | semisynthetic | 80 | craf | naive_point | false_member | 0.000 | 0.000 | 0.000 | 2000 |
| N6_hard | sgc_ridge | 20 | craf | craf_children | false_member | 0.000 | 0.000 | 0.000 | 144 |
| N6_hard | sgc_ridge | 40 | craf | craf_children | false_member | 0.000 | 0.000 | 0.000 | 144 |
| N6_hard | sgc_ridge | 80 | craf | craf_children | false_member | 0.000 | 0.000 | 0.000 | 144 |
| P3_multi | sgc_ridge | 20 | craf | craf_children | false_member | 0.000 | 0.000 | 0.000 | 72 |
| P3_multi | sgc_ridge | 40 | craf | craf_children | false_member | 0.000 | 0.000 | 0.000 | 72 |
| P3_multi | sgc_ridge | 80 | craf | craf_children | false_member | 0.000 | 0.000 | 0.000 | 72 |
| S7_easy | sgc_ridge | 20 | craf | craf_children | false_member | 0.000 | 0.000 | 0.000 | 144 |
| S7_easy | sgc_ridge | 40 | craf | craf_children | false_member | 0.000 | 0.000 | 0.000 | 144 |
| S7_easy | sgc_ridge | 80 | craf | craf_children | false_member | 0.000 | 0.000 | 0.000 | 144 |
| S7_hard | sage | 20 | craf | craf_children | false_member | 0.000 | 0.000 | 0.000 | 72 |
| S7_hard | sage | 40 | craf | craf_children | false_member | 0.000 | 0.000 | 0.000 | 72 |
| S7_hard | sage | 80 | craf | craf_children | false_member | 0.000 | 0.000 | 0.000 | 72 |
| S7_hard | sgc_ridge | 20 | craf | craf_children | false_member | 0.000 | 0.000 | 0.000 | 144 |
| S7_hard | sgc_ridge | 40 | craf | craf_children | false_member | 0.000 | 0.000 | 0.000 | 144 |
| S7_hard | sgc_ridge | 80 | craf | craf_children | false_member | 0.000 | 0.000 | 0.000 | 144 |
| S8_small_hard | sgc_ridge | 20 | craf | craf_children | false_member | 0.000 | 0.000 | 0.000 | 72 |
| S8_small_hard | sgc_ridge | 40 | craf | craf_children | false_member | 0.000 | 0.000 | 0.000 | 72 |
| S8_small_hard | sgc_ridge | 80 | craf | craf_children | false_member | 0.000 | 0.000 | 0.000 | 72 |
| SS_boundary | semisynthetic | 20 | craf | craf_children | false_member | 0.000 | 0.000 | 0.000 | 2000 |
| SS_boundary | semisynthetic | 40 | craf | craf_children | false_member | 0.000 | 0.000 | 0.000 | 2000 |
| SS_boundary | semisynthetic | 80 | craf | craf_children | false_member | 0.000 | 0.000 | 0.000 | 2000 |
| SS_near | semisynthetic | 20 | craf | craf_children | false_member | 0.000 | 0.000 | 0.000 | 2000 |
| SS_near | semisynthetic | 40 | craf | craf_children | false_member | 0.000 | 0.000 | 0.000 | 2000 |
| SS_near | semisynthetic | 80 | craf | craf_children | false_member | 0.000 | 0.000 | 0.000 | 2000 |
| SS_nonmono_A | semisynthetic | 20 | craf | craf_children | false_member | -0.252 | -0.271 | -0.232 | 2000 |
| SS_nonmono_A | semisynthetic | 40 | craf | craf_children | false_member | -0.536 | -0.558 | -0.514 | 2000 |
| SS_nonmono_A | semisynthetic | 80 | craf | craf_children | false_member | -0.875 | -0.890 | -0.861 | 2000 |
| SS_nonmono_B | semisynthetic | 20 | craf | craf_children | false_member | 0.000 | 0.000 | 0.000 | 2000 |
| SS_nonmono_B | semisynthetic | 40 | craf | craf_children | false_member | 0.000 | 0.000 | 0.000 | 2000 |
| SS_nonmono_B | semisynthetic | 80 | craf | craf_children | false_member | 0.000 | 0.000 | 0.000 | 2000 |
