# CUBE-REV R1.15 — Korean Semantic Master

> 상태: **논문 의미 구조 초안 / evidence 아님 / manuscript freeze 아님**
>
> 목적: 문장을 예쁘게 만드는 것이 아니라, 현재 seal들이 실제로 지지하는 가장 좁고 강한 논증을 드러내고 반증 가능하게 만드는 것.

## Working title

**Behavioral Reconstruction Traces Are Not Self-Interpreting: Observation-operator Failure, Transport, and Authority in Competitive Speedcubing**

한국어 작업 제목:

**행동 재구성 로그는 스스로 해석되지 않는다: 경쟁 큐빙에서 관측연산자의 실패·수송·주장권한**

## 1. 문제

전문가가 남긴 세밀한 행동 로그는 풍부해 보이지만, 로그 자체가 곧바로 인지과정의 관측치는 아니다. 특히 Rubik's Cube reconstruction은 move notation, annotated phase label, cubie state, solving-method convention을 동시에 포함한다. 같은 move sequence도 어떤 연산자로 읽느냐에 따라 `redundant detour`, `phase reversal`, `subgoal violation`, `frame change`, `ordinary algorithm geometry` 중 전혀 다른 사건으로 분류될 수 있다.

따라서 핵심 문제는 '어떤 move가 실수였는가'가 아니라 다음이다.

> **행동 trace에서 연구용 현상으로 넘어가는 observation operator가 실제로 식별 가능한가? 그 operator의 불변성·null behavior·transportability·authority를 어떻게 검증할 것인가?**

## 2. 논문의 중심 주장

CUBE-REV의 현재 가장 강한 논문 크기 주장은 cognitive-recovery prevalence가 아니다.

현재 가장 방어 가능한 주장은 다음이다.

> **Behavioral reconstruction traces are not self-interpreting. Plausible observation operators can generate apparently meaningful signals while failing representation, null, transport, or method-semantic courts. A defensible trace-based methodology therefore requires operator-specific falsification, provenance-aware calibration, and explicit claim authority before behavioral interpretation.**

이 주장은 speedcubing을 case study로 사용하지만, 모든 행동로그에 대한 보편정리로 확장하지 않는다.

## 3. 왜 Rubik's Cube reconstruction인가

Rubik's Cube는 몇 가지 특성이 동시에 존재한다.

1. 상태공간과 move algebra가 정확히 정의돼 있다.
2. 실제 경쟁 수행과 public result infrastructure가 존재한다.
3. 인간 reconstruction에는 move sequence와 phase/method annotation이 남는다.
4. 전문가는 primitive move보다 learned algorithm, block, pair, orientation/permutation 같은 중간 구조를 사용한다.
5. 따라서 notation과 latent subgoal 사이의 간극을 state-level로 공격할 수 있다.

기존 Rubik's Cube 연구에는 skill acquisition, expertise, decomposition/macro-operator, algorithm acquisition, collective improvement 등이 존재한다. R1.15의 제한적 문헌 탐색에서는 실제 reconstruction trace의 observation-operator authority를 본 논문과 같은 방식으로 다루는 직접 analogue를 찾지 못했다. 그러나 이 novelty 문장은 systematic review가 끝날 때까지 HOLD다.

## 4. Empirical spine와 증거 계층

CUBE-REV의 empirical spine은 public WCA/reco.nz linkage와 reconstruction trace다. 하지만 모든 artifact를 독립된 증거로 세지 않는다.

증거 계층은 다음처럼 본다.

- **Public-data provenance:** WCA results + reco.nz reconstruction linkage.
- **Development/calibration lineage:** 기존 route corpus에서 operator 설계·반증·null calibration.
- **Attempt-disjoint/prospective tests:** operator 또는 null을 outcome 전에 동결한 후 평가.
- **Preexisting-unseen transport:** development에는 없지만 baseline에는 이미 있던 route에 frozen operator 적용.
- **Post-freeze fresh authority:** baseline 이후 새로 생긴 route에 frozen operator 적용 — 현재 DATA_WAIT.

동일 generation 내부의 여러 JSON/runner는 독립 replication 수로 세지 않는다.

## 5. Observation-operator succession

### 5.1 Exact-local move equivalence

초기 아이디어는 더 짧거나 동등한 local route가 존재하면 관찰된 추가 move를 detour/recovery 후보로 볼 수 있다는 것이었다. 그러나 equivalence를 더 엄격하게 만들수록 신호가 붕괴했고, 최종 noncommuting primitive definition은 이후 R1.8 attempt-disjoint holdout에서도 0/888로 재현됐다.

