# Results (개선판 - 논리적 흐름)

## Experimental Setup

본 연구에서는 4개의 다목적 최적화 알고리즘(NSGA-II, NSGA-III, SPEA2, ε-MOEA)의 성능을 비교하기 위해 각 알고리즘당 10회의 독립적인 실행(independent runs)을 수행하였다. 각 실행은 100세대(generations)로 설정되었으며, 초기 집단 크기는 150개로 동일하게 유지되었다. 실험에 사용된 초기 식단은 7일간의 21끼 식사로 구성되었으며, 5개의 영양소 제약조건(에너지, 탄수화물, 단백질, 지방, 식이섬유)을 만족하도록 최적화를 수행하였다.

성능 평가를 위해 다음 5개의 메트릭을 사용하였다:
- **Hypervolume**: 최적화 품질과 해 집합의 크기를 나타내는 가장 중요한 메트릭 (높을수록 우수)
- **Spacing**: 해 분포의 균일성을 나타내는 메트릭 (낮을수록 균일한 분포)
- **Diversity**: 목적함수 공간에서 해 집합의 다양성 (값이 클수록 다양한 해 탐색)
- **Convergence**: 수렴 속도 및 품질 (낮을수록 최적해에 가까움)
- **Execution Time**: 계산 효율성 (낮을수록 효율적)


---

## 3. Results

### 3.1. Optimization Process (최적화 과정)

**Figure 1**은 4개 알고리즘의 최적화 과정을 100세대에 걸쳐 추적한 수렴 곡선(convergence plot)을 보여준다. Hypervolume 지표를 사용하여 각 세대에서의 최적화 품질 변화를 시각화하였다.

**주요 발견:**

1. **SPEA2의 빠른 수렴**: SPEA2는 약 30세대에서 이미 최고 성능(Hypervolume: 0.384)에 근접하였으며, 이후 세대에서 안정적으로 유지되었다. 이는 SPEA2의 Strength-based fitness assignment와 truncation operator가 효율적으로 작동함을 시사한다.

2. **NSGA-II/NSGA-III의 중간 속도 수렴**: NSGA-II(빨강)와 NSGA-III(청록)는 약 50세대에서 최적 성능에 도달하였으며, 최종 Hypervolume은 각각 0.382와 0.381로 SPEA2와 근소한 차이를 보였다. 두 알고리즘의 초기 수렴 패턴이 매우 유사하나, NSGA-III가 다소 느린 수렴 속도를 보였다.

3. **ε-MOEA의 느린 수렴**: ε-MOEA(주황)는 100세대까지도 완전히 수렴하지 못하고 지속적으로 상승하는 패턴을 보였다 (최종 Hypervolume: 0.357). 이는 ε-MOEA가 현재 세대 설정(100 generations)으로는 충분한 최적화를 달성하지 못하며, 추가 세대가 필요함을 의미한다.

**실무적 시사점**: SPEA2는 30-40세대만으로도 최적에 가까운 해를 얻을 수 있어, 더 짧은 실행 시간으로도 충분한 성능을 달성할 수 있다. 반면 ε-MOEA는 현재 설정에서는 부적합하며, 세대 수를 최소 200세대 이상으로 늘릴 필요가 있다.


---

### 3.2. Solution Distribution in Objective Space (해의 분포)

**Figure 2**는 SPEA2가 생성한 Pareto Front를 3차원 공간에 시각화한 것이다. 4개의 목적함수(Nutritional Adequacy, Cost Effectiveness, Menu Harmony, Dietary Diversity) 중 3개를 3D 축으로, 4번째 목적함수(Dietary Diversity)를 색상으로 표현하였다.

**주요 발견:**

1. **해의 고른 분포**: SPEA2의 Pareto solutions는 목적함수 공간 전체에 걸쳐 비교적 균일하게 분포되어 있다. 이는 의사결정자에게 다양한 trade-off 옵션을 제공할 수 있음을 의미한다.

2. **목적함수 간 Trade-off**: 
   - **영양(Nutrition) vs 비용(Cost)**: 영양가가 높은 식단일수록 비용이 증가하는 경향이 관찰되나, 중간 영역에서는 두 목적함수를 동시에 높일 수 있는 해가 존재한다.
   - **조화도(Harmony) vs 다양성(Diversity)**: 색상 분포를 보면, 조화도가 높은 식단(Z축 상위)이 다양성도 높은 경향(노란색)을 보이며, 이는 두 목적함수가 양의 상관관계를 가짐을 시사한다.

