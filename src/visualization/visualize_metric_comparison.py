import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle, FancyBboxPatch
import seaborn as sns
from pathlib import Path

# Create output directory
output_dir = Path('results/figures/metric_examples')
output_dir.mkdir(parents=True, exist_ok=True)

# Set style
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.unicode_minus'] = False

# Create a comprehensive comparison figure
fig = plt.figure(figsize=(18, 12))
gs = fig.add_gridspec(3, 3, hspace=0.4, wspace=0.3)

# ========== 1. HYPERVOLUME COMPARISON ==========
ax1 = fig.add_subplot(gs[0, :2])

# Create two solution sets
np.random.seed(42)
good_solutions = np.random.rand(20, 2) * 0.5 + 0.4  # High quality, well distributed
bad_solutions = np.random.rand(10, 2) * 0.3 + 0.2   # Lower quality, sparse

# Reference point
ref_point = [0, 0]

# Plot
ax1.scatter(good_solutions[:, 0], good_solutions[:, 1], 
           s=100, c='#2ecc71', alpha=0.7, edgecolors='black', linewidth=2,
           label='Algorithm A (Good)', zorder=3)
ax1.scatter(bad_solutions[:, 0], bad_solutions[:, 1], 
           s=100, c='#e74c3c', alpha=0.7, edgecolors='black', linewidth=2,
           label='Algorithm B (Poor)', zorder=3)

# Draw hypervolume regions
for sol in good_solutions[:5]:  # Show a few examples
    width = sol[0] - ref_point[0]
    height = sol[1] - ref_point[1]
    rect = Rectangle(ref_point, width, height, 
                    linewidth=1, edgecolor='#2ecc71', 
                    facecolor='#2ecc71', alpha=0.1)
    ax1.add_patch(rect)

ax1.scatter([0], [0], s=200, c='red', marker='x', linewidth=3, 
           label='Reference Point', zorder=4)
ax1.set_xlabel('Objective 1 (Nutrition) →', fontsize=13, fontweight='bold')
ax1.set_ylabel('Objective 2 (Cost) →', fontsize=13, fontweight='bold')
ax1.set_title('1. Hypervolume: 해 집합이 지배하는 공간의 부피\n(Algorithm A > Algorithm B)', 
             fontsize=14, fontweight='bold', pad=15)
ax1.legend(loc='upper left', fontsize=11, framealpha=0.9)
ax1.grid(True, alpha=0.3, linestyle='--')
ax1.set_xlim(-0.1, 1.0)
ax1.set_ylim(-0.1, 1.0)

# Add annotations
ax1.annotate('넓은 영역 커버\n(Higher Hypervolume)', 
            xy=(0.6, 0.7), fontsize=12, color='#27ae60',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#d5f4e6', alpha=0.8),
            ha='center', fontweight='bold')
ax1.annotate('좁은 영역 커버\n(Lower Hypervolume)', 
            xy=(0.3, 0.3), fontsize=12, color='#c0392b',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#fadbd8', alpha=0.8),
            ha='center', fontweight='bold')

# ========== 2. SPACING COMPARISON ==========
ax2 = fig.add_subplot(gs[0, 2])

# Create uniform and non-uniform distributions
uniform_x = np.linspace(0.2, 0.9, 8)
uniform_y = np.linspace(0.2, 0.9, 8)

non_uniform_x = np.array([0.2, 0.25, 0.28, 0.55, 0.60, 0.85, 0.88, 0.90])
non_uniform_y = np.array([0.2, 0.25, 0.28, 0.55, 0.60, 0.85, 0.88, 0.90])

# Plot uniform
ax2.plot(uniform_x, uniform_y, 'o-', color='#2ecc71', 
        markersize=10, linewidth=2, label='Uniform (Low Spacing)', alpha=0.8)
ax2.plot(non_uniform_x, non_uniform_y, 's-', color='#e74c3c', 
        markersize=10, linewidth=2, label='Non-uniform (High Spacing)', alpha=0.8)

ax2.set_xlabel('Objective 1 →', fontsize=11, fontweight='bold')
ax2.set_ylabel('Objective 2 →', fontsize=11, fontweight='bold')
ax2.set_title('2. Spacing: 해들 간격의 균일성\n(Lower = More Uniform)', 
             fontsize=12, fontweight='bold', pad=10)
ax2.legend(loc='upper left', fontsize=9, framealpha=0.9)
ax2.grid(True, alpha=0.3, linestyle='--')

# Add distance annotations
ax2.annotate('', xy=(uniform_x[1], uniform_y[1]), xytext=(uniform_x[0], uniform_y[0]),
            arrowprops=dict(arrowstyle='<->', color='#27ae60', lw=2))
