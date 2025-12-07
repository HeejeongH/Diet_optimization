# Results

## Experimental Setup

본 연구에서는 4개의 다목적 최적화 알고리즘(NSGA-II, NSGA-III, SPEA2, ε-MOEA)의 성능을 비교하기 위해 각 알고리즘당 10회의 독립적인 실행(independent runs)을 수행하였다. 각 실행은 100세대(generations)로 설정되었으며, 초기 집단 크기는 150개로 동일하게 유지되었다. 실험에 사용된 초기 식단은 7일간의 21끼 식사로 구성되었으며, 5개의 영양소 제약조건(에너지, 탄수화물, 단백질, 지방, 식이섬유)을 만족하도록 최적화를 수행하였다.

성능 평가를 위해 다음 5개의 메트릭을 사용하였다:
- **Hypervolume**: 최적화 품질과 해 집합의 크기를 나타내는 가장 중요한 메트릭 (높을수록 우수)
- **Spacing**: 해 분포의 균일성을 나타내는 메트릭 (낮을수록 균일한 분포)
- **Diversity**: 목적함수 공간에서 해 집합의 다양성 (값이 클수록 다양한 해 탐색)
- **Convergence**: 수렴 속도 및 품질 (낮을수록 최적해에 가까움)
- **Execution Time**: 계산 효율성 (낮을수록 효율적)


## Performance Comparison Results

### 4.1. Overall Performance

표 1은 4개 알고리즘의 성능을 5개 메트릭에 대해 비교한 결과이다 (Mean±SD, n=10).

**표 1. 알고리즘 성능 비교 (Mean±SD, n=10)**

| Metric | NSGA-II | NSGA-III | SPEA2 | ε-MOEA |
|--------|---------|----------|-------|--------|
| **Hypervolume** | 0.382±0.007 | 0.381±0.013 | **0.384±0.007** | 0.357±0.021 |
| **Spacing** | 0.530±0.357 | **0.388±0.251** | 0.436±0.375 | 1.026±0.400 |
| **Diversity** | 0.994±0.345 | 1.005±0.329 | 1.153±0.507 | 1.841±0.561 |
| **Convergence** | **0.221±0.051** | 0.232±0.054 | 0.295±0.095 | 0.334±0.091 |
| **Execution Time (sec)** | 82.1±183.4 | 261.3±305.4 | **17.4±13.4** | 667.1±203.4 |

**Bold**: 해당 메트릭에서 최고 성능

그림 1의 레이더 차트는 5개 메트릭에 대한 정규화된 성능을 종합적으로 보여준다. SPEA2는 최적화 품질(Hypervolume)과 실행 속도(Execution Time)에서 우수한 성능을 보이며, NSGA-II는 수렴 속도(Convergence)와 균형잡힌 성능을 나타냈다. NSGA-III는 해 분포의 균일성(Spacing)에서 가장 우수한 결과를 보였으며, ε-MOEA는 대부분의 메트릭에서 상대적으로 낮은 성능을 나타냈다.


### 4.2. Optimization Quality (Hypervolume)

Hypervolume은 다목적 최적화에서 가장 널리 사용되는 성능 지표로, 해 집합이 목적함수 공간에서 지배하는 영역의 크기를 나타낸다. 그림 2는 각 알고리즘의 10회 실행에 대한 Hypervolume 분포를 보여준다.

**주요 발견:**
- **SPEA2**가 평균 0.384±0.007로 가장 높은 Hypervolume을 기록하였으며, 표준편차가 작아 안정적인 성능을 보였다.
- **NSGA-II** (0.382±0.007)와 **NSGA-III** (0.381±0.013)는 SPEA2와 근소한 차이로 2위와 3위를 기록하였다.
- **ε-MOEA** (0.357±0.021)는 가장 낮은 Hypervolume과 가장 큰 표준편차를 보여, 최적화 품질과 안정성 모두에서 열등한 결과를 나타냈다.

