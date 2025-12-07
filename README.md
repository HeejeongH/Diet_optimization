# Diet Optimization for Elderly Care Facilities

**Multi-objective Enhanced Tool for Optimal meal Recommendation (METOR)**

노인 요양 시설을 위한 다목적 최적화 기반 식단 추천 시스템

---

## 📋 목차

- [개요](#개요)
- [주요 기능](#주요-기능)
- [알고리즘](#알고리즘)
- [설치 방법](#설치-방법)
- [사용 방법](#사용-방법)
- [프로젝트 구조](#프로젝트-구조)
- [연구 결과](#연구-결과)

---

## 🎯 개요

이 프로젝트는 **노인 요양 시설의 식단을 최적화**하는 다목적 진화 알고리즘(MOEA) 프레임워크를 구현합니다. 4가지 경쟁적인 목표를 동시에 최적화합니다:

1. **영양 적정성** (Nutritional Adequacy) - 일일 영양 요구량 충족
2. **비용 효율성** (Cost Effectiveness) - 품질 유지하며 식재료 비용 최소화
3. **메뉴 조화도** (Menu Harmony) - 문화적으로 적절한 음식 조합
4. **식단 다양성** (Dietary Diversity) - 식단 피로 방지를 위한 다양성 제공

---

## ✨ 주요 기능

### 핵심 기능

- 🍽️ **다목적 최적화** - 4가지 목표 동시 최적화
- 📊 **성능 비교** - 알고리즘 간 종합적인 벤치마킹
- 📈 **통계 분석** - 엄격한 통계적 검증
- 💾 **데이터 내보내기** - Excel 보고서 및 CSV 출력

### 고급 기능

- ⚙️ **유연한 제공량 비율** - 조절 가능한 1인분 크기 (0.6-1.0, 최적 범위: 0.65-0.9)
- 🔄 **적응형 종료** - 스마트 중지 기준
- 💪 **병렬 처리** - 멀티스레드 적합도 평가
- 📦 **캐싱 시스템** - 성능 최적화를 위한 LRU 캐시
- ✅ **현실적 제약조건** - jeongseong 데이터 기반 영양소 범위 설정

---

## 🔬 알고리즘

구현된 4가지 다목적 진화 알고리즘:

1. **NSGA-II** - Non-dominated Sorting Genetic Algorithm II
2. **NSGA-III** - 참조점 기반 선택을 사용하는 NSGA-III
3. **SPEA2** - Strength Pareto Evolutionary Algorithm 2
4. **ε-MOEA** - Epsilon Multi-Objective Evolutionary Algorithm

---

## 🚀 설치 방법

### 요구사항

- Python 3.9 이상
- pip 패키지 관리자

### 1단계: 저장소 클론

```bash
git clone https://github.com/HeejeongH/Diet_optimization.git
cd Diet_optimization
```

### 2단계: 가상 환경 생성 (권장)

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3단계: 의존성 설치

```bash
pip install -r requirements.txt
```

### 필수 패키지

```
numpy>=1.24.0
pandas>=2.0.0
matplotlib>=3.7.0
seaborn>=0.12.0
scipy>=1.10.0
openpyxl>=3.1.0
```

---

## 📖 사용 방법

### 논문용 알고리즘 성능 비교 실험 (main.ipynb)

**main.ipynb**는 **논문용 알고리즘 성능 비교 실험**을 수행합니다:

```bash
cd src
jupyter notebook main.ipynb
```

**실험 설계:**
- **알고리즘**: NSGA-II, NSGA-III, SPEA2, ε-MOEA
- **반복 횟수**: 각 알고리즘당 10회 독립 실행
- **세대 수**: 100 generations
- **평가 지표**: Hypervolume, Spacing, Diversity, Convergence, Execution Time

**출력:**
- `optimization_comparison_results.xlsx` - 성능 비교 데이터 (통계 분석용)

### 실무용 식단 개선 제안 (app.py)

**app.py**는 **실무 활용을 위한 식단 개선 제안**을 제공합니다:

```bash
cd src
python app.py
```

**기능:**
- 초기 식단을 입력받아 개선된 식단 최대 5개 제안
- 영양, 비용, 조화, 다양성 점수 개선율 표시
- 카테고리별 메뉴 변경 비율 분석

### Python 스크립트로 실행

```python
from load_data import load_and_process_data, create_nutrient_constraints, load_all_menus
from spea2_optimizer import SPEA2Optimizer

# 데이터 로드
diet_db_path = '../data/sarang_DB/processed_DB/DIET_jeongseong.xlsx'
menu_db_path = '../data/sarang_DB/processed_DB/Menu_ingredient_nutrient_jeongseong.xlsx'
ingredient_db_path = '../data/sarang_DB/processed_DB/Ingredient_Price_jeongseong.xlsx'

diet_db = load_and_process_data(diet_db_path, menu_db_path, ingredient_db_path)
all_menus = load_all_menus(menu_db_path, ingredient_db_path)
nutrient_constraints = create_nutrient_constraints()

# 최적화 실행
optimizer = SPEA2Optimizer(all_menus, nutrient_constraints, harmony_matrix)
optimized_diets = optimizer.optimize(diet_db, initial_diet, generations=100)
```

---

## 📁 프로젝트 구조

```
Diet_optimization/
│
├── src/                          # 소스 코드
│   ├── Diet_class.py             # 핵심 데이터 구조 (Menu, Meal, Diet)
│   ├── load_data.py              # 데이터 로딩 및 전처리
│   ├── evaluation_function.py   # 목적 함수 구현
│   ├── optimizer_base.py         # 최적화 알고리즘 기본 클래스
│   ├── nsga2_optimizer.py        # NSGA-II 구현
│   ├── nsga3_optimizer.py        # NSGA-III 구현
│   ├── spea2_optimizer.py        # SPEA2 구현
│   ├── emoea_optimizer.py        # ε-MOEA 구현
│   ├── performance_metrics.py    # 성능 평가 지표
│   ├── utils.py                  # 유틸리티 함수
│   ├── main.ipynb                # 메인 실행 노트북
│   └── generate_figures.py       # 논문용 그림 생성
│
├── data/                         # 데이터 파일
│   └── sarang_DB/                # 메인 데이터베이스
│       └── processed_DB/         # 전처리된 데이터
│           ├── DIET_jeongseong.xlsx              # 과거 식단 데이터
│           ├── Menu_ingredient_nutrient_jeongseong.xlsx  # 메뉴 데이터베이스
│           └── Ingredient_Price_jeongseong.xlsx  # 식재료 가격
│
├── .gitignore                    # Git 무시 규칙
├── requirements.txt              # Python 의존성
└── README.md                     # 이 파일
```

---

## 📊 연구 결과

### 성능 요약 (Mean ± SD, n=10)

| Metric | NSGA-II | NSGA-III | SPEA2 | ε-MOEA |
|--------|---------|----------|-------|--------|
| **Hypervolume** | 0.382±0.007 | 0.381±0.013 | **0.384±0.007** | 0.357±0.021 |
| **Spacing** | 0.530±0.357 | **0.388±0.251** | 0.436±0.375 | 1.026±0.400 |
| **Diversity** | 0.994±0.345 | 1.005±0.329 | 1.153±0.507 | **1.841±0.561** |
| **Convergence** | **0.221±0.051** | 0.232±0.054 | 0.295±0.095 | 0.334±0.091 |
| **Time (sec)** | 82.1±183.4 | 261.3±305.4 | **17.4±13.4** | 667.1±203.4 |

**Bold**: Best performance for each metric  
**Data source**: `Weekly_diet_ex.xlsx` (7 days / 21 meals)  
**Experiment**: 100 generations × 10 independent runs per algorithm

### 주요 발견 사항

#### 🏆 SPEA2: 실용적 응용에 최적
- ✅ **최고의 최적화 품질** (Hypervolume: 0.384±0.007)
- ✅ **압도적으로 빠른 속도** (17.4±13.4초, 다른 알고리즘 대비 15-38배 빠름)
- ✅ **안정적인 성능** (낮은 표준편차)
- 💡 **권장 사항**: 실시간 식단 추천 시스템 및 웹/모바일 애플리케이션에 최적

#### 🥈 NSGA-II: 균형잡힌 선택
- ✅ **가장 빠른 수렴** (Convergence: 0.221±0.051)
- ✅ SPEA2와 유사한 최적화 품질 (Hypervolume: 0.382±0.007)
- ⚠️ 중간 수준의 실행 속도 (표준편차 큼)
- 💡 **권장 사항**: 수렴 속도가 중요한 경우

#### 🥉 NSGA-III: 다양한 해 탐색
- ✅ **가장 균일한 해 분포** (Spacing: 0.388±0.251)
- ✅ NSGA-II와 유사한 최적화 품질
- ⚠️ 느린 실행 속도 (261.3±305.4초)
- 💡 **권장 사항**: 사용자에게 다양한 식단 옵션 제공이 중요한 경우

#### ⚠️ ε-MOEA: 현재 설정에서는 비효율적
- ❌ 가장 낮은 최적화 품질 (Hypervolume: 0.357±0.021)
- ❌ 가장 불균일한 해 분포 (Spacing: 1.026±0.400)
- ❌ 가장 느린 실행 속도 (667.1±203.4초)
- 💡 현재 식단 최적화 설정에서는 권장하지 않음

### 📈 그림 및 상세 분석

프로젝트에 포함된 6개 그림:
- **Figure 1**: Performance Radar Chart (다차원 성능 비교)
- **Figure 2**: Hypervolume Box Plots (분포 분석)
- **Figure 3**: Spacing Comparison (해 분포 균일성)
- **Figure 4**: Diversity vs Convergence (트레이드오프 분석)
- **Figure 5**: Execution Time Comparison (계산 효율성)
- **Figure 6**: Performance Summary Table (종합 비교)

상세한 Results 섹션은 [`docs/paper/results_section.md`](docs/paper/results_section.md)를 참조하세요.

---

## 📄 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다.

---

## 👥 저자

- **한희정** - *초기 작업* - [HeejeongH](https://github.com/HeejeongH)

---

## 📧 문의

질문이나 협업 제안:
- GitHub Issues: [이슈 생성](https://github.com/HeejeongH/Diet_optimization/issues)
- Repository: https://github.com/HeejeongH/Diet_optimization

---

## 🙏 감사의 말

- 정선 요양원의 실제 데이터 제공
- 한국인 영양소 섭취기준(KDRIs) 2020
- 연구팀 구성원들의 기여

---

## 📚 인용

이 소프트웨어를 연구에 사용하시는 경우 다음과 같이 인용해 주세요:

```bibtex
@article{han2024diet,
  title={Multi-objective Enhanced Tool for Optimal meal Recommendation},
  author={Han, Heejeong and others},
  journal={Journal Name},
  year={2024},
  note={Under review}
}
```

---

**Happy Optimizing! 🍽️**

---

## 📊 영양소 제약조건

### 현재 설정 (jeongseong 데이터 기반)

| 영양소 | 최소값 (1일) | 최대값 (1일) | 비고 |
|--------|--------------|--------------|------|
| 에너지(kcal) | 1440 | 2600 | 노인 1일 권장량 기준 |
| 탄수화물(g) | 220 | 400 | 총 에너지의 55-65% |
| 단백질(g) | 54 | 100 | 총 에너지의 15-20% |
| 지방(g) | 32 | 85 | 총 에너지의 20-25% |
| 식이섬유(g) | 12 | 50 | 장 건강 유지 |

**주의사항:**
- 제약조건은 1일 평균 영양소 섭취량을 기준으로 합니다
- serving_ratio 0.65~0.9 범위에서 제약조건 만족 가능
- 메뉴 DB의 영양소 데이터를 기반으로 현실적으로 설정됨

