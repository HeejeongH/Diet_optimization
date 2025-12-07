"""
성능 지표 시각적 설명 - 직관적 이해를 위한 2D 예시
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# 한글 폰트 설정
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

# 출력 디렉토리
import os
os.makedirs('metric_examples', exist_ok=True)

# ============================================
# 1. Hypervolume 시각화 (2D 예시)
# ============================================
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Case 1: 좋은 Hypervolume (많은 해, 넓은 영역)
ax = axes[0]
solutions_good = np.array([
    [0.3, 0.9], [0.4, 0.85], [0.5, 0.8], 
    [0.6, 0.75], [0.7, 0.7], [0.8, 0.6], [0.9, 0.4]
])
ax.scatter(solutions_good[:, 0], solutions_good[:, 1], 
           s=200, c='green', marker='o', edgecolors='black', linewidth=2, 
           label='Solutions', zorder=3)

# Hypervolume 영역 표시
reference_point = [1.0, 0.0]
for sol in solutions_good:
    rect = patches.Rectangle(sol, reference_point[0]-sol[0], reference_point[1]-sol[1],
                             linewidth=0, facecolor='green', alpha=0.2)
    ax.add_patch(rect)

ax.scatter(*reference_point, s=300, c='red', marker='x', linewidth=3, 
           label='Reference Point', zorder=3)
ax.set_xlim([0, 1.1])
ax.set_ylim([0, 1])
ax.set_xlabel('Objective 1 (e.g., Cost)', fontsize=13, fontweight='bold')
ax.set_ylabel('Objective 2 (e.g., Nutrition)', fontsize=13, fontweight='bold')
ax.set_title('Good Hypervolume\n(Many solutions, Wide coverage)', 
             fontsize=14, fontweight='bold', color='green')
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)
ax.text(0.5, 0.95, 'Hypervolume ≈ 0.42', fontsize=12, ha='center', 
        bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))

# Case 2: 중간 Hypervolume
ax = axes[1]
solutions_mid = np.array([
    [0.4, 0.8], [0.5, 0.75], [0.6, 0.7], [0.7, 0.6], [0.8, 0.5]
])
ax.scatter(solutions_mid[:, 0], solutions_mid[:, 1], 
           s=200, c='orange', marker='o', edgecolors='black', linewidth=2, zorder=3)

for sol in solutions_mid:
    rect = patches.Rectangle(sol, reference_point[0]-sol[0], reference_point[1]-sol[1],
                             linewidth=0, facecolor='orange', alpha=0.2)
    ax.add_patch(rect)

ax.scatter(*reference_point, s=300, c='red', marker='x', linewidth=3, zorder=3)
ax.set_xlim([0, 1.1])
ax.set_ylim([0, 1])
ax.set_xlabel('Objective 1 (e.g., Cost)', fontsize=13, fontweight='bold')
ax.set_ylabel('Objective 2 (e.g., Nutrition)', fontsize=13, fontweight='bold')
ax.set_title('Medium Hypervolume\n(Fewer solutions, Moderate coverage)', 
             fontsize=14, fontweight='bold', color='orange')
ax.grid(True, alpha=0.3)
ax.text(0.5, 0.95, 'Hypervolume ≈ 0.28', fontsize=12, ha='center',
        bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

# Case 3: 나쁜 Hypervolume (적은 해, 좁은 영역)
ax = axes[2]
solutions_bad = np.array([
    [0.6, 0.65], [0.65, 0.6], [0.7, 0.58]
])
ax.scatter(solutions_bad[:, 0], solutions_bad[:, 1], 
           s=200, c='red', marker='o', edgecolors='black', linewidth=2, zorder=3)

for sol in solutions_bad:
    rect = patches.Rectangle(sol, reference_point[0]-sol[0], reference_point[1]-sol[1],
                             linewidth=0, facecolor='red', alpha=0.2)
    ax.add_patch(rect)

ax.scatter(*reference_point, s=300, c='red', marker='x', linewidth=3, zorder=3)
ax.set_xlim([0, 1.1])
ax.set_ylim([0, 1])
ax.set_xlabel('Objective 1 (e.g., Cost)', fontsize=13, fontweight='bold')
ax.set_ylabel('Objective 2 (e.g., Nutrition)', fontsize=13, fontweight='bold')
ax.set_title('Poor Hypervolume\n(Few solutions, Narrow coverage)', 
             fontsize=14, fontweight='bold', color='red')
ax.grid(True, alpha=0.3)
ax.text(0.5, 0.95, 'Hypervolume ≈ 0.12', fontsize=12, ha='center',
        bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.8))

plt.tight_layout()
plt.savefig('metric_examples/1_hypervolume_comparison.png', dpi=300, bbox_inches='tight')
plt.close()

print("✅ 1. Hypervolume 비교 이미지 생성 완료")

# ============================================
# 2. Spacing 시각화
# ============================================
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Case 1: 균일한 Spacing (좋음)
ax = axes[0]
x_uniform = np.linspace(0.2, 0.9, 8)
y_uniform = 1 - x_uniform
ax.plot(x_uniform, y_uniform, 'o-', color='green', markersize=15, 
        linewidth=2, markeredgecolor='black', markeredgewidth=2, label='Solutions')

# 간격 표시
for i in range(len(x_uniform)-1):
    mid_x = (x_uniform[i] + x_uniform[i+1]) / 2
    mid_y = (y_uniform[i] + y_uniform[i+1]) / 2
    distance = np.sqrt((x_uniform[i+1]-x_uniform[i])**2 + (y_uniform[i+1]-y_uniform[i])**2)
    ax.annotate('', xy=(x_uniform[i+1], y_uniform[i+1]), xytext=(x_uniform[i], y_uniform[i]),
                arrowprops=dict(arrowstyle='<->', color='blue', lw=2))
    ax.text(mid_x, mid_y-0.05, f'{distance:.2f}', fontsize=10, ha='center', color='blue')

ax.set_xlim([0, 1])
ax.set_ylim([0, 1])
ax.set_xlabel('Objective 1 (e.g., Cost)', fontsize=13, fontweight='bold')
ax.set_ylabel('Objective 2 (e.g., Nutrition)', fontsize=13, fontweight='bold')
ax.set_title('Uniform Spacing (Low = Good)\nNSGA-III Style', 
             fontsize=14, fontweight='bold', color='green')
ax.grid(True, alpha=0.3)
ax.text(0.5, 0.95, 'Spacing ≈ 0.01 (균일)', fontsize=12, ha='center',
        bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))

# Case 2: 불균일한 Spacing (나쁨)
ax = axes[1]
x_nonuniform = np.array([0.2, 0.25, 0.3, 0.5, 0.52, 0.85, 0.87, 0.9])
y_nonuniform = 1 - x_nonuniform
ax.plot(x_nonuniform, y_nonuniform, 'o-', color='red', markersize=15, 
        linewidth=2, markeredgecolor='black', markeredgewidth=2)

# 간격 표시
for i in range(len(x_nonuniform)-1):
    mid_x = (x_nonuniform[i] + x_nonuniform[i+1]) / 2
    mid_y = (y_nonuniform[i] + y_nonuniform[i+1]) / 2
    distance = np.sqrt((x_nonuniform[i+1]-x_nonuniform[i])**2 + (y_nonuniform[i+1]-y_nonuniform[i])**2)
    ax.annotate('', xy=(x_nonuniform[i+1], y_nonuniform[i+1]), xytext=(x_nonuniform[i], y_nonuniform[i]),
                arrowprops=dict(arrowstyle='<->', color='red', lw=2))
    ax.text(mid_x, mid_y-0.05, f'{distance:.2f}', fontsize=10, ha='center', color='red')

ax.set_xlim([0, 1])
ax.set_ylim([0, 1])
ax.set_xlabel('Objective 1 (e.g., Cost)', fontsize=13, fontweight='bold')
ax.set_ylabel('Objective 2 (e.g., Nutrition)', fontsize=13, fontweight='bold')
ax.set_title('Non-uniform Spacing (High = Bad)\nε-MOEA Style', 
             fontsize=14, fontweight='bold', color='red')
ax.grid(True, alpha=0.3)
ax.text(0.5, 0.95, 'Spacing ≈ 0.15 (불균일)', fontsize=12, ha='center',
        bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.8))

plt.tight_layout()
plt.savefig('metric_examples/2_spacing_comparison.png', dpi=300, bbox_inches='tight')
plt.close()

print("✅ 2. Spacing 비교 이미지 생성 완료")

# ============================================
# 3. Diversity 시각화
# ============================================
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Case 1: 높은 Diversity (넓은 탐색)
ax = axes[0]
x_high_div = np.linspace(0.1, 0.95, 10)
y_high_div = 1 - x_high_div + np.random.normal(0, 0.05, 10)
ax.scatter(x_high_div, y_high_div, s=200, c='purple', marker='o', 
           edgecolors='black', linewidth=2, label='Solutions')

# 범위 표시
ax.axvline(x_high_div.min(), color='blue', linestyle='--', linewidth=2, alpha=0.7)
ax.axvline(x_high_div.max(), color='blue', linestyle='--', linewidth=2, alpha=0.7)
ax.axhline(y_high_div.min(), color='blue', linestyle='--', linewidth=2, alpha=0.7)
ax.axhline(y_high_div.max(), color='blue', linestyle='--', linewidth=2, alpha=0.7)

# 영역 강조
ax.fill_between([x_high_div.min(), x_high_div.max()], 
                [y_high_div.min(), y_high_div.min()],
                [y_high_div.max(), y_high_div.max()],
                alpha=0.2, color='purple')

ax.set_xlim([0, 1])
ax.set_ylim([0, 1.1])
ax.set_xlabel('Objective 1 (e.g., Cost)', fontsize=13, fontweight='bold')
ax.set_ylabel('Objective 2 (e.g., Nutrition)', fontsize=13, fontweight='bold')
ax.set_title('High Diversity\nε-MOEA Style (Wide exploration)', 
             fontsize=14, fontweight='bold', color='purple')
ax.grid(True, alpha=0.3)
ax.text(0.5, 1.05, f'Range X: {x_high_div.max()-x_high_div.min():.2f}\nRange Y: {y_high_div.max()-y_high_div.min():.2f}', 
        fontsize=11, ha='center',
        bbox=dict(boxstyle='round', facecolor='lavender', alpha=0.8))

# Case 2: 낮은 Diversity (좁은 탐색)
ax = axes[1]
x_low_div = np.linspace(0.4, 0.6, 10)
y_low_div = 1 - x_low_div + np.random.normal(0, 0.02, 10)
ax.scatter(x_low_div, y_low_div, s=200, c='brown', marker='o', 
           edgecolors='black', linewidth=2)

# 범위 표시
ax.axvline(x_low_div.min(), color='red', linestyle='--', linewidth=2, alpha=0.7)
ax.axvline(x_low_div.max(), color='red', linestyle='--', linewidth=2, alpha=0.7)
ax.axhline(y_low_div.min(), color='red', linestyle='--', linewidth=2, alpha=0.7)
ax.axhline(y_low_div.max(), color='red', linestyle='--', linewidth=2, alpha=0.7)

# 영역 강조
ax.fill_between([x_low_div.min(), x_low_div.max()], 
                [y_low_div.min(), y_low_div.min()],
                [y_low_div.max(), y_low_div.max()],
                alpha=0.2, color='brown')

ax.set_xlim([0, 1])
ax.set_ylim([0, 1.1])
ax.set_xlabel('Objective 1 (e.g., Cost)', fontsize=13, fontweight='bold')
ax.set_ylabel('Objective 2 (e.g., Nutrition)', fontsize=13, fontweight='bold')
ax.set_title('Low Diversity\nNSGA-II Style (Focused search)', 
             fontsize=14, fontweight='bold', color='brown')
ax.grid(True, alpha=0.3)
ax.text(0.5, 1.05, f'Range X: {x_low_div.max()-x_low_div.min():.2f}\nRange Y: {y_low_div.max()-y_low_div.min():.2f}', 
        fontsize=11, ha='center',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

plt.tight_layout()
plt.savefig('metric_examples/3_diversity_comparison.png', dpi=300, bbox_inches='tight')
plt.close()

print("✅ 3. Diversity 비교 이미지 생성 완료")

# ============================================
# 4. Convergence 시각화
# ============================================
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# 참조 Pareto Front (진짜 최적해)
x_ref = np.linspace(0.1, 0.9, 20)
y_ref = 1 - x_ref

# Case 1: 좋은 Convergence (최적해에 가까움)
ax = axes[0]
ax.plot(x_ref, y_ref, 'k-', linewidth=3, label='True Pareto Front', zorder=1)

x_good_conv = x_ref[::2] + np.random.normal(0, 0.02, 10)
y_good_conv = (1 - x_good_conv) + np.random.normal(0, 0.02, 10)
ax.scatter(x_good_conv, y_good_conv, s=200, c='green', marker='o', 
           edgecolors='black', linewidth=2, label='Algorithm Solutions', zorder=2)

# 거리 표시
for i in range(0, len(x_good_conv), 3):
    ax.plot([x_good_conv[i], x_ref[i*2]], [y_good_conv[i], y_ref[i*2]], 
            'r--', linewidth=1.5, alpha=0.7)
    distance = np.sqrt((x_good_conv[i]-x_ref[i*2])**2 + (y_good_conv[i]-y_ref[i*2])**2)
    mid_x = (x_good_conv[i] + x_ref[i*2]) / 2
    mid_y = (y_good_conv[i] + y_ref[i*2]) / 2
    ax.text(mid_x, mid_y+0.05, f'{distance:.3f}', fontsize=9, color='red')

ax.set_xlim([0, 1])
ax.set_ylim([0, 1.1])
ax.set_xlabel('Objective 1 (e.g., Cost)', fontsize=13, fontweight='bold')
ax.set_ylabel('Objective 2 (e.g., Nutrition)', fontsize=13, fontweight='bold')
ax.set_title('Good Convergence (Low = Good)\nNSGA-II Style', 
             fontsize=14, fontweight='bold', color='green')
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)
ax.text(0.5, 1.05, 'Avg Distance ≈ 0.02 (가까움)', fontsize=12, ha='center',
        bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))

# Case 2: 나쁜 Convergence (최적해에서 멀음)
ax = axes[1]
ax.plot(x_ref, y_ref, 'k-', linewidth=3, label='True Pareto Front', zorder=1)

x_bad_conv = x_ref[::2] + np.random.normal(0, 0.08, 10)
y_bad_conv = (1 - x_bad_conv) - 0.15 + np.random.normal(0, 0.05, 10)
ax.scatter(x_bad_conv, y_bad_conv, s=200, c='red', marker='o', 
           edgecolors='black', linewidth=2, label='Algorithm Solutions', zorder=2)

# 거리 표시
for i in range(0, len(x_bad_conv), 3):
    ax.plot([x_bad_conv[i], x_ref[i*2]], [y_bad_conv[i], y_ref[i*2]], 
            'r--', linewidth=1.5, alpha=0.7)
    distance = np.sqrt((x_bad_conv[i]-x_ref[i*2])**2 + (y_bad_conv[i]-y_ref[i*2])**2)
    mid_x = (x_bad_conv[i] + x_ref[i*2]) / 2
    mid_y = (y_bad_conv[i] + y_ref[i*2]) / 2
    ax.text(mid_x, mid_y+0.05, f'{distance:.3f}', fontsize=9, color='red')

ax.set_xlim([0, 1])
ax.set_ylim([0, 1.1])
ax.set_xlabel('Objective 1 (e.g., Cost)', fontsize=13, fontweight='bold')
ax.set_ylabel('Objective 2 (e.g., Nutrition)', fontsize=13, fontweight='bold')
ax.set_title('Poor Convergence (High = Bad)\nε-MOEA Style', 
             fontsize=14, fontweight='bold', color='red')
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)
ax.text(0.5, 1.05, 'Avg Distance ≈ 0.16 (멀음)', fontsize=12, ha='center',
        bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.8))

plt.tight_layout()
plt.savefig('metric_examples/4_convergence_comparison.png', dpi=300, bbox_inches='tight')
plt.close()

print("✅ 4. Convergence 비교 이미지 생성 완료")

# ============================================
# 5. 5개 지표 종합 비교 (METOR 결과)
# ============================================
fig, ax = plt.subplots(figsize=(14, 8))

algorithms = ['NSGA-II', 'NSGA-III', 'SPEA2', 'ε-MOEA']
metrics = ['Hypervolume\n(높을수록 좋음)', 'Spacing\n(낮을수록 좋음)', 
           'Diversity', 'Convergence\n(낮을수록 좋음)', 'Execution Time\n(낮을수록 좋음)']

# 실제 METOR 데이터 (정규화 0-1)
data = {
    'NSGA-II':   [0.98, 0.48, 0.35, 0.90, 0.88],  # Hypervolume높음, Convergence낮음(좋음)
    'NSGA-III':  [0.97, 1.00, 0.38, 0.88, 0.61],  # Spacing낮음(좋음)
    'SPEA2':     [1.00, 0.61, 0.50, 0.70, 1.00],  # Hypervolume최고, Time최고(좋음)
    'ε-MOEA':    [0.00, 0.00, 1.00, 0.00, 0.00],  # 모든 지표 최악
}

x = np.arange(len(metrics))
width = 0.2

colors = {'NSGA-II': '#FF6B6B', 'NSGA-III': '#4ECDC4', 
          'SPEA2': '#95E1D3', 'ε-MOEA': '#FFA07A'}

for i, (algo, values) in enumerate(data.items()):
    offset = width * (i - 1.5)
    bars = ax.bar(x + offset, values, width, label=algo, 
                   color=colors[algo], edgecolor='black', linewidth=1.5)
    
    # 값 표시
    for bar, val in zip(bars, values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                f'{val:.2f}', ha='center', va='bottom', fontsize=9, fontweight='bold')

ax.set_ylabel('Normalized Performance (0-1)', fontsize=14, fontweight='bold')
ax.set_xlabel('Performance Metrics', fontsize=14, fontweight='bold')
ax.set_title('METOR Results: 5 Performance Metrics Comparison\n(Normalized to 0-1 scale)', 
             fontsize=16, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(metrics, fontsize=11)
ax.legend(loc='upper left', fontsize=12, frameon=True, shadow=True)
ax.set_ylim([0, 1.15])
ax.grid(True, alpha=0.3, axis='y')

# 주석 추가
ax.text(0, 1.08, '✅ SPEA2:\n최고 품질 + 최고 속도', fontsize=10, ha='center',
        bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
ax.text(1, 1.08, '✅ NSGA-III:\n최고 균일성', fontsize=10, ha='center',
        bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
ax.text(3, 1.08, '✅ NSGA-II:\n최고 수렴', fontsize=10, ha='center',
        bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
ax.text(4, 1.08, '❌ ε-MOEA:\n모든 지표 최악', fontsize=10, ha='center',
        bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.8))

plt.tight_layout()
plt.savefig('metric_examples/5_metor_results_summary.png', dpi=300, bbox_inches='tight')
plt.close()

print("✅ 5. METOR 결과 종합 비교 이미지 생성 완료")

print("\n" + "="*60)
print("모든 성능 지표 시각화 완료!")
print("="*60)
print("\n저장 위치: docs/paper/metric_examples/")
print("  1. 1_hypervolume_comparison.png")
print("  2. 2_spacing_comparison.png")
print("  3. 3_diversity_comparison.png")
print("  4. 4_convergence_comparison.png")
print("  5. 5_metor_results_summary.png")
