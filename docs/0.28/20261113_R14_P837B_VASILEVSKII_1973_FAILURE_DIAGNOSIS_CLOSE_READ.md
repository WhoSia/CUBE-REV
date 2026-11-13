# R14-P8.37B — Vasilevskii (1973), Failure Diagnosis of Automata: failure-vs-state identification

Original [canonical journal translation PDF](https://drive.google.com/file/d/17l_o-qW9esqefiBl73bc3OzBa4sR6Y3N/view) SHA-256 `97918787df36d8962e2e16dbd1a4e4036580a9df8a4e81ae3875101084e4dca1`, 13 PDF pages, publisher print pp. 653–665; DOI [10.1007/BF01068590](https://doi.org/10.1007/BF01068590). Springer metadata calls it *Cybernetics* 9, 653–665 **(1973)** and marks English translation of *Kibernetika* **4**, 98–108 (July–August 1973), submission 25 Nov. 1972. The scanned English PDF has a literal ©**1975** Plenum imprint; this is a source-edition/copyright discrepancy, NOT grounds to rewrite the publisher bibliography as 1975 or pretend the page is a 1973 original-language scan.

## Problem read directly from text

Vasilevskii's opening adopts a Moore-type conformance setting: the experimenter knows a target finite-state machine (A), and sees another machine with only a bound (k) on the number of states; decide whether observed behavior equals (A)'s. This is **machine failure diagnosis / conformance**, not simply determination of an unknown starting state of a known machine. The paper explicitly uses Mealy machines and distinguishes **simple** experiments (one chosen input word) from **multiple** experiments (several words applied to a *reset initial state*). It measures total input-letter length and, for multiple experiments, multiplicity. Its introductory discussion says the multiple-experiment upper-bound order approaches known lower bounds and frames its experiments as **unconditional**, where the first behavior discrepancy resolves the conformance decision.

This choice of goal and experiment boundary matters: do NOT transfer the paper's bounds wholesale into the reversible Rubik posterior color game. Our experiment has one hidden legal initial cube state and known legal moves, two-site color responses and a worst-case **number of observation frames**. We do not assume multiple physical independent resets to an unknown initial machine state, nor count only action-letter length.

## Specific proof/technical relation

The article's early lemmas construct short lexicographically ordered input words that reach distinct automaton states. Distinguishing input-word sets induce a testing suite; this is related to **separating families** and source-vs-target sample complexity but has a different notion of failure, admissibility, and reset semantics. When conducting CUBE-REV 19-frame tests, record explicitly whether proposed policies rely on resetting to an original state, on observing the current state, or on allowing cost-free moves; these change the theorem being proved.

## New checkable risk for Paper B

A 19-frame solver must not reuse results about *multiple reset experiments*, or output diagnosis of a faulty **unknown automaton**, to justify a branch-depth lower bound for a **single unknown legal group element**. The clean transfer is only definitional: a family of input-output histories partitions the initial candidate set; different experimental cost functions entail different minimax recurrences.

Retained uncertainty: full theorem-by-theorem transcription from the 1975-imprint English scan has not been reconstructed in formal notation; scanned math has OCR artifacts. This report grounds the early definitions, not an unverified reproduction of every quantitative theorem.