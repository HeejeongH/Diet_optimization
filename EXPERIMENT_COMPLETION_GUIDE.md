# 실험 완료 후 자동화 가이드

## 📊 현재 상황
- **실험 진행 중**: main.ipynb 실행 (예상 3000분 = 50시간)
- **실험 조건**: 
  - 4개 알고리즘 (NSGA-II, NSGA-III, SPEA2, ε-MOEA)
  - 10회 반복
  - 100세대
  - **수정된 제약조건** 사용 ✅

---

## 🎯 실험 완료 시 자동 처리 사항

### 1️⃣ 결과 파일 확인
**생성될 파일:**
```
optimization_comparison_results.xlsx
```

**파일 위치:**
```bash
# 예상 경로 (main.ipynb 실행 디렉토리)
/home/user/diet_optimization_clean/optimization_comparison_results.xlsx
```

**파일 구조 (예상):**
- `Raw Results`: 10회 반복 원본 데이터
- `Statistical Analysis`: 정규성 검정, Kruskal-Wallis, Mann-Whitney U
- `Summary Statistics`: Mean, Std, Min, Max

---

### 2️⃣ 그림 자동 생성 스크립트

**명령어:**
```bash
cd /home/user/diet_optimization_clean/src
python3 generate_figures_v2.py
```

**생성될 그림 (6개):**
1. **Figure 1**: Performance Radar Chart (4개 알고리즘 종합 비교)
2. **Figure 2**: Hypervolume Box Plots (수렴 품질)
3. **Figure 3**: Spacing Comparison (해의 분포 균일성)
4. **Figure 4**: Diversity vs Convergence Scatter (다양성-수렴 관계)
5. **Figure 5**: Execution Time Comparison (실행 시간)
6. **Figure 6**: Statistical Significance Heatmap (통계적 유의성)

**저장 위치:**
```
visualization/figures/
├── figure1_radar_chart.pdf
├── figure1_radar_chart.png
├── figure2_hypervolume_boxplots.pdf
├── figure2_hypervolume_boxplots.png
├── figure3_spacing_comparison.pdf
├── figure3_spacing_comparison.png
├── figure4_diversity_convergence.pdf
├── figure4_diversity_convergence.png
├── figure5_execution_time.pdf
├── figure5_execution_time.png
├── figure6_significance_heatmap.pdf
└── figure6_significance_heatmap.png
```

---

### 3️⃣ 논문 Results 섹션 자동 생성

**실행 명령어:**
```bash
cd /home/user/diet_optimization_clean
python3 generate_paper_results.py
```

**생성 내용:**
1. **성능 비교 표** (LaTeX/Markdown)
2. **통계 분석 결과**
3. **주요 발견 사항**
4. **그림 설명문 (Figure captions)**

**저장 위치:**
```
docs/paper/
├── results_section.md
├── results_section.tex (LaTeX)
├── performance_table.tex
└── statistical_results.tex
```

---

## 🚀 자동 실행 워크플로우

### 옵션 A: 전체 자동화 (권장)

**하나의 명령어로 모든 작업 완료:**
```bash
cd /home/user/diet_optimization_clean
python3 auto_process_results.py
```

**처리 순서:**
1. 결과 파일 확인 및 검증
2. 데이터 추출 및 분석
3. 6개 그림 생성
4. 논문 Results 섹션 생성
5. GitHub 자동 커밋 & 푸시
6. 완료 리포트 생성

---

### 옵션 B: 단계별 실행

```bash
# 1. 결과 파일 확인
cd /home/user/diet_optimization_clean
python3 << EOF
import pandas as pd
import os

result_file = 'optimization_comparison_results.xlsx'
if os.path.exists(result_file):
    print(f"✅ 결과 파일 확인: {result_file}")
    xls = pd.ExcelFile(result_file)
    print(f"시트 목록: {xls.sheet_names}")
else:
    print(f"❌ 결과 파일 없음: {result_file}")
EOF

# 2. 그림 생성
cd /home/user/diet_optimization_clean/src
python3 generate_figures_v2.py

# 3. 논문 결과 생성
cd /home/user/diet_optimization_clean
python3 generate_paper_results.py

# 4. GitHub 업로드
cd /home/user/diet_optimization_clean
git add .
git commit -m "feat: Add v2 experiment results and figures"
git push origin main
```

---

## 📋 준비된 스크립트

