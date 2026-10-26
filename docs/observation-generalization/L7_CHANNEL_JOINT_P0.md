# L7 physical observation across three error channels — P0 receipt

## Physical model and proof boundary

Every experiment is a seven-action word in the 18 HTM generators. Each
source state is one of 12 oriented-edge start slots with initial bit zero;
the observation transcript is the sequence of seven post-action orientation
bits. The target family consists of all 220 triples and all 495 quadruples.
For each target source set, some ONE dictionary word must allow correction
under the given noise channel. Words are shared across targets but the word
used for a particular target may differ.

- `substitution1`: minimum pairwise Hamming distance >= 3.
- `erasure1`: minimum pairwise Hamming distance >= 2 (known erased position).
- `burst_erasure2`: any two adjacent known erased positions leave pairwise
  unequal transcripts.

## Channel dominance theorem

For every physical word and source set,

```
cover(substitution1, word) subset cover(erasure1, word)
cover(substitution1, word) subset cover(burst_erasure2, word)
```

Reason: a nonzero difference in at least three time positions cannot be
eliminated by one known erasure or by two adjacent erased time positions.
Therefore an experiment that succeeds in all three channels is exactly one
that succeeds in `substitution1`. If a common dictionary is required to
cover the source family under every channel, but experiments can be chosen
per target/channel, the conclusion remains true: the substitution channel
is a necessary condition, and covering it is sufficient for the others.
Thus, within the stated semantics and full physical word universe:

`M*_joint(L,R,{substitution1, erasure1, burst_erasure2}) =
 M*_substitution1(L,R)`.

This equality is structural and does NOT assert that individual
`erasure1` and `burst_erasure2` minima are equal.

## Independently replayed constructive bounds

An exact 2^11-subdictionary enumeration of the existing eleven L7
physical words shows that each of the three channels requires all eleven
when selection is restricted to these eleven words, despite different
individual-word coverage.

A reproducible seeded search used 5,000 one-to-four-action mutations around
the eleven incumbent words (seed 20261026); 4,108 unique actual words were
generated. A separate 715-row MILP on up to 850 high-coverage distinct
physical columns per channel plus incumbent columns yielded:

| channel | feasible L7 dictionary size | finite-pool MILP result |
|---|---:|---|
| substitution1 | 11 | optimum 11 in screened pool |
| erasure1 | **7** | optimum 7 in screened pool |
| burst_erasure2 | 11 | optimum 11 in screened pool |
| simultaneous joint | **11** | by channel dominance; physical 11-word certificate |

The seven-word physical known-erasure witness is archived at
`docs/observation-generalization/L7_ERASURE1_7_WORD_COVER.json`;
independent 54-sticker replay is in
`scripts/cuberev-observation/verify_l7_erasure7_cover.py`.
It covers all 715 source sets for one known erasure but covers only 332
under one arbitrary substitution, so the distinction between channel
design problems is substantive. The proof that the screened column optimum
is seven is NOT a global seven-word minimum theorem.

Established global bounds inherited from earlier work:
`3 <= M*_substitution1(7, R3 U R4) <= 11`, and consequently
`M*_erasure1(7, R3 U R4) <= 7`,
`M*_burst_erasure2(7,R3 U R4) <= 11`.
The earlier zero-error 7-step noninjectivity of any one word gives a
universal lower bound at least three for each channel using every triple
and quadruple source set (the two-collision-pair argument), subject to
the same observation semantics. Hence tentative physical ranges:
`3 <= M*_erasure1 <= 7`, `3 <= M*_burst_erasure2 <= 11`,
`3 <= M*_joint = M*_substitution1 <= 11`.
These are NOT proven exact global optima.

## Relation to existing literature

Hierons & Türker, *Incomplete Distinguishing Sequences for Finite State
Machines*, Computer Journal 58 (2015), 3089–3113,
doi:10.1093/comjnl/bxv041, already study collections of incomplete
distinguishing sequences and related complexity. Türker, Hierons &
Jourdan, *Minimizing Characterizing sets*, Science of Computer Programming
208 (2021), 102645, doi:10.1016/j.scico.2021.102645, specifically
addresses minimizing state-characterizing test sets. There is no basis
to claim that set-cover or the noise-channel monotonicity theorem is
globally novel. The research candidate is the exact physical
action-observation structure, channel-dependent optimal dictionaries,
and independently certified physical bounds.