ax2.text(0.22, 0.35, 'Equal\nGaps', fontsize=9, color='#27ae60', fontweight='bold')

ax2.annotate('', xy=(non_uniform_x[2], non_uniform_y[2]), xytext=(non_uniform_x[1], non_uniform_y[1]),
            arrowprops=dict(arrowstyle='<->', color='#c0392b', lw=2))
ax2.text(0.26, 0.40, 'Small', fontsize=8, color='#c0392b', fontweight='bold')

ax2.annotate('', xy=(non_uniform_x[4], non_uniform_y[4]), xytext=(non_uniform_x[3], non_uniform_y[3]),
            arrowprops=dict(arrowstyle='<->', color='#c0392b', lw=2))
ax2.text(0.50, 0.70, 'Large\nGap', fontsize=8, color='#c0392b', fontweight='bold')

# ========== 3. DIVERSITY COMPARISON ==========
ax3 = fig.add_subplot(gs[1, 0])

# High diversity
high_div_x = np.random.uniform(0.1, 0.95, 15)
high_div_y = np.random.uniform(0.1, 0.95, 15)

# Low diversity
low_div_x = np.random.uniform(0.4, 0.7, 15)
low_div_y = np.random.uniform(0.4, 0.7, 15)

ax3.scatter(high_div_x, high_div_y, s=100, c='#3498db', 
           alpha=0.7, edgecolors='black', linewidth=1.5,
           label='High Diversity', zorder=3)
ax3.scatter(low_div_x, low_div_y, s=100, c='#95a5a6', 
           alpha=0.7, edgecolors='black', linewidth=1.5,
           label='Low Diversity', zorder=3)

# Draw extent rectangles
high_extent = Rectangle((min(high_div_x), min(high_div_y)), 
                        max(high_div_x) - min(high_div_x), 
                        max(high_div_y) - min(high_div_y),
                        linewidth=3, edgecolor='#2980b9', 
                        facecolor='none', linestyle='--', label='High Range')
low_extent = Rectangle((min(low_div_x), min(low_div_y)), 
                       max(low_div_x) - min(low_div_x), 
                       max(low_div_y) - min(low_div_y),
                       linewidth=3, edgecolor='#7f8c8d', 
                       facecolor='none', linestyle='--', label='Low Range')
ax3.add_patch(high_extent)
ax3.add_patch(low_extent)

ax3.set_xlabel('Objective 1 →', fontsize=11, fontweight='bold')
ax3.set_ylabel('Objective 2 →', fontsize=11, fontweight='bold')
ax3.set_title('3. Diversity: 목적함수 공간에서의 탐색 범위\n(Higher = Wider Range)', 
             fontsize=12, fontweight='bold', pad=10)
ax3.legend(loc='upper left', fontsize=9, framealpha=0.9)
ax3.grid(True, alpha=0.3, linestyle='--')
ax3.set_xlim(0, 1)
ax3.set_ylim(0, 1)

# ========== 4. CONVERGENCE COMPARISON ==========
ax4 = fig.add_subplot(gs[1, 1])

# True Pareto front
true_front_x = np.linspace(0.2, 0.9, 20)
true_front_y = 1.0 - true_front_x**0.5

# Good convergence
good_conv_x = true_front_x + np.random.normal(0, 0.02, 20)
good_conv_y = true_front_y + np.random.normal(0, 0.02, 20)

# Poor convergence
poor_conv_x = true_front_x + np.random.normal(0, 0.08, 20)
poor_conv_y = true_front_y + np.random.normal(-0.15, 0.08, 20)

ax4.plot(true_front_x, true_front_y, 'k-', linewidth=3, 
        label='True Pareto Front', zorder=4)
ax4.scatter(good_conv_x, good_conv_y, s=100, c='#2ecc71', 
           alpha=0.7, edgecolors='black', linewidth=1.5,
           label='Good Convergence', zorder=3)
ax4.scatter(poor_conv_x, poor_conv_y, s=100, c='#e74c3c', 
           alpha=0.7, edgecolors='black', linewidth=1.5,
           label='Poor Convergence', zorder=3)

# Draw distance arrows
for i in [5, 10, 15]:
    ax4.annotate('', xy=(true_front_x[i], true_front_y[i]), 
                xytext=(poor_conv_x[i], poor_conv_y[i]),
                arrowprops=dict(arrowstyle='->', color='#c0392b', 
                              lw=2, linestyle='--'))

ax4.set_xlabel('Objective 1 →', fontsize=11, fontweight='bold')
ax4.set_ylabel('Objective 2 →', fontsize=11, fontweight='bold')
ax4.set_title('4. Convergence: 진짜 최적해까지의 거리\n(Lower = Closer to Optimum)', 
             fontsize=12, fontweight='bold', pad=10)
