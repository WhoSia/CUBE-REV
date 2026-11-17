# The ten-state example and its observation response

For a legal fixed-center state $x$ and an original edge or corner sticker position $i$, write $c_i(x)$ for the sticker color. For an ordered pair $q=(e,k)$ of one edge and one corner position, define $R_q(x)=(c_e(x),c_k(x))$. With tracked legal turns, these coordinates are pulled back to the initial state. For a history $H=((q_t,a_t))_t$, the surviving set is $S(H)=\{x\in\Omega:R_{q_t}(x)=a_t\text{ for every }t\}$, where $\Omega$ is the stated legal state space. The notation is a proposed convention for the new manuscript.

In the worked example all corners and seven edges are known in their solved configurations. The five remaining edge positions are UR, UF, UL, UB, DR, in that order. Starting from the solved ordered labels, enumerate the 60 even permutations and 16 even flip assignments. At position A read both slots as F,U; at positions B and C read the first slot as R and U respectively. Ten states survive. The six unqueried edge slots are B2, C2, D1, D2, E1, E2. All other coordinates are constant in this example.

For a specified first query, the program separately optimizes worst-case depth and total stopping depth over the remaining decision trees. The uniform expected size after the first response is the sum of squared branch sizes divided by ten. It is a one-step quantity. C2 is the only first query guaranteeing depth two. D1 has five responses and leaves an expected 13/5 candidates, compared with three responses and 18/5 for C2. Their minimum mean costs are both two, with respective minimum worst costs three and two. The fixed optimum is three. The probability assumption applies only to the mean and expected-size calculations.

Run from the repository root:

    python3 scripts/cuberev-observation/audit_r29_ten_state_query_cost.py

The program enumerates the legal residual assignments and computes the table directly. Compare its output with the committed JSON.

## Identifying a property of the same ten states

A target assigns each state to one of several answer classes. A query history identifies the target when all states consistent with that history lie in one class. For a fixed plan, group the states by their joint color signature at its selected addresses and require each group to be contained in one answer class. For an adaptive plan, each admissible query is followed by the worst of its nonempty color branches, and the algorithm minimizes over the next query. A branch stops as soon as the target is constant on its candidates.

For example, ask whether D holds UL or UR. The answers to C2 are L, B, and R. The target is false on the L branch and true on the B and R branches, so one query suffices. Identifying the initial arrangement of all the pieces on this same restricted instance costs three fixed reads or two adaptive reads.

The count below ranges over **unlabeled partitions**, not named physical properties. For each target, the entire fixed list or adaptive policy may be chosen with knowledge of that target. The underlying ten states and the six allowed addresses are the same throughout.

| Number of answer classes | Fixed 1, adaptive 1 | Fixed 2, adaptive 2 | Fixed 3, adaptive 2 |
| --- | ---: | ---: | ---: |
| 2 | 61 | 450 | 0 |
| 3 | 101 | 8,400 | 829 |

The total numbers are 511 and 9,330. The 829 three-class examples are formal partitions of this instance. They do not imply that three classes are necessary for an adaptive advantage on other cube histories. A two-read list may differ from one target to the next; no two-read list identifies all ten states.

Run from the repository root:

    python3 scripts/cuberev-observation/audit_r29_ten_state_query_cost.py --targets

### A second history with a binary gap

Keep the known pieces and the four observed addresses. Change their returned colors from F,U,R,U to U,F,U,U in the order A1,A2,B1,C1. This history leaves 12 candidates. The binary target is true exactly on the six unread words BLURDR, BRRDLU, LBDRUR, LRBURD, RBLURD, RLRDBU, in slot order B2,C2,D1,D2,E1,E2. This is a specified mathematical grouping of the twelve states.

Read B2 first. Its replies R and L use D1 next, and reply B uses E1. The program checks that each resulting leaf has a single target value. It also checks every fixed pair and finds a collision across target values in each. For example, reading D1 and E1 cannot distinguish LBDRUR and BRDRUL, both of which give (D,U). The fixed list B2,C2,D1 succeeds, so the fixed and adaptive depths are 3 and 2. Thus the absence of a two-class gap on the ten states depends on the history, even with the same known pieces and query addresses.

## Prior work for the manuscript

- Moore, *Gedanken-Experiments on Sequential Machines* (1956), “Experiments,” discusses inputs that depend on previous outputs. DOI 10.1515/9781400882618-006.
- Lee and Yannakakis, *Testing Finite-State Machines: State Identification and Verification* (1994), Section III, Definition 3.1, defines adaptive identification by a tree and its length by depth. DOI 10.1109/12.272431.
- Buhrman and de Wolf, *Complexity Measures and Decision Tree Complexity: A Survey* (2002), Introduction, gives the deterministic query and depth terminology for Boolean functions. DOI 10.1016/S0304-3975(01)00144-X.
- Cicalese, Laber and Saettler, *Diagnosis Determination: Decision Trees Optimizing Simultaneously Worst and Expected Testing Cost* (2014), Section 1, formulates hypothesis identification through discrete queries and distinguishes worst and expected cost. PMLR 32(1), 414–422.

Bellala, Bhavnani and Scott, *Group-Based Active Query Selection for Rapid Diagnosis in Time-Critical Situations* (2012), Section III, distinguishes identification of an object from identification of its class. The paper optimizes expected query count for binary queries and given priors. The census above uses worst-case depth on multi-color sticker queries. DOI [10.1109/TIT.2011.2169296](https://doi.org/10.1109/TIT.2011.2169296).

The fixed 21-edge-color and 14-corner-color construction, including the use of corner parity to resolve the edge assignment, is already described in a [public answer from 2019](https://math.stackexchange.com/questions/3297610/how-many-colors-of-a-rubiks-cube-must-be-known-to-locate-all). The paired-frame lower bound, schedule characterization and adaptive optimum belong to the present analysis.

The contribution is the exact 21/19 result in the specified two-probe legal cube model, with its constructive policy and lower bound. The ten-state example illustrates the mechanisms and separates one-step discrimination from optimal continuation. Its enumeration is a finite local reproduction. Priority against every equivalent cube model remains open.