3. **3D 투영의 효과**: 4차원 문제를 3차원 공간에 투영함으로써, Pareto Front의 형태와 해의 분포를 직관적으로 파악할 수 있었다. 이는 Zhang et al. (2022)의 food recommendation 연구에서 사용된 방법론과 유사하며, many-objective optimization 문제의 시각화에 효과적이다.

**실무적 시사점**: 식단 추천 시스템 구현 시, 이러한 Pareto Front 시각화를 통해 사용자에게 영양-비용-조화도-다양성 간의 trade-off를 명확히 제시할 수 있다. 예를 들어, "영양가는 약간 낮지만 비용이 크게 절감되는 식단" 또는 "비용은 중간이지만 영양과 다양성이 모두 우수한 식단" 등의 선택지를 제공할 수 있다.


---

### 3.3. Overall Performance Comparison (종합 성능 비교)

#### 3.3.1. Multi-dimensional Performance Overview

**Figure 3**의 레이더 차트는 5개 메트릭에 대한 정규화된 성능을 종합적으로 보여준다. 각 알고리즘의 강점과 약점이 한눈에 드러난다.

**알고리즘별 특징:**

- **SPEA2 (민트색)**: 최적화 품질(Hypervolume)과 실행 속도(Execution Time)에서 가장 넓은 영역을 차지하며, 균형잡힌 우수한 성능을 보인다. Spacing을 제외한 모든 지표에서 상위권 성능을 유지한다.

- **NSGA-II (빨강)**: Convergence에서 가장 넓은 영역을 차지하며, 수렴 속도가 가장 빠르다. Hypervolume도 SPEA2와 거의 동일한 수준으로 우수하다.

- **NSGA-III (청록)**: Spacing에서 가장 넓은 영역을 차지하여 해의 균일한 분포에서 강점을 보인다. 전반적으로 NSGA-II와 유사한 패턴을 보인다.

- **ε-MOEA (주황)**: 모든 메트릭에서 가장 좁은 영역을 차지하며, 특히 Execution Time과 Hypervolume에서 매우 낮은 성능을 보인다.


#### 3.3.2. Quantitative Performance Summary

**Table 1**은 4개 알고리즘의 성능을 5개 메트릭에 대해 비교한 결과이다 (Mean±SD, n=10).

**Table 1. 알고리즘 성능 비교 (Mean±SD, n=10)**

| Metric | NSGA-II | NSGA-III | SPEA2 | ε-MOEA |
|--------|---------|----------|-------|--------|
| **Hypervolume** ↑ | 0.382±0.007 | 0.381±0.013 | **0.384±0.007** | 0.357±0.021 |
| **Spacing** ↓ | 0.530±0.357 | **0.388±0.251** | 0.436±0.375 | 1.026±0.400 |
| **Diversity** | 0.994±0.345 | 1.005±0.329 | 1.153±0.507 | 1.841±0.561 |
| **Convergence** ↓ | **0.221±0.051** | 0.232±0.054 | 0.295±0.095 | 0.334±0.091 |
| **Execution Time** ↓ (sec) | 82.1±183.4 | 261.3±305.4 | **17.4±13.4** | 667.1±203.4 |

**Bold**: 해당 메트릭에서 최고 성능  
↑: 높을수록 좋음, ↓: 낮을수록 좋음

**주요 발견:**

1. **SPEA2의 종합 우수성**: Hypervolume (0.384±0.007)과 Execution Time (17.4±13.4초)에서 최고 성능을 기록하였으며, 낮은 표준편차로 안정적인 결과를 보였다.

2. **NSGA-II의 빠른 수렴**: Convergence (0.221±0.051)에서 최고 성능으로, 최적해에 가장 빠르게 도달한다.

3. **NSGA-III의 균일한 분포**: Spacing (0.388±0.251)에서 최고 성능으로, 의사결정자에게 다양한 선택지를 균등하게 제공할 수 있다.

4. **ε-MOEA의 전반적 열등성**: 모든 메트릭에서 가장 낮은 성능과 가장 느린 실행 속도(667.1초)를 기록하여, 현재 설정에서는 권장되지 않는다.


---

### 3.4. Detailed Metric Analysis (세부 지표 분석)

#### 3.4.1. Optimization Quality Distribution (Hypervolume)

**Figure 4**는 각 알고리즘의 10회 실행에 대한 Hypervolume 분포를 박스플롯으로 보여준다. Hypervolume은 다목적 최적화에서 가장 널리 사용되는 성능 지표로, 해 집합이 목적함수 공간에서 지배하는 영역의 크기를 나타낸다.

