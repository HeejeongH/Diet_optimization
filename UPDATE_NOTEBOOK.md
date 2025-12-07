# Table 1 생성 업데이트 완료

## 변경 사항

### ✅ `generate_figures.py` 수정 완료
- `figure6_performance_summary()` → Table 1로 변경
- 출력 파일명: `table1.png`, `table1.pdf`
- 타이틀: "Table 1: Algorithm Performance Comparison Summary"

### 📊 생성되는 파일
1. **Figure 1-5**: 메인 그림 (5개)
   - figure1_radar_chart.png/pdf
   - figure2_hypervolume_boxplots.png/pdf
   - figure3_spacing_comparison.png/pdf
   - figure4_diversity_convergence.png/pdf
   - figure5_execution_time.png/pdf

2. **Table 1**: 성능 비교 표
   - table1.png/pdf

### 📝 Table 1 내용
- Metric 열: Hypervolume, Spacing, Diversity, Convergence, Time (sec)
- Algorithm 열: NSGA-II, NSGA-III, SPEA2, ε-MOEA
- 각 셀: Mean±Std 형식
- 최고 성능 셀: 초록색 하이라이트

### 🚀 실행 방법
```bash
# 단일 스크립트 실행
cd /home/user/diet_optimization_clean/src/visualization
python generate_figures.py

# 또는 Jupyter 노트북에서
jupyter notebook generate_all_figures.ipynb
```

### ⚠️ 필수 파일
- `optimization_comparison_results.xlsx` (실험 결과 데이터)
- 위치: `src/visualization/` 폴더

### 📌 다음 단계
1. 실제 실험 결과 엑셀 파일 준비
2. `src/visualization/` 폴더에 배치
3. 노트북 또는 스크립트 실행
4. `results/figures/` 폴더에서 결과 확인

