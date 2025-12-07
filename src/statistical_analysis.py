#!/usr/bin/env python3
"""
Statistical Significance Analysis for Diet Optimization Paper
==============================================================

This script performs comprehensive statistical analysis on the experiment results:
1. Kruskal-Wallis H-test (non-parametric ANOVA)
2. Mann-Whitney U test (pairwise comparisons)
3. Effect size calculation (Cliff's Delta)
4. Normality tests (Shapiro-Wilk)
5. Visualization of statistical significance

Author: Diet Optimization Research Team
Date: 2024-12
"""

import numpy as np
import pandas as pd
from scipy import stats
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Set Korean font
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

def load_data_from_excel():
    """Load experiment results from Excel file"""
    file_path = Path('optimization_comparison_results.xlsx')
    if not file_path.exists():
        raise FileNotFoundError(f"Cannot find {file_path}")
    
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


def shapiro_wilk_test(data_dict, alpha=0.05):
    """
    Perform Shapiro-Wilk normality test
    H0: Data follows normal distribution
    """
    print("\n" + "="*80)
    print("1. NORMALITY TEST (Shapiro-Wilk)")
    print("="*80)
    print("\nH0: Data follows normal distribution (p > 0.05)")
    print("H1: Data does NOT follow normal distribution (p ≤ 0.05)\n")
    
    results = {}
    for metric, algo_data in data_dict.items():
        print(f"\n{metric}:")
        print(f"{'Algorithm':<15} {'W-statistic':<15} {'p-value':<15} {'Normal?':<15}")
        print("-"*80)
        
        results[metric] = {}
        for algo, values in algo_data.items():
            stat, p_value = stats.shapiro(values)
            is_normal = "Yes" if p_value > alpha else "No"
            results[metric][algo] = {'statistic': stat, 'p_value': p_value, 'normal': is_normal}
            print(f"{algo:<15} {stat:<15.6f} {p_value:<15.6f} {is_normal:<15}")
    
    # Overall conclusion
    print("\n" + "="*80)
    print("CONCLUSION:")
    all_normal = all(
        result['normal'] == 'Yes' 
        for metric_results in results.values() 
        for result in metric_results.values()
    )
    
    if all_normal:
        print("✓ All data follow normal distribution → Use parametric tests (ANOVA)")
    else:
        print("✗ Some data do NOT follow normal distribution → Use non-parametric tests (Kruskal-Wallis)")
    
    return results


def kruskal_wallis_test(data_dict, alpha=0.05):
    """
    Perform Kruskal-Wallis H-test (non-parametric ANOVA)
    H0: All groups have the same distribution
    """
    print("\n" + "="*80)
    print("2. KRUSKAL-WALLIS H-TEST (Non-parametric ANOVA)")
    print("="*80)
    print("\nH0: All algorithms have the same performance (p > 0.05)")
    print("H1: At least one algorithm differs (p ≤ 0.05)\n")
    
    results = {}
    print(f"{'Metric':<20} {'H-statistic':<15} {'p-value':<15} {'Significant?':<15}")
    print("-"*80)
    
    for metric, algo_data in data_dict.items():
        # Prepare data for Kruskal-Wallis test
        samples = [values for values in algo_data.values()]
        
        # Perform test
        h_stat, p_value = stats.kruskal(*samples)
        is_significant = "Yes ***" if p_value < 0.001 else "Yes **" if p_value < 0.01 else "Yes *" if p_value < alpha else "No"
        
        results[metric] = {'h_statistic': h_stat, 'p_value': p_value, 'significant': p_value < alpha}
        print(f"{metric:<20} {h_stat:<15.6f} {p_value:<15.6f} {is_significant:<15}")
    
    print("\n*** p<0.001, ** p<0.01, * p<0.05")
    
    return results


def cliffs_delta(x, y):
    """
    Calculate Cliff's Delta effect size
    
    Returns:
    - delta: effect size (-1 to 1)
    - interpretation: small/medium/large/negligible
    
    Interpretation (Romano et al., 2006):
    - |d| < 0.147: negligible
    - 0.147 ≤ |d| < 0.33: small
    - 0.33 ≤ |d| < 0.474: medium
    - |d| ≥ 0.474: large
    """
    n1, n2 = len(x), len(y)
    
    # Count dominance
    dominance = 0
    for xi in x:
        for yi in y:
            if xi > yi:
                dominance += 1
            elif xi < yi:
                dominance -= 1
    
    delta = dominance / (n1 * n2)
    
    # Interpretation
    abs_delta = abs(delta)
    if abs_delta < 0.147:
        interpretation = "negligible"
    elif abs_delta < 0.33:
        interpretation = "small"
    elif abs_delta < 0.474:
        interpretation = "medium"
    else:
        interpretation = "large"
    
    return delta, interpretation