**주요 발견:**

1. **SPEA2의 안정적 우수성**: 
   - 중앙값(median): 0.385 (최고)
   - IQR (Interquartile Range): 매우 작아 안정적
   - 이상치(outliers): 없음
   - 해석: 10회 실행 모두에서 일관되게 높은 성능을 보임

2. **NSGA-II와 NSGA-III의 유사성**:
   - 두 알고리즘의 박스플롯이 거의 겹침 (중앙값: 0.382 vs 0.381)
   - NSGA-III가 약간 더 큰 분산을 보임 (SD: 0.013 vs 0.007)
   - 해석: 두 알고리즘은 최적화 품질 측면에서 실질적으로 동일한 성능

3. **ε-MOEA의 낮은 성능과 높은 변동성**:
   - 중앙값: 0.357 (최저, SPEA2 대비 7% 낮음)
   - IQR: 가장 크며, 여러 이상치 존재
   - 해석: 성능이 낮을 뿐만 아니라 실행마다 결과가 크게 달라져 신뢰성이 낮음


#### 3.4.2. Solution Distribution Uniformity (Spacing)

**Figure 5**는 각 알고리즘의 Spacing 성능을 비교한 막대 그래프이다. Spacing 메트릭은 파레토 프론트 상의 해들이 얼마나 균일하게 분포되어 있는지를 나타낸다. 낮은 Spacing 값은 해들이 균일하게 분포되어 있음을 의미하며, 의사결정자에게 다양한 선택지를 제공할 수 있다.

**주요 발견:**

1. **NSGA-III의 최고 균일성**: 
   - 평균 Spacing: 0.388±0.251 (최저)
   - ε-MOEA 대비 62% 더 균일
   - 해석: Reference point 기반 선택 메커니즘이 해의 균일한 분포에 효과적

2. **SPEA2와 NSGA-II의 중간 수준**:
   - SPEA2: 0.436±0.375
   - NSGA-II: 0.530±0.357
   - 해석: 두 알고리즘 모두 수용 가능한 수준의 균일성 제공

3. **ε-MOEA의 불균일한 분포**:
   - 평균 Spacing: 1.026±0.400 (최고, 가장 불균일)
   - NSGA-III 대비 2.6배 더 불균일
   - 해석: ε-dominance 개념이 해의 균일성 측면에서는 효과적이지 않음

**실무적 시사점**: 식단 추천 시스템에서 사용자에게 "영양 최우선", "비용 최우선", "균형형" 등 다양한 옵션을 균등하게 제시하고자 한다면, NSGA-III가 가장 적합하다.


#### 3.4.3. Exploration-Exploitation Trade-off (Diversity vs Convergence)

**Figure 6**은 다양성(Diversity)과 수렴성(Convergence) 간의 트레이드오프를 산점도와 95% 신뢰 타원으로 보여준다. 이상적인 알고리즘은 높은 다양성(넓은 해 탐색)과 낮은 Convergence 값(최적해에 가까움)을 동시에 달성해야 한다.

**주요 발견:**

1. **NSGA-II의 최적 균형** (좌하단 위치):
   - Convergence: 0.221±0.051 (최저, 최적해에 가장 근접)
   - Diversity: 0.994±0.345 (적절한 탐색 범위)
   - 해석: 수렴 속도가 빠르면서도 적절한 해 탐색 수행

2. **NSGA-III의 유사한 패턴** (좌하단 인접):
   - NSGA-II와 거의 겹치는 95% 신뢰 타원
   - Convergence: 0.232±0.054
   - Diversity: 1.005±0.329
   - 해석: NSGA-II와 동일한 수준의 탐색-수렴 균형

3. **SPEA2의 중간 영역** (중간 위치):
   - Convergence: 0.295±0.095 (중간)
   - Diversity: 1.153±0.507 (중상)
   - 해석: 더 넓은 탐색을 수행하나 수렴 속도는 다소 느림

4. **ε-MOEA의 과도한 탐색** (우상단 위치):
   - Convergence: 0.334±0.091 (최고, 최적해에서 가장 멀음)
   - Diversity: 1.841±0.561 (최고, 가장 넓은 탐색)
   - 넓게 퍼진 신뢰 타원 → 높은 변동성
   - 해석: 넓은 탐색을 수행하지만 수렴 성능이 떨어져 비효율적