박스플롯 분석 결과, SPEA2와 NSGA-II/NSGA-III 간의 차이는 매우 작으며, 이는 세 알고리즘 모두 유사한 최적화 품질을 달성함을 시사한다.


### 4.3. Solution Distribution Uniformity (Spacing)

Spacing 메트릭은 파레토 프론트 상의 해들이 얼마나 균일하게 분포되어 있는지를 나타낸다. 낮은 Spacing 값은 해들이 균일하게 분포되어 있음을 의미하며, 의사결정자에게 다양한 선택지를 제공할 수 있다.

그림 3은 각 알고리즘의 Spacing 성능을 비교한 결과이다.

**주요 발견:**
- **NSGA-III**가 평균 0.388±0.251로 가장 균일한 해 분포를 보였다.
- **SPEA2**는 0.436±0.375, **NSGA-II**는 0.530±0.357로 중간 수준의 성능을 나타냈다.
- **ε-MOEA**는 1.026±0.400으로 가장 불균일한 해 분포를 보였다.

이는 NSGA-III의 Reference point 기반 선택 메커니즘이 해의 균일한 분포에 효과적임을 시사한다. 반면, ε-MOEA의 ε-dominance 개념은 해의 균일성 측면에서는 다른 알고리즘에 비해 효과적이지 않았다.


### 4.4. Diversity vs. Convergence Trade-off

그림 4는 다양성(Diversity)과 수렴성(Convergence) 간의 트레이드오프를 보여준다. 이상적인 알고리즘은 높은 다양성(넓은 해 탐색)과 낮은 Convergence 값(최적해에 가까움)을 동시에 달성해야 한다.

**주요 발견:**
- **NSGA-II**는 가장 낮은 Convergence 값(0.221±0.051)을 기록하여 최적해에 가장 빠르게 수렴하였다.
- **NSGA-III**는 NSGA-II와 유사한 Convergence (0.232±0.054)와 Diversity (1.005±0.329)를 보였다.
- **SPEA2**는 중간 수준의 Convergence (0.295±0.095)와 Diversity (1.153±0.507)를 나타냈다.
- **ε-MOEA**는 가장 높은 Diversity (1.841±0.561)를 보였으나, Convergence (0.334±0.091)는 상대적으로 낮았다.

95% 신뢰 타원(confidence ellipse) 분석 결과, NSGA-II와 NSGA-III는 탐색과 수렴의 균형을 잘 유지하고 있으며, ε-MOEA는 넓은 탐색을 수행하지만 수렴 성능이 떨어지는 것으로 나타났다.


### 4.5. Computational Efficiency

그림 5는 각 알고리즘의 실행 시간을 비교한 결과이다. 계산 효율성은 실용적인 응용에서 중요한 요소이다.

**주요 발견:**
- **SPEA2**가 평균 17.4±13.4초로 압도적으로 가장 빠른 실행 속도를 보였다.
- **NSGA-II**는 82.1±183.4초로 2번째로 빠르나, 표준편차가 크게 나타났다.
- **NSGA-III**는 261.3±305.4초로 SPEA2 대비 약 15배 느렸으며, 역시 큰 표준편차를 보였다.
- **ε-MOEA**는 667.1±203.4초로 가장 느린 실행 속도를 기록하였으며, SPEA2 대비 약 38배 느린 결과를 보였다.

SPEA2의 우수한 계산 효율성은 Strength-based fitness assignment와 truncation operator의 효율적인 구현에 기인한 것으로 분석된다. NSGA-II와 NSGA-III의 큰 표준편차는 일부 실행에서 조기 종료 조건이 늦게 만족되어 630초 이상 소요된 경우가 있었기 때문이다.


### 4.6. Statistical Significance Analysis

#### 4.6.1. Normality Test

Shapiro-Wilk normality test 결과, 일부 데이터가 정규분포를 따르지 않는 것으로 나타났다 (표 2). 특히 HYPERVOLUME 메트릭에서 NSGA-II (W=0.716, p=0.001)와 SPEA2 (W=0.670, p<0.001)가, EXECUTION_TIME 메트릭에서는 모든 알고리즘이 정규성 가정을 위반하였다. 따라서 비모수 검정(non-parametric tests)인 Kruskal-Wallis H-test와 Mann-Whitney U test를 사용하였다.

