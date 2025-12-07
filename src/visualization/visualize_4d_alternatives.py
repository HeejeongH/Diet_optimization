"""
4차원 목적함수 시각화를 위한 추가 옵션들
METOR 프로젝트: Nutrition, Cost, Harmony, Diversity
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
from pathlib import Path

# Create output directory
output_dir = Path('results/figures/4d_visualization')
output_dir.mkdir(parents=True, exist_ok=True)

# 샘플 데이터 (실제로는 Pareto Front 해들)
np.random.seed(42)
n_solutions = 50

# 4개 목적함수 (0~1로 정규화된 값)
data = {
    'Nutrition': np.random.uniform(0.7, 1.0, n_solutions),
    'Cost': np.random.uniform(0.6, 0.95, n_solutions),
    'Harmony': np.random.uniform(0.65, 0.98, n_solutions),
    'Diversity': np.random.uniform(0.7, 0.95, n_solutions),
    'Algorithm': np.random.choice(['NSGA-II', 'NSGA-III', 'SPEA2'], n_solutions)
}
df = pd.DataFrame(data)

# 출력 디렉토리
import os
os.makedirs('figures/4d_visualization', exist_ok=True)

# ===========================================
# 방법 1: 3D + Color Mapping
# ===========================================
fig = plt.figure(figsize=(12, 9))
ax = fig.add_subplot(111, projection='3d')

for algo, color in zip(['NSGA-II', 'NSGA-III', 'SPEA2'], 
                       ['#FF6B6B', '#4ECDC4', '#95E1D3']):
    mask = df['Algorithm'] == algo
    scatter = ax.scatter(
        df.loc[mask, 'Nutrition'],
        df.loc[mask, 'Cost'],
        df.loc[mask, 'Harmony'],
        c=df.loc[mask, 'Diversity'],  # 4번째 목적함수를 색상으로
        s=150,
        alpha=0.7,
        cmap='viridis',
        edgecolors='black',
        linewidth=1,
        label=algo
    )

ax.set_xlabel('Nutritional Adequacy', fontsize=12, fontweight='bold')
ax.set_ylabel('Cost Effectiveness', fontsize=12, fontweight='bold')
ax.set_zlabel('Menu Harmony', fontsize=12, fontweight='bold')
ax.set_title('4D Pareto Front Visualization\n(Color = Dietary Diversity)', 
             fontsize=14, fontweight='bold', pad=20)

# Colorbar for 4th objective
cbar = plt.colorbar(scatter, ax=ax, pad=0.1, shrink=0.8)
cbar.set_label('Dietary Diversity', fontsize=11, fontweight='bold')

ax.legend(loc='upper left', fontsize=10)
ax.view_init(elev=25, azim=45)

plt.tight_layout()
plt.savefig('results/figures/4d_visualization/method1_3d_color_mapping.png', dpi=300, bbox_inches='tight')
plt.savefig('results/figures/4d_visualization/method1_3d_color_mapping.pdf', bbox_inches='tight')
plt.close()

# ===========================================
# 방법 2: Pairwise Scatter Matrix (2D 조합)
# ===========================================
fig, axes = plt.subplots(3, 2, figsize=(14, 16))
objectives = ['Nutrition', 'Cost', 'Harmony', 'Diversity']
colors_map = {'NSGA-II': '#FF6B6B', 'NSGA-III': '#4ECDC4', 'SPEA2': '#95E1D3'}

pairs = [
    ('Nutrition', 'Cost'),
    ('Nutrition', 'Harmony'),
    ('Nutrition', 'Diversity'),
    ('Cost', 'Harmony'),
    ('Cost', 'Diversity'),
    ('Harmony', 'Diversity')
]

for idx, (obj1, obj2) in enumerate(pairs):
    ax = axes.flat[idx]
    for algo in ['NSGA-II', 'NSGA-III', 'SPEA2']:
        mask = df['Algorithm'] == algo
        ax.scatter(df.loc[mask, obj1], df.loc[mask, obj2], 
                  color=colors_map[algo], label=algo, 
                  s=80, alpha=0.6, edgecolors='black', linewidth=0.5)
    
    ax.set_xlabel(obj1, fontsize=11, fontweight='bold')
    ax.set_ylabel(obj2, fontsize=11, fontweight='bold')
    ax.set_title(f'{obj1} vs {obj2}', fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3)
    if idx == 0:
        ax.legend(fontsize=9)

plt.suptitle('4D Pareto Front: Pairwise Objective Comparisons', 
             fontsize=16, fontweight='bold', y=0.995)
plt.tight_layout()
plt.savefig('results/figures/4d_visualization/method2_pairwise_scatter.png', dpi=300, bbox_inches='tight')
plt.savefig('results/figures/4d_visualization/method2_pairwise_scatter.pdf', bbox_inches='tight')
plt.close()

# ===========================================
# 방법 3: Parallel Coordinates Plot
# ===========================================
from pandas.plotting import parallel_coordinates

fig, ax = plt.subplots(figsize=(14, 8))

parallel_coordinates(
    df,
    'Algorithm',
    cols=['Nutrition', 'Cost', 'Harmony', 'Diversity'],
    color=['#FF6B6B', '#4ECDC4', '#95E1D3'],
    alpha=0.3,
    linewidth=1.5,
    ax=ax
)

ax.set_title('4D Pareto Front: Parallel Coordinates', 
             fontsize=16, fontweight='bold', pad=20)
ax.set_ylabel('Normalized Objective Value', fontsize=12, fontweight='bold')
ax.set_ylim([0.5, 1.05])
ax.grid(True, alpha=0.3, axis='y')
ax.legend(loc='lower right', fontsize=11)

plt.tight_layout()
plt.savefig('results/figures/4d_visualization/method3_parallel_coordinates.png', dpi=300, bbox_inches='tight')
plt.savefig('results/figures/4d_visualization/method3_parallel_coordinates.pdf', bbox_inches='tight')
plt.close()

# ===========================================
# 방법 4: Heatmap Matrix (알고리즘 × 목적함수)
# ===========================================
fig, ax = plt.subplots(figsize=(10, 6))

# 알고리즘별 평균 성능
heatmap_data = df.groupby('Algorithm')[objectives].mean()

sns.heatmap(
    heatmap_data.T,  # Transpose for better layout
    annot=True,
    fmt='.3f',
    cmap='YlGnBu',
    cbar_kws={'label': 'Performance (0-1)'},
    linewidths=1,
    linecolor='white',
    ax=ax
)

ax.set_title('4D Performance Heatmap: Algorithm Comparison', 
             fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Algorithm', fontsize=12, fontweight='bold')
ax.set_ylabel('Objective Function', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig('results/figures/4d_visualization/method4_heatmap_matrix.png', dpi=300, bbox_inches='tight')
plt.savefig('results/figures/4d_visualization/method4_heatmap_matrix.pdf', bbox_inches='tight')
plt.close()

print("=" * 60)
print("4D 시각화 방법 비교 완료!")
print("=" * 60)
print("\n생성된 파일:")
print("  📊 방법 1: 3D + Color Mapping (4번째 목적함수를 색상으로)")
print("  📊 방법 2: Pairwise Scatter Matrix (6개 2D 조합)")
print("  📊 방법 3: Parallel Coordinates (모든 목적함수 동시 비교)")
print("  📊 방법 4: Heatmap Matrix (알고리즘별 평균 성능)")
print("\n저장 위치: figures/4d_visualization/")
print("=" * 60)
