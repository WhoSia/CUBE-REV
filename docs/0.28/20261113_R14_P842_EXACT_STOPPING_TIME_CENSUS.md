# R14-P8.42 — Exact stopping-time census for the 19-frame policy

The P8.41 theorem establishes the worst-case adaptive value of 19 paired frames. Here the initial cube is uniform over the legal fixed-center states. We count the stopping times of the specific P8.40 policy and of a variant that minimizes the worst-case continuation depth for each eleven-read edge history. Both use the same corner scan and learn edge permutation sign only after frame 14.

## From canonical replay to an exact population count

Fix an ordered eleven-color edge prefix. Its P8.40 transport to a representative maps every completion bijectively, including the sign offset, and transports the adaptive policy. For a feasible count vector (n), precisely (11!/\prod_c n_c!) ordered prefixes have that vector. For a representative (r), sum these multinomials over the vectors that map to (r) to obtain the multiplicity (w_r). Multiply its canonical frame histogram by (w_r) and sum over the 52 representatives.

An independent orientation count checks every member's fiber size. Enumerate the (2^{11}) even-flip assignments to the twelve distinct edge labels and choose which label sits at the unread position. Count the resulting eleven-color multiset. With one ordered history fixed, each such orientation and unread-label choice yields exactly (\prod_c n_c!) assignments of the labeled observed edges. The script checks this product against the canonical enumerator for each of the 1,362 count vectors. The total weighted edge population is (12!2^{11}=980,995,276,800).

Each edge state admits (8!3^7/2=44,089,920) legal corner completions of its own sign. In both policies the only corner information affecting the edge schedule is that sign at frame 14, when full corner recovery is guaranteed. Thus each edge state's stopping frame applies to all its corner completions, giving the exact cube population of 43,252,003,274,489,856,000.

## Exact results

| Stopping frame | P8.40 edge states | Prefix-minimax edge states | P8.40 probability | Prefix-minimax probability |
| --- | ---: | ---: | ---: | ---: |
| 17 | 83,783,145,600 | 85,863,254,400 | 8.54063% | 8.75267% |
| 18 | 812,872,368,000 | 837,226,051,200 | 82.86201% | 85.34455% |
| 19 | 84,339,763,200 | 57,905,971,200 | 8.59737% | 5.90278% |

The mean drops from 7962875/442368 (18.00057) to 7950017/442368 (17.97150) frames, an exact reduction of 2143/73728 frames. The 19-frame tail drops by 2.69459 percentage points, or about 31.34% relative. The receipt also gives exact full-cube counts. The probabilities refer to a uniform initial legal cube.

## Conditional minimax

Use the same exact P8.40 continuation recurrence, with a three-frame delay before parity is supplied. Try increasing continuation budgets at each representative until the first feasible one. The resulting root ceilings are 17 frames for 6 representatives, 18 for 34, and 19 for 12. The 12 hard representatives account for 280,694,937,600 edge states, about 28.61% of the population. This is the mass of histories with a 19-frame conditional ceiling. Within each such history an individual state may finish earlier. The receipt separately gives the exact stopping counts for each policy and the conditional ceiling counts.

A remaining objective is minimizing expected stopping time across all suffix trees subject to the 19-frame global cap. Conditional minimax solves the maximum-depth objective independently at each prefix. In particular, minimizing the conditional maximum and minimizing the global mean are distinct objectives, and neither statement compares policies with different prefix designs or a different corner schedule.

## Reproduce

Run `python3 scripts/cuberev-observation/audit_r14_p842_stopping_times.py` and compare its output with `data/0.28/R14_P842_STOPPING_TIME_RECEIPT.json`. The script also replays the prefix-minimax variant on the 2,001 fixed physical geometry states and verifies all 576 probe pairs via the P8.40 physical replay.