def mann_whitney_pairwise(data_dict, alpha=0.05):
    """
    Perform Mann-Whitney U test for all pairwise comparisons
    H0: Two groups have the same distribution
    """
    print("\n" + "="*80)
    print("3. MANN-WHITNEY U TEST (Pairwise Comparisons)")
    print("="*80)
    print("\nH0: Two algorithms have the same performance (p > 0.05)")
    print("H1: Two algorithms differ (p ≤ 0.05)\n")
    
    algorithms = list(next(iter(data_dict.values())).keys())
    comparisons = []
    for i in range(len(algorithms)):
        for j in range(i+1, len(algorithms)):
            comparisons.append((algorithms[i], algorithms[j]))
    
    results = {}
    for metric, algo_data in data_dict.items():
        print(f"\n{'='*80}")
        print(f"METRIC: {metric}")
        print(f"{'='*80}")
        print(f"{'Comparison':<30} {'U-statistic':<15} {'p-value':<15} {'Effect Size':<20} {'Significant?':<15}")
        print("-"*100)
        
        results[metric] = {}
        for algo1, algo2 in comparisons:
            data1 = algo_data[algo1]
            data2 = algo_data[algo2]
            
            # Mann-Whitney U test
            u_stat, p_value = stats.mannwhitneyu(data1, data2, alternative='two-sided')
            
            # Effect size (Cliff's Delta)
            delta, interpretation = cliffs_delta(data1, data2)
            
            # Significance
            if p_value < 0.001:
                sig = "Yes ***"
            elif p_value < 0.01:
                sig = "Yes **"
            elif p_value < alpha:
                sig = "Yes *"
            else:
                sig = "No"
            
            comparison_name = f"{algo1} vs {algo2}"
            results[metric][comparison_name] = {
                'u_statistic': u_stat,
                'p_value': p_value,
                'effect_size': delta,
                'interpretation': interpretation,
                'significant': p_value < alpha
            }
            
            print(f"{comparison_name:<30} {u_stat:<15.2f} {p_value:<15.6f} {delta:>6.3f} ({interpretation:<12}) {sig:<15}")
        
        print()
    
    print("*** p<0.001, ** p<0.01, * p<0.05")
    print("\nEffect Size (Cliff's Delta): |d|<0.147 (negligible), 0.147≤|d|<0.33 (small), 0.33≤|d|<0.474 (medium), |d|≥0.474 (large)")
    
    return results


def bonferroni_correction(results, n_comparisons):
    """
    Apply Bonferroni correction for multiple comparisons
    Adjusted alpha = alpha / n_comparisons
    """
    print("\n" + "="*80)
    print("4. BONFERRONI CORRECTION (Multiple Comparison Adjustment)")
    print("="*80)
    
    original_alpha = 0.05
    adjusted_alpha = original_alpha / n_comparisons
    
    print(f"\nOriginal alpha: {original_alpha}")
    print(f"Number of comparisons: {n_comparisons}")
    print(f"Adjusted alpha (Bonferroni): {adjusted_alpha:.6f}")
    print("\nAfter Bonferroni correction:\n")
    
    corrected_results = {}
    for metric, comparisons in results.items():
        print(f"{metric}:")
        corrected_results[metric] = {}
        
        for comparison, stats_dict in comparisons.items():
            p_value = stats_dict['p_value']
            still_significant = p_value < adjusted_alpha
            
            if still_significant:
                sig_marker = "***" if p_value < 0.001 else "**" if p_value < 0.01 else "*"
                print(f"  {comparison}: p={p_value:.6f} → Still significant {sig_marker}")
            else:
                print(f"  {comparison}: p={p_value:.6f} → NOT significant (after correction)")
            
            corrected_results[metric][comparison] = {
                **stats_dict,
                'significant_after_correction': still_significant
            }
        
        print()
    
    return corrected_results


