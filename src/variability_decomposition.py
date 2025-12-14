import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from typing import Dict, List, Tuple
import os
import openpyxl
from statsmodels.formula.api import mixedlm
from pathlib import Path


class VariabilityDecomposition:
    def __init__(self, metrics: List[str] = None, algorithms: List[str] = None):
        self.metrics = metrics or ['hypervolume', 'spacing', 'diversity', 'convergence', 'execution_time']
        self.algorithms = algorithms or ['NSGA-II', 'NSGA-III', 'SPEA2', 'ε-MOEA']
        self.data = None

    def load_all_datasets(self, excel_dir: str) -> pd.DataFrame:
        files = sorted([f for f in os.listdir(excel_dir) if f.endswith('.xlsx')])

        all_data = []

        for dataset_idx, filename in enumerate(files, 1):
            filepath = os.path.join(excel_dir, filename)
            wb = openpyxl.load_workbook(filepath, data_only=True)
            ws = wb['Raw Results']

            # Extract dataset name from filename
            dataset_name = f"Dataset_{dataset_idx}"

            # Parse each metric section
            current_metric = None
            metric_name_map = {
                'HYPERVOLUME': 'hypervolume',
                'SPACING': 'spacing',
                'DIVERSITY': 'diversity',
                'CONVERGENCE': 'convergence',
                'EXECUTION_TIME': 'execution_time'
            }

            for row in ws.iter_rows(values_only=True):
                if row[0] and isinstance(row[0], str):
                    upper_row = row[0].upper()
                    if upper_row in metric_name_map:
                        current_metric = metric_name_map[upper_row]
                        continue

                    if row[0] == 'Algorithm':
                        continue

                    if current_metric and row[0] in self.algorithms:
                        algorithm = row[0]
                        for run_idx, value in enumerate(row[1:11], 1):  # Runs 1-10
                            if value is not None:
                                all_data.append({
                                    'Algorithm': algorithm,
                                    'Dataset': dataset_name,
                                    'Dataset_ID': dataset_idx,
                                    'Run': run_idx,
                                    'Metric': current_metric,
                                    'Value': float(value)
                                })

            wb.close()

        self.data = pd.DataFrame(all_data)
        print(f"Loaded {len(self.data)} data points from {len(files)} datasets")
        return self.data

    def calculate_icc(self, subset: pd.DataFrame) -> float:
        """Calculate ICC for a given subset of data."""
        if len(subset) == 0:
            return 0.0

        # Calculate between-dataset variance
        dataset_means = subset.groupby('Dataset')['Value'].mean()
        between_var = dataset_means.var(ddof=1)

        # Calculate within-dataset variance
        within_vars = []
        for dataset in subset['Dataset'].unique():
            dataset_data = subset[subset['Dataset'] == dataset]['Value']
            if len(dataset_data) > 1:
                within_vars.append(dataset_data.var(ddof=1))

        within_var = np.mean(within_vars) if within_vars else 0.0

        # Total variance
        total_var = subset['Value'].var(ddof=1)

        # ICC
        if total_var > 0:
            icc = between_var / total_var
            icc = max(0.0, min(1.0, icc))
        else:
            icc = 0.0

        return icc

    def bootstrap_icc_ci(self, algorithm: str, metric: str, n_bootstrap: int = 1000,
                        confidence_level: float = 0.95, random_seed: int = 42) -> Tuple[float, float, float]:
        """
        Calculate bootstrap confidence interval for ICC.

        Args:
            algorithm: Algorithm name
            metric: Metric name
            n_bootstrap: Number of bootstrap samples (default: 1000)
            confidence_level: Confidence level (default: 0.95 for 95% CI)
            random_seed: Random seed for reproducibility

        Returns:
            Tuple of (ICC point estimate, lower CI, upper CI)
        """
        # Filter data
        subset = self.data[
            (self.data['Algorithm'] == algorithm) &
            (self.data['Metric'] == metric)
        ].copy()

        if len(subset) == 0:
            return 0.0, 0.0, 0.0

        # Calculate original ICC
        original_icc = self.calculate_icc(subset)

        # Bootstrap resampling
        np.random.seed(random_seed)
        bootstrap_iccs = []

        datasets = subset['Dataset'].unique()
        n_datasets = len(datasets)

        for _ in range(n_bootstrap):
            # Resample datasets with replacement
            bootstrap_datasets = np.random.choice(datasets, size=n_datasets, replace=True)

            # Create bootstrap sample
            bootstrap_sample = []
            for dataset in bootstrap_datasets:
                dataset_data = subset[subset['Dataset'] == dataset].copy()
                bootstrap_sample.append(dataset_data)

            bootstrap_df = pd.concat(bootstrap_sample, ignore_index=True)

            # Calculate ICC for this bootstrap sample
            bootstrap_icc = self.calculate_icc(bootstrap_df)
            bootstrap_iccs.append(bootstrap_icc)

        # Calculate confidence interval
        alpha = 1 - confidence_level
        lower_percentile = (alpha / 2) * 100
        upper_percentile = (1 - alpha / 2) * 100

        ci_lower = np.percentile(bootstrap_iccs, lower_percentile)
        ci_upper = np.percentile(bootstrap_iccs, upper_percentile)

        return original_icc, ci_lower, ci_upper

    def calculate_variance_components(self, algorithm: str, metric: str) -> Dict[str, float]:
        # Filter data
        subset = self.data[
            (self.data['Algorithm'] == algorithm) &
            (self.data['Metric'] == metric)
        ].copy()

        if len(subset) == 0:
            return {
                'total_var': 0.0,
                'total_sd': 0.0,
                'between_dataset_var': 0.0,
                'between_dataset_sd': 0.0,
                'within_dataset_var': 0.0,
                'within_dataset_sd': 0.0,
                'icc': 0.0
            }

        # Calculate between-dataset variance
        dataset_means = subset.groupby('Dataset')['Value'].mean()
        grand_mean = subset['Value'].mean()
        n_runs_per_dataset = subset.groupby('Dataset')['Value'].count().mean()

        # Between-dataset variance (variance of dataset means)
        between_var = dataset_means.var(ddof=1)

        # Within-dataset variance (average variance within each dataset)
        within_vars = []
        for dataset in subset['Dataset'].unique():
            dataset_data = subset[subset['Dataset'] == dataset]['Value']
            if len(dataset_data) > 1:
                within_vars.append(dataset_data.var(ddof=1))

        within_var = np.mean(within_vars) if within_vars else 0.0

        # Total variance
        total_var = subset['Value'].var(ddof=1)

        # Intraclass Correlation Coefficient (ICC)
        if total_var > 0:
            icc = between_var / total_var
            icc = max(0.0, min(1.0, icc))
        else:
            icc = 0.0

        return {
            'total_var': total_var,
            'total_sd': np.sqrt(total_var),
            'between_dataset_var': between_var,
            'between_dataset_sd': np.sqrt(between_var),
            'within_dataset_var': within_var,
            'within_dataset_sd': np.sqrt(within_var),
            'icc': icc
        }

    def variance_decomposition_table(self, metric: str, include_bootstrap: bool = True) -> pd.DataFrame:
        results = []

        for algorithm in self.algorithms:
            components = self.calculate_variance_components(algorithm, metric)

            row = {
                'Algorithm': algorithm,
                'Total SD': f"{components['total_sd']:.4f}",
                'Within-Dataset SD': f"{components['within_dataset_sd']:.4f}",
                'Between-Dataset SD': f"{components['between_dataset_sd']:.4f}",
                'ICC': f"{components['icc']:.3f}"
            }

            # Add bootstrap confidence interval if requested
            if include_bootstrap:
                icc_est, ci_lower, ci_upper = self.bootstrap_icc_ci(algorithm, metric)
                row['ICC 95% CI'] = f"[{ci_lower:.3f}, {ci_upper:.3f}]"

            results.append(row)

        return pd.DataFrame(results)

    def mixed_effects_analysis(self, metric: str) -> Dict:
        # Filter data for this metric
        subset = self.data[self.data['Metric'] == metric].copy()

        # Fit mixed-effects model
        try:
            model = mixedlm(
                "Value ~ Algorithm",
                data=subset,
                groups=subset["Dataset"]
            )
            result = model.fit(reml=True)

            return {
                'summary': result.summary(),
                'fixed_effects': result.fe_params.to_dict(),
                'random_effects_variance': result.cov_re.iloc[0, 0] if hasattr(result, 'cov_re') else 0.0,
                'residual_variance': result.scale,
                'aic': result.aic,
                'bic': result.bic
            }
        except Exception as e:
            print(f"Mixed-effects model failed for {metric}: {e}")
            return None

    def plot_dataset_level_profiles(self, metric: str, save_path: str = None):
        # Filter data
        subset = self.data[self.data['Metric'] == metric].copy()

        # Calculate dataset-level statistics
        dataset_stats = subset.groupby(['Algorithm', 'Dataset_ID']).agg({
            'Value': ['mean', 'std']
        }).reset_index()
        dataset_stats.columns = ['Algorithm', 'Dataset_ID', 'Mean', 'SD']

        # Create plot
        fig, ax = plt.subplots(figsize=(14, 7))

        colors = {'NSGA-II': '#1f77b4', 'NSGA-III': '#ff7f0e',
                  'SPEA2': '#2ca02c', 'ε-MOEA': '#d62728'}
        markers = {'NSGA-II': 'o', 'NSGA-III': 's',
                   'SPEA2': '^', 'ε-MOEA': 'D'}

        for algorithm in self.algorithms:
            alg_data = dataset_stats[dataset_stats['Algorithm'] == algorithm]
            ax.errorbar(
                alg_data['Dataset_ID'],
                alg_data['Mean'],
                yerr=alg_data['SD'],
                label=algorithm,
                marker=markers.get(algorithm, 'o'),
                markersize=8,
                capsize=5,
                capthick=2,
                linewidth=2,
                color=colors.get(algorithm, None),
                alpha=0.8
            )

        ax.set_xlabel('Dataset ID', fontsize=14, fontweight='bold')
        ax.set_ylabel(metric.replace('_', ' ').title(), fontsize=14, fontweight='bold')
        ax.set_title(f'Dataset-Level Performance Profile: {metric.replace("_", " ").title()}',
                     fontsize=16, fontweight='bold', pad=20)
        ax.legend(fontsize=12, loc='best', framealpha=0.9)
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.set_xticks(range(1, 11))

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Saved dataset-level profile to {save_path}")

        return fig

    def plot_icc_comparison(self, metric: str, save_path: str = None):
        """
        Plot ICC values with bootstrap confidence intervals for all algorithms.
        Overlapping confidence intervals suggest no significant difference.
        """
        # Calculate ICC and confidence intervals for all algorithms
        icc_data = []
        for algorithm in self.algorithms:
            icc_est, ci_lower, ci_upper = self.bootstrap_icc_ci(algorithm, metric)
            icc_data.append({
                'Algorithm': algorithm,
                'ICC': icc_est,
                'CI_Lower': ci_lower,
                'CI_Upper': ci_upper,
                'CI_Width': ci_upper - ci_lower
            })

        df = pd.DataFrame(icc_data)

        # Create plot
        fig, ax = plt.subplots(figsize=(10, 7))

        colors = {'NSGA-II': '#1f77b4', 'NSGA-III': '#ff7f0e',
                  'SPEA2': '#2ca02c', 'ε-MOEA': '#d62728'}

        y_positions = np.arange(len(self.algorithms))

        for idx, row in df.iterrows():
            algorithm = row['Algorithm']
            color = colors.get(algorithm, '#333333')

            # Plot confidence interval as error bar
            ax.errorbar(
                row['ICC'],
                idx,
                xerr=[[row['ICC'] - row['CI_Lower']], [row['CI_Upper'] - row['ICC']]],
                fmt='o',
                markersize=12,
                capsize=8,
                capthick=2,
                linewidth=2.5,
                color=color,
                label=algorithm,
                alpha=0.8
            )

            # Add ICC value annotation
            ax.text(
                row['CI_Upper'] + 0.02,
                idx,
                f"{row['ICC']:.3f}\n[{row['CI_Lower']:.3f}, {row['CI_Upper']:.3f}]",
                va='center',
                fontsize=9,
                color=color,
                fontweight='bold'
            )

        ax.set_yticks(y_positions)
        ax.set_yticklabels(self.algorithms, fontsize=12)
        ax.set_xlabel('ICC (Intraclass Correlation Coefficient)', fontsize=14, fontweight='bold')
        ax.set_title(
            f'ICC Comparison with 95% Bootstrap Confidence Intervals\n{metric.replace("_", " ").title()}',
            fontsize=16,
            fontweight='bold',
            pad=20
        )
        ax.set_xlim(-0.05, 1.05)
        ax.grid(True, alpha=0.3, linestyle='--', axis='x')
        ax.axvline(x=0.5, color='gray', linestyle=':', linewidth=1.5, alpha=0.5, label='ICC = 0.5')

        # Add interpretation text
        interpretation = (
            "Interpretation:\n"
            "• Overlapping CIs → No significant difference\n"
            "• Non-overlapping CIs → Significant difference\n"
            "• ICC > 0.5 → Between-dataset variance dominates"
        )
        ax.text(
            0.02, 0.98,
            interpretation,
            transform=ax.transAxes,
            fontsize=9,
            verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3)
        )

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Saved ICC comparison plot to {save_path}")

        return fig

    def plot_variance_components(self, metric: str, save_path: str = None):
        # Calculate variance components for all algorithms
        components_data = []
        for algorithm in self.algorithms:
            components = self.calculate_variance_components(algorithm, metric)
            total_var = components['total_var']

            if total_var > 0:
                between_pct = (components['between_dataset_var'] / total_var) * 100
                within_pct = (components['within_dataset_var'] / total_var) * 100
            else:
                between_pct = 0.0
                within_pct = 0.0

            components_data.append({
                'Algorithm': algorithm,
                'Between-Dataset': between_pct,
                'Within-Dataset': within_pct
            })

        df = pd.DataFrame(components_data)

        # Create stacked bar chart
        fig, ax = plt.subplots(figsize=(10, 7))

        x = np.arange(len(self.algorithms))
        width = 0.6

        p1 = ax.bar(x, df['Between-Dataset'], width,
                    label='Between-Dataset Variance', color='#3498db', alpha=0.8)
        p2 = ax.bar(x, df['Within-Dataset'], width, bottom=df['Between-Dataset'],
                    label='Within-Dataset Variance', color='#e74c3c', alpha=0.8)

        ax.set_ylabel('Variance Component (%)', fontsize=14, fontweight='bold')
        ax.set_xlabel('Algorithm', fontsize=14, fontweight='bold')
        ax.set_title(f'Variance Decomposition: {metric.replace("_", " ").title()}',
                     fontsize=16, fontweight='bold', pad=20)
        ax.set_xticks(x)
        ax.set_xticklabels(self.algorithms, fontsize=12)
        ax.legend(fontsize=12, loc='upper right', framealpha=0.9)
        ax.set_ylim(0, 105)
        ax.grid(True, alpha=0.3, linestyle='--', axis='y')

        # Add percentage labels
        for i, alg in enumerate(self.algorithms):
            between_val = df.loc[i, 'Between-Dataset']
            within_val = df.loc[i, 'Within-Dataset']

            # Between-dataset label
            if between_val > 5:
                ax.text(i, between_val/2, f'{between_val:.1f}%',
                       ha='center', va='center', fontweight='bold', fontsize=11)

            # Within-dataset label
            if within_val > 5:
                ax.text(i, between_val + within_val/2, f'{within_val:.1f}%',
                       ha='center', va='center', fontweight='bold', fontsize=11)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Saved variance components plot to {save_path}")

        return fig

    def generate_comprehensive_report(self, output_dir: str):
        os.makedirs(output_dir, exist_ok=True)

        print("\n" + "="*80)
        print("2-LEVEL VARIABILITY DECOMPOSITION ANALYSIS")
        print("="*80 + "\n")

        # 1. Variance decomposition tables
        print("\n1. VARIANCE DECOMPOSITION TABLES")
        print("-" * 80)

        tables_dir = os.path.join(output_dir, 'tables')
        os.makedirs(tables_dir, exist_ok=True)

        for metric in self.metrics:
            print(f"\n{metric.upper().replace('_', ' ')}")
            table = self.variance_decomposition_table(metric)
            print(table.to_string(index=False))

            # Save to CSV
            table.to_csv(os.path.join(tables_dir, f'variance_decomposition_{metric}.csv'),
                        index=False)

        # 2. Dataset-level performance profiles
        print("\n\n2. GENERATING DATASET-LEVEL PERFORMANCE PROFILES")
        print("-" * 80)

        profiles_dir = os.path.join(output_dir, 'dataset_profiles')
        os.makedirs(profiles_dir, exist_ok=True)

        for metric in self.metrics:
            save_path = os.path.join(profiles_dir, f'dataset_profile_{metric}.png')
            self.plot_dataset_level_profiles(metric, save_path)
            plt.close()

        # 3. ICC comparison plots with bootstrap confidence intervals
        print("\n\n3. GENERATING ICC COMPARISON PLOTS (Bootstrap 95% CI)")
        print("-" * 80)

        icc_dir = os.path.join(output_dir, 'icc_comparison')
        os.makedirs(icc_dir, exist_ok=True)

        for metric in self.metrics:
            save_path = os.path.join(icc_dir, f'icc_comparison_{metric}.png')
            print(f"  Computing bootstrap confidence intervals for {metric}...")
            self.plot_icc_comparison(metric, save_path)
            plt.close()

        # 4. Variance component plots
        print("\n\n4. GENERATING VARIANCE COMPONENT PLOTS")
        print("-" * 80)

        components_dir = os.path.join(output_dir, 'variance_components')
        os.makedirs(components_dir, exist_ok=True)

        for metric in self.metrics:
            save_path = os.path.join(components_dir, f'variance_components_{metric}.png')
            self.plot_variance_components(metric, save_path)
            plt.close()

        # 5. Mixed-effects model analysis
        print("\n\n5. MIXED-EFFECTS MODEL ANALYSIS")
        print("-" * 80)

        mixed_dir = os.path.join(output_dir, 'mixed_effects')
        os.makedirs(mixed_dir, exist_ok=True)

        for metric in self.metrics:
            print(f"\n{metric.upper().replace('_', ' ')}")
            result = self.mixed_effects_analysis(metric)

            if result:
                # Save summary to text file
                with open(os.path.join(mixed_dir, f'mixed_effects_{metric}.txt'), 'w') as f:
                    f.write(str(result['summary']))

                print(f"  AIC: {result['aic']:.2f}")
                print(f"  BIC: {result['bic']:.2f}")
                print(f"  Random Effects Variance: {result['random_effects_variance']:.6f}")
                print(f"  Residual Variance: {result['residual_variance']:.6f}")

        # 6. Summary statistics
        print("\n\n6. SUMMARY STATISTICS")
        print("-" * 80)

        summary_data = []
        for metric in self.metrics:
            for algorithm in self.algorithms:
                components = self.calculate_variance_components(algorithm, metric)
                subset = self.data[
                    (self.data['Algorithm'] == algorithm) &
                    (self.data['Metric'] == metric)
                ]

                # Calculate bootstrap CI for ICC
                icc_est, ci_lower, ci_upper = self.bootstrap_icc_ci(algorithm, metric)

                summary_data.append({
                    'Metric': metric,
                    'Algorithm': algorithm,
                    'Mean': subset['Value'].mean(),
                    'Total_SD': components['total_sd'],
                    'Within_SD': components['within_dataset_sd'],
                    'Between_SD': components['between_dataset_sd'],
                    'ICC': components['icc'],
                    'ICC_CI_Lower': ci_lower,
                    'ICC_CI_Upper': ci_upper
                })

        summary_df = pd.DataFrame(summary_data)
        summary_df.to_csv(os.path.join(output_dir, 'summary_statistics.csv'), index=False)

        print("\nSummary statistics saved to summary_statistics.csv")

        print("\n" + "="*80)
        print("ANALYSIS COMPLETE")
        print(f"All outputs saved to: {output_dir}")
        print("="*80 + "\n")


def main():
    """Main execution function."""
    # Configuration
    excel_dir = '/home/user/Diet_optimization/result/optimization results'
    output_dir = '/home/user/Diet_optimization/result/variability_analysis'

    # Initialize analyzer
    analyzer = VariabilityDecomposition()

    # Load all datasets
    print("Loading datasets...")
    analyzer.load_all_datasets(excel_dir)

    # Generate comprehensive report
    analyzer.generate_comprehensive_report(output_dir)


if __name__ == '__main__':
    main()
