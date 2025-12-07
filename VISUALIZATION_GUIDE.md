# 📊 METOR 시각화 가이드

## 🎯 가장 간단한 방법

```bash
python src/visualization/generate_main_figures.py
```

**이 명령어 하나로:**
- Figure 1-8 (논문 메인 그림 8개) ✅
- Table 1 (성능 요약 테이블) ✅
- 성능 지표 설명 (2개) ✅

**총 11개 파일이 `results/figures/`에 생성됩니다!**

---

## 📁 src/visualization/ 폴더 구성

### ✅ 실제로 사용하는 스크립트 (4개)

```
src/visualization/
├── generate_main_figures.py        ⭐ 이것 실행! (필수 그림만)
├── generate_all_figures.py         (필수 + 4D 대안 포함)
├── generate_figures.py             (Figure 1-8, Table 1)
└── visualize_metric_comparison.py  (성능 지표 설명)
```

### 📦 선택사항

```
src/visualization/
├── visualize_4d_alternatives.py    (4D 시각화 대안 - 논문 비교용)
└── archive/                        (개발 중 사용한 유틸리티들)
    ├── additional_figures.py
    ├── reorganize_figures.py
    └── visualize_metrics.py
```

---

## 🎨 각 스크립트가 생성하는 그림

### 1️⃣ generate_main_figures.py (권장) ⭐
**실행**: `python src/visualization/generate_main_figures.py`

**생성되는 것:**
```
results/figures/
├── figure1.png/pdf    # Convergence Plot
├── figure2.png/pdf    # 3D Pareto Front
├── figure3.png/pdf    # Radar Chart
├── table1.png/pdf     # Performance Table
├── figure4.png/pdf    # Hypervolume Box Plots
├── figure5.png/pdf    # Spacing Bar Chart
├── figure6.png/pdf    # Diversity vs Convergence
├── figure7.png/pdf    # Execution Time
├── figure8.png/pdf    # Statistical Heatmap
└── metric_examples/   # 성능 지표 설명 2개
    ├── comprehensive_metrics_comparison.png/pdf
    └── hypervolume_detailed.png/pdf
```

**총 11개 파일 (9 main + 2 explanation)**

---

### 2️⃣ generate_all_figures.py (전체)
**실행**: `python src/visualization/generate_all_figures.py`

**추가로 생성:**
```
results/figures/4d_visualization/
├── method1_3d_color_mapping.png/pdf
├── method2_pairwise_scatter.png/pdf
├── method3_parallel_coordinates.png/pdf
└── method4_heatmap_matrix.png/pdf
```

**총 19개 파일 (11 main + 8 alternatives)**

---

## 🤔 어떤 스크립트를 사용해야 하나?

### 대부분의 경우:
```bash
python src/visualization/generate_main_figures.py
```
✅ 논문에 필요한 모든 필수 그림  
✅ 빠른 실행 (~30-60초)  
✅ 충분한 그림 (11개)

### 4D 시각화 방법 비교가 필요할 때:
```bash
python src/visualization/generate_all_figures.py
```
✅ 필수 그림 + 4D 대안 방법  
⏱️ 조금 느림 (~60-90초)  
📊 더 많은 그림 (19개)

---

## 📊 그림 설명

| 그림 | 내용 | 논문 섹션 |
|------|------|-----------|
| **Figure 1** | Convergence Plot (세대별 성능) | 3.1 최적화 과정 |
| **Figure 2** | 3D Pareto Front (해 분포) | 3.2 해 분포 |
| **Figure 3** | Radar Chart (4개 알고리즘 비교) | 3.3 전체 성능 |
| **Table 1** | 성능 요약 표 | 3.3 전체 성능 |
| **Figure 4** | Hypervolume Box Plots | 3.4.1 최적화 품질 |
| **Figure 5** | Spacing Bar Chart | 3.4.2 해 분포 균일성 |
| **Figure 6** | Diversity vs Convergence | 3.4.3 트레이드오프 |
| **Figure 7** | Execution Time | 3.4.4 계산 효율성 |
| **Figure 8** | Statistical Heatmap | 3.5 통계 검증 |

---

## 💾 출력 위치

**모든 그림:**
```
results/figures/
```

**그림 종류:**
- `.png` - 논문/프레젠테이션용 (고해상도 300dpi)
- `.pdf` - 논문 출판용 (벡터 그래픽)

---

## 🔧 문제 해결

### Q: "optimization_comparison_results.xlsx not found"
**A**: 프로젝트 루트에서 실행하세요
```bash
cd /home/user/diet_optimization_clean
python src/visualization/generate_main_figures.py
```

### Q: 그림이 이상하게 나와요
**A**: 데이터 파일 확인
```bash
ls optimization_comparison_results.xlsx
```

### Q: 특정 그림만 다시 생성하려면?
**A**: 개별 스크립트 실행
```bash
# Figure 1-8만
python src/visualization/generate_figures.py

# 지표 설명만
python src/visualization/visualize_metric_comparison.py
```

---

## 🎯 핵심 요약

**99% 경우:**
```bash
python src/visualization/generate_main_figures.py
```

**이것만 기억하세요!** ✨

---

**프로젝트**: METOR (Multi-objective Enhanced Tool for Optimal meal Recommendation)  
**GitHub**: https://github.com/HeejeongH/Diet_optimization
