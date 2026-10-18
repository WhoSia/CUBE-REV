# CUBE-REV 0.27 P4 — Exact 54-Facelet Contiguous-Window Replacement Court and 17HTM Search Pivot

**Result date 2026-10-18, source-fixed LOCAL finite computation. No shortest-distance promotion.**

## Exact physical experiment
Original Seoul Summer 2026 Final A #1 scramble:
`R' B' F2 D2 F2 L2 R2 U' F2 L2 D2 B2 D F L' R2 B U2 F2 R2`.
Known exactly verified original fixed-frame 18HTM witness:
`F U F D' R' F' L' F' D' L B L2 F2 U2 L2 U F' R2`.
The code rereads original P11 C++ physical `packed_physical.hpp` P[18][54] and checks literal source concatenated with witness restores all 54 labeled stickers.

**Theorem confined to this frozen witness:** No single contiguous subword of length 2 through 9 can be replaced by a strictly shorter HTM word representing the same full 54-sticker permutation. There are **108** such windows, all exhaustively checked. Their counts by width 2–9: 17,16,15,14,13,12,11,10. A complete canonical HTM solved-radius4 enumeration gave exact whole-54-site layer sizes **1,18,243,3240,43239**, union **46741** distinct group elements. For widths≤8, all replacements length≤7 split into left≤4 and right≤3. For width9 all replacements length≤8 split into left≤4 and right≤4. The code evaluates each target subword's exact 54-permutation, computes `left=target∘inverse(right)`, and matches a full-state, not projected, hash map of all left words≤4; strict length check. **810606 exact full permutation hash queries; ZERO strict shortenings**. Controls check source+witness=identity, `U U=U2` and commute `U D=D U`. Algorithm execution and code in T0 `P4_EXACT_LOCAL_WINDOW_COURT.zip`, SHA256 `e31e37a416f81c2b651885b9a9007528516d84db3ee7f9d5bbbf94f9af4459f4`. Machine receipt contains all 108 windows and authentic original C++ header SHA.

## Retrospective reason for pivot
Older original 0.26 R3-P11-P2 Court A fully tried 3502 premove q's at length≤3 with fixed 11-action phase1 p, enumerated 582 fixed-DR source completions, and found no trace-reduced 17-word. Court B 525 adjacent phase1 variants×3502 q was exploratory and found no new 17 witness. That negative scoped court plus today's exact full-HTM short-window court make **further local edits to this one witness low priority**. They do NOT exclude a genuine globally different 17HTM word; they do not establish a probability of no17.

## Main hard problem and proof architecture
Remaining exact-distance alternatives:
- Independently find one full-54-facelet-verified 17HTM solving word for the original scramble; combined with the now externally reproduced conditional lower17 that would establish `d18(s)=17` under existing canonical/physical assumptions.
- Or rigorously exclude every length17 solution using source-complete depth11 versus solved B6 or another admissible complete split, establishing `d18(s)=18` with existing upper witness. The previous source-depth10 vs B6 court proves only no length16.

**Next experiments should explore genuinely different DR-entry prefixes / all DR axes / nonlocal NISS phase1 families, using full-state exact final verification, unique witness logging, and measured resource/case coverage. Do not promote a sample or bounded phase1 family to a global negative theorem.** The main thesis becomes a proof-carrying fixed-source geodesic method with exact-distance search as the next substantial theorem, not simply an ever larger exploration transcript.

## Proof boundary
P4 is a **LOCAL complete finite subfamily refutation** only. No new GH Actions run, no new formal Lean statement, no claim of globally d=18. The 0.27 external Go 10-root run #39087089460 remains PASS and the archived Drive T2 bundle remains sealed. Scientific interval externally reproduced under stated physical and canonical assumptions is 17..18.