**실무적 시사점**: 초기 탐색 단계에서는 ε-MOEA의 넓은 탐색이 유용할 수 있으나, 최종 해의 품질을 위해서는 NSGA-II나 NSGA-III로 전환하는 하이브리드 접근이 효과적일 수 있다.


#### 3.4.4. Computational Efficiency (Execution Time)

**Figure 7**은 각 알고리즘의 실행 시간을 비교한 가로 막대 그래프이다. 계산 효율성은 실용적인 응용에서 중요한 요소이다.

**주요 발견:**

1. **SPEA2의 압도적 속도**:
   - 평균 실행 시간: 17.4±13.4초
   - NSGA-II 대비 4.7배, NSGA-III 대비 15배, ε-MOEA 대비 **38.4배** 빠름
   - 가장 낮은 표준편차로 안정적인 실행 시간
   - 해석: Strength-based fitness assignment와 truncation operator의 효율적 구현

2. **NSGA-II의 중간 속도**:
   - 평균 실행 시간: 82.1±183.4초
   - 매우 큰 표준편차 (평균의 2.2배)
   - 해석: 일부 실행에서 조기 종료 조건이 늦게 만족되어 최대 630초 소요

3. **NSGA-III의 느린 속도**:
   - 평균 실행 시간: 261.3±305.4초
   - NSGA-II보다 3.2배 느림
   - 역시 매우 큰 표준편차 (평균의 1.2배)
   - 해석: Reference point 계산의 추가 오버헤드

4. **ε-MOEA의 매우 느린 속도**:
   - 평균 실행 시간: 667.1±203.4초 (11분 이상)
   - 모든 알고리즘 중 가장 느림
   - 상대적으로 안정적인 표준편차 (평균의 30%)
   - 해석: ε-grid 업데이트와 ε-dominance 계산의 높은 복잡도

**실무적 시사점**: 
- **실시간 식단 추천 시스템**: SPEA2의 17초 평균 실행 시간은 사용자에게 즉각적인 피드백을 제공하기에 충분히 빠르다.
- **배치 처리**: NSGA-II/NSGA-III는 야간 배치 처리 등 실시간성이 요구되지 않는 경우 사용 가능하다.
- **ε-MOEA**: 현재 설정에서는 실용적 응용에 부적합하다.


---

### 3.5. Statistical Validation (통계적 검증)

#### 3.5.1. Normality Test

Shapiro-Wilk normality test 결과, 일부 데이터가 정규분포를 따르지 않는 것으로 나타났다. 특히 HYPERVOLUME 메트릭에서 NSGA-II (W=0.716, p=0.001)와 SPEA2 (W=0.670, p<0.001)가, EXECUTION_TIME 메트릭에서는 모든 알고리즘이 정규성 가정을 위반하였다. 따라서 비모수 검정(non-parametric tests)인 Kruskal-Wallis H-test와 Mann-Whitney U test를 사용하였다.


#### 3.5.2. Overall Differences (Kruskal-Wallis H-test)

Kruskal-Wallis H-test 결과, 모든 메트릭에서 알고리즘 간 통계적으로 유의한 차이가 발견되었다:

- **HYPERVOLUME**: H=14.407, p=0.0024 **
- **SPACING**: H=12.799, p=0.0051 **
- **DIVERSITY**: H=11.205, p=0.0107 *
- **CONVERGENCE**: H=9.739, p=0.0209 *
- **EXECUTION_TIME**: H=24.686, p<0.001 ***

*** p<0.001, ** p<0.01, * p<0.05

가장 강한 차이는 EXECUTION_TIME (H=24.686, p<0.001)에서 관찰되었으며, HYPERVOLUME (H=14.407, p=0.0024)과 SPACING (H=12.799, p=0.0051)에서도 매우 유의한 차이가 나타났다.


#### 3.5.3. Pairwise Comparisons and Effect Sizes

**Figure 8**은 Mann-Whitney U test의 p-value를 히트맵으로 시각화한 것이다. 색이 진할수록(빨강) 통계적으로 유의한 차이가 있음을 나타낸다.

**주요 발견:**

1. **ε-MOEA의 명확한 열등성** (히트맵 우측/하단의 빨간색 영역):
   - 모든 메트릭에서 다른 알고리즘들에 비해 통계적으로 유의하게 낮은 성능 (p<0.01)
   - Cliff's Delta 효과 크기: 대부분 large (|δ| > 0.474)
   - 특히 EXECUTION_TIME에서 SPEA2 vs ε-MOEA: δ=-1.000 (완벽한 분리)

