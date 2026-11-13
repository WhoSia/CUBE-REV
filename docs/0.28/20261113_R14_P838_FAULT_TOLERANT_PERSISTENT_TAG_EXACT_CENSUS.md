# CUBE-REV R14-P8.38 — One and two arbitrary permanent-sensor failures: exact static census

**Date:** 2026-11-13. **Proof model:** full pose (position AND orientation) of chosen persistently labeled original corners or edges of a legal fixed-center 3×3 cube, with **adversarial sensor erasure**, not erroneous sensor values. An entire chosen original cubie measurement may fail and become unavailable. Color-frame sensor model is **not** used.

## Mathematical definition and main exact results

Let \(\Omega=C\sqcup E\), with \(|C|=8\), \(|E|=12\). For a state subset \(X\subseteq G\), define \(\mathcal I(X)\) as in P8.34. Let
\[
\mathcal I_f(X)=\{S\subseteq\Omega:\ \forall F\subseteq S,\ |F|\le f\implies S\setminus F\in\mathcal I(X)\}.
\]
This is adversarial **deletion** of at most \(f\) *entire original-cubie full-pose sensors*, with detection of which sensor failed. No replacement sensor measurements, duplicate physical sensors, reset operation, or probabilistic assumption.

**Freshly computed and independently passed CI result**:
| selected tag count | identify B6, 0 failures | B6 tolerant to 1 failure | B6 tolerant to 2 failures | identify B7, 0 failures | B7 tolerant to 1 failure | B7 tolerant to 2 failures |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 16 | 156 | 0 | 0 | 0 | 0 | 0 |
| 17 | 672 | 0 | 0 | 0 | 0 | 0 |
| 18 | 174 | 0 | 0 | 96 | 0 | 0 |
| 19 | 20 | **12** | 0 | 20 | 0 | 0 |
| 20 | 1 | **1** | 0 | 1 | **1** | 0 |

Thus the exact optimal single-erasure designs at B6 number **12** with 19 selected tags. For B7 (and globally) the **only** single-erasure design is the complete set of all 20 original tags. There is **NO** 2-erasure-tolerant design on B6 or B7 using at most one independent pose reading per original cubie. The 19-tag B6 robust designs omit one original **edge** each; this type conclusion is a combinatorial interpretation of the 12 symmetry-related cases and should be separately enumerated if made a kernel-level formal proof assertion. The 20-tag design is the obvious one-extra-tag descendant and is not minimal at B6.

**Analytic global/B7 explanation:** P8.34 proved \(\mathcal I(B_7)=\mathcal I(G)=\{S:|S\cap C|\ge7,|S\cap E|\ge11\}\). A single failure from a selected set can remove a corner or edge. To preserve the thresholds under *any* one deletion, it is necessary to initially select **all eight corners AND all twelve edges** (unless one type was never selected, already excluded). Conversely, the 20-tag set after any one removal retains at least seven corners and eleven edges. Two deletions from all20 can remove two corners and violate the B7 pair-collision certificate. Thus B7 is not 2-erasure-tolerant.

**Analytic B6 impossibility under two deletions:** P8.34 showed not all 18-tag layouts identify B6: only 174 of 190 are valid. The complete 20-tag layout can lose any two sensors, so the 16 bad eighteen-tag deletions immediately defeat its 2-erasure tolerance. Any smaller layout also cannot be 2-erasure-tolerant: if S were, any of its supersets would be by upward closure under arbitrary deletions, contradicting failure for all20.

## Executable evidence

[Fresh exact executable](../../scripts/cuberev-observation/audit_r14_p838_static_fault_tolerant_sensor_family.py) imports and replays prior physical obstruction generators (872 B6 and 94 B7 supports). It first builds the upward closure of each physical mask, then runs all \(2^{20}=1,048,576\) original-tag subset selections, and for each B6/B7-identifying selection tests all 0/1/2 deleted subsets. **The positive B6 verdict still relies on P8.33's 41-target exact C++ MITM proof**; no false claim that this Python script recomputed 41 C++ distance certificates.

[Read-only CI run 43361772300](https://github.com/WhoSia/CUBE-REV/actions/runs/43361772300) completed SUCCESS; job 131676713947, test and receipt upload succeeded. The verified JSON reports B6 one-fault 19-tag count 12, 20-tag count 1, and B7 one-fault 20-tag count 1; all two-fault counts zero. The program is an **exact finite census**, not an extrapolation or random sampling.

## Scientific connection to Krishnan & Rajan 2016

The newly read [*Fault-Tolerant Resolvability of Certain Crystal Structures*](https://drive.google.com/file/d/1QoXCxia9GnLZ_Z8sGpbm2D8n7wbsLdAx/view) defines fault-tolerant **metric resolving sets** where removing any one selected **graph vertex landmark** leaves all graph vertices distinguished by shortest-path distances. Our erasure quantifier has a formally analogous pattern but uses **different observation maps** (full original-cubie pose instead of graph distance), so we must NOT call these CUBE-REV numbers metric dimension, or attribute this combinatorial design result to Krishnan–Rajan. Its general robustness concept is prior art, not a new principle.

## Next scientific questions

1. Does the first B6 robust family also undergo a strict collapse when moving to B7? **Yes**, exactly 13 one-failure tolerant B6 designs reduce to 1 at B7, losing 12. The exact sets should be archived as explicit 20-bit masks in future artifact for third-party reproduction.
2. Test erasures where sensor values are not missing but can be **incorrect**: identification under adversarial substitution requires code-distance ≥2f+1, not the same as erasure-failure tolerance; no such theorem is claimed here.
3. Explore **redundant repeated sensors of the same original cubie** as a separate hardware design space. All20 sensor erasure limit disappears if independent duplicates are allowed, so cardinality must be redefined, and the current impossibility does not apply.

**Editorial verdict:** valuable focused robustness appendix or supporting note for Paper A, rather than a third main theorem of unified C0.3; keep the general-paper ambition centered on radius-six-to-seven family saturation and the distinct adaptive color channel.