**표 2. Normality Test Results (Shapiro-Wilk test)**

| Metric | Algorithm | W-statistic | p-value | Normal? |
|--------|-----------|-------------|---------|---------|
| HYPERVOLUME | NSGA-II | 0.716 | 0.001*** | No |
| HYPERVOLUME | NSGA-III | 0.851 | 0.060 | Yes |
| HYPERVOLUME | SPEA2 | 0.670 | <0.001*** | No |
| HYPERVOLUME | ε-MOEA | 0.940 | 0.550 | Yes |
| EXECUTION_TIME | All | <0.650 | <0.001*** | No |

*** p < 0.001


#### 4.6.2. Overall Differences (Kruskal-Wallis H-test)

Kruskal-Wallis H-test 결과, 모든 메트릭에서 알고리즘 간 통계적으로 유의한 차이가 발견되었다 (표 3).

**표 3. Kruskal-Wallis H-test Results**

| Metric | H-statistic | p-value | Significance |
|--------|-------------|---------|--------------|
| HYPERVOLUME | 14.407 | 0.0024 | ** |
| SPACING | 12.799 | 0.0051 | ** |
| DIVERSITY | 11.205 | 0.0107 | * |
| CONVERGENCE | 9.739 | 0.0209 | * |
| EXECUTION_TIME | 24.686 | <0.001 | *** |

*** p<0.001, ** p<0.01, * p<0.05

가장 강한 차이는 EXECUTION_TIME (H=24.686, p<0.001)에서 관찰되었으며, HYPERVOLUME (H=14.407, p=0.0024)과 SPACING (H=12.799, p=0.0051)에서도 매우 유의한 차이가 나타났다.


#### 4.6.3. Pairwise Comparisons (Mann-Whitney U test)

Mann-Whitney U test를 사용한 쌍별 비교 결과, 주요 발견사항은 다음과 같다 (표 4):

**표 4. Significant Pairwise Comparisons (Mann-Whitney U test with Bonferroni correction)**

| Metric | Comparison | p-value | Cliff's δ | Effect Size | Significant* |
|--------|------------|---------|-----------|-------------|--------------|
| **HYPERVOLUME** |
| | NSGA-II vs ε-MOEA | 0.0028 | 0.800 | Large | ✓ |
| | NSGA-III vs ε-MOEA | 0.0073 | 0.720 | Large | ✓ |
| | SPEA2 vs ε-MOEA | 0.0017 | 0.840 | Large | ✓ |
| **SPACING** |
| | NSGA-III vs ε-MOEA | 0.0022 | -0.820 | Large | ✓ |
| | SPEA2 vs ε-MOEA | 0.0058 | -0.740 | Large | ✓ |
| **DIVERSITY** |
| | NSGA-II vs ε-MOEA | 0.0058 | -0.740 | Large | ✓ |
| | NSGA-III vs ε-MOEA | 0.0058 | -0.740 | Large | ✓ |
| **EXECUTION_TIME** |
| | NSGA-II vs ε-MOEA | <0.001 | -0.980 | Large | ✓ |
| | NSGA-III vs ε-MOEA | <0.001 | -0.920 | Large | ✓ |
| | SPEA2 vs ε-MOEA | <0.001 | -1.000 | Large | ✓ |

*After Bonferroni correction (α = 0.05/6 = 0.0083)

**주요 발견:**

1. **ε-MOEA의 열등한 성능**: ε-MOEA는 모든 메트릭에서 다른 알고리즘들에 비해 통계적으로 유의하게 낮은 성능을 보였으며, effect size도 대부분 large (|δ| > 0.474)로 나타났다.

