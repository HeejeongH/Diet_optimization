# 식단 최적화 관련 논문 시각화 방법 비교 분석

## 📚 분석 대상 논문

### 1️⃣ Paper 1: Open-source multi-objective optimization software for menu planning (2024)
- **저널**: Expert Systems With Applications
- **목적함수 수**: 6개 (Color, Consistency, Main ingredients, Nutrient, Repetition, Meal group)
- **알고리즘**: NSGA-II, NSGA-III, SMSEMOA, AGEMOEA

### 2️⃣ Paper 2: Celiac disease multi-purpose diet plan (2023)
- **저널**: Expert Systems With Applications
- **목적함수 수**: 8개 (Calorie, Cost, Protein, Carbohydrate, Fat, Milk, Cereal, Meat)
- **방법론**: Goal Programming + Interval Type-2 Fuzzy TOPSIS

### 3️⃣ Paper 3: Many-objective optimization meets recommendation systems (2022)
- **저널**: Neurocomputing
- **목적함수 수**: 4개 (User preference, Nutrition, Diversity, Diet pattern)
- **알고리즘**: SPEA2, NSGA-II, SPEA2+SDE

---

## 🎨 시각화 방법 상세 비교

| 논문 | 목적함수 | 주요 시각화 방법 | Pareto Front | 특징 |
|------|----------|------------------|--------------|------|
| **Paper 1** (6-obj) | 6개 | Box Plot, Convergence Plot, Expert Evaluation | ❌ 없음 | Hypervolume/IGD/GD 지표 사용 |
| **Paper 2** (8-obj) | 8개 | Multi-line Plot, Sensitivity Analysis | ❌ 없음 | Closeness Index, Penalty Function |
| **Paper 3** (4-obj) | 4개 | **Pareto Front Plots**, Histogram | ✅ **있음** | 3D Pareto Front 직접 표현 |
| **METOR** (4-obj) | 4개 | Radar Chart, Box Plot, Scatter, Heatmap | ❌ 없음 | 종합 성능 비교 중심 |

---

## 📊 각 논문의 Figure 구성

### Paper 1 (6-objective, 2024)

**Figure 1-3**: 방법론 도식화
- Fig. 1: Menu Planning Problem 표현 방식
- Fig. 2: Crossover Operator
- Fig. 3: Mutation Operator

**Figure 4**: **Box Plot** (핵심 성능 비교)
- **4개 지표**: Hypervolume, IGD, GD, Calculation Time
- **4개 알고리즘**: NSGA-II, NSGA-III, SMSEMOA, AGEMOEA
- **30회 반복** 실험 결과의 분포 (median, quartiles, outliers)
- **특징**: 
  - SMSEMOA와 AGEMOEA가 Hypervolume에서 우수
  - 표준편차가 작아 안정적

**Figure 5**: **Convergence Plot** (수렴 과정 시각화)
- **3개 지표**: Hypervolume, GD, IGD
- **X축**: Generation (세대)
- **Y축**: Metric Value
- **특징**:
  - NSGA-II와 NSGA-III가 초기에 비슷
  - 세대가 진행됨에 따라 성능 차이 명확

**Figure 6**: **Expert Evaluation** (전문가 평가)
- **평가 기준**: 영양사가 생성된 식단 평가
- **최고/최저 식단** 비교
- **Bar Plot + Error Bars** 형태

**✅ 장점**:
- Box Plot으로 알고리즘 안정성(variability) 명확히 보여줌
- Convergence Plot으로 최적화 과정 투명하게 공개
- 전문가 평가로 실용성 검증

**❌ 단점**:
- 6개 목적함수를 직접 시각화하지 않음
- Pareto Front를 보여주지 않아 해의 분포 파악 어려움

---

### Paper 2 (8-objective, 2023)

**Figure 1-2**: 방법론 Flow Chart
- Fig. 1: Proposed Methodology Flow-Chart
- Fig. 2: MCDM Process Concept

**Figure 3**: **Multi-Line Plot (Sensitivity Analysis)**
- **X축**: Cases (Current Case, Case1, Case2, ...)
- **Y축**: Closeness Index (0.0 ~ 0.8)
- **8개 선**: 각 목적함수(A1-A8)의 민감도
- **목적**: 가중치 변화에 따른 각 목적함수의 중요도 변화 분석