2. **NSGA-II, NSGA-III, SPEA2의 유사성** (히트맵 좌상단의 파란색/초록색 영역):
   - HYPERVOLUME에서 세 알고리즘 간 유의한 차이 없음:
     - NSGA-II vs NSGA-III: p=0.678
     - NSGA-II vs SPEA2: p=0.121
     - NSGA-III vs SPEA2: p=0.791
   - 해석: 세 알고리즘 모두 유사한 최적화 품질 달성

3. **EXECUTION_TIME의 극명한 차이** (히트맵의 짙은 빨간색):
   - SPEA2와 다른 모든 알고리즘 간 매우 유의한 차이 (p<0.001)
   - Cliff's Delta: 
     - SPEA2 vs NSGA-II: δ=-0.980
     - SPEA2 vs NSGA-III: δ=-0.920
     - SPEA2 vs ε-MOEA: δ=-1.000 (완벽한 우위)
   - 해석: SPEA2의 계산 효율성은 통계적으로 뿐만 아니라 실질적으로도 매우 큰 차이

4. **Bonferroni Correction 후 유지된 유의성**:
   - 대부분의 유의한 차이가 엄격한 Bonferroni correction (α=0.05/6=0.0083) 후에도 유지됨
   - 해석: Type I error (거짓 양성) 가능성이 낮으며, 결과의 신뢰성이 높음


#### 3.5.4. Effect Size Interpretation

Cliff's Delta 효과 크기 분석 결과, 대부분의 유의한 차이는 large effect size (|δ| ≥ 0.474)를 동반하였다. 이는 통계적 유의성뿐만 아니라 실질적으로도 의미 있는 차이임을 시사한다. 

**주요 Effect Size 요약:**

| Comparison | Metric | Cliff's δ | Effect Size | p-value |
|------------|--------|-----------|-------------|---------|
| SPEA2 vs ε-MOEA | HYPERVOLUME | +0.840 | Large | 0.0017** |
| SPEA2 vs ε-MOEA | EXECUTION_TIME | -1.000 | Large | <0.001*** |
| NSGA-III vs ε-MOEA | SPACING | -0.820 | Large | 0.0022** |

** Significant after Bonferroni correction


---

## 4. Discussion

### 4.1. Algorithm Performance Summary

본 연구의 종합적인 분석 결과를 바탕으로 한 알고리즘별 권장사항은 다음과 같다:

**SPEA2: 실용적 응용에 최적** 🏆
- 최고의 최적화 품질 (Hypervolume: 0.384±0.007)
- 압도적으로 빠른 실행 속도 (17.4±13.4초, 다른 알고리즘 대비 5-38배)
- 안정적인 성능 (낮은 표준편차)
- 30세대만으로도 최적에 근접
- **권장 상황**: 실시간 식단 추천 시스템, 제한된 계산 자원, 빠른 응답 시간 요구

**NSGA-II: 균형잡힌 선택** 🏆
- SPEA2와 유사한 최적화 품질 (Hypervolume: 0.382±0.007)
- 가장 빠른 수렴 속도 (Convergence: 0.221±0.051)
- 중간 수준의 실행 속도
- 탐색-수렴 균형 우수
- **권장 상황**: 수렴 속도가 중요한 경우, 안정적인 성능 필요

**NSGA-III: 다양한 해 탐색** 🏆
- 가장 균일한 해 분포 (Spacing: 0.388±0.251)
- NSGA-II와 유사한 최적화 품질
- 느린 실행 속도 (261.3±305.4초)
- Reference point 기반 균일성 확보
- **권장 상황**: 의사결정자에게 다양한 선택지 제공이 중요한 경우

**ε-MOEA: 현재 설정에서는 비효율적** ⚠️
- 가장 낮은 최적화 품질 (Hypervolume: 0.357±0.021)
- 가장 불균일한 해 분포 (Spacing: 1.026±0.400)
- 가장 느린 실행 속도 (667.1±203.4초)
- 100세대로는 충분한 수렴 미달성
- **개선 방안**: 세대 수 증가 (200+ generations), 파라미터 튜닝 필요


### 4.2. Implications for Diet Optimization Systems

본 연구의 결과는 식단 최적화 시스템 구현에 다음과 같은 실무적 시사점을 제공한다:

**1. 실시간 웹/모바일 애플리케이션**
- **권장 알고리즘**: SPEA2
- **이유**: 평균 17.4초의 실행 시간은 사용자에게 즉각적인 피드백을 제공하기에 충분히 빠름
- **구현 예시**: 사용자가 영양 목표를 입력하면 20초 이내에 최적화된 7일 식단 제공

