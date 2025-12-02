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

- ⚙️ **유연한 제공량 비율** - 조절 가능한 1인분 크기 (0.6-1.0)
- 🔄 **적응형 종료** - 스마트 중지 기준
- 💪 **병렬 처리** - 멀티스레드 적합도 평가
- 📦 **캐싱 시스템** - 성능 최적화를 위한 LRU 캐시

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

### Jupyter Notebook으로 실행 (추천)

```bash
cd src
jupyter notebook main.ipynb
```

**main.ipynb**를 열고 모든 셀을 실행하면 다음이 수행됩니다:

1. **데이터 로딩** - 식단, 메뉴, 식재료 데이터 불러오기
2. **4개 알고리즘 실행** - 각각 100세대 최적화
3. **성능 비교** - 10회 반복 실행으로 통계적 비교
4. **결과 저장** - Excel 파일로 결과 내보내기

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

### 성능 요약 (Mean ± Std, 10회 반복)

| 지표 | NSGA-II | NSGA-III | SPEA2 | ε-MOEA |
|------|---------|----------|-------|--------|
| **Hypervolume** | 0.409±0.012 | 0.401±0.008 | **0.426±0.026** | 0.370±0.048 |
| **Spacing** | **0.604±0.985** | 1.367±3.139 | 5.415±5.266 | 4.785±2.343 |
| **Diversity** | 1.132±0.614 | 1.572±2.137 | 6.236±4.556 | **9.449±3.058** |
| **Convergence** | 0.334±0.105 | 0.383±0.115 | **0.703±0.348** | 0.430±0.149 |
| **Time (초)** | 1423.5±579.5 | 1145.4±26.0 | **992.1±576.1** | 1889.8±477.0 |

**굵은 글씨**: 각 지표별 최고 성능

### 주요 발견 사항

1. **보편적인 우승자 없음** - 각 알고리즘이 다른 차원에서 우수함
2. **SPEA2 추천** - 운영 배포용 (가장 빠른 실행 시간 16.5분)
3. **NSGA-II 우수** - 의사결정 지원용 (최고의 spacing: 0.604)
4. **ε-MOEA 최고** - 탐색용 (최고의 다양성: 9.449)

### 통계적 검증

- **Hypervolume**: 유의한 차이 없음 (Kruskal-Wallis p = 0.642)
- **Spacing**: 유의한 차이 (p = 0.011), NSGA-II > SPEA2/ε-MOEA
- **Diversity**: 매우 유의함 (p < 0.001), ε-MOEA > 모든 알고리즘
- **Convergence**: 매우 유의함 (p < 0.001), SPEA2 > 모든 알고리즘
- **Time**: 매우 유의함 (p < 0.001), SPEA2 가장 빠름

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