def create_significance_heatmap(pairwise_results, output_dir):
    """
    Create heatmap showing p-values for all pairwise comparisons
    """
    print("\nGenerating significance heatmap...")
    
    algorithms = ['NSGA-II', 'NSGA-III', 'SPEA2', 'ε-MOEA']
    metrics = ['HYPERVOLUME', 'SPACING', 'DIVERSITY', 'CONVERGENCE', 'EXECUTION_TIME']
    metric_labels = ['Hypervolume', 'Spacing', 'Diversity', 'Convergence', 'Time']
    
    # Create figure with subplots for each metric
    fig, axes = plt.subplots(1, 5, figsize=(20, 4))
    
    for idx, (metric, label) in enumerate(zip(metrics, metric_labels)):
        ax = axes[idx]
        
        # Create p-value matrix
        n_algo = len(algorithms)
        p_matrix = np.ones((n_algo, n_algo))
        
        for comparison, stats_dict in pairwise_results[metric].items():
            algo1, algo2 = comparison.split(' vs ')
            i = algorithms.index(algo1)
            j = algorithms.index(algo2)
            p_value = stats_dict['p_value']
            p_matrix[i, j] = p_value
            p_matrix[j, i] = p_value
        
        # Create heatmap
        im = ax.imshow(-np.log10(p_matrix + 1e-10), cmap='RdYlGn_r', vmin=0, vmax=3)
        
        # Add text annotations
        for i in range(n_algo):
            for j in range(n_algo):
                if i == j:
                    text = '-'
                    color = 'black'
                else:
                    p = p_matrix[i, j]
                    if p < 0.001:
                        text = '***'
                        color = 'white'
                    elif p < 0.01:
                        text = '**'
                        color = 'white'
                    elif p < 0.05:
                        text = '*'
                        color = 'black'
                    else:
                        text = 'ns'
                        color = 'black'
                
                ax.text(j, i, text, ha='center', va='center', color=color, fontsize=10, weight='bold')
        
        # Set ticks and labels
        ax.set_xticks(np.arange(n_algo))
        ax.set_yticks(np.arange(n_algo))
        ax.set_xticklabels(algorithms, rotation=45, ha='right', fontsize=9)
        ax.set_yticklabels(algorithms, fontsize=9)
        ax.set_title(label, fontsize=11, weight='bold')
        
        # Remove spines
        for spine in ax.spines.values():
            spine.set_visible(False)
    
    # Add colorbar
    cbar = fig.colorbar(im, ax=axes, orientation='horizontal', pad=0.15, aspect=40)
    cbar.set_label('-log10(p-value)', fontsize=10, weight='bold')
    
    plt.suptitle('Statistical Significance Matrix (Mann-Whitney U Test)\n*** p<0.001, ** p<0.01, * p<0.05, ns: not significant', 
                 fontsize=12, weight='bold', y=1.05)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'statistical_significance_heatmap.png', dpi=300, bbox_inches='tight')
    plt.savefig(output_dir / 'statistical_significance_heatmap.pdf', bbox_inches='tight')
    plt.close()
    
    print("✓ Significance heatmap saved")


def summarize_findings(kw_results, pw_results):
    """
    Summarize key statistical findings
    """
    print("\n" + "="*80)
    print("5. SUMMARY OF STATISTICAL FINDINGS")
    print("="*80)
    
    print("\n📊 Overall Differences (Kruskal-Wallis H-test):\n")
    
    for metric, stats_dict in kw_results.items():
        p_value = stats_dict['p_value']
        if p_value < 0.001:
            sig_level = "highly significant (p < 0.001)"
        elif p_value < 0.01:
            sig_level = "very significant (p < 0.01)"
        elif p_value < 0.05:
            sig_level = "significant (p < 0.05)"
        else:
            sig_level = "NOT significant (p ≥ 0.05)"
        
        print(f"  • {metric}: {sig_level}")
        print(f"    → H = {stats_dict['h_statistic']:.4f}, p = {p_value:.6f}")
    
    print("\n🔍 Pairwise Comparisons (Mann-Whitney U test):\n")
    
    for metric, comparisons in pw_results.items():
        print(f"\n  {metric}:")
        
        significant_pairs = []
        for comparison, stats_dict in comparisons.items():
            if stats_dict['significant']:
                p_value = stats_dict['p_value']
                effect = stats_dict['interpretation']
                delta = stats_dict['effect_size']
                
                if p_value < 0.001:
                    sig_marker = "***"
                elif p_value < 0.01:
                    sig_marker = "**"
                else:
                    sig_marker = "*"
                
                significant_pairs.append(f"{comparison} (δ={delta:.3f}, {effect}) {sig_marker}")
        
        if significant_pairs:
            for pair in significant_pairs:
                print(f"    → {pair}")
        else:
            print(f"    → No significant differences")
    
    print("\n" + "="*80)


