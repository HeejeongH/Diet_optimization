"""
Additional Visualizations for Variability Decomposition Analysis

Creates supplementary figures for paper and presentations:
1. ICC comparison across all metrics (radar chart)
2. Combined performance summary (multi-panel figure)
3. Algorithm performance heatmap
4. Box plot distributions
5. Correlation matrix between metrics

Author: Claude
Date: 2025-12-13
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import os


class AdditionalVisualizations:
    """Create supplementary visualizations for the paper."""

    def __init__(self, data_path: str):
        """Initialize with path to summary statistics."""
        self.df = pd.read_csv(data_path)
        self.algorithms = ['NSGA-II', 'NSGA-III', 'SPEA2', 'ε-MOEA']
        self.metrics = ['hypervolume', 'spacing', 'diversity', 'convergence', 'execution_time']

    def plot_icc_comparison(self, save_path: str = None):
        """
        Create radar chart comparing ICC across all metrics for all algorithms.
        Shows at a glance which algorithms are robust for which metrics.
        """
        # Prepare data
        icc_data = {}
        for algorithm in self.algorithms:
            icc_values = []
            for metric in self.metrics:
                icc = self.df[
                    (self.df['Algorithm'] == algorithm) &
                    (self.df['Metric'] == metric)
                ]['ICC'].values[0]
                icc_values.append(icc)
            icc_data[algorithm] = icc_values

        # Create radar chart
        angles = np.linspace(0, 2 * np.pi, len(self.metrics), endpoint=False).tolist()
        angles += angles[:1]  # Complete the circle

        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))

        colors = {'NSGA-II': '#1f77b4', 'NSGA-III': '#ff7f0e',
                  'SPEA2': '#2ca02c', 'ε-MOEA': '#d62728'}

        for algorithm in self.algorithms:
            values = icc_data[algorithm]
            values += values[:1]  # Complete the circle
            ax.plot(angles, values, 'o-', linewidth=2, label=algorithm,
                   color=colors[algorithm], markersize=8)
            ax.fill(angles, values, alpha=0.15, color=colors[algorithm])

        # Customize plot
        metric_labels = [m.replace('_', ' ').title() for m in self.metrics]
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(metric_labels, size=12, fontweight='bold')
        ax.set_ylim(0, 1)
        ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
        ax.set_yticklabels(['0.2', '0.4', '0.6', '0.8', '1.0'], size=10)
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.set_title('ICC Comparison Across All Metrics\n(Higher = More Robust)',
                     size=16, fontweight='bold', pad=30)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=12)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Saved ICC comparison to {save_path}")

        return fig

    def plot_combined_performance_summary(self, save_path: str = None):
        """
        Create 2x3 panel figure showing key metrics comparison.
        Perfect for paper as a comprehensive overview.
        """
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('Comprehensive Performance Comparison', fontsize=20, fontweight='bold', y=0.995)

        colors = {'NSGA-II': '#1f77b4', 'NSGA-III': '#ff7f0e',
                  'SPEA2': '#2ca02c', 'ε-MOEA': '#d62728'}

        # Panel 1: Mean Performance (Hypervolume)
        ax = axes[0, 0]
        hv_data = self.df[self.df['Metric'] == 'hypervolume']
        x_pos = np.arange(len(self.algorithms))
        means = [hv_data[hv_data['Algorithm'] == alg]['Mean'].values[0] for alg in self.algorithms]
        stds = [hv_data[hv_data['Algorithm'] == alg]['Total_SD'].values[0] for alg in self.algorithms]
        bars = ax.bar(x_pos, means, yerr=stds, capsize=10, alpha=0.7,
                     color=[colors[alg] for alg in self.algorithms], edgecolor='black', linewidth=1.5)
        ax.set_xticks(x_pos)
        ax.set_xticklabels(self.algorithms, fontsize=11, fontweight='bold')
        ax.set_ylabel('Hypervolume', fontsize=13, fontweight='bold')
        ax.set_title('(A) Optimization Quality', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
        # Add value labels
        for i, (m, s) in enumerate(zip(means, stds)):
            ax.text(i, m + s + 0.005, f'{m:.3f}', ha='center', va='bottom', fontweight='bold', fontsize=10)

        # Panel 2: Execution Time
        ax = axes[0, 1]
        et_data = self.df[self.df['Metric'] == 'execution_time']
        means = [et_data[et_data['Algorithm'] == alg]['Mean'].values[0] for alg in self.algorithms]
        stds = [et_data[et_data['Algorithm'] == alg]['Total_SD'].values[0] for alg in self.algorithms]
        bars = ax.bar(x_pos, means, yerr=stds, capsize=10, alpha=0.7,
                     color=[colors[alg] for alg in self.algorithms], edgecolor='black', linewidth=1.5)
        ax.set_xticks(x_pos)
        ax.set_xticklabels(self.algorithms, fontsize=11, fontweight='bold')
        ax.set_ylabel('Time (seconds)', fontsize=13, fontweight='bold')
        ax.set_title('(B) Computational Efficiency', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
        ax.set_ylim(0, 450)
        # Add value labels
        for i, (m, s) in enumerate(zip(means, stds)):
            ax.text(i, m + s + 10, f'{m:.1f}s', ha='center', va='bottom', fontweight='bold', fontsize=10)

        # Panel 3: ICC for Hypervolume
        ax = axes[0, 2]
        hv_data = self.df[self.df['Metric'] == 'hypervolume']
        iccs = [hv_data[hv_data['Algorithm'] == alg]['ICC'].values[0] for alg in self.algorithms]
        bars = ax.bar(x_pos, iccs, alpha=0.7,
                     color=[colors[alg] for alg in self.algorithms], edgecolor='black', linewidth=1.5)
        ax.set_xticks(x_pos)
        ax.set_xticklabels(self.algorithms, fontsize=11, fontweight='bold')
        ax.set_ylabel('ICC', fontsize=13, fontweight='bold')
        ax.set_title('(C) Robustness (Hypervolume ICC)', fontsize=14, fontweight='bold')
        ax.set_ylim(0, 1.0)
        ax.axhline(y=0.5, color='red', linestyle='--', linewidth=2, alpha=0.7, label='ICC = 0.5')
        ax.grid(True, alpha=0.3, axis='y')
        ax.legend(fontsize=10)
        # Add value labels
        for i, icc in enumerate(iccs):
            ax.text(i, icc + 0.03, f'{icc:.2f}', ha='center', va='bottom', fontweight='bold', fontsize=10)

        # Panel 4: Within-Dataset SD (Robustness)
        ax = axes[1, 0]
        metrics_to_compare = ['hypervolume', 'convergence', 'execution_time']
        metric_labels = ['Hypervolume', 'Convergence', 'Exec Time']
        x = np.arange(len(metrics_to_compare))
        width = 0.2
        for i, algorithm in enumerate(self.algorithms):
            within_sds = []
            for metric in metrics_to_compare:
                within_sd = self.df[
                    (self.df['Algorithm'] == algorithm) &
                    (self.df['Metric'] == metric)
                ]['Within_SD'].values[0]
                # Normalize execution time for visualization
                if metric == 'execution_time':
                    within_sd = within_sd / 100  # Scale down
                within_sds.append(within_sd)
            ax.bar(x + i * width, within_sds, width, label=algorithm,
                  color=colors[algorithm], alpha=0.7, edgecolor='black', linewidth=1)
        ax.set_xlabel('Metric', fontsize=13, fontweight='bold')
        ax.set_ylabel('Within-Dataset SD', fontsize=13, fontweight='bold')
        ax.set_title('(D) Initialization Sensitivity', fontsize=14, fontweight='bold')
        ax.set_xticks(x + width * 1.5)
        ax.set_xticklabels(metric_labels, fontsize=11, fontweight='bold')
        ax.legend(fontsize=10, loc='upper left')
        ax.grid(True, alpha=0.3, axis='y')
        ax.text(0.5, 0.95, 'Exec Time scaled ÷100', transform=ax.transAxes,
               fontsize=9, style='italic', ha='center', va='top',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

        # Panel 5: Convergence Quality
        ax = axes[1, 1]
        conv_data = self.df[self.df['Metric'] == 'convergence']
        means = [conv_data[conv_data['Algorithm'] == alg]['Mean'].values[0] for alg in self.algorithms]
        stds = [conv_data[conv_data['Algorithm'] == alg]['Total_SD'].values[0] for alg in self.algorithms]
        bars = ax.bar(x_pos, means, yerr=stds, capsize=10, alpha=0.7,
                     color=[colors[alg] for alg in self.algorithms], edgecolor='black', linewidth=1.5)
        ax.set_xticks(x_pos)
        ax.set_xticklabels(self.algorithms, fontsize=11, fontweight='bold')
        ax.set_ylabel('Convergence', fontsize=13, fontweight='bold')
        ax.set_title('(E) Solution Improvement', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
        # Add value labels
        for i, (m, s) in enumerate(zip(means, stds)):
            ax.text(i, m + s + 0.05, f'{m:.2f}', ha='center', va='bottom', fontweight='bold', fontsize=10)

        # Panel 6: ICC Heatmap
        ax = axes[1, 2]
        icc_matrix = []
        for metric in self.metrics:
            row = []
            for algorithm in self.algorithms:
                icc = self.df[
                    (self.df['Algorithm'] == algorithm) &
                    (self.df['Metric'] == metric)
                ]['ICC'].values[0]
                row.append(icc)
            icc_matrix.append(row)

        sns.heatmap(icc_matrix, annot=True, fmt='.2f', cmap='RdYlGn', vmin=0, vmax=1,
                   xticklabels=self.algorithms, yticklabels=[m.replace('_', ' ').title() for m in self.metrics],
                   cbar_kws={'label': 'ICC'}, ax=ax, linewidths=1, linecolor='black')
        ax.set_title('(F) ICC Heatmap (All Metrics)', fontsize=14, fontweight='bold')
        ax.set_xlabel('Algorithm', fontsize=13, fontweight='bold')
        ax.set_ylabel('Metric', fontsize=13, fontweight='bold')

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Saved combined performance summary to {save_path}")

        return fig

    def plot_algorithm_ranking_heatmap(self, save_path: str = None):
        """
        Create heatmap showing algorithm rankings (1-4) for each metric.
        Useful for quick comparison.
        """
        fig, ax = plt.subplots(figsize=(12, 8))

        # Define what "better" means for each metric
        better_higher = ['hypervolume', 'diversity', 'convergence']
        better_lower = ['spacing', 'execution_time']

        ranking_matrix = []
        for metric in self.metrics:
            metric_data = self.df[self.df['Metric'] == metric].copy()

            if metric in better_higher:
                metric_data['Rank'] = metric_data['Mean'].rank(ascending=False)
            else:
                metric_data['Rank'] = metric_data['Mean'].rank(ascending=True)

            ranks = []
            for algorithm in self.algorithms:
                rank = metric_data[metric_data['Algorithm'] == algorithm]['Rank'].values[0]
                ranks.append(int(rank))
            ranking_matrix.append(ranks)

        # Create heatmap (reverse colormap so rank 1 is best/green)
        sns.heatmap(ranking_matrix, annot=True, fmt='d', cmap='RdYlGn_r', vmin=1, vmax=4,
                   xticklabels=self.algorithms,
                   yticklabels=[m.replace('_', ' ').title() for m in self.metrics],
                   cbar_kws={'label': 'Rank (1 = Best)', 'ticks': [1, 2, 3, 4]},
                   ax=ax, linewidths=2, linecolor='black', annot_kws={'fontsize': 14, 'fontweight': 'bold'})

        ax.set_title('Algorithm Performance Rankings by Metric\n(1 = Best, 4 = Worst)',
                    fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Algorithm', fontsize=14, fontweight='bold')
        ax.set_ylabel('Metric', fontsize=14, fontweight='bold')

        # Add legend explaining ranking criteria
        legend_text = ('Rankings based on:\n'
                      '• Hypervolume, Diversity, Convergence: Higher is better\n'
                      '• Spacing, Execution Time: Lower is better')
        ax.text(1.15, 0.5, legend_text, transform=ax.transAxes,
               fontsize=11, verticalalignment='center',
               bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Saved ranking heatmap to {save_path}")

        return fig

    def plot_metric_correlation_matrix(self, excel_dir: str, save_path: str = None):
        """
        Create correlation matrix showing relationships between metrics.
        Helps understand if metrics are redundant or complementary.
        """
        # Load full dataset to calculate correlations
        from variability_decomposition import VariabilityDecomposition

        analyzer = VariabilityDecomposition()
        full_data = analyzer.load_all_datasets(excel_dir)

        fig, axes = plt.subplots(1, 4, figsize=(20, 5))
        fig.suptitle('Metric Correlations by Algorithm', fontsize=18, fontweight='bold')

        for idx, algorithm in enumerate(self.algorithms):
            ax = axes[idx]

            # Filter data for this algorithm
            alg_data = full_data[full_data['Algorithm'] == algorithm].pivot_table(
                index=['Dataset', 'Run'], columns='Metric', values='Value'
            )

            # Calculate correlation
            corr = alg_data.corr()

            # Plot heatmap
            sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', center=0,
                       vmin=-1, vmax=1, square=True, ax=ax,
                       cbar_kws={'label': 'Correlation'}, linewidths=1, linecolor='black')

            ax.set_title(f'{algorithm}', fontsize=14, fontweight='bold')
            ax.set_xlabel('')
            ax.set_ylabel('')

            # Rotate labels
            metric_labels = [m.replace('_', '\n').title() for m in self.metrics]
            ax.set_xticklabels(metric_labels, rotation=45, ha='right', fontsize=10)
            ax.set_yticklabels(metric_labels, rotation=0, fontsize=10)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Saved correlation matrix to {save_path}")

        return fig

    def plot_box_plot_comparison(self, excel_dir: str, save_path: str = None):
        """
        Create box plots showing distribution of key metrics.
        Shows median, quartiles, and outliers.
        """
        from variability_decomposition import VariabilityDecomposition

        analyzer = VariabilityDecomposition()
        full_data = analyzer.load_all_datasets(excel_dir)

        # Select key metrics for visualization
        key_metrics = ['hypervolume', 'execution_time', 'convergence']

        fig, axes = plt.subplots(1, 3, figsize=(18, 6))
        fig.suptitle('Distribution Comparison (Box Plots)', fontsize=18, fontweight='bold')

        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']

        for idx, metric in enumerate(key_metrics):
            ax = axes[idx]

            metric_data = full_data[full_data['Metric'] == metric]

            # Create box plot
            bp = ax.boxplot(
                [metric_data[metric_data['Algorithm'] == alg]['Value'].values
                 for alg in self.algorithms],
                labels=self.algorithms,
                patch_artist=True,
                widths=0.6,
                showmeans=True,
                meanprops=dict(marker='D', markerfacecolor='red', markeredgecolor='black', markersize=8)
            )

            # Color boxes
            for patch, color in zip(bp['boxes'], colors):
                patch.set_facecolor(color)
                patch.set_alpha(0.7)
                patch.set_linewidth(1.5)

            ax.set_ylabel(metric.replace('_', ' ').title(), fontsize=13, fontweight='bold')
            ax.set_xlabel('Algorithm', fontsize=13, fontweight='bold')
            ax.set_title(f'({chr(65+idx)}) {metric.replace("_", " ").title()}',
                        fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3, axis='y')

            # Rotate x labels if needed
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=15, ha='right')

        # Add legend
        legend_elements = [
            plt.Line2D([0], [0], color='black', linewidth=1.5, label='Median'),
            plt.Line2D([0], [0], marker='D', color='w', markerfacecolor='red',
                      markeredgecolor='black', markersize=8, label='Mean')
        ]
        fig.legend(handles=legend_elements, loc='upper right', fontsize=12,
                  bbox_to_anchor=(0.98, 0.98))

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Saved box plot comparison to {save_path}")

        return fig


def main():
    """Generate all additional visualizations."""
    # Paths
    summary_path = '/home/user/Diet_optimization/result/variability_analysis/summary_statistics.csv'
    excel_dir = '/home/user/Diet_optimization/result/optimization results'
    output_dir = '/home/user/Diet_optimization/result/variability_analysis/additional_figures'

    os.makedirs(output_dir, exist_ok=True)

    # Initialize visualizer
    viz = AdditionalVisualizations(summary_path)

    print("\n" + "="*80)
    print("GENERATING ADDITIONAL VISUALIZATIONS")
    print("="*80 + "\n")

    # 1. ICC Comparison Radar Chart
    print("1. Creating ICC comparison radar chart...")
    viz.plot_icc_comparison(os.path.join(output_dir, 'icc_radar_comparison.png'))
    plt.close()

    # 2. Combined Performance Summary
    print("\n2. Creating combined performance summary (6-panel figure)...")
    viz.plot_combined_performance_summary(os.path.join(output_dir, 'combined_performance_summary.png'))
    plt.close()

    # 3. Algorithm Ranking Heatmap
    print("\n3. Creating algorithm ranking heatmap...")
    viz.plot_algorithm_ranking_heatmap(os.path.join(output_dir, 'algorithm_ranking_heatmap.png'))
    plt.close()

    # 4. Metric Correlation Matrix
    print("\n4. Creating metric correlation matrices...")
    viz.plot_metric_correlation_matrix(excel_dir, os.path.join(output_dir, 'metric_correlations.png'))
    plt.close()

    # 5. Box Plot Comparison
    print("\n5. Creating box plot distributions...")
    viz.plot_box_plot_comparison(excel_dir, os.path.join(output_dir, 'box_plot_comparison.png'))
    plt.close()

    print("\n" + "="*80)
    print("ADDITIONAL VISUALIZATIONS COMPLETE")
    print(f"All figures saved to: {output_dir}")
    print("="*80 + "\n")

    print("Generated figures:")
    print("  1. icc_radar_comparison.png - ICC comparison across all metrics")
    print("  2. combined_performance_summary.png - 6-panel comprehensive overview")
    print("  3. algorithm_ranking_heatmap.png - Performance rankings by metric")
    print("  4. metric_correlations.png - Correlation matrices by algorithm")
    print("  5. box_plot_comparison.png - Distribution box plots")


if __name__ == '__main__':
    main()
