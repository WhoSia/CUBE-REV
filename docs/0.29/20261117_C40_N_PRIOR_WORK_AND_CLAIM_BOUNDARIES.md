# CUBE-REV 0.29 / C40-N — Prior work and contribution boundary

Date: 2026-11-17.  This is an audit/draft note, **not** a claim that prior manuscripts should be superseded.  Preserve the separate E–M prose alternatives.

## Scholarly placement

1. E. F. Moore, *Gedanken-Experiments on Sequential Machines*, in *Automata Studies* (1956), 129–154, DOI 10.1515/9781400882618-006: foundational experimental state distinguishability.
2. Arthur Gill, *State-identification experiments in finite automata*, *Information and Control* 4 (1961), 132–154, DOI 10.1016/S0019-9958(61)80003-X: explicitly examines minimal preset and adaptive identification experiments.
3. D. Lee and M. Yannakakis, *Testing finite-state machines: State identification and verification*, *IEEE Transactions on Computers* 43 (1994), 306–320, DOI 10.1109/12.272431: generic-machine preset/adaptive existence and complexity.  The 1996 survey DOI 10.1109/5.533956 provides background.
4. G. Bellala, S. K. Bhavnani, C. Scott, *Group-Based Active Query Selection for Rapid Diagnosis in Time-Critical Situations*, *IEEE Transactions on Information Theory* 58 (2012), 459–478, DOI 10.1109/TIT.2011.2169296: target-group identification distinct from complete-state identification.
5. hmakholm (2019), [Rubik's Cube sticker-inspection answer](https://math.stackexchange.com/questions/3297610/how-many-colors-of-a-rubiks-cube-must-be-known-to-locate-all): already states the 21-edge-sticker and 14-corner-sticker fixed construction for 3x3; **attribute it**.
6. D. Eigler (2026), corrected [three-face photograph study](https://dietereigler.at/how-much-of-a-rubiks-cube-does-a-three-face-photograph-determine-wie-viel-verraet-ein-foto-ueber-einen-zauberwuerfel/) and [five-face multiplicities study](https://dietereigler.at/exact-completion-multiplicities-from-five-observed-faces-of-a-rubiks-cube/): entire-face observations, not individually chosen paired sticker frames.  The original five-face universal-uniqueness claim was withdrawn.  Confirm final Zenodo version identifiers before bibliographic freeze.

## What the current manuscript claims

- Equivalence between paired physical probes under free known legal turns and initial-address pair queries (all 24 x 24 = 576 address pairs).
- Exact minimax preset cost 21 paired frames and complete classification of successful 21-frame **address sets**.
- Exact minimax adaptive cost 19 paired frames, attained with a final corner-sign release.
- Global 18-query obstruction *even when the full corner configuration is disclosed*; full quantification over each possible next edge query via adversary certificate.

**Do not claim** that the preset/adaptive distinction, 2019 fixed construction, noisy diagnosis algorithms, generic finite-automaton complexity, or five-face completion problem are new results of this paper.

The complete bilingual drafting work is in Notion:
- [N — Related Work](https://app.notion.com/p/41bef561cf928116bbf8d3f83ddf305b)
- [O — Computational methods](https://app.notion.com/p/41bef561cf9281d5af16ebd27e9a50df)
- [L body](https://app.notion.com/p/41bef561cf9281e9aa94cd2ebfebbd89)
- [M appendices](https://app.notion.com/p/41bef561cf9281259c79da4d854316ae)

## Editorial gates

- Final bibliography should cite Gill (1961) and Lee–Yannakakis (1994), not only the later survey.
- Separate preset 21 *existence* (prior art) from our fixed lower bound and characterization.
- Distinguish exact worst-case paired-frame costs from observed-face counts and expected query costs.
- Resolve DOI/version ambiguity for Eigler's corrected work prior to release.
