# 📊 다목적 최적화 성능 지표 - 한눈에 이해하기

## 빠른 요약 표

| 지표 | 측정 내용 | 좋은 값 | 의미 | 비유 |
|------|-----------|---------|------|------|
| **Hypervolume** | 해 집합이 커버하는 공간의 부피 | **높을수록** | 최적화 품질 (수렴 + 다양성) | 🏆 **가장 중요한 지표** - 축구 경기의 최종 스코어 |
| **Spacing** | 해들 간격의 균일성 | **낮을수록** | 해 분포의 균일성 | 📏 옷 사이즈가 골고루 있는가? (S, M, L, XL) |
| **Diversity** | 목적함수 공간의 탐색 범위 | **높을수록** | 탐색 능력 | 🌈 얼마나 넓은 영역을 조사했는가? |
| **Convergence** | 진짜 최적해까지의 거리 | **낮을수록** | 수렴 속도 | 🎯 목표 지점에 얼마나 가까운가? |
| **Execution Time** | 알고리즘 실행 시간 | **낮을수록** | 계산 효율성 | ⏱️ 얼마나 빨리 결과를 주는가? |

---

## 🎯 5가지 지표를 왜 모두 측정하는가?

### 단일 지표만으로는 부족합니다!

```
예시: 식당 평가에 비유

Hypervolume만 보면?
→ 음식 맛은 좋은데, 메뉴가 편향될 수 있음

Spacing도 보면?
→ 메뉴가 골고루 있는지 확인

Diversity도 보면?
→ 다양한 취향을 커버하는지 확인

Convergence도 보면?
→ 최고 수준의 요리에 얼마나 가까운지 확인

Execution Time도 보면?
→ 주문 후 얼마나 빨리 나오는지 확인
```

**→ 종합 평가가 필요! 🏆**

---

## 📈 지표별 시각적 설명

### 1️⃣ Hypervolume (하이퍼볼륨) 📦
**"해 집합이 목적함수 공간에서 차지하는 부피"**

<img src="hypervolume_detailed.png" width="600">

✅ **왜 가장 중요한가?**
- 유일하게 **수렴(convergence) + 다양성(diversity)을 동시에 측정**
- Pareto dominance와 완벽히 일치
- 학술 논문에서 가장 인정받는 지표

**METOR 결과:**
- SPEA2: 0.384 🏆 (최고)
- NSGA-II: 0.382
- NSGA-III: 0.381
- ε-MOEA: 0.357 (최저)

**해석:** SPEA2가 가장 넓은 영역을 커버 → **최고 품질의 해 집합**

---

### 2️⃣ Spacing (스페이싱) 📏
**"해들 간의 간격이 얼마나 균일한가?"**

```
균일한 분포 (Spacing = 0.388):
o----o----o----o----o  ✅ 좋음

불균일한 분포 (Spacing = 1.026):
o-o--------oo------o  ❌ 나쁨
```

**식단 최적화 비유:**
- **균일 분포**: 영양 우선, 균형형, 비용 우선 식단이 골고루 제공
- **불균일 분포**: 비슷한 식단만 여러 개 → 선택의 의미 없음

**METOR 결과:**
- NSGA-III: 0.388 🏆 (가장 균일)
- SPEA2: 0.436
- NSGA-II: 0.530
- ε-MOEA: 1.026 (가장 불균일)

**해석:** NSGA-III가 사용자에게 **가장 다양한 선택지를 제공**

---

### 3️⃣ Diversity (다양성) 🌈
**"얼마나 넓은 범위를 탐색했는가?"**

```
높은 Diversity (1.841):
  영양: 50% ~ 95% (범위 45%)
  비용: 40% ~ 90% (범위 50%)
  → 매우 넓게 탐색 ✅

낮은 Diversity (0.994):
  영양: 80% ~ 90% (범위 10%)
  비용: 75% ~ 85% (범위 10%)
  → 좁은 범위에 집중 ⚠️
```

**주의:** 높다고 무조건 좋은 것은 아님!
- 너무 넓게 탐색 → 수렴이 느려질 수 있음
- ε-MOEA: Diversity는 최고지만 Hypervolume은 최저

**METOR 결과:**
- ε-MOEA: 1.841 (가장 높음, 하지만 품질 낮음)
- SPEA2: 1.153 ✅ (적절한 탐색)
- NSGA-III: 1.005
- NSGA-II: 0.994 (가장 낮음)

---

### 4️⃣ Convergence (수렴성) 🎯
**"알고리즘의 해가 진짜 최적해에 얼마나 가까운가?"**

```
낮은 Convergence (0.221): 🎯
  알고리즘의 해 ●●●●
  진짜 최적해    ★★★★
  → 거의 일치! ✅

높은 Convergence (0.334): ❌
  알고리즘의 해 ●●●●
  진짜 최적해          ★★★★
  → 거리가 멀다 ⚠️
```

**METOR 결과:**
- NSGA-II: 0.221 🏆 (최고 수렴 속도)
- NSGA-III: 0.232
- SPEA2: 0.295
- ε-MOEA: 0.334 (느린 수렴)

**해석:** NSGA-II가 **가장 빠르게 최적해에 도달**

