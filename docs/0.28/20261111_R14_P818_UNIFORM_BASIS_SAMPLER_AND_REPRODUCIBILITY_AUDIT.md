# CUBE-REV 0.28 — R14-P8.18: Uniform Certified Bases and Source-Reproducibility Repair

Date: 2026-11-11. Status: mathematically exact finite algorithm, CONDITIONAL on inherited physically certified B6=16 and 156 complete minimum sensor layout family; independent local rank/unrank comparison PASS. No new 41-class physical shortest-distance execution, unrestricted P48 color-frame optimum, or Lean kernel result.

## Theorem: exact, zero-rejection uniform optimum generation

An original cube edge h is one of twelve. The previously certified geometrical admissibility relation P(h) contains exactly thirteen unordered pairs of original edges, for each h. Omit the two corners adjacent to h and the two edges in a pair chosen from P(h). Every one of the 12*13=156 choices produces an identifying 16-tag sensor arrangement on B6, and each of the 156 arrangements is generated EXACTLY ONCE. Thus choosing h uniformly and then its allowed pair uniformly samples an arbitrary globally optimal 16-tag design with mass 1/156, without a post-hoc trial/rejection or a new injectivity oracle.

## Exact indexing of all 432 inclusionwise minimal designs

The 276 nonminimum minimal 17-tag designs split into 12 omissions of an original core edge and its two endpoint original corners, and 264 omissions of one original corner plus one of 33 special original-edge pairs for each of eight corners. For corner c, those 33 edge pairs are the complement of the union of the three positive-16 edge-pair families of the three incident original core edges. Thus there is a unique deterministic unranking from ranks 0..155 to all 156 optimal layouts, from ranks 156..431 to all 276 minimal17 layouts, and a uniform random integer rank from 0..431 samples every inclusion-wise minimal design uniformly.

Uniform over all minimal designs gives P(minimum16)=156/432=13/36, P(nonminimum minimal17)=23/36, expected retained sensor count =599/36. This differs from uniform-validity-oracle greedy deletion success 1166/1995 and corner-first greedy success 11/12. Uniform terminal sampling does not imply a high chance of reaching global optimum. Naive uniform random omissions of any four of 20 original tags succeed with probability 156/4845=52/1615, and choosing a core edge followed by an unrestricted uniform unordered edge pair succeeds with probability 13/66, whereas the exact admissible-core generator succeeds with probability one. These are proposal-acceptance probabilities, not estimates of total physical experiment cost.

## Executable proof / independent regression

New source: scripts/cuberev-observation/audit_r14_p818_exact_uniform_basis_sampler.py; exhaustively maps each of the 156 minimum and 276 other minimal indices to a distinct exact sensor omission, compares sets against independently classified P8.13 geometric arrays, and outputs one JSON. A separate local Python construction independently verified the 156 and 276 bijections, their disjointness, and full 432 coverage. Physical support and B12 distance facts are INHERITED from prior CUBE-REV; this local computation does not rerun them.

Reproducibility repair #1: P8.13 validation printed a full JSON receipt when imported. Its P8.14 import consumer consequently received a second unsolicited result, violating the one-JSON-per-executable contract. The P8.13 output has been placed beneath a __main__ guard without changing its standalone certificate calculation. Read-only workflow .github/workflows/cuberev-r14-p818-uniform-minimal-bases.yml requires import stdout to be empty and P8.14/P8.18 JSON responses to parse independently. The remote result has NOT been observed, so actual CI PASS is pending.

Reproducibility repair #2: P8.15 seeded Monte Carlo used eligible actions in unordered frozenset iteration order. Fixing the RNG seed without sorting that list did not guarantee the same experimental sample across Python hash seeds. The action candidates are now sorted before using random.choice. Exact rational probabilities have not been modified. Prior reported 58413/100000 was diagnostic, not a stable cross-process transcript.

## Academic judgment and next gate

Do not claim a separate new publication from uniform sampling: it is a useful constructive corollary of physically certified 156/276 classification. The current more promising broad question is how physically restricted B_r sensing changes with r, and what structural obstructions force genuinely nonmatroidal minimal sensors; requires at least a second radius with independent source-complete evidence. Focus next on independent 41 positive B12-geodesic class and 872 support-mask replay with raw inputs, and the full-P48 categorical 19-frame unresolved question. Preserve merged C0.1 as one candidate, not as the main research task.

No new Drive intake or PDF rewrites; preserve human WhoSia GitHub commits on research/current, read-only CI, Notion as semantic registry.
