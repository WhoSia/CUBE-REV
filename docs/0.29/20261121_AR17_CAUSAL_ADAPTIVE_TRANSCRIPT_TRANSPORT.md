# CUBE-REV 0.29 AR17 — Causal Decision-Tree Transcript Transport and Referee Controls

**21 November 2026 · Research claim with Lean implementation in `formal/029/SignedPolicyTranscript.lean` pending pinned run verification.**

## 1. Why a posterior theorem is not by itself a policy-execution theorem

AR2 established an exact normalized posterior equality after an *arbitrary fixed sequence* of labeled paired observations. This is the correct algebra of beliefs, but a skeptical algorithms referee can ask whether the **queries chosen by an adaptive controller**, themselves dependent on previous responses, are transported in the same order.

To answer this objection without enumerating all paths, consider a representative decision tree `P` that, at each read node, chooses a representative address `q` and branches according to paired reply `r`. Fix the color-normalization map `sigma`, a 12-edge slot reordering `beta` with a concrete inverse, and a correction bit selected from the preceding eleven replies. The actual physical-coordinate policy is `P.adapt queryToOriginal (responseToRepresentative sigma) decode`.

The key point is that `queryToOriginal beta q` is constructed *from the current node's representative address* and the past-fixed order before the physical sensor replies, and the actual answer is then recoded to `responseToRepresentative sigma q r`. Neither operation may inspect a future reply.

## 2. The causal feedback transcript theorem

Let `Log(P)` denote the same adaptive decision tree with a terminal output equal to the ordered sequence of its visited pairs `(q_0,r_0),...,(q_k,r_k)`. The source adapter executes physical original-address queries, then recodes the replies and logs them **in representative coordinates**:
```
TLog(sigma,beta,P)
  := (P.logged []).adapt
       (queryToOriginal beta)
       (responseToRepresentative sigma)
       identity
```

The AR17 Lean theorem states that for every eligible `sigma`, every explicit invertible slot order `beta`, any **fixed** parity-correction bit `eps`, all tagged original cubie/corner states `s`, and **every** representative adaptive policy `P`,
```
TLog(sigma,beta,P).run signedRealPairRead s
   = P.transcript signedRepresentativePairRead
       (signedRepresentativeEncode sigma beta eps s).
```

**Proof.** AR1's exact paired-response equivariance proves equality of the recoded physical sensor reply and the representative model's reply at every possible chosen query, *not merely at the queries visited by one initial simulation*. `Policy.run_fixed_reply_equiv`, applied to `P.logged []`, then shows the logged controller follows identical response-dependent branches on both sides. `Policy.adapt_run` equates the actual adapted controller's run to this recoded representative log, and `Policy.logged_run` identifies the logged output with the ordered `Policy.transcript` of `P`. No enumeration of six-color reply strings or final cube states is required. □

The accompanying budget theorem follows by composing `Policy.logged_fits` (logging does not add reads) with `Policy.adapt_fits` (address and answer recoding do not add reads):
```
Fits k P -> Fits k (TLog sigma beta P).
```

**Crucial scope boundary:** this theorem is about the *entire adaptive continuation after a chosen fixed normalization witness*, not a proof that the first-eleven normalization selector is itself correct. The result logs representative addresses and replies. The physical addresses differ by the explicit `queryToOriginal` map, exactly as the physical probe compiler requires.

## 3. Terminal criterion and parity oracle impossibility

A representative terminal must be checked against the actual legal belief to show it uniquely determines the initial physical state. `SignedTerminalIdentification.lean` implements exact nonempty singleton terminal beliefs, their equivalence under the invertible signed-state map for *every ordered history*, and a direct impossibility theorem for a freely attached, unobservable Bool parity tag.

The latter theorem is universal in policy length: given the same original cubie/corner coloring `s`, the paired sticker sensor returns identical answers in the states `(s,false)` and `(s,true)`. Hence every adaptive decision tree follows the same branch path and cannot output both distinct tagged states correctly. A genuine parity choice at frame nineteen requires a separately proved legal-cube relation from **actually observed** corner colors, never a free sign query.

## 4. Reviewer attack and formal test outline

| Attack | Expected failure prevented by |
| --- | --- |
| A policy chooses its next physical sensor address using the answer to that same query | `Policy.adapt` builds address from the current representative tree node before receiving a response |
| Static eleven-color histogram normalization used to infer arbitrary continuation history | Exact `Policy.logged_run` equality over every feedback `P`, and a fixed witness selected before continuation |
| A hidden scalar sign is appended to paired color responses | The signed real observation ignores the tag; `cannot_recover_an_independent_parity_oracle` proves it could not be recovered for both choices |
| Empty posterior silently passes as a valid identified initial cube | `beliefExactlyOne` requires an explicit candidate and excludes empty beliefs |
| Two opposite-parity candidates are collapsed merely because they share a first-color histogram | Explicit signed encoder is injective and remembers `sigma,beta,eps` |
| A final theorem claims 19 recovery based solely on 52 counts | Still requires exact 52-tree reification, every feasible branch, terminal corner parity, and physical routing |

## 5. What remains mathematically novel and unproved

The two new AR17 theorems are universal **structural transport** results for adaptive decision trees. They materially reduce the complexity of the last proof: instead of checking correspondence separately for 141,097 frozen policy nodes, one can check **one observation covariance law and one causal interpreter**. But they do not establish the existence of a correct actual 19-frame policy; that burden is held by the frozen 52-tree certificate and its missing Lean semantic coupling.

For the next unit, construct a *total chosen* normalization from every feasible ordered first-eleven original color string, prove the stable-sort position order really is an `EdgeSlotOrder`, and prove that the correction `eps` is the signed color-label/position-sort cocycle. The exact 19-frame corner scan's final usable information time must also be preserved.
