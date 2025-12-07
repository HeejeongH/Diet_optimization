"""
Figure 재구성: 논리적 흐름에 맞게 순서 변경
1. 최적화 과정 → 2. 해 분포 → 3. 종합 성능 → 4. 세부 분석 → 5. 통계 검증
"""
import os
import shutil

# 현재 figures 디렉토리 백업
figures_dir = 'figures'
backup_dir = 'figures_backup'

if os.path.exists(backup_dir):
    shutil.rmtree(backup_dir)
shutil.copytree(figures_dir, backup_dir)

print("=" * 70)
print("Figure 재구성 계획")
print("=" * 70)

# 새로운 Figure 순서 정의
new_order = {
    # Stage 1: 최적화 과정 (How)
    'figure1': {
        'old': 'figure8_convergence_plot',
        'title': 'Convergence Plot of Four Algorithms',
        'description': '최적화 과정: 세대별 Hypervolume 변화 (100 generations)',
        'section': '3.1 Optimization Process'
    },
    
    # Stage 2: 해의 분포 (What)
    'figure2': {
        'old': 'figure7_3d_pareto_front',
        'title': '3D Pareto Front Visualization',
        'description': '해의 분포: SPEA2의 Pareto solutions (3D+color)',
        'section': '3.2 Solution Distribution'
    },
    
    # Stage 3: 종합 성능 (Overview)
    'figure3': {
        'old': 'figure1_radar_chart',
        'title': 'Performance Radar Chart',
        'description': '종합 성능: 4개 알고리즘의 다차원 비교',
        'section': '3.3 Overall Performance'
    },
    
    'table1': {
        'old': 'figure6_performance_summary',
        'title': 'Performance Summary Table',
        'description': '성능 요약: 모든 지표의 평균±표준편차',
        'section': '3.3 Overall Performance'
    },
    
    # Stage 4: 세부 분석 (Details)
    'figure4': {
        'old': 'figure2_hypervolume_boxplots',
        'title': 'Hypervolume Distribution (Box Plots)',
        'description': '세부 분석 1: Hypervolume의 분포와 안정성 (10 runs)',
        'section': '3.4 Detailed Analysis'
    },
    
    'figure5': {
        'old': 'figure3_spacing_comparison',
        'title': 'Spacing Comparison (Bar Chart)',
        'description': '세부 분석 2: 해의 분포 균일성',
        'section': '3.4 Detailed Analysis'
    },
    
    'figure6': {
        'old': 'figure4_diversity_convergence',
        'title': 'Diversity vs Convergence (Scatter Plot)',
        'description': '세부 분석 3: Exploration-Exploitation Trade-off',
        'section': '3.4 Detailed Analysis'
    },
    
    'figure7': {
        'old': 'figure5_execution_time',
        'title': 'Execution Time Comparison',
        'description': '세부 분석 4: 계산 효율성',
        'section': '3.4 Detailed Analysis'
    },
    
    # Stage 5: 통계 검증 (Statistical Validation)
    'figure8': {
        'old': 'statistical_significance_heatmap',
        'title': 'Statistical Significance Heatmap',
        'description': '통계 검증: Mann-Whitney U test (p-values)',
        'section': '3.5 Statistical Validation'
    }
}

print("\n새로운 Figure 순서:\n")
for new_name, info in new_order.items():
    print(f"  {new_name.upper():<10} ← {info['old']}")
    print(f"             {info['title']}")
    print(f"             ({info['description']})")
    print(f"             Section: {info['section']}\n")

# 파일 복사 (이름 변경)
print("=" * 70)
print("파일 복사 중...")
print("=" * 70)

for new_name, info in new_order.items():
    old_base = info['old']
    
    # PNG, PDF 모두 처리
    for ext in ['png', 'pdf']:
        old_file = os.path.join(figures_dir, f"{old_base}.{ext}")
        new_file = os.path.join(figures_dir, f"{new_name}.{ext}")
        
        if os.path.exists(old_file):
            shutil.copy2(old_file, new_file)
            print(f"  ✅ {new_name}.{ext}")

print("\n" + "=" * 70)
print("완료! 새로운 Figure 파일 생성됨")
print("=" * 70)
print("\n기존 파일은 figures_backup/에 백업되었습니다.")
print("새로운 파일은 figures/에 생성되었습니다.")
