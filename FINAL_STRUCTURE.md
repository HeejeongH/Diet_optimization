# METOR 프로젝트 최종 구조

## 📁 깔끔하게 정리된 구조

```
diet_optimization_clean/
│
├── src/                              # 소스 코드
│   │
│   ├── visualization/                # ✨ 시각화 코드 (여기만!)
│   │   ├── generate_all_figures.py  # 🎯 마스터 스크립트 (이것만 실행!)
│   │   ├── generate_figures.py      # 메인 그림 (Figure 1-8, Table 1)
│   │   ├── visualize_4d_alternatives.py    # 4D 시각화 방법
│   │   ├── visualize_metric_comparison.py  # 성능 지표 설명
│   │   ├── additional_figures.py    # 보충 그림
│   │   └── README.md                # 시각화 가이드
│   │
│   ├── Diet_class.py                # 식단 클래스
│   ├── evaluation_function.py       # 목적 함수
│   ├── load_data.py                 # 데이터 로딩
│   ├── optimizer_base.py            # 최적화 기본 클래스
│   ├── nsga2_optimizer.py           # NSGA-II
│   ├── nsga3_optimizer.py           # NSGA-III
│   ├── spea2_optimizer.py           # SPEA2
│   ├── emoea_optimizer.py           # ε-MOEA
│   ├── performance_metrics.py       # 성능 평가
│   ├── statistical_analysis.py      # 통계 분석
│   ├── food_mapper.py               # 식품 매핑
│   ├── diet_converter.py            # 식단 변환
│   ├── utils.py                     # 유틸리티
│   └── app.py                       # 웹 앱
│
├── results/                         # 📊 결과 (여기만!)
│   └── figures/                     # 모든 그림 출력
│       ├── figure1.png/pdf          # Convergence Plot
│       ├── figure2.png/pdf          # 3D Pareto Front
│       ├── figure3.png/pdf          # Radar Chart
│       ├── table1.png/pdf           # Performance Table
│       ├── figure4.png/pdf          # Hypervolume Box Plots
│       ├── figure5.png/pdf          # Spacing Bar Chart
│       ├── figure6.png/pdf          # Diversity vs Convergence
│       ├── figure7.png/pdf          # Execution Time
│       ├── figure8.png/pdf          # Statistical Heatmap
│       ├── 4d_visualization/        # 4D 시각화 방법들
│       └── metric_examples/         # 성능 지표 설명
│
├── docs/                            # 문서
│   └── paper/                       # 논문 관련
│       ├── results_section_v2.md
│       └── performance_metrics_explained.md
│
├── data/                            # 데이터
│   ├── food_data.csv
│   └── nutrition_requirements.json
│
├── optimization_comparison_results.xlsx  # 실험 결과
├── README.md
├── requirements.txt
└── .gitignore
```

## 🎯 핵심 요약

### src/ 폴더 = 코드만
- **알고리즘 코드**: `*_optimizer.py`
- **평가/분석**: `evaluation_function.py`, `performance_metrics.py`, `statistical_analysis.py`
- **시각화**: `src/visualization/` (한 곳에 모음!)
- **기타**: `app.py`, `utils.py` 등

### results/ 폴더 = 출력만
- **모든 그림**: `results/figures/`
- **하위 폴더**: `4d_visualization/`, `metric_examples/`

## 🚀 사용법

### 그림 생성 (가장 간단!)
```bash
python src/visualization/generate_all_figures.py
```

이 명령어 하나로 모든 그림이 `results/figures/`에 생성됩니다!

## ✅ 정리된 파일 개수

- **src/ 파일**: 14개 (알고리즘 + 유틸리티)
- **src/visualization/ 파일**: 6개 (시각화만)
- **중복 제거**: generate_figures.py, visualize_4d_alternatives.py, additional_figures.py

**→ 깔끔하고 명확한 구조! ✨**