### `auto_process_results.py` (메인 자동화)
```python
#!/usr/bin/env python3
"""
실험 완료 후 결과 자동 처리 스크립트

1. 결과 파일 확인 및 검증
2. 데이터 추출 및 분석
3. 그림 생성
4. 논문 결과 섹션 생성
5. GitHub 자동 커밋
"""

import os
import sys
import subprocess
from datetime import datetime

def main():
    print("="*80)
    print("🚀 실험 결과 자동 처리 시작")
    print("="*80)
    
    # 1. 결과 파일 확인
    print("\n[1/5] 결과 파일 확인 중...")
    result_file = 'optimization_comparison_results.xlsx'
    
    if not os.path.exists(result_file):
        print(f"❌ 결과 파일이 없습니다: {result_file}")
        print("main.ipynb 실행이 완료되지 않았을 수 있습니다.")
        sys.exit(1)
    
    print(f"✅ 결과 파일 확인: {result_file}")
    
    # 2. 데이터 검증
    print("\n[2/5] 데이터 검증 중...")
    import pandas as pd
    xls = pd.ExcelFile(result_file)
    print(f"  - 시트 개수: {len(xls.sheet_names)}")
    print(f"  - 시트 목록: {xls.sheet_names}")
    
    # 3. 그림 생성
    print("\n[3/5] 그림 생성 중...")
    subprocess.run(['python3', 'src/generate_figures_v2.py'], check=True)
    print("✅ 6개 그림 생성 완료")
    
    # 4. 논문 결과 생성
    print("\n[4/5] 논문 Results 섹션 생성 중...")
    subprocess.run(['python3', 'generate_paper_results.py'], check=True)
    print("✅ 논문 결과 생성 완료")
    
    # 5. GitHub 커밋
    print("\n[5/5] GitHub 업로드 중...")
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    commit_msg = f"feat: Add v2 experiment results ({timestamp})"
    
    subprocess.run(['git', 'add', '.'], check=True)
    subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
    subprocess.run(['git', 'push', 'origin', 'main'], check=True)
    print("✅ GitHub 업로드 완료")
    
    # 완료 리포트
    print("\n" + "="*80)
    print("🎉 모든 작업 완료!")
    print("="*80)
    print(f"""
생성된 파일:
- 그림: visualization/figures/*.pdf, *.png
- 논문: docs/paper/results_section.md
- 결과: {result_file}

다음 단계:
1. 그림 확인: ls -lh visualization/figures/
2. 논문 확인: cat docs/paper/results_section.md
3. GitHub: https://github.com/HeejeongH/Diet_optimization
""")

if __name__ == '__main__':
    main()
```

---

### `generate_figures_v2.py` (그림 생성)
```python
#!/usr/bin/env python3
"""
v2 실험 결과 기반 6개 그림 자동 생성
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

def load_results(file_path='optimization_comparison_results.xlsx'):
    """결과 파일에서 데이터 로드"""
    # Summary Statistics 읽기
    df = pd.read_excel(file_path, sheet_name='Summary Statistics', header=None)
    
    # 데이터 파싱
    metrics = {}
    current_metric = None
    
    for idx, row in df.iterrows():
        if pd.notna(row[0]):
            if row[0] in ['HYPERVOLUME', 'SPACING', 'DIVERSITY', 
                          'CONVERGENCE', 'EXECUTION_TIME', 'TIME']:
                current_metric = row[0]
                metrics[current_metric] = {}
            elif current_metric and row[0] not in ['Algorithm', 'NaN']:
                algo = row[0]
                metrics[current_metric][algo] = {
                    'mean': row[1],
                    'std': row[2],
                    'min': row[3],
                    'max': row[4]
                }
    
    return metrics

def generate_all_figures(metrics):
    """6개 그림 모두 생성"""
    output_dir = Path('visualization/figures')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Figure 1: Radar Chart
    generate_radar_chart(metrics, output_dir)
    
    # Figure 2: Hypervolume Boxplots
    generate_hypervolume_boxplots(metrics, output_dir)
    
    # Figure 3: Spacing Comparison
    generate_spacing_comparison(metrics, output_dir)
    
    # Figure 4: Diversity vs Convergence
    generate_diversity_convergence(metrics, output_dir)
    
    # Figure 5: Execution Time
    generate_execution_time(metrics, output_dir)
    
    # Figure 6: Statistical Significance
    generate_significance_heatmap(metrics, output_dir)
    
    print(f"✅ All figures saved to {output_dir}/")

# ... (각 그림 생성 함수 구현)

if __name__ == '__main__':
    print("Loading results...")
    metrics = load_results()
    
    print("Generating figures...")
    generate_all_figures(metrics)
    
    print("Done!")
```

---

### `generate_paper_results.py` (논문 결과 생성)
```python
#!/usr/bin/env python3
"""
논문 Results 섹션 자동 생성
"""

import pandas as pd
from pathlib import Path

def generate_performance_table(metrics):
    """성능 비교 표 생성"""
    # Markdown 테이블
    md_table = """
## Performance Comparison

| Metric | NSGA-II | NSGA-III | SPEA2 | ε-MOEA |
|--------|---------|----------|-------|--------|
"""
    
    for metric, data in metrics.items():
        row = f"| **{metric}** |"
        for algo in ['NSGA-II', 'NSGA-III', 'SPEA2', 'ε-MOEA']:
            if algo in data:
                mean = data[algo]['mean']
                std = data[algo]['std']
                row += f" {mean:.4f}±{std:.4f} |"
        md_table += row + "\n"
    
    return md_table

def generate_results_section(metrics):
    """Results 섹션 전체 생성"""
    results = f"""
# Results

## 4.1 Performance Metrics

{generate_performance_table(metrics)}

## 4.2 Key Findings

1. **Best Overall Performance**: ...
2. **Execution Time**: ...
3. **Statistical Significance**: ...

## 4.3 Discussion

...
"""
    
    return results

# ... (나머지 구현)
```

---

## 📞 실험 완료 시 알림

**실험이 완료되면 이렇게 알려주세요:**
```
"실험 완료했어요!" 또는
"main.ipynb 끝났어요!"
```

**그러면 제가 바로:**
1. 결과 파일 확인 ✅
2. 그림 생성 ✅
3. 논문 결과 작성 ✅
4. GitHub 업로드 ✅

모든 작업을 **5분 안에** 완료해드립니다! 🚀

---

**작성일**: 2025-12-06  
**대기 중**: main.ipynb 실험 (예상 50시간)