def export_results_to_excel(normality_results, kw_results, pw_results, corrected_results):
    """
    Export all statistical results to Excel file
    """
    print("\nExporting results to Excel...")
    
    output_file = Path('statistical_analysis_results.xlsx')
    
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # Sheet 1: Normality Test
        normality_data = []
        for metric, algo_results in normality_results.items():
            for algo, stats_dict in algo_results.items():
                normality_data.append({
                    'Metric': metric,
                    'Algorithm': algo,
                    'W-statistic': stats_dict['statistic'],
                    'p-value': stats_dict['p_value'],
                    'Normal?': stats_dict['normal']
                })
        
        df_normality = pd.DataFrame(normality_data)
        df_normality.to_excel(writer, sheet_name='Normality Test', index=False)
        
        # Sheet 2: Kruskal-Wallis Test
        kw_data = []
        for metric, stats_dict in kw_results.items():
            kw_data.append({
                'Metric': metric,
                'H-statistic': stats_dict['h_statistic'],
                'p-value': stats_dict['p_value'],
                'Significant': 'Yes' if stats_dict['significant'] else 'No'
            })
        
        df_kw = pd.DataFrame(kw_data)
        df_kw.to_excel(writer, sheet_name='Kruskal-Wallis Test', index=False)
        
        # Sheet 3: Pairwise Comparisons (Original)
        pw_data = []
        for metric, comparisons in pw_results.items():
            for comparison, stats_dict in comparisons.items():
                pw_data.append({
                    'Metric': metric,
                    'Comparison': comparison,
                    'U-statistic': stats_dict['u_statistic'],
                    'p-value': stats_dict['p_value'],
                    'Cliff\'s Delta': stats_dict['effect_size'],
                    'Effect Size': stats_dict['interpretation'],
                    'Significant (α=0.05)': 'Yes' if stats_dict['significant'] else 'No'
                })
        
        df_pw = pd.DataFrame(pw_data)
        df_pw.to_excel(writer, sheet_name='Pairwise Comparisons', index=False)
        
        # Sheet 4: Bonferroni Corrected
        corrected_data = []
        for metric, comparisons in corrected_results.items():
            for comparison, stats_dict in comparisons.items():
                corrected_data.append({
                    'Metric': metric,
                    'Comparison': comparison,
                    'p-value': stats_dict['p_value'],
                    'Original Significant': 'Yes' if stats_dict['significant'] else 'No',
                    'Bonferroni Significant': 'Yes' if stats_dict['significant_after_correction'] else 'No',
                    'Cliff\'s Delta': stats_dict['effect_size'],
                    'Effect Size': stats_dict['interpretation']
                })
        
        df_corrected = pd.DataFrame(corrected_data)
        df_corrected.to_excel(writer, sheet_name='Bonferroni Corrected', index=False)
    
    print(f"✓ Results exported to {output_file}")


def main():
    """Main analysis pipeline"""
    print("\n" + "="*80)
    print("STATISTICAL ANALYSIS FOR DIET OPTIMIZATION PAPER")
    print("="*80)
    print("\nLoading data from optimization_comparison_results.xlsx...")
    
    # Load data
    algorithms, data_dict = load_data_from_excel()
    
    print(f"✓ Data loaded successfully")
    print(f"  - Algorithms: {', '.join(algorithms)}")
    print(f"  - Metrics: {', '.join(data_dict.keys())}")
    print(f"  - Sample size per algorithm: n=10")
    
    # Create output directory
    output_dir = Path('figures')
    output_dir.mkdir(exist_ok=True)
    
    # 1. Normality test
    normality_results = shapiro_wilk_test(data_dict)
    
    # 2. Kruskal-Wallis test
    kw_results = kruskal_wallis_test(data_dict)
    
    # 3. Pairwise comparisons
    pw_results = mann_whitney_pairwise(data_dict)
    
    # 4. Bonferroni correction
    n_comparisons = len(algorithms) * (len(algorithms) - 1) // 2  # 6 comparisons
    corrected_results = bonferroni_correction(pw_results, n_comparisons)
    
    # 5. Create visualization
    create_significance_heatmap(pw_results, output_dir)
    
    # 6. Summary
    summarize_findings(kw_results, pw_results)
    
    # 7. Export to Excel
    export_results_to_excel(normality_results, kw_results, pw_results, corrected_results)
    
    print("\n" + "="*80)
    print("STATISTICAL ANALYSIS COMPLETED SUCCESSFULLY!")
    print("="*80)
    print("\nGenerated files:")
    print("  - statistical_analysis_results.xlsx")
    print("  - figures/statistical_significance_heatmap.png")
    print("  - figures/statistical_significance_heatmap.pdf")
    print("\n" + "="*80)


if __name__ == "__main__":
    main()