---

### 5️⃣ Execution Time (실행 시간) ⏱️
**"얼마나 빨리 결과를 주는가?"**

**METOR 결과:**
```
SPEA2:   17.4초 ✅ → 웹/모바일 앱 적용 가능!
NSGA-II: 82.1초 ✅ → 수용 가능
NSGA-III: 261.3초 ⚠️ → 좀 느림
ε-MOEA: 667.1초 ❌ → 11분! 비실용적
```

**실용성:**
- **< 100초**: 실시간 응용 가능 ✅
- **< 300초**: 수용 가능 ⚠️
- **> 600초**: 비실용적 ❌

**해석:** SPEA2가 압도적으로 빠름 → **실용적 응용에 최적**

---

## 🏆 METOR 프로젝트 최종 결론

### 알고리즘별 강점 요약

| 알고리즘 | 주요 강점 | 추천 용도 |
|----------|-----------|-----------|
| **SPEA2** 🏆 | 최고 품질 + 최고 속도 | **실용적 응용** (웹/모바일 앱) |
| **NSGA-II** 🎯 | 최고 수렴 속도 | **빠른 최적해 탐색** |
| **NSGA-III** 📐 | 최고 균일성 | **다양한 옵션 제공** (의사결정 지원) |
| **ε-MOEA** ⚠️ | (현재 설정으로는 비추천) | 100세대로 부족, 더 많은 세대 필요 |

---

## 📊 지표 간 관계 & 트레이드오프

### Exploration vs. Exploitation

```
┌─────────────────────────────────────────┐
│  초기 세대 (0-30)                        │
│  → Exploration (탐색) 중요               │
│  → Diversity ↑ (넓게 탐색)              │
│  → Convergence ↓ (아직 최적해에서 멀음) │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  중기 세대 (30-70)                       │
│  → 균형                                  │
│  → Diversity 유지 + Convergence 개선     │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  후기 세대 (70-100)                      │
│  → Exploitation (착취) 중요              │
│  → Convergence ↑ (최적해에 가까워짐)    │
│  → Diversity ↓ (좋은 해 주변 집중)       │
└─────────────────────────────────────────┘
```

### 지표 간 독립성

| 지표 A | 지표 B | 관계 | 설명 |
|--------|--------|------|------|
| Hypervolume | Convergence | 음의 상관 | 잘 수렴하면 Hypervolume ↑ |
| Hypervolume | Diversity | 양의 상관 | 넓게 탐색하면 Hypervolume ↑ (단, 수렴 필요) |
| Spacing | Diversity | **독립적** | 넓게 탐색해도 불균일할 수 있음 |
| Convergence | Diversity | **트레이드오프** | 빨리 수렴 ↔ 넓게 탐색 |
| Execution Time | 나머지 | 독립적 | 빠르다고 품질이 좋은 건 아님 |

---

## 💡 실무 의사결정 가이드

### Q1: 어떤 지표를 가장 중요하게 봐야 하나요?

**우선순위:**
1. **Hypervolume** (1순위) - 가장 중요! 🏆
   - 수렴 + 다양성을 동시에 측정
   - 학술적으로 가장 인정받음

2. **Execution Time** (2순위) - 실용성 ⏱️
   - 실제 응용에서 가장 직접적 영향
   - 웹/모바일 앱이면 반드시 고려

3. **Spacing 또는 Convergence** (3순위) - 목적에 따라
   - **의사결정 지원**: Spacing 중요
   - **최적해 찾기**: Convergence 중요

4. **Diversity** (참고용) - 균형 파악 🌈
   - Exploration-Exploitation 균형 확인
   - 높다고 무조건 좋은 것은 아님

---

### Q2: METOR 프로젝트의 최종 추천은?

```
✅ 일반 식단 추천 앱:
   → SPEA2 (최고 품질 + 최고 속도)

✅ 빠른 프로토타입 개발:
   → NSGA-II (최고 수렴 속도)

✅ 영양사 의사결정 지원 시스템:
   → NSGA-III (최고 균일성, 다양한 옵션)

❌ 현재 설정으로는 비추천:
   → ε-MOEA (100세대로 부족, 느림)
```

---

## 📚 참고 논문

1. **Hypervolume**:
   - Zitzler, E., & Thiele, L. (1998). *Multiobjective optimization using evolutionary algorithms—a comparative case study.*

2. **Spacing**:
   - Schott, J. R. (1995). *Fault tolerant design using single and multicriteria genetic algorithm optimization.*

3. **Generational Distance (GD/Convergence)**:
   - Van Veldhuizen, D. A., & Lamont, G. B. (1998). *Multiobjective evolutionary algorithm research: A history and analysis.*

---

**작성일**: 2025-12-07  
**프로젝트**: METOR (Multi-objective Enhanced Tool for Optimal meal Recommendation)  
**GitHub**: https://github.com/HeejeongH/Diet_optimization

---

## 📁 생성된 시각화 파일

- `comprehensive_metrics_comparison.png/pdf` - 전체 6가지 지표 종합 비교
- `hypervolume_detailed.png/pdf` - Hypervolume 상세 설명