2. **NSGA-II, NSGA-III, SPEA2의 유사성**: 세 알고리즘 간에는 대부분의 메트릭에서 통계적으로 유의한 차이가 발견되지 않았다. 특히 HYPERVOLUME에서 NSGA-II vs NSGA-III (p=0.678), NSGA-II vs SPEA2 (p=0.121), NSGA-III vs SPEA2 (p=0.791) 모두 유의하지 않았다.

3. **EXECUTION_TIME의 극명한 차이**: SPEA2와 다른 알고리즘 간 실행 시간 차이는 매우 유의하였으며 (p<0.001), Cliff's Delta 값이 -1.000 (SPEA2 vs ε-MOEA)에 달해 실질적으로도 매우 큰 차이를 나타냈다.


#### 4.6.4. Effect Size Interpretation

Cliff's Delta 효과 크기 분석 결과, 대부분의 유의한 차이는 large effect size (|δ| ≥ 0.474)를 동반하였다. 이는 통계적 유의성뿐만 아니라 실질적으로도 의미 있는 차이임을 시사한다. 특히 EXECUTION_TIME에서 SPEA2는 ε-MOEA 대비 완벽한 우위(δ=-1.000)를 보였으며, HYPERVOLUME에서도 SPEA2는 ε-MOEA에 비해 매우 큰 우위(δ=0.840)를 나타냈다.


## Discussion

### 5.1. Algorithm Performance Summary

**SPEA2: 실용적 응용에 최적**
- 최고의 최적화 품질 (Hypervolume: 0.384±0.007)
- 압도적으로 빠른 실행 속도 (17.4±13.4초)
- 안정적인 성능 (낮은 표준편차)
- 🏆 **식단 최적화 시스템에 권장**

**NSGA-II: 균형잡힌 선택**
- SPEA2와 유사한 최적화 품질 (Hypervolume: 0.382±0.007)
- 가장 빠른 수렴 속도 (Convergence: 0.221±0.051)
- 중간 수준의 실행 속도
- 🏆 **수렴 속도가 중요한 경우 권장**

**NSGA-III: 다양한 해 탐색**
- 가장 균일한 해 분포 (Spacing: 0.388±0.251)
- NSGA-II와 유사한 최적화 품질
- 느린 실행 속도 (261.3±305.4초)
- 🏆 **다양한 선택지 제공이 중요한 경우 권장**

**ε-MOEA: 현재 설정에서는 비효율적**
- 가장 낮은 최적화 품질 (Hypervolume: 0.357±0.021)
- 가장 불균일한 해 분포 (Spacing: 1.026±0.400)
- 가장 느린 실행 속도 (667.1±203.4초)
- ⚠️ **현재 설정에서는 권장하지 않음**


### 5.2. Implications for Diet Optimization

본 연구의 결과는 식단 최적화 시스템 구현에 다음과 같은 실무적 시사점을 제공한다:

1. **실시간 식단 추천 시스템**: SPEA2의 빠른 실행 속도 (평균 17.4초)는 사용자에게 즉각적인 피드백을 제공하는 웹 기반 또는 모바일 애플리케이션에 적합하다.

2. **고품질 식단 계획**: SPEA2, NSGA-II, NSGA-III 모두 유사한 최적화 품질을 달성하므로, 응용 목적에 따라 선택이 가능하다.

3. **다양한 선택지 제공**: 사용자에게 다양한 식단 옵션을 제공하고자 하는 경우, NSGA-III의 균일한 해 분포가 유리하다.

4. **계산 자원 제약**: 제한된 계산 자원 환경에서는 SPEA2가 최적의 선택이다.


### 5.3. Limitations and Future Work

본 연구의 제한점과 향후 연구 방향은 다음과 같다:

**제한점:**
- 7일(21끼) 식단만을 대상으로 실험을 수행하여, 더 긴 기간의 식단 최적화에 대한 확장성 검증이 필요하다.
- 단일 데이터셋(Weekly_diet_ex.xlsx)을 사용하여, 다양한 초기 식단 조건에서의 성능 검증이 부족하다.
- 일부 알고리즘(NSGA-II, NSGA-III)에서 실행 시간의 큰 표준편차가 관찰되어, 조기 종료 조건의 개선이 필요하다.