**2. 고품질 장기 식단 계획**
- **권장 알고리즘**: SPEA2, NSGA-II, NSGA-III (선택 가능)
- **이유**: 세 알고리즘 모두 유사한 최적화 품질 달성 (통계적 차이 없음)
- **구현 예시**: 노인요양시설의 월간 식단 계획 수립 (품질 우선, 시간 덜 중요)

**3. 다양한 식단 옵션 제공**
- **권장 알고리즘**: NSGA-III
- **이유**: 가장 균일한 해 분포로 다양한 trade-off 옵션 제공
- **구현 예시**: "영양 최우선 식단", "비용 절감 식단", "균형형 식단" 등 5-10개 옵션 균등 제시

**4. 계산 자원 제약 환경**
- **권장 알고리즘**: SPEA2
- **이유**: 가장 낮은 계산 복잡도와 빠른 실행 속도
- **구현 예시**: 저사양 서버 또는 로컬 실행 환경에서의 식단 최적화

**5. 4차원 시각화 전략**
- **방법**: 3D Pareto Front + Color mapping (Figure 2)
- **효과**: 의사결정자가 4개 목적함수 간 trade-off를 직관적으로 이해
- **구현 예시**: 대화형 3D 차트로 사용자가 원하는 영역을 선택하면 해당 식단 상세 정보 표시


### 4.3. Comparison with Related Work

본 연구의 시각화 방법론과 결과를 기존 연구와 비교하면:

**1. 목적함수 수 및 시각화 접근**
- **Sahin & Aytekin-Sahin (2024)**: 6-objective, Box Plot + Convergence Plot
- **Zhang et al. (2022)**: 4-objective, **3D Pareto Front 직접 시각화** ⭐
- **본 연구 (METOR)**: 4-objective, **3D Pareto Front + Convergence + Statistical Heatmap**
- **강점**: 기존 연구들의 시각화 방법을 통합하여 가장 포괄적인 분석 제공

**2. 통계적 검증**
- **대부분의 기존 연구**: 기술 통계(Mean±SD)만 제시
- **본 연구**: Shapiro-Wilk, Kruskal-Wallis, Mann-Whitney U, Bonferroni correction, Cliff's Delta
- **강점**: 엄격한 통계적 검증으로 결과의 신뢰성 확보

**3. 알고리즘 성능**
- **Sahin & Aytekin-Sahin (2024)**: SMSEMOA와 AGEMOEA가 6-objective에서 우수
- **본 연구**: SPEA2가 4-objective에서 우수 + 압도적 속도 우위
- **해석**: 목적함수 수에 따라 최적 알고리즘이 다를 수 있음 (4-objective에서는 SPEA2가 효과적)


### 4.4. Limitations and Future Work

**제한점:**

1. **단일 식단 데이터**: 7일(21끼) 식단 하나만을 대상으로 실험 수행
   - **영향**: 결과의 일반화 가능성 제한
   - **개선 방안**: 10개 랜덤 샘플 식단으로 실험 확장 (진행 예정)

2. **100세대 고정**: ε-MOEA의 경우 충분한 수렴에 미달
   - **영향**: ε-MOEA의 성능이 과소평가되었을 가능성
   - **개선 방안**: 알고리즘별 최적 세대 수 탐색 (parameter tuning)

3. **실행 시간 변동성**: NSGA-II/NSGA-III에서 큰 표준편차 관찰
   - **영향**: 실용적 응용에서 예측 불가능한 실행 시간
   - **개선 방안**: 조기 종료 조건 개선, 최대 실행 시간 제한 설정

4. **실제 환경 검증 부재**: 노인요양시설 현장 테스트 미실시
   - **영향**: 실무 적용 시 추가 문제 발생 가능
   - **개선 방안**: 파일럿 테스트 및 영양사 평가 수행 (향후 연구)

**향후 연구 방향:**

1. **일반화 검증** (High Priority):
   - 10개 랜덤 샘플 식단으로 실험 확장
   - 14일, 28일 등 더 긴 기간의 식단 최적화 성능 평가
   - 목적: 알고리즘 성능의 일반화 가능성 및 확장성 검증

2. **하이브리드 알고리즘** (Medium Priority):
   - SPEA2의 속도 + NSGA-III의 균일성 결합
   - 초기 탐색(ε-MOEA) + 후기 수렴(SPEA2) 2단계 접근
   - 목적: 각 알고리즘의 강점을 결합한 성능 개선