**결론:** shorter/equivalent local representation은 standalone cognitive-recovery operator가 아니다.

### 5.2 Full-state phase-endpoint distance

다음 아이디어는 phase endpoint로부터의 full-state distance였다. 중간에 거리가 증가했다가 돌아오면 recovery처럼 보일 수 있었다. 하지만 raw pre-endpoint reversal은 약 63.8%로 흔했고, frozen max-excursion null은 candidate-reversal statistic과 맞지 않게 과도하게 보수적이었다. matched posthoc statistic에서 나타난 4.36% standardized tail도 calibration familywise null 5.96%를 넘지 않았다.

**결론:** full-state reversal 역시 standalone recovery marker가 아니다.

### 5.3 Phase-objective quotient geometry

R1.9는 irrelevant cubie coordinates를 quotient하고 phase-specific objective/preservation structure를 사용했다. 이 geometry와 directly attempt-level familywise null은 calibration court를 통과했지만, future-score transport가 solving method별로 달랐다. CFOP/ZB는 안정적이었고 Roux가 global transport를 무너뜨렸다.

**결론:** 더 좋은 geometry도 method semantics를 무시하면 transport authority를 얻지 못한다.

### 5.4 Roux frame/gauge problem

Roux에서는 first/second block identity를 어떻게 시간축에 보존할지가 핵심이 됐다. center-canonical frame, arbitrary orientation quotient, first-SB annotation endpoint 등은 각각 실패했다.

- first `ROUX_SB` line은 대개 completed second block이 아니라 `SS` subphase였다.
- orientation-free first block은 찾을 수 있었지만 많은 경우 center/color relabeling을 요구했다.
- per-state center canonicalization은 route-persistent frame으로 기능하지 않았다.

R1.12–13은 결국 FB prefix만으로 unique route gauge를 식별하고 explicit x/y/z rotation 아래 gauge를 transport하는 구조로 이동했다. 이 과정에서도 'rotation이 residual failure의 원인'이라는 targeted hypothesis와 wide/slice general cocycle 가설은 각각 반증됐다.

**결론:** 수학적으로 정의 가능한 coordinate transformation과 연구대상에 맞는 method ontology는 다른 문제다.

### 5.5 G4 canonical block-preservation ontology

R1.14는 다음 observable categories를 outcome score와 독립적으로 정의했다.

- `CANONICAL_FB_PRESERVING`
- `BLOCK_DISRUPTIVE_RESIDUAL`
- `FB_PRESERVED_NO_COMPLETION_RESIDUAL`

Development 130 eligible routes에서 114/12/4로 분리됐고, canonical 114개만으로 rebuilt reference null이 zero fallback과 1% empirical resolution을 유지했다.

그 뒤 development에 쓰지 않은 preexisting-unseen 120 raw Roux route에 frozen operator를 적용했다.

- state-certified 117/120
- prefix unique 116/117
- canonical 105/117 = 89.74%
- block-disruptive 11
- canonical feature 731
- local-reference fallback 0
- reference contamination 0

따라서 **G4 ontology transport는 preexisting-unseen lane에서 PASS**했다.

그러나 post-freeze genuinely fresh Roux route는 0개였으므로 future authority는 release되지 않았다.

## 6. 통계적 기여의 범위

이 논문의 통계적 핵심은 새로운 estimator 자체라기보다 **measurement operator와 multiplicity/transport authority를 연결하는 protocol**이다.

중요한 설계는 다음이다.

1. segment threshold를 여러 번 본 뒤 any-positive로 합치지 않고 attempt statistic을 직접 calibration한다.
2. outer test fold가 local reference와 familywise reference 모두에 들어가지 않는 nested construction을 사용한다.
3. future-scale scorer와 crossfit score의 compatibility를 별도 gate로 검사한다.
4. add-one empirical tail의 finite resolution을 데이터 N과 함께 명시한다.
5. posthoc diagnostic과 prospective authority를 분리한다.

## 7. 실패는 결과다

이 프로젝트의 논문 가치가 positive phenotype 하나에 있지 않은 이유는 실패한 operator들이 단순 시행착오가 아니라 **falsified measurement hypotheses**이기 때문이다.

압축하면:

- shorter path ≠ cognitive detour
- full-state reversal ≠ cognitive recovery
- annotation family ≠ completed subgoal
- orientation equivalence ≠ persistent physical frame
- valid group action ≠ sufficient method ontology
- preexisting-unseen transport ≠ genuinely fresh authority

이 succession 자체가 observation-operator validation의 사례가 된다.

## 8. 현재 허용되는 가장 강한 결론

현재 seal들이 지지하는 결론은 다음 정도다.

