# The ten-state example and its observation response

For a legal fixed-center state $x$ and an original edge or corner sticker position $i$, write $c_i(x)$ for the sticker color. For an ordered pair $q=(e,k)$ of one edge and one corner position, define $R_q(x)=(c_e(x),c_k(x))$. With tracked legal turns, these coordinates are pulled back to the initial state. For a history $H=((q_t,a_t))_t$, the surviving set is $S(H)=\{x\in\Omega:R_{q_t}(x)=a_t\text{ for every }t\}$, where $\Omega$ is the stated legal state space. The notation is a proposed convention for the new manuscript.

In the worked example all corners and seven edges are known in their solved configurations. The five remaining edge positions are UR, UF, UL, UB, DR, in that order. Starting from the solved ordered labels, enumerate the 60 even permutations and 16 even flip assignments. At position A read both slots as F,U; at positions B and C read the first slot as R and U respectively. Ten states survive. The six unqueried edge slots are B2, C2, D1, D2, E1, E2. All other coordinates are constant in this example.

For a specified first query, the program separately optimizes worst-case depth and total stopping depth over the remaining decision trees. The uniform expected size after the first response is the sum of squared branch sizes divided by ten. It is a one-step quantity. C2 is the only first query guaranteeing depth two. D1 has five responses and leaves an expected 13/5 candidates, compared with three responses and 18/5 for C2. Their minimum mean costs are both two, with respective minimum worst costs three and two. The fixed optimum is three. The probability assumption applies only to the mean and expected-size calculations.

Run from the repository root:

    python3 scripts/cuberev-observation/audit_r29_ten_state_query_cost.py

The program enumerates the legal residual assignments and computes the table directly. Compare its output with the committed JSON.

## Prior work for the manuscript

- Moore, *Gedanken-Experiments on Sequential Machines* (1956), “Experiments,” discusses inputs that depend on previous outputs. DOI 10.1515/9781400882618-006.
- Lee and Yannakakis, *Testing Finite-State Machines: State Identification and Verification* (1994), Section III, Definition 3.1, defines adaptive identification by a tree and its length by depth. DOI 10.1109/12.272431.
- Buhrman and de Wolf, *Complexity Measures and Decision Tree Complexity: A Survey* (2002), Introduction, gives the deterministic query and depth terminology for Boolean functions. DOI 10.1016/S0304-3975(01)00144-X.
- Cicalese, Laber and Saettler, *Diagnosis Determination: Decision Trees Optimizing Simultaneously Worst and Expected Testing Cost* (2014), Section 1, formulates hypothesis identification through discrete queries and distinguishes worst and expected cost. PMLR 32(1), 414–422.

The contribution is the exact 21/19 result in the specified two-probe legal cube model, with its constructive policy and lower bound. The ten-state example illustrates the mechanisms and separates one-step discrimination from optimal continuation. Its enumeration is a finite local reproduction. Priority against every equivalent cube model remains open.
