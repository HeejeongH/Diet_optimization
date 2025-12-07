# METOR 시각화 스크립트

## 🎯 가장 쉬운 방법 (권장!)

### **필수 그림만 생성 (논문용)**
```bash
python src/visualization/generate_main_figures.py
```

**생성되는 것:**
- ✅ Figure 1-8 (메인 논문 그림 8개)
- ✅ Table 1 (성능 요약 테이블)
- ✅ 성능 지표 설명 그림 2개

**총 11개 파일** → `results/figures/`

---

## 📋 스크립트 설명

### 필수 스크립트 (2개)

#### 1. **generate_main_figures.py** ⭐ (가장 추천!)
**용도**: 논문에 필요한 모든 필수 그림 생성
```bash
python src/visualization/generate_main_figures.py
```

**생성 내용:**
- Figure 1: Convergence Plot
- Figure 2: 3D Pareto Front
- Figure 3: Radar Chart
- Table 1: Performance Summary
- Figure 4: Hypervolume Box Plots
- Figure 5: Spacing Bar Chart
- Figure 6: Diversity vs Convergence
- Figure 7: Execution Time
- Figure 8: Statistical Heatmap
- 성능 지표 설명 그림 2개

**실행 시간**: ~30-60초

---

#### 2. **generate_all_figures.py** (전체 버전)
**용도**: 필수 그림 + 선택적 4D 시각화 방법까지 모두 생성
```bash
python src/visualization/generate_all_figures.py
```

**추가 생성 내용:**
- 4D 시각화 대안 방법 4개 (선택사항)

**실행 시간**: ~60-90초

---

### 개별 스크립트 (직접 실행 가능)

#### **generate_figures.py**
메인 Figure 1-8 + Table 1 생성
```bash
python src/visualization/generate_figures.py
```

#### **visualize_metric_comparison.py**
성능 지표 설명 그림 생성
```bash
python src/visualization/visualize_metric_comparison.py
```

#### **visualize_4d_alternatives.py** (선택사항)
4D 시각화 대안 방법 생성
```bash
python src/visualization/visualize_4d_alternatives.py
```

---

## 📊 출력 구조

```
results/figures/
├── figure1.png/pdf         # Convergence Plot
├── figure2.png/pdf         # 3D Pareto Front
├── figure3.png/pdf         # Radar Chart
├── table1.png/pdf          # Performance Table
├── figure4.png/pdf         # Hypervolume Box Plots
├── figure5.png/pdf         # Spacing Bar Chart
├── figure6.png/pdf         # Diversity vs Convergence
├── figure7.png/pdf         # Execution Time
├── figure8.png/pdf         # Statistical Heatmap
├── metric_examples/        # 성능 지표 설명
│   ├── comprehensive_metrics_comparison.png/pdf
│   └── hypervolume_detailed.png/pdf
└── 4d_visualization/       # (선택사항) 4D 대안 방법
    ├── method1_3d_color_mapping.png/pdf
    ├── method2_pairwise_scatter.png/pdf
    ├── method3_parallel_coordinates.png/pdf
    └── method4_heatmap_matrix.png/pdf
```

---

## 🗂️ Archive 폴더

**archive/**: 개발 중 사용했던 유틸리티 스크립트들
- `additional_figures.py` - 대안 버전 (중복)
- `reorganize_figures.py` - 파일 재배치 유틸리티
- `visualize_metrics.py` - 테스트용

**→ 실제 논문 작성에는 사용 안 함**

---

## 💡 사용 가이드

### 논문 작성 시

**1단계**: 필수 그림만 생성
```bash
python src/visualization/generate_main_figures.py
```

**2단계**: results/figures/ 확인
- Figure 1-8 + Table 1 사용

### 4D 시각화 방법 비교가 필요할 때

**전체 버전 실행:**
```bash
python src/visualization/generate_all_figures.py
```

**또는 4D만 추가 생성:**
```bash
python src/visualization/visualize_4d_alternatives.py
```

---

## 📦 의존성

모든 스크립트가 필요로 하는 라이브러리:
- numpy
- pandas
- matplotlib
- seaborn
- scipy

**설치:**
```bash
pip install numpy pandas matplotlib seaborn scipy openpyxl
```

---

## 🎯 핵심 요약

| 목적 | 실행 명령어 | 생성 파일 수 |
|------|------------|-------------|
| **논문용 (권장)** | `generate_main_figures.py` | 11개 |
| **전체 (4D 포함)** | `generate_all_figures.py` | 19개 |
| **메인 그림만** | `generate_figures.py` | 9개 |
| **지표 설명만** | `visualize_metric_comparison.py` | 2개 |
| **4D 대안만** | `visualize_4d_alternatives.py` | 8개 |

---

**대부분의 경우 `generate_main_figures.py` 하나면 충분합니다!** ✨
