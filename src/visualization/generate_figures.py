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
- Table 1: Performance Summary Table

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

# Set Korean font
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

# Set style
plt.style.use('seaborn-v0_8-paper')
sns.set_palette("husl")

# Load data from optimization_comparison_results.xlsx
def load_data_from_excel():
    """Load experiment results from Excel file"""
    file_path = Path('optimization_comparison_results.xlsx')
    if not file_path.exists():
        raise FileNotFoundError(f"Cannot find {file_path}. Please ensure optimization_comparison_results.xlsx is in the same directory.")
    
    df_raw = pd.read_excel(file_path, sheet_name='Raw Results')
    
    algorithms = ['NSGA-II', 'NSGA-III', 'SPEA2', 'ε-MOEA']
    metrics_data = {
        'HYPERVOLUME': {},
        'SPACING': {},
        'DIVERSITY': {},
        'CONVERGENCE': {},
        'EXECUTION_TIME': {}
    }
    
    # Row ranges for each metric
    row_ranges = {
        'HYPERVOLUME': [1, 2, 3, 4],
        'SPACING': [8, 9, 10, 11],
        'DIVERSITY': [15, 16, 17, 18],
        'CONVERGENCE': [22, 23, 24, 25],
        'EXECUTION_TIME': [29, 30, 31, 32]
    }
    
    for metric, rows in row_ranges.items():
        for idx in rows:
            row = df_raw.iloc[idx]
            algo = str(row['HYPERVOLUME']).strip()
            if algo in algorithms:
                values = []
                for col in df_raw.columns[1:11]:
                    val = row[col]
                    if pd.notna(val):
                        try:
                            values.append(float(val))
                        except:
                            pass
                metrics_data[metric][algo] = values
    
    return algorithms, metrics_data


ALGORITHMS, DATA = load_data_from_excel()