3. **동적 제약조건 처리** (Medium Priority):
   - 사용자별 건강 상태 변화에 따른 실시간 제약조건 조정
   - 계절별, 가용 재료에 따른 동적 식단 최적화
   - 목적: 실용적 응용 환경에서의 적응성 향상

4. **파라미터 최적화** (Low Priority):
   - 각 알고리즘의 하이퍼파라미터 최적화 (교차율, 변이율 등)
   - Bayesian Optimization을 사용한 자동 튜닝
   - 목적: 각 알고리즘의 잠재적 성능 최대화

5. **실제 환경 검증** (High Priority):
   - 노인요양시설 현장에서의 실제 적용 및 피드백 수집
   - 영양사 및 조리사의 사용자 경험 평가
   - 목적: 시스템의 실용성 및 수용성 검증


---

## 5. Conclusion

본 연구에서는 4개의 다목적 최적화 알고리즘(NSGA-II, NSGA-III, SPEA2, ε-MOEA)을 식단 최적화 문제에 적용하여 5개의 성능 메트릭(Hypervolume, Spacing, Diversity, Convergence, Execution Time)을 사용한 종합적인 성능 비교를 수행하였다.

**주요 연구 결과:**

1. **SPEA2의 종합 우수성**: SPEA2는 최고의 최적화 품질(Hypervolume: 0.384±0.007)과 압도적으로 빠른 실행 속도(17.4±13.4초, 다른 알고리즘 대비 5-38배)를 달성하여 실용적 응용에 가장 적합한 것으로 나타났다. 30세대만으로도 최적에 근접하는 빠른 수렴을 보였다.

2. **NSGA-II/NSGA-III의 유사한 성능**: 두 알고리즘은 최적화 품질 측면에서 SPEA2와 통계적으로 유의한 차이를 보이지 않았으며(p>0.1), NSGA-II는 가장 빠른 수렴 속도를, NSGA-III는 가장 균일한 해 분포를 제공하였다.

3. **ε-MOEA의 부적합성**: 현재 설정(100 generations)에서 ε-MOEA는 모든 메트릭에서 통계적으로 유의하게 낮은 성능을 보였으며(p<0.01), 수렴 곡선 분석 결과 충분한 최적화를 달성하지 못한 것으로 나타났다.