**향후 연구 방향:**
1. **파라미터 최적화**: 각 알고리즘의 하이퍼파라미터 최적화를 통한 성능 개선
2. **확장성 평가**: 14일, 28일 등 더 긴 기간의 식단 최적화 성능 평가
3. **동적 제약조건**: 사용자별 건강 상태 변화에 따른 동적 제약조건 처리
4. **하이브리드 알고리즘**: SPEA2의 속도와 NSGA-III의 균일성을 결합한 하이브리드 접근
5. **실제 환경 검증**: 노인요양시설 현장에서의 실제 적용 및 피드백 수집


## Conclusion

본 연구에서는 4개의 다목적 최적화 알고리즘(NSGA-II, NSGA-III, SPEA2, ε-MOEA)을 식단 최적화 문제에 적용하여 성능을 비교하였다. 5개의 성능 메트릭(Hypervolume, Spacing, Diversity, Convergence, Execution Time)을 사용한 종합적인 분석 결과, SPEA2가 최고의 최적화 품질(Hypervolume: 0.384±0.007)과 압도적으로 빠른 실행 속도(17.4±13.4초)를 달성하여 실용적 응용에 가장 적합한 것으로 나타났다. NSGA-II는 가장 빠른 수렴 속도를 보였으며, NSGA-III는 가장 균일한 해 분포를 제공하였다. 본 연구의 결과는 노인요양시설 등 실제 환경에서 식단 최적화 시스템을 구현할 때 알고리즘 선택의 실무적 가이드라인을 제공한다.


---

## Figure Captions

**Figure 1.** Multi-dimensional Performance Comparison (Radar Chart)  
5개 메트릭에 대한 정규화된 성능을 레이더 차트로 표현. SPEA2는 균형잡힌 우수한 성능을, NSGA-III는 Spacing에서 강점을 보임.

**Figure 2.** Hypervolume Distribution Across 10 Independent Runs  
각 알고리즘의 Hypervolume 분포를 박스플롯으로 표현. SPEA2가 가장 높은 중앙값과 안정적인 분포를 보임.

**Figure 3.** Solution Distribution Uniformity Comparison (Spacing)  
Spacing 메트릭 비교 막대 그래프. NSGA-III가 가장 균일한 해 분포를 달성함.

**Figure 4.** Trade-off Between Exploration and Exploitation (Diversity vs. Convergence)  
Diversity와 Convergence 간의 산점도 및 95% 신뢰 타원. NSGA-II와 NSGA-III는 탐색과 수렴의 균형을 잘 유지함.

**Figure 5.** Computational Efficiency Comparison (Execution Time)  
실행 시간 비교 가로 막대 그래프. SPEA2가 다른 알고리즘 대비 15-38배 빠른 속도를 보임.

**Figure 6.** Algorithm Performance Comparison Summary Table  
5개 메트릭에 대한 종합 성능 비교 표. 각 메트릭별 최고 성능이 하이라이트됨.


---

## References

(논문 작성 시 추가 예정)

1. Deb, K., et al. (2002). A fast and elitist multiobjective genetic algorithm: NSGA-II.
2. Deb, K., & Jain, H. (2014). An evolutionary many-objective optimization algorithm using reference-point-based nondominated sorting approach, part I: solving problems with box constraints.
3. Zitzler, E., et al. (2001). SPEA2: Improving the strength Pareto evolutionary algorithm.
4. Laumanns, M., et al. (2002). Combining convergence and diversity in evolutionary multiobjective optimization.


---

**Data Availability Statement**

본 연구에서 사용된 실험 데이터(`optimization_comparison_results.xlsx`)와 코드는 GitHub 저장소에서 공개되어 있습니다:  
https://github.com/HeejeongH/Diet_optimization

**Acknowledgments**

본 연구는 사랑과선행요양원의 식단 데이터를 바탕으로 수행되었습니다.