**Figure 4**: **Cost-Deviation Trade-off Plot**
- **X축**: Cost Value (예산)
- **Y축**: Penalty Function Point (총 편차)
- **목적**: 예산 증가 시 목적함수 달성도 개선 정도 시각화
- **특징**:
  - 예산이 증가하면 penalty(편차)가 감소
  - Diminishing returns 효과 확인 가능

**✅ 장점**:
- 8개 목적함수에 대한 민감도 분석 명확
- 예산-성능 Trade-off 직관적 표현
- 실용적 의사결정 지원

**❌ 단점**:
- 알고리즘 간 비교 없음 (단일 방법론)
- Pareto Front 시각화 없음
- 통계적 유의성 검증 부재

---

### Paper 3 (4-objective, 2022) ⭐ **가장 관련성 높음**

**Figure 1**: **Histogram (사용자 선호도)**
- **4명 사용자**의 음식 소비 빈도
- **X축**: Food ID
- **Y축**: Frequency
- **목적**: 개인화 추천의 기반 데이터 시각화

**Figure 2-5**: **🌟 3D Pareto Front Plots** (가장 중요!)
- **3개 목적함수 조합** (User Preference, Nutrition, Diversity)
- **3D 산점도** 형태
- **알고리즘별 색상** 구분 (SPEA2, NSGA-II, SPEA2+SDE)
- **특징**:
  - Pareto Front의 형태를 직접 확인 가능
  - 알고리즘 간 해의 분포 차이 명확
  - Trade-off 관계 시각적으로 이해

**Figure 6-8**: **Multi-dimensional Performance Plots**
- **Fig. 6**: 1명 사용자 (4개 목적함수 평균)
- **Fig. 7**: 5명 사용자 (4개 목적함수 평균)
- **Fig. 8**: 10명 사용자 (4개 목적함수 평균)
- **형태**: Radar Chart 또는 Multi-axis Plot 추정
- **목적**: 사용자 수 증가에 따른 성능 변화 분석

**Figure 9**: **Hypervolume 개념 도식화**
- **2D 예시**로 Hypervolume 계산 방법 설명
- **교육적 목적**: 독자가 Hypervolume 지표 이해 돕기

**Figure 10**: **Algorithm Running Time**
- **X축**: User Group Size (1, 5, 10)
- **Y축**: Running Time (seconds)
- **3개 선**: SPEA2, NSGA-II, SPEA2+SDE
- **목적**: 확장성(scalability) 분석

**✅ 장점**:
- **3D Pareto Front 직접 시각화** (4차원 문제를 3차원으로 투영)
- Hypervolume 개념 도식화로 독자 이해 향상
- 사용자 수에 따른 확장성 분석

**❌ 단점**:
- 4번째 목적함수(Diet Pattern)는 3D Pareto Front에 미포함
- 통계적 유의성 검증 시각화 없음

---

## 🎯 METOR 프로젝트에 적용 가능한 아이디어

### 현재 METOR 프로젝트의 시각화 (Stage 2)

| Figure | 내용 | 사용된 기법 |
|--------|------|-------------|
| Figure 1 | Performance Radar Chart | 4차원 균형 비교 |
| Figure 2 | Hypervolume Box Plots | 분포 및 안정성 |
| Figure 3 | Spacing Comparison | Bar Chart |
| Figure 4 | Diversity vs Convergence | Scatter Plot |
| Figure 5 | Execution Time | Horizontal Bar Chart |
| Figure 6 | Performance Summary | Table |
| **추가** | Statistical Significance Heatmap | Heatmap |

---

## 💡 개선 제안 (우선순위별)

### 🔴 **High Priority: 논문에 꼭 포함해야 할 것**

#### 1️⃣ **3D Pareto Front Visualization 추가** (Paper 3 참고)
- **목적**: 4개 목적함수 중 3개를 3D 공간에 표현, 4번째는 색상으로
- **예시 코드**:
```python
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(12, 9))
ax = fig.add_subplot(111, projection='3d')

# 3개 목적함수를 3D 축으로, 4번째는 색상으로
ax.scatter(nutrition, cost, harmony, 
           c=diversity,  # 4번째 목적함수
           cmap='viridis', s=100, alpha=0.7)
```
- **배치**: Figure 7로 추가, Results Section의 3.3에 포함
- **설명**: "Figure 7은 SPEA2의 Pareto Front를 3차원 공간에 표현한 것이다. 색상은 4번째 목적함수(Diversity)를 나타낸다."