> Public expert reconstruction traces can support rigorous state-level measurement research, but only after the trace-to-phenomenon mapping is treated as a falsifiable observation operator. In CUBE-REV, multiple plausible mappings failed representation, null, or transport courts. A later Roux ontology based on prefix-identifiable gauge and first-block preservation transported to a development-unseen reconstruction set under a frozen reference null. This does not yet establish cognitive recovery/error prevalence or genuinely post-freeze Roux authority.

## 9. 현재 쓰면 안 되는 결론

- '우리는 speedcuber의 cognitive recovery를 측정했다.'
- 'canonical/residual은 인간의 전략 유형이다.'
- 'Roux solver의 약 10%가 first-block을 깨는 전략을 쓴다.'
- 'G4는 population prevalence를 추정한다.'
- 'preexisting unseen은 independent fresh replication이다.'
- 'CUBE-REV가 세계 최초다.'

## 10. Literature bridge — 현재 상태

현재 targeted search에서 확인한 이웃 문헌:

- Rubik's Cube real-world skill acquisition and ability predictors.
- macro-operators and non-serializable subgoals in Rubik's Cube problem solving.
- decomposition patterns and incomplete representations in Rubik-like tasks.
- collective algorithm acquisition and expert performance in competitive cube communities.
- computational cube-state representation, symmetry, and solving agents.

현재 gap hypothesis:

> Existing work studies learning, expertise, search, algorithms, decomposition, or performance, while CUBE-REV focuses on the validity of the observation operator mapping real reconstruction traces into behavioral constructs.

이 문장은 **systematic literature gap court 이전에는 hypothesis**다.

## 11. 예상 referee attack

1. **'이건 긴 디버깅 로그를 논문화한 것 아닌가?'**  
   답: 단순 bug history는 버리고, 결과를 바꾼 falsified measurement hypotheses만 본문에 남겨야 한다. operational bugs는 reproducibility appendix/TRACE로 분리한다.

2. **'인지과학 논문인데 인간 ground truth가 없다.'**  
   답: 그러므로 cognitive prevalence를 주장하지 않는다. 논문을 measurement-methodology paper로 한정한다. 인간 ground truth가 필요한 claim은 debt로 남긴다.

3. **'R1.7–R1.14가 모두 같은 데이터의 반복 튜닝 아닌가?'**  
   답: 맞는 부분이 있다. 그래서 artifact count를 replication count로 쓰지 않고 lineage-level evidence로 취급한다. strongest external test는 frozen G4를 development-unseen 120-route lane에 transport한 것이다. post-freeze fresh authority는 아직 없다.

4. **'Roux ontology가 cubing community convention을 코드로 옮긴 것뿐 아닌가?'**  
   답: convention은 prospective observable definition을 정하는 motivation일 뿐이다. classification은 annotation text가 아니라 state trajectory와 frozen gauge operator가 결정한다. 다만 ontology가 cognition을 의미한다는 주장은 하지 않는다.

5. **'왜 speedcubing이어야 하나?'**  
   답: exact algebra/state plus natural expert traces plus algorithmic subgoals가 동시에 존재하여 observation-operator falsification을 unusually tractable하게 만든다. Generalization은 discussion hypothesis로만 제시한다.

## 12. Manuscript debt

### Blocking before preprint freeze

- systematic novelty/literature-gap audit
- figure-ready operator succession schematic
- provenance-family ablation of central argument
- exact source-map linking every numeric sentence to sealed artifact
- decide whether CFOP/ZB should remain a secondary branch or be removed from the main narrative for focus

### Blocking only stronger scientific claims

- post-freeze fresh Roux N≥20 for future authority
- human validation for any cognitive recovery/error interpretation
- population-support design for full-WCA prevalence

## 13. Proposed paper spine

1. Introduction: trace abundance does not solve construct validity.
2. Observation-operator framework.
3. Data/provenance and authority hierarchy.
4. Successive falsification of local-equivalence and full-state-distance operators.
5. Phase quotient and attempt-level null.
6. Method-semantic failure and Roux gauge problem.
7. G4 state ontology and development-unseen transport.
8. What remains unvalidated: fresh authority and cognition.
9. Discussion: observation operators as first-class objects in expert behavioral trace research.

## 14. Current disposition

**A coherent paper-sized methodological claim exists.**

하지만 현재 상태는 `MANUSCRIPT_BRIDGE`, not `MANUSCRIPT_FROZEN`이다. 다음 단계는 더 많은 결과를 만드는 것이 아니라, claim compression과 provenance-family ablation을 통과시키고 systematic literature debt를 닫는 것이다.