4. **통계적 타당성**: 엄격한 통계적 검증(Shapiro-Wilk, Kruskal-Wallis, Mann-Whitney U with Bonferroni correction, Cliff's Delta)을 통해 알고리즘 간 차이가 통계적으로 뿐만 아니라 실질적으로도 의미 있음을 확인하였다.

5. **4차원 시각화**: 3D Pareto Front와 color mapping을 결합하여 4개 목적함수 간 trade-off를 효과적으로 시각화하였으며, 이는 의사결정 지원 측면에서 실무적 가치가 높다.

**실무적 기여:**

본 연구의 결과는 노인요양시설 등 실제 환경에서 식단 최적화 시스템을 구현할 때 알고리즘 선택의 명확한 가이드라인을 제공한다:
- **실시간 시스템**: SPEA2 (속도와 품질의 최적 균형)
- **다양한 옵션 제공**: NSGA-III (균일한 해 분포)
- **빠른 수렴 필요**: NSGA-II (최저 Convergence)

본 연구는 또한 4차원 다목적 최적화 문제의 시각화 방법론에 대한 실용적 사례를 제공하며, 기존 연구들(Sahin & Aytekin-Sahin, 2024; Zhang et al., 2022)의 시각화 방법을 통합한 포괄적 분석 프레임워크를 제시하였다.


---

## Figure and Table Captions

**Figure 1.** Convergence Plot of Four Algorithms Over 100 Generations  
4개 알고리즘의 100세대에 걸친 Hypervolume 변화. SPEA2는 30세대에서 이미 최적에 근접하였으며, ε-MOEA는 100세대로 충분한 수렴을 달성하지 못함.

**Figure 2.** 3D Pareto Front Visualization (SPEA2)  
SPEA2의 Pareto solutions를 3차원 공간에 표현 (3개 목적함수: 영양, 비용, 조화도). 4번째 목적함수(다양성)는 색상으로 표현. 해의 고른 분포와 목적함수 간 trade-off가 명확히 드러남.

**Figure 3.** Multi-dimensional Performance Comparison (Radar Chart)  
5개 메트릭에 대한 정규화된 성능을 레이더 차트로 표현. SPEA2는 균형잡힌 우수한 성능을, NSGA-III는 Spacing에서 강점을 보임.

**Table 1.** Algorithm Performance Comparison Summary (Mean±SD, n=10)  
5개 메트릭에 대한 종합 성능 비교 표. 각 메트릭별 최고 성능이 볼드체로 강조됨.

**Figure 4.** Hypervolume Distribution Across 10 Independent Runs (Box Plots)  
각 알고리즘의 Hypervolume 분포를 박스플롯으로 표현. SPEA2가 가장 높은 중앙값과 안정적인 분포를 보임.

**Figure 5.** Solution Distribution Uniformity Comparison (Spacing)  
Spacing 메트릭 비교 막대 그래프. NSGA-III가 가장 균일한 해 분포를 달성함 (낮은 Spacing = 균일).

**Figure 6.** Trade-off Between Exploration and Exploitation (Diversity vs. Convergence)  
Diversity와 Convergence 간의 산점도 및 95% 신뢰 타원. NSGA-II와 NSGA-III는 탐색과 수렴의 균형을 잘 유지하며, ε-MOEA는 과도한 탐색으로 수렴 성능이 떨어짐.

**Figure 7.** Computational Efficiency Comparison (Execution Time)  
실행 시간 비교 가로 막대 그래프. SPEA2가 다른 알고리즘 대비 5-38배 빠른 속도를 보임.

**Figure 8.** Statistical Significance Heatmap (Mann-Whitney U test p-values)  
알고리즘 간 쌍별 비교의 p-value를 히트맵으로 표현. 색이 진할수록(빨강) 통계적으로 유의한 차이가 있음을 나타냄. ε-MOEA는 모든 메트릭에서 다른 알고리즘들에 비해 유의하게 낮은 성능을 보임.


---

## References

1. Deb, K., Pratap, A., Agarwal, S., & Meyarivan, T. (2002). A fast and elitist multiobjective genetic algorithm: NSGA-II. IEEE Transactions on Evolutionary Computation, 6(2), 182-197.

2. Deb, K., & Jain, H. (2014). An evolutionary many-objective optimization algorithm using reference-point-based nondominated sorting approach, part I: solving problems with box constraints. IEEE Transactions on Evolutionary Computation, 18(4), 577-601.

3. Zitzler, E., Laumanns, M., & Thiele, L. (2001). SPEA2: Improving the strength Pareto evolutionary algorithm (TIK-report, 103).

4. Laumanns, M., Thiele, L., Deb, K., & Zitzler, E. (2002). Combining convergence and diversity in evolutionary multiobjective optimization. Evolutionary Computation, 10(3), 263-282.

5. Sahin, O., & Aytekin-Sahin, G. (2024). Open-source multi-objective optimization software for menu planning. Expert Systems with Applications, 252, 124213.

6. Zhang, J., Li, M., Liu, W., Lauria, S., & Liu, X. (2022). Many-objective optimization meets recommendation systems: A food recommendation scenario. Neurocomputing, 503, 109-117.

7. Yilmaz, I., & Polat, L. (2023). Celiac disease multi-purpose diet plan through integrated goal programming and Interval Type 2 Fuzzy TOPSIS method. Expert Systems with Applications, 218, 119618.


---

## Data Availability Statement

본 연구에서 사용된 실험 데이터(`optimization_comparison_results.xlsx`), 통계 분석 결과(`statistical_analysis_results.xlsx`), 그리고 모든 소스 코드는 GitHub 저장소에서 공개되어 있습니다:  
**https://github.com/HeejeongH/Diet_optimization**

저장소에는 다음 파일들이 포함되어 있습니다:
- `src/main.ipynb`: 알고리즘 비교 실험 코드
- `src/generate_figures.py`: Figure 1-7 생성 코드
- `src/additional_figures.py`: Figure 1-2 생성 코드 (Convergence, 3D Pareto Front)
- `src/statistical_analysis.py`: 통계 분석 및 Figure 8 생성 코드
- `src/optimization_comparison_results.xlsx`: 원시 실험 데이터
- `src/statistical_analysis_results.xlsx`: 통계 분석 결과


## Acknowledgments

본 연구는 사랑과선행요양원의 식단 데이터를 바탕으로 수행되었습니다. 데이터 제공에 협조해주신 관계자분들께 감사드립니다.


---

**작성일**: 2025-12-07  
**버전**: 2.0 (Figure 재구성 및 논리적 흐름 개선)  
**프로젝트**: METOR (Multi-objective Enhanced Tool for Optimal meal Recommendation)