ax4.legend(loc='upper right', fontsize=9, framealpha=0.9)
ax4.grid(True, alpha=0.3, linestyle='--')

ax4.text(0.5, 0.15, 'Large Distance\n(Poor)', fontsize=10, 
        color='#c0392b', ha='center', fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#fadbd8', alpha=0.8))

# ========== 5. EXECUTION TIME COMPARISON ==========
ax5 = fig.add_subplot(gs[1, 2])

algorithms = ['SPEA2', 'NSGA-II', 'NSGA-III', 'ε-MOEA']
times = [17.4, 82.1, 261.3, 667.1]
colors = ['#2ecc71', '#f39c12', '#e67e22', '#e74c3c']

bars = ax5.bar(algorithms, times, color=colors, edgecolor='black', linewidth=2, alpha=0.8)

# Add value labels
for i, (bar, time) in enumerate(zip(bars, times)):
    height = bar.get_height()
    ax5.text(bar.get_x() + bar.get_width()/2., height,
            f'{time:.1f}s\n{"✅" if time < 100 else "⚠️" if time < 400 else "❌"}',
            ha='center', va='bottom', fontsize=11, fontweight='bold')

ax5.set_ylabel('Execution Time (seconds)', fontsize=11, fontweight='bold')
ax5.set_title('5. Execution Time: 실행 시간\n(Lower = Faster)', 
             fontsize=12, fontweight='bold', pad=10)
ax5.grid(True, axis='y', alpha=0.3, linestyle='--')
ax5.set_ylim(0, 750)

# Add horizontal lines for reference
ax5.axhline(y=100, color='#27ae60', linestyle='--', linewidth=2, alpha=0.5, label='Real-time (< 100s)')
ax5.axhline(y=300, color='#e67e22', linestyle='--', linewidth=2, alpha=0.5, label='Acceptable (< 300s)')
ax5.legend(loc='upper left', fontsize=9, framealpha=0.9)

# ========== 6. METOR RESULTS COMPARISON ==========
ax6 = fig.add_subplot(gs[2, :])

# Data from METOR results
metrics = ['Hypervolume\n(Higher Better)', 'Spacing\n(Lower Better)', 
           'Diversity\n(Context-Dependent)', 'Convergence\n(Lower Better)', 
           'Exec Time (s)\n(Lower Better)']

spea2_scores = [0.384, 0.436, 1.153, 0.295, 17.4]
nsgaii_scores = [0.382, 0.530, 0.994, 0.221, 82.1]
nsgaiii_scores = [0.381, 0.388, 1.005, 0.232, 261.3]
emoea_scores = [0.357, 1.026, 1.841, 0.334, 667.1]

# Normalize for visualization (0-1 scale, considering direction)
def normalize_metric(values, lower_is_better=False):
    min_val, max_val = min(values), max(values)
    if max_val == min_val:
        return [0.5] * len(values)
    normalized = [(v - min_val) / (max_val - min_val) for v in values]
    if lower_is_better:
        normalized = [1 - n for n in normalized]
    return normalized

# Normalize each metric
all_scores = [spea2_scores, nsgaii_scores, nsgaiii_scores, emoea_scores]
normalized_scores = []

for i in range(len(metrics)):
    metric_values = [scores[i] for scores in all_scores]
    lower_is_better = i in [1, 3, 4]  # Spacing, Convergence, Time
    normalized = normalize_metric(metric_values, lower_is_better)
    normalized_scores.append(normalized)

# Transpose for plotting
plot_data = list(zip(*normalized_scores))

x = np.arange(len(metrics))
width = 0.2

colors_bar = ['#2ecc71', '#f39c12', '#3498db', '#e74c3c']
labels = ['SPEA2 🏆', 'NSGA-II 🎯', 'NSGA-III 📐', 'ε-MOEA ⚠️']

for i, (data, color, label) in enumerate(zip(plot_data, colors_bar, labels)):
    offset = width * (i - 1.5)
    bars = ax6.bar(x + offset, data, width, label=label, 
                   color=color, edgecolor='black', linewidth=1.5, alpha=0.8)

ax6.set_ylabel('Normalized Performance\n(1.0 = Best)', fontsize=12, fontweight='bold')
ax6.set_xlabel('Performance Metrics', fontsize=12, fontweight='bold')
ax6.set_title('6. METOR 프로젝트 종합 성능 비교 (정규화된 점수)', 
             fontsize=14, fontweight='bold', pad=15)
ax6.set_xticks(x)
ax6.set_xticklabels(metrics, fontsize=10, fontweight='bold')
ax6.legend(loc='upper left', ncol=4, fontsize=11, framealpha=0.9)
ax6.grid(True, axis='y', alpha=0.3, linestyle='--')
ax6.set_ylim(0, 1.2)
ax6.axhline(y=1.0, color='green', linestyle='--', linewidth=2, alpha=0.5)
ax6.axhline(y=0.5, color='orange', linestyle='--', linewidth=1, alpha=0.3)

# Add summary text box
summary_text = """
📊 METOR 프로젝트 핵심 결과 요약:

✅ SPEA2: 최고 품질 + 최고 속도 → 실용적 응용에 최적
✅ NSGA-II: 최고 수렴 속도 → 빠르게 최적해 도달
✅ NSGA-III: 최고 균일성 → 다양한 옵션 제공
⚠️ ε-MOEA: 100세대로 부족 → 더 많은 세대 필요
"""

fig.text(0.5, 0.02, summary_text, ha='center', fontsize=11, 
        bbox=dict(boxstyle='round,pad=1', facecolor='#ecf0f1', alpha=0.9),
        family='monospace', verticalalignment='bottom')

plt.suptitle('📊 다목적 최적화 성능 지표 비교 시각화 (METOR 프로젝트)', 
            fontsize=16, fontweight='bold', y=0.995)

# Save
plt.savefig('results/figures/metric_examples/comprehensive_metrics_comparison.png', 
           dpi=300, bbox_inches='tight')
plt.savefig('results/figures/metric_examples/comprehensive_metrics_comparison.pdf', 
           bbox_inches='tight')
print("✅ Generated: comprehensive_metrics_comparison.png/pdf")
plt.close()

# ========== CREATE INDIVIDUAL METRIC EXAMPLES ==========

# Individual 1: Hypervolume Detail
fig, ax = plt.subplots(1, 1, figsize=(10, 8))

np.random.seed(42)
solutions = np.random.rand(15, 2) * 0.7 + 0.2

ax.scatter(solutions[:, 0], solutions[:, 1], 
          s=150, c='#2ecc71', alpha=0.8, edgecolors='black', linewidth=2, zorder=3)

ref_point = [0, 0]
for i, sol in enumerate(solutions[:8]):
    width = sol[0] - ref_point[0]
    height = sol[1] - ref_point[1]
    rect = Rectangle(ref_point, width, height, 
                    linewidth=1.5, edgecolor='#27ae60', 
                    facecolor='#2ecc71', alpha=0.15)
    ax.add_patch(rect)
    
    # Add arrow from reference to solution
    if i in [2, 5]:
        ax.annotate('', xy=sol, xytext=ref_point,
                   arrowprops=dict(arrowstyle='->', color='#e74c3c', lw=2.5, linestyle='--'))

ax.scatter([0], [0], s=250, c='red', marker='X', linewidth=3, 
          label='Reference Point', zorder=4)

ax.set_xlabel('Objective 1: Nutritional Adequacy →', fontsize=14, fontweight='bold')
ax.set_ylabel('Objective 2: Cost Effectiveness →', fontsize=14, fontweight='bold')
ax.set_title('Hypervolume: 해 집합이 지배하는 4차원 공간의 부피\n' + 
            '(각 해가 기준점으로부터 만드는 초직육면체의 합집합)',
            fontsize=15, fontweight='bold', pad=20)
ax.legend(loc='upper left', fontsize=12, framealpha=0.9)
ax.grid(True, alpha=0.3, linestyle='--')
ax.set_xlim(-0.15, 1.0)
ax.set_ylim(-0.15, 1.0)

# Add formula
formula_text = r'$HV = \sum_{i=1}^{|S|} volume(\{x_i, ref\})$'
ax.text(0.5, -0.08, formula_text, fontsize=14, ha='center',
       bbox=dict(boxstyle='round,pad=0.7', facecolor='yellow', alpha=0.7))

# Add explanation box
explanation = """
✅ Higher Hypervolume = Better
   • More solutions
   • Better quality solutions  
   • Wider coverage of objective space
   
⚠️ Combines convergence + diversity
"""
ax.text(0.98, 0.02, explanation, fontsize=11, ha='right', va='bottom',
       transform=ax.transAxes, family='monospace',
       bbox=dict(boxstyle='round,pad=0.8', facecolor='#d5f4e6', alpha=0.9))

plt.tight_layout()
plt.savefig('results/figures/metric_examples/hypervolume_detailed.png', dpi=300, bbox_inches='tight')
plt.savefig('results/figures/metric_examples/hypervolume_detailed.pdf', bbox_inches='tight')
print("✅ Generated: hypervolume_detailed.png/pdf")
plt.close()

print("\n✅ All metric comparison visualizations generated successfully!")
print("📁 Location: results/figures/metric_examples/")