def setup_output_directory():
    """Create output directory for figures"""
    output_dir = Path('results/figures')
    output_dir.mkdir(parents=True, exist_ok=True)
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
    hypervolume = np.array([np.mean(DATA['HYPERVOLUME'][algo]) for algo in ALGORITHMS])
    spacing = np.array([np.mean(DATA['SPACING'][algo]) for algo in ALGORITHMS])
    diversity = np.array([np.mean(DATA['DIVERSITY'][algo]) for algo in ALGORITHMS])
    convergence = np.array([np.mean(DATA['CONVERGENCE'][algo]) for algo in ALGORITHMS])
    time = np.array([np.mean(DATA['EXECUTION_TIME'][algo]) for algo in ALGORITHMS])
    
    # Normalize (0-1 scale)
    def normalize(values, invert=False):
        if invert:
            values = 1.0 / (values + 0.001)  # Avoid division by zero
        normalized = (values - values.min()) / (values.max() - values.min() + 1e-10)
        return normalized
    
    data_matrix = np.array([
        normalize(hypervolume),
        normalize(spacing, invert=True),  # Lower is better
        normalize(diversity),
        normalize(convergence, invert=True),  # Lower is better
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
    Shows distribution and statistical differences
    """
    print("Generating Figure 2: Hypervolume Box Plots...")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Prepare data
    data_list = [DATA['HYPERVOLUME'][algo] for algo in ALGORITHMS]
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
    ax.set_title('Hypervolume Distribution Across 10 Independent Runs', 
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
    Shows algorithm comparison for solution distribution uniformity
    """
    print("Generating Figure 3: Spacing Comparison...")
    
    fig, ax = plt.subplots(figsize=(10, 7))
    
    means = [np.mean(DATA['SPACING'][algo]) for algo in ALGORITHMS]
    stds = [np.std(DATA['SPACING'][algo]) for algo in ALGORITHMS]
    
    x = np.arange(len(ALGORITHMS))
    colors = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12']
    
    bars = ax.bar(x, means, yerr=stds, capsize=5, alpha=0.7, 
                  color=colors, edgecolor='black', linewidth=1.5)
    
    # Add value labels on bars
    for i, (mean, std) in enumerate(zip(means, stds)):
        ax.text(i, mean + std + 0.05, f'{mean:.2f}', 
               ha='center', va='bottom', fontsize=11, weight='bold')
    
    # Formatting
    ax.set_xticks(x)
    ax.set_xticklabels(ALGORITHMS, fontsize=12, weight='bold')
    ax.set_ylabel('Spacing (Lower is Better)', fontsize=12, weight='bold')
    ax.set_title('Solution Distribution Uniformity Comparison', 
                fontsize=13, weight='bold')
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
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
        diversity_runs = DATA['DIVERSITY'][algo]
        convergence_runs = DATA['CONVERGENCE'][algo]
        
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
    
    # Formatting
    ax.set_xlabel('Diversity (Objective Space Extent)', fontsize=12, weight='bold')
    ax.set_ylabel('Convergence (Lower is Better)', fontsize=12, weight='bold')
    ax.set_title('Trade-off Between Exploration and Exploitation\n(95% confidence ellipses)', 
                fontsize=13, weight='bold')
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(fontsize=11, loc='upper left')
    
    plt.tight_layout()
    plt.savefig(output_dir / 'figure4_diversity_convergence.png', dpi=300, bbox_inches='tight')
    plt.savefig(output_dir / 'figure4_diversity_convergence.pdf', bbox_inches='tight')
    plt.close()
    print("✓ Figure 4 saved")


def figure5_execution_time(output_dir):
    """
    Figure 5: Execution Time Comparison
    Shows computational efficiency differences
    """
    print("Generating Figure 5: Execution Time Comparison...")
    
    fig, ax = plt.subplots(figsize=(10, 7))
    
    means = np.array([np.mean(DATA['EXECUTION_TIME'][algo]) for algo in ALGORITHMS])
    stds = np.array([np.std(DATA['EXECUTION_TIME'][algo]) for algo in ALGORITHMS])
    
    x = np.arange(len(ALGORITHMS))
    colors = ['#3498db', '#f39c12', '#2ecc71', '#e74c3c']
    
    bars = ax.barh(x, means, xerr=stds, capsize=5, alpha=0.7,
                   color=colors, edgecolor='black', linewidth=1.5)
    
    # Add value labels
    for i, (mean, std) in enumerate(zip(means, stds)):
        ax.text(mean + std + 10, i, f'{mean:.1f}s', 
               va='center', fontsize=11, weight='bold')
    
    # Add speedup factors
    fastest_idx = np.argmin(means)
    fastest = means[fastest_idx]
    speedups = means / fastest
    for i, speedup in enumerate(speedups):
        if i != fastest_idx:
            ax.text(20, i, f'{speedup:.2f}× slower', 
                   va='center', fontsize=10, style='italic',
                   bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3))
    
    # Formatting
    ax.set_yticks(x)
    ax.set_yticklabels(ALGORITHMS, fontsize=12, weight='bold')
    ax.set_xlabel('Execution Time (seconds)', fontsize=12, weight='bold')
    ax.set_title('Computational Efficiency Comparison\n(Mean ± Std)', 
                fontsize=13, weight='bold')
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.savefig(output_dir / 'figure5_execution_time.png', dpi=300, bbox_inches='tight')
    plt.savefig(output_dir / 'figure5_execution_time.pdf', bbox_inches='tight')
    plt.close()
    print("✓ Figure 5 saved")


def figure6_performance_summary(output_dir):
    """
    Figure 6: Performance Summary Table Visualization (Table 1)
    Shows comprehensive comparison of all metrics
    """
    print("Generating Table 1: Performance Summary...")
    
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.axis('tight')
    ax.axis('off')
    
    # Prepare data
    metrics = ['HYPERVOLUME', 'SPACING', 'DIVERSITY', 'CONVERGENCE', 'EXECUTION_TIME']
    metric_labels = ['Hypervolume', 'Spacing', 'Diversity', 'Convergence', 'Time (sec)']
    
    table_data = []
    table_data.append(['Metric'] + ALGORITHMS)
    
    for metric, label in zip(metrics, metric_labels):
        row = [label]
        for algo in ALGORITHMS:
            mean = np.mean(DATA[metric][algo])
            std = np.std(DATA[metric][algo])
            if metric == 'EXECUTION_TIME':
                row.append(f'{mean:.1f}±{std:.1f}')
            else:
                row.append(f'{mean:.3f}±{std:.3f}')
        table_data.append(row)
    
    # Create table
    table = ax.table(cellText=table_data, cellLoc='center', loc='center',
                     colWidths=[0.2, 0.2, 0.2, 0.2, 0.2])
    
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 2.5)
    
    # Style header row
    for i in range(5):
        cell = table[(0, i)]
        cell.set_facecolor('#3498db')
        cell.set_text_props(weight='bold', color='white')
    
    # Style metric column
    for i in range(1, 6):
        cell = table[(i, 0)]
        cell.set_facecolor('#ecf0f1')
        cell.set_text_props(weight='bold')
    
    # Highlight best values
    colors = ['#2ecc71', '#f39c12', '#e74c3c', '#9b59b6']
    for i, metric in enumerate(metrics, start=1):
        means = [np.mean(DATA[metric][algo]) for algo in ALGORITHMS]
        if metric in ['SPACING', 'CONVERGENCE', 'EXECUTION_TIME']:
            best_idx = np.argmin(means)
        else:
            best_idx = np.argmax(means)
        
        cell = table[(i, best_idx + 1)]
        cell.set_facecolor('#2ecc71')
        cell.set_text_props(weight='bold')
    
    ax.set_title('Table 1: Algorithm Performance Comparison Summary\n(Mean±Std, n=10 runs)', 
                fontsize=14, weight='bold', pad=20)
    
    plt.tight_layout()
    # Save as table1 instead of figure6
    plt.savefig(output_dir / 'table1.png', dpi=300, bbox_inches='tight')
    plt.savefig(output_dir / 'table1.pdf', bbox_inches='tight')
    plt.close()
    print("✓ Table 1 saved")


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
    figure6_performance_summary(output_dir)
    
    print("\n" + "="*60)
    print("ALL FIGURES GENERATED SUCCESSFULLY!")
    print("="*60)
    print(f"\nFiles saved in: {output_dir.absolute()}")
    print("\nGenerated files:")
    for file in sorted(output_dir.glob('figure*.png')) + sorted(output_dir.glob('table*.png')):
        print(f"  - {file.name}")
    print("\nBoth PNG (for Word) and PDF (for LaTeX) versions created.")


if __name__ == "__main__":
    generate_all_figures()