#### 2️⃣ **Convergence Plot 추가** (Paper 1 참고)
- **목적**: 알고리즘의 최적화 과정을 세대별로 시각화
- **X축**: Generation (0-100)
- **Y축**: Hypervolume Value
- **4개 선**: NSGA-II, NSGA-III, SPEA2, ε-MOEA
- **배치**: Figure 8로 추가
- **의미**: 
  - SPEA2가 빠르게 수렴함을 보여줌
  - ε-MOEA는 100세대로 불충분함을 시각적으로 증명

### 🟡 **Medium Priority: 있으면 좋은 것**

#### 3️⃣ **Pairwise Scatter Matrix** (현재 생성한 method2)
- **목적**: 4개 목적함수 간 Trade-off 관계 명확히 분석
- **배치**: Supplementary Materials 또는 Appendix
- **6개 subplot**: 모든 2개 조합 (C(4,2) = 6)

#### 4️⃣ **Sensitivity Analysis** (Paper 2 참고)
- **목적**: 제약조건(영양 상한/하한) 변화에 따른 성능 변화
- **예시**: "탄수화물 상한을 400g → 450g으로 변경 시 Hypervolume 변화"
- **배치**: Discussion Section

### 🟢 **Low Priority: 선택적**

#### 5️⃣ **Expert Evaluation** (Paper 1 참고)
- **목적**: 생성된 식단을 영양사가 평가
- **평가 기준**: 영양, 조화도, 실용성
- **시간**: 2-3일 소요

---

## 📈 각 논문의 Figure 개수 비교

| 논문 | 방법론 도식 | 성능 비교 Figure | Pareto Front | 총 Figure 수 |
|------|-------------|------------------|--------------|--------------|
| **Paper 1** | 3개 | 3개 (Box, Convergence, Evaluation) | ❌ 0개 | **6개** |
| **Paper 2** | 2개 | 2개 (Sensitivity, Trade-off) | ❌ 0개 | **4개** |
| **Paper 3** | 1개 | **9개** (Pareto×4, Multi-dim×3, Time×1, HV×1) | ✅ **4개** | **10개** |
| **METOR (현재)** | 0개 | 7개 (Radar, Box, Bar, Scatter, Time, Table, Heatmap) | ❌ 0개 | **7개** |
| **METOR (개선 후)** | 0개 | **9개** (+Pareto Front, +Convergence) | ✅ **1개** | **9개** |

---

## 🎯 결론 및 Action Items

### ✅ METOR 프로젝트의 강점
1. **Statistical Significance 시각화** (Heatmap) - 다른 논문들에 없음
2. **Radar Chart**로 4차원 균형 비교 - 직관적
3. **Box Plot**으로 알고리즘 안정성 분석 - Paper 1과 동일 수준

### ⚠️ 보완이 필요한 부분
1. **Pareto Front 직접 시각화 없음** (Paper 3는 4개, METOR는 0개)
2. **Convergence 과정 시각화 없음** (Paper 1은 있음)
3. **Trade-off 관계 분석 부족** (Paper 2는 Cost-Deviation Plot)

### 🚀 추천 개선 순서
1. **1차 개선** (오늘 완료 가능):
   - 3D Pareto Front 추가 (Figure 7)
   - Convergence Plot 추가 (Figure 8)
   
2. **2차 개선** (1-2일):
   - Pairwise Scatter Matrix (Supplementary)
   - Sensitivity Analysis (Discussion에 텍스트로)

3. **3차 개선** (선택적, 3-5일):
   - Expert Evaluation 실시
   - 랜덤 샘플링 10개 식단으로 일반화 검증

---

## 📚 참고: 각 논문의 핵심 Takeaway

### Paper 1 (6-objective)
- **핵심**: Box Plot + Convergence Plot = 완벽한 알고리즘 성능 비교
- **METOR 적용**: Convergence Plot 추가 필요

### Paper 2 (8-objective)
- **핵심**: Sensitivity Analysis로 실용적 의사결정 지원
- **METOR 적용**: Discussion에서 제약조건 변화 영향 분석

### Paper 3 (4-objective) ⭐
- **핵심**: 3D Pareto Front로 4차원 문제 시각화
- **METOR 적용**: **반드시 추가 필요!** (가장 직접적 경쟁 논문)

---

**작성일**: 2025-12-07  
**프로젝트**: METOR (Multi-objective Enhanced Tool for Optimal meal Recommendation)  
**GitHub**: https://github.com/HeejeongH/Diet_optimization
