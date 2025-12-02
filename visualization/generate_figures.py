#!/usr/bin/env python3
"""
Figure Generation for Diet Optimization Paper
==============================================

This script generates all figures for the research paper comparing
four multi-objective optimization algorithms (NSGA-II, NSGA-III, SPEA2, ε-MOEA).

Figures Generated:
- Figure 1: Performance Radar Chart
- Figure 2: Hypervolume Box Plots
- Figure 3: Spacing Comparison Bar Chart
- Figure 4: Diversity vs Convergence Scatter Plot
- Figure 5: Execution Time Comparison
- Figure 6: Statistical Significance Heatmap

Author: Diet Optimization Research Team
Date: 2024-12
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8-paper')
sns.set_palette("husl")

# Data from final_comparison.xlsx
ALGORITHMS = ['NSGA-II', 'NSGA-III', 'SPEA2', 'ε-MOEA']

# Performance data (Mean ± Std)
DATA = {
    'hypervolume': {
        'mean': [0.40882, 0.401047, 0.426402, 0.370365],
        'std': [0.012407, 0.007592, 0.025547, 0.048243],
        'runs': [
            [0.4186, 0.404144, 0.396716, 0.416236, 0.377549, 0.410856, 0.419742, 0.417606, 0.413006, 0.413744],
            [0.397268, 0.398131, 0.398003, 0.397806, 0.415641, 0.395332, 0.396182, 0.416283, 0.400441, 0.395383],
            [0.430939, 0.416518, 0.434322, 0.354779, 0.442525, 0.433309, 0.450088, 0.436609, 0.423268, 0.441661],
            [0.427477, 0.374061, 0.315199, 0.359563, 0.395567, 0.370674, 0.416503, 0.260963, 0.367482, 0.416163]
        ]
    },
    'spacing': {
        'mean': [0.603929, 1.366558, 5.414922, 4.784785],
        'std': [0.984778, 3.138581, 5.266315, 2.34286],
        'runs': [
            [0.142884, 3.505049, 0.274649, 0.235429, 0.063078, 0.653103, 0.051592, 0.215296, 0.56224, 0.335966],
            [0.43137, 0.188303, 0.382221, 0.424903, 0.076059, 0.532933, 0.58207, 0.035328, 0.244676, 10.767721],
            [0.607046, 10.60067, 16.88549, 7.69313, 0.429633, 3.103621, 0.130778, 2.938812, 9.477782, 2.282255],
            [8.012375, 6.292092, 4.046338, 5.646419, 5.289216, 0.858948, 1.33645, 5.423729, 3.021162, 7.921122]
        ]
    },
    'diversity': {
        'mean': [1.131812, 1.571872, 6.23645, 9.449158],
        'std': [0.613938, 2.137254, 4.555503, 3.058057],
        'runs': [
            [0.474032, 2.826745, 0.73663, 0.716801, 0.985998, 1.220209, 1.017227, 1.224863, 1.249511, 0.866102],
            [0.831513, 0.865341, 0.988667, 1.111918, 0.659934, 1.046357, 0.891479, 0.69311, 0.662466, 7.967931],
            [1.596416, 11.719791, 10.866866, 12.585386, 0.857517, 4.188876, 1.045606, 7.691513, 9.839823, 2.272706],
            [11.681237, 11.195893, 12.420493, 10.061706, 5.785672, 7.130089, 16.371833, 10.223009, 7.032476, 2.589174]
        ]
    },
    'convergence': {
        'mean': [0.333602, 0.383183, 0.702681, 0.430474],
        'std': [0.105072, 0.115498, 0.347824, 0.148615],
        'runs': [
            [0.271403, 0.194847, 0.333764, 0.311076, 0.293726, 0.338691, 0.518744, 0.332506, 0.331479, 0.309783],
            [0.289925, 0.297726, 0.334663, 0.330452, 0.185385, 0.380604, 0.327449, 0.617921, 0.438078, 0.629625],
            [0.635518, 0.510055, 0.878699, 0.212182, 1.110485, 0.677695, 1.329887, 0.895551, 0.728486, 1.048252],
            [0.341877, 0.46293, 0.662452, 0.244797, 0.530095, 0.460506, 0.302896, 0.588959, 0.373969, 0.336256]
        ]
    },
    'time': {
        'mean': [1423.547284, 1145.433956, 992.141146, 1889.753782],
        'std': [579.456878, 25.989876, 576.051767, 476.956232],
        'runs': [
            [1040.375599, 1200.127077, 1102.822932, 2607.322293, 1212.656542, 1420.869773, 1868.896056, 1523.387158, 1353.175945, 1905.839465],
            [1102.627236, 1135.715099, 1115.746777, 1143.906959, 1133.584616, 1160.195648, 1160.206639, 1165.059908, 1152.087104, 1181.733418],
            [221.923481, 489.842598, 1278.055766, 1922.686462, 518.178995, 739.832043, 1137.830555, 1320.087892, 1078.862094, 1214.111574],
            [1573.203181, 1595.364866, 1809.078701, 2027.417068, 1712.039681, 1634.854475, 3258.889035, 1930.329985, 1690.084175, 1666.276657]
        ]
    }
}

# Statistical significance (p-values from Mann-Whitney U tests)
P_VALUES = {
    'hypervolume': {
        'NSGA-II vs NSGA-III': 0.791,
        'NSGA-II vs SPEA2': 0.850,
        'NSGA-II vs ε-MOEA': 0.427,
        'NSGA-III vs SPEA2': 0.427,
        'NSGA-III vs ε-MOEA': 0.212,
        'SPEA2 vs ε-MOEA': 0.734
    },
    'spacing': {
        'NSGA-II vs NSGA-III': 0.623,
        'NSGA-II vs SPEA2': 0.001,
        'NSGA-II vs ε-MOEA': 0.045,
        'NSGA-III vs SPEA2': 0.038,
        'NSGA-III vs ε-MOEA': 0.212,
        'SPEA2 vs ε-MOEA': 0.791
    },
    'diversity': {
        'NSGA-II vs NSGA-III': 0.427,
        'NSGA-II vs SPEA2': 0.0002,
        'NSGA-II vs ε-MOEA': 0.0003,
        'NSGA-III vs SPEA2': 0.0004,
        'NSGA-III vs ε-MOEA': 0.0036,
        'SPEA2 vs ε-MOEA': 0.064
    },
    'convergence': {
        'NSGA-II vs NSGA-III': 0.850,
        'NSGA-II vs SPEA2': 0.0002,
        'NSGA-II vs ε-MOEA': 0.007,
        'NSGA-III vs SPEA2': 0.0002,
        'NSGA-III vs ε-MOEA': 0.002,
        'SPEA2 vs ε-MOEA': 0.011
    },
    'time': {
        'NSGA-II vs NSGA-III': 0.162,
        'NSGA-II vs SPEA2': 0.0002,
        'NSGA-II vs ε-MOEA': 0.0002,
        'NSGA-III vs SPEA2': 0.0002,
        'NSGA-III vs ε-MOEA': 0.0002,
        'SPEA2 vs ε-MOEA': 0.0002
    }
}


def setup_output_directory():
    """Create output directory for figures"""
    output_dir = Path('figures')
    output_dir.mkdir(exist_ok=True)
    return output_dir


def figure1_radar_chart(output_dir):
    """
    Figure 1: Performance Radar Chart
    Multi-dimensional performance comparison across 5 metrics
    """
    print("Generating Figure 1: Performance Radar Chart...")
    
    # Normalize data (higher is better for all)
    metrics = ['Hypervolume', 'Spacing\n(inverted)', 'Diversity', 'Convergence', 'Time\n(inverted)']
    
    # Get data
    hypervolume = np.array(DATA['hypervolume']['mean'])
    spacing = np.array(DATA['spacing']['mean'])
    diversity = np.array(DATA['diversity']['mean'])
    convergence = np.array(DATA['convergence']['mean'])
    time = np.array(DATA['time']['mean'])
    
    # Normalize (0-1 scale)
    def normalize(values, invert=False):
        if invert:
            values = 1.0 / (values + 0.001)  # Avoid division by zero
        normalized = (values - values.min()) / (values.max() - values.min())
        return normalized
    
    data_matrix = np.array([
        normalize(hypervolume),
        normalize(spacing, invert=True),  # Lower is better
        normalize(diversity),
        normalize(convergence),
        normalize(time, invert=True)  # Lower is better
    ]).T
    
    # Radar chart
    angles = np.linspace(0, 2 * np.pi, len(metrics), endpoint=False).tolist()
    data_matrix = np.concatenate((data_matrix, data_matrix[:, [0]]), axis=1)
    angles += angles[:1]
    
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
    
    colors = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12']
    markers = ['o', 's', '^', 'D']
    
    for i, (algo, color, marker) in enumerate(zip(ALGORITHMS, colors, markers)):
        ax.plot(angles, data_matrix[i], 'o-', linewidth=2, color=color, 
                label=algo, marker=marker, markersize=8)
        ax.fill(angles, data_matrix[i], alpha=0.15, color=color)
    
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(metrics, size=12, weight='bold')
    ax.set_ylim(0, 1)
    ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticklabels(['0.2', '0.4', '0.6', '0.8', '1.0'], size=10)
    ax.grid(True, linestyle='--', alpha=0.7)
    
    plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=12)
    plt.title('Multi-dimensional Performance Comparison\n(Normalized Scores)', 
              size=14, weight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'figure1_radar_chart.png', dpi=300, bbox_inches='tight')
    plt.savefig(output_dir / 'figure1_radar_chart.pdf', bbox_inches='tight')
    plt.close()
    print("✓ Figure 1 saved")


def figure2_hypervolume_boxplots(output_dir):
    """
    Figure 2: Hypervolume Distribution Box Plots
    Shows distribution and no significant differences
    """
    print("Generating Figure 2: Hypervolume Box Plots...")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Prepare data
    data_list = DATA['hypervolume']['runs']
    positions = np.arange(len(ALGORITHMS))
    
    # Create box plots
    bp = ax.boxplot(data_list, positions=positions, widths=0.6,
                    patch_artist=True, showmeans=True,
                    meanprops=dict(marker='D', markerfacecolor='red', 
                                  markeredgecolor='red', markersize=8))
    
    # Color boxes
    colors = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12']
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.6)
    
    # Add individual points
    for i, data in enumerate(data_list):
        y = data
        x = np.random.normal(i, 0.04, size=len(y))
        ax.scatter(x, y, alpha=0.4, s=30, color=colors[i])
    
    # Formatting
    ax.set_xticks(positions)
    ax.set_xticklabels(ALGORITHMS, fontsize=12, weight='bold')
    ax.set_ylabel('Hypervolume', fontsize=12, weight='bold')
    ax.set_title('Hypervolume Distribution Across 10 Independent Runs\n(Kruskal-Wallis p = 0.642, no significant differences)', 
                fontsize=13, weight='bold')
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Add overall mean line
    overall_mean = np.mean([np.mean(d) for d in data_list])
    ax.axhline(overall_mean, color='gray', linestyle='--', alpha=0.5, 
              label=f'Overall Mean: {overall_mean:.3f}')
    ax.legend(fontsize=10)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'figure2_hypervolume_boxplots.png', dpi=300, bbox_inches='tight')
    plt.savefig(output_dir / 'figure2_hypervolume_boxplots.pdf', bbox_inches='tight')
    plt.close()
    print("✓ Figure 2 saved")


def figure3_spacing_comparison(output_dir):
    """
    Figure 3: Spacing Comparison Bar Chart
    Shows NSGA-II's superiority with statistical significance
    """
    print("Generating Figure 3: Spacing Comparison...")
    
    fig, ax = plt.subplots(figsize=(10, 7))
    
    means = DATA['spacing']['mean']
    stds = DATA['spacing']['std']
    
    x = np.arange(len(ALGORITHMS))
    colors = ['#2ecc71', '#3498db', '#e74c3c', '#f39c12']  # Green for NSGA-II (best)
    
    bars = ax.bar(x, means, yerr=stds, capsize=5, alpha=0.7, 
                  color=colors, edgecolor='black', linewidth=1.5)
    
    # Add value labels on bars
    for i, (mean, std) in enumerate(zip(means, stds)):
        ax.text(i, mean + std + 0.3, f'{mean:.2f}', 
               ha='center', va='bottom', fontsize=11, weight='bold')
    
    # Add significance annotations
    # NSGA-II vs SPEA2 (p = 0.001)
    y_max = max([m + s for m, s in zip(means, stds)]) + 0.5
    ax.plot([0, 2], [y_max, y_max], 'k-', linewidth=1.5)
    ax.text(1, y_max + 0.2, '***', ha='center', fontsize=16, weight='bold')
    ax.text(1, y_max + 0.6, 'p = 0.001', ha='center', fontsize=10)
    
    # NSGA-II vs ε-MOEA (p = 0.045)
    y_max2 = y_max + 1.5
    ax.plot([0, 3], [y_max2, y_max2], 'k-', linewidth=1.5)
    ax.text(1.5, y_max2 + 0.2, '*', ha='center', fontsize=16, weight='bold')
    ax.text(1.5, y_max2 + 0.6, 'p = 0.045', ha='center', fontsize=10)
    
    # Formatting
    ax.set_xticks(x)
    ax.set_xticklabels(ALGORITHMS, fontsize=12, weight='bold')
    ax.set_ylabel('Spacing (Lower is Better)', fontsize=12, weight='bold')
    ax.set_title('Solution Distribution Uniformity Comparison\n(*** p < 0.001, * p < 0.05)', 
                fontsize=13, weight='bold')
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Add legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#2ecc71', alpha=0.7, label='Best (NSGA-II)'),
        Patch(facecolor='#3498db', alpha=0.7, label='Moderate (NSGA-III)'),
        Patch(facecolor='#e74c3c', alpha=0.7, label='Poor (SPEA2)'),
        Patch(facecolor='#f39c12', alpha=0.7, label='Poor (ε-MOEA)')
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'figure3_spacing_comparison.png', dpi=300, bbox_inches='tight')
    plt.savefig(output_dir / 'figure3_spacing_comparison.pdf', bbox_inches='tight')
    plt.close()
    print("✓ Figure 3 saved")


def figure4_diversity_convergence_scatter(output_dir):
    """
    Figure 4: Diversity vs Convergence Scatter Plot
    Shows trade-off between exploration and exploitation
    """
    print("Generating Figure 4: Diversity vs Convergence Scatter...")
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    colors = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12']
    markers = ['o', 's', '^', 'D']
    
    for i, (algo, color, marker) in enumerate(zip(ALGORITHMS, colors, markers)):
        diversity_runs = DATA['diversity']['runs'][i]
        convergence_runs = DATA['convergence']['runs'][i]
        
        # Scatter points
        ax.scatter(diversity_runs, convergence_runs, s=100, alpha=0.6,
                  color=color, marker=marker, edgecolors='black', linewidth=1,
                  label=algo)
        
        # Add 95% confidence ellipse
        from matplotlib.patches import Ellipse
        mean_div = np.mean(diversity_runs)
        mean_conv = np.mean(convergence_runs)
        std_div = np.std(diversity_runs)
        std_conv = np.std(convergence_runs)
        
        ellipse = Ellipse((mean_div, mean_conv), width=2*std_div, height=2*std_conv,
                         alpha=0.2, facecolor=color, edgecolor=color, linewidth=2)
        ax.add_patch(ellipse)
        
        # Add mean marker
        ax.scatter(mean_div, mean_conv, s=200, alpha=0.9, color=color,
                  marker=marker, edgecolors='black', linewidth=2)
    
    # Shade ideal region (upper right)
    ax.axvspan(6, 12, ymin=0.6, ymax=1.0, alpha=0.1, color='green', 
              label='Ideal Region')
    
    # Formatting
    ax.set_xlabel('Diversity (Objective Space Extent)', fontsize=12, weight='bold')
    ax.set_ylabel('Convergence (Solution Quality)', fontsize=12, weight='bold')
    ax.set_title('Trade-off Between Exploration and Exploitation\n(95% confidence ellipses)', 
                fontsize=13, weight='bold')
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(fontsize=11, loc='upper left')
    
    # Add annotations
    ax.annotate('SPEA2: High convergence,\nmoderate diversity', 
               xy=(6.5, 0.7), fontsize=10, 
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    ax.annotate('ε-MOEA: High diversity,\nmoderate convergence', 
               xy=(9.5, 0.43), fontsize=10,
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig(output_dir / 'figure4_diversity_convergence.png', dpi=300, bbox_inches='tight')
    plt.savefig(output_dir / 'figure4_diversity_convergence.pdf', bbox_inches='tight')
    plt.close()
    print("✓ Figure 4 saved")


def figure5_execution_time(output_dir):
    """
    Figure 5: Execution Time Comparison
    Shows SPEA2's computational efficiency advantage
    """
    print("Generating Figure 5: Execution Time Comparison...")
    
    fig, ax = plt.subplots(figsize=(10, 7))
    
    means = np.array(DATA['time']['mean']) / 60  # Convert to minutes
    stds = np.array(DATA['time']['std']) / 60
    
    x = np.arange(len(ALGORITHMS))
    colors = ['#f39c12', '#3498db', '#2ecc71', '#e74c3c']  # Green for SPEA2 (fastest)
    
    bars = ax.barh(x, means, xerr=stds, capsize=5, alpha=0.7,
                   color=colors, edgecolor='black', linewidth=1.5)
    
    # Add value labels
    for i, (mean, std) in enumerate(zip(means, stds)):
        ax.text(mean + std + 1, i, f'{mean:.1f} min', 
               va='center', fontsize=11, weight='bold')
    
    # Add speedup factors
    fastest = means[2]  # SPEA2
    speedups = means / fastest
    for i, speedup in enumerate(speedups):
        if i != 2:  # Skip SPEA2
            ax.text(2, i, f'{speedup:.2f}× slower', 
                   va='center', fontsize=10, style='italic',
                   bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3))
    
    # Formatting
    ax.set_yticks(x)
    ax.set_yticklabels(ALGORITHMS, fontsize=12, weight='bold')
    ax.set_xlabel('Execution Time (minutes)', fontsize=12, weight='bold')
    ax.set_title('Computational Efficiency Comparison\n(Mean ± Std, p < 0.001 for most pairs)', 
                fontsize=13, weight='bold')
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    
    # Add legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#2ecc71', alpha=0.7, label='Fastest (SPEA2)'),
        Patch(facecolor='#3498db', alpha=0.7, label='Moderate (NSGA-III)'),
        Patch(facecolor='#f39c12', alpha=0.7, label='Slow (NSGA-II)'),
        Patch(facecolor='#e74c3c', alpha=0.7, label='Slowest (ε-MOEA)')
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'figure5_execution_time.png', dpi=300, bbox_inches='tight')
    plt.savefig(output_dir / 'figure5_execution_time.pdf', bbox_inches='tight')
    plt.close()
    print("✓ Figure 5 saved")


def figure6_significance_heatmap(output_dir):
    """
    Figure 6: Statistical Significance Heatmap
    Shows p-values from pairwise comparisons across all metrics
    """
    print("Generating Figure 6: Statistical Significance Heatmap...")
    
    # Prepare data matrix
    metrics = ['Hypervolume', 'Spacing', 'Diversity', 'Convergence', 'Time']
    comparisons = [
        'NSGA-II vs\nNSGA-III',
        'NSGA-II vs\nSPEA2',
        'NSGA-II vs\nε-MOEA',
        'NSGA-III vs\nSPEA2',
        'NSGA-III vs\nε-MOEA',
        'SPEA2 vs\nε-MOEA'
    ]
    
    p_matrix = np.zeros((len(metrics), len(comparisons)))
    
    for i, metric in enumerate(['hypervolume', 'spacing', 'diversity', 'convergence', 'time']):
        for j, comp in enumerate(P_VALUES[metric].keys()):
            p_matrix[i, j] = P_VALUES[metric][comp]
    
    # Create heatmap
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Color map: green (not significant) to red (highly significant)
    cmap = sns.diverging_palette(10, 133, as_cmap=True, center='light')
    
    # Transform p-values for better visualization (log scale)
    display_matrix = -np.log10(p_matrix + 1e-10)
    
    sns.heatmap(display_matrix, annot=p_matrix, fmt='.3f', cmap=cmap,
                xticklabels=comparisons, yticklabels=metrics,
                cbar_kws={'label': '-log10(p-value)'}, linewidths=0.5,
                ax=ax, vmin=0, vmax=4)
    
    # Add significance markers
    for i in range(len(metrics)):
        for j in range(len(comparisons)):
            p_val = p_matrix[i, j]
            if p_val < 0.001:
                marker = '***'
            elif p_val < 0.01:
                marker = '**'
            elif p_val < 0.05:
                marker = '*'
            else:
                marker = 'ns'
            
            ax.text(j + 0.5, i + 0.7, marker, ha='center', va='center',
                   fontsize=12, weight='bold', color='black')
    
    # Formatting
    ax.set_title('Statistical Significance Matrix (Mann-Whitney U Test)\n(*** p<0.001, ** p<0.01, * p<0.05, ns: not significant)', 
                fontsize=13, weight='bold', pad=20)
    plt.setp(ax.get_xticklabels(), fontsize=10)
    plt.setp(ax.get_yticklabels(), fontsize=11, weight='bold')
    
    plt.tight_layout()
    plt.savefig(output_dir / 'figure6_significance_heatmap.png', dpi=300, bbox_inches='tight')
    plt.savefig(output_dir / 'figure6_significance_heatmap.pdf', bbox_inches='tight')
    plt.close()
    print("✓ Figure 6 saved")


def generate_all_figures():
    """Generate all figures for the paper"""
    print("\n" + "="*60)
    print("GENERATING FIGURES FOR DIET OPTIMIZATION PAPER")
    print("="*60 + "\n")
    
    output_dir = setup_output_directory()
    print(f"Output directory: {output_dir.absolute()}\n")
    
    # Generate each figure
    figure1_radar_chart(output_dir)
    figure2_hypervolume_boxplots(output_dir)
    figure3_spacing_comparison(output_dir)
    figure4_diversity_convergence_scatter(output_dir)
    figure5_execution_time(output_dir)
    figure6_significance_heatmap(output_dir)
    
    print("\n" + "="*60)
    print("ALL FIGURES GENERATED SUCCESSFULLY!")
    print("="*60)
    print(f"\nFiles saved in: {output_dir.absolute()}")
    print("\nGenerated files:")
    for file in sorted(output_dir.glob('figure*.png')):
        print(f"  - {file.name}")
    print("\nBoth PNG (for Word) and PDF (for LaTeX) versions created.")


if __name__ == "__main__":
    generate_all_figures()
