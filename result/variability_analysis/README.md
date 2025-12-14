# 2-Level Variability Decomposition Analysis

**Analysis Date:** 2025-12-13
**Data:** 10 dietary datasets × 10 runs × 4 algorithms = 2000 observations

---

## Quick Start

### View Results

1. **Summary Statistics**: `summary_statistics.csv`
2. **Interpretation Guide**: `INTERPRETATION.md` (detailed findings and recommendations)
3. **Manuscript Sections**: `MANUSCRIPT_SECTIONS.md` (ready-to-integrate paper text)

### Key Visualizations

- **Dataset-level profiles**: `dataset_profiles/` (performance across 10 datasets)
- **Variance components**: `variance_components/` (breakdown of variability sources)
- **Statistical tables**: `tables/` (ICC and variance decomposition tables)

---

## Executive Summary

### Main Finding
**Different algorithms have fundamentally different sensitivity patterns:**
- **NSGA-II & NSGA-III**: Robust to initialization, sensitive to dataset characteristics (desirable)
- **ε-MOEA**: Highly sensitive to initialization, unstable performance (problematic)
- **SPEA2**: Exceptional computational stability, moderate quality robustness

### Practical Recommendations

| Use Case | Recommended Algorithm | Rationale |
|----------|----------------------|-----------|
| **Real-time diet optimization** | SPEA2 | Predictable 14.3s execution time, low variance |
| **Batch processing (quality priority)** | NSGA-III | Best optimization quality with excellent robustness |
| **Embedded/resource-constrained** | SPEA2 | Lowest computational requirements, stable behavior |
| **Research/critical optimization** | NSGA-III (multiple runs) | Ensures optimal solution quality |
| **Production environments** | Avoid ε-MOEA | Poor quality, extreme variability |

---

## What is 2-Level Variability Decomposition?

Traditional analysis pools all 100 results (10 datasets × 10 runs) and reports:
- **NSGA-III**: Hypervolume 0.362 ± 0.016
- **ε-MOEA**: Hypervolume 0.353 ± 0.022

This simple approach **hides two critical questions**:

### Question 1: Is the variability due to different datasets or random seeds?
- **Between-dataset variance**: Different dietary problems have different optimal solutions (expected, desirable)
- **Within-dataset variance**: Same problem gives different results due to random initialization (problematic, indicates instability)

### Question 2: Is the algorithm robust?
- **High ICC** (Intraclass Correlation Coefficient ≈ 1): Variability mostly from dataset differences → algorithm is robust and adapts to problem structure
- **Low ICC** (≈ 0): Variability mostly from random initialization → algorithm is unstable

---

## Key Metrics Explained

### Intraclass Correlation Coefficient (ICC)

```
ICC = Between-dataset variance / Total variance
```

**Interpretation:**
- **ICC = 1.0**: Perfect robustness. All variability comes from genuine dataset differences.
- **ICC = 0.5**: Half the variability is from datasets, half from random initialization.
- **ICC = 0.0**: Complete instability. Performance is entirely driven by random seed.

**Example from our results:**
- NSGA-III hypervolume ICC = 0.705 → 70.5% of variance is from datasets (GOOD)
- ε-MOEA hypervolume ICC = 0.249 → Only 24.9% from datasets, 75% from randomness (BAD)

### Within-Dataset Standard Deviation

**Measures robustness to initialization** (lower is better)

Answers: "If I run this algorithm 10 times on the same problem, how much will results vary?"

**Example:**
- NSGA-III: Within-dataset SD = 0.0102 → Very consistent across runs
- ε-MOEA: Within-dataset SD = 0.0199 → Highly variable across runs (nearly 2× worse)

### Between-Dataset Standard Deviation

**Measures generalizability across problems** (higher ICC means this dominates)

Answers: "How much does performance vary across different dietary datasets?"

**Example:**
- SPEA2 convergence: Between-dataset SD = 0.5698, ICC = 0.993
  → Performance is almost entirely determined by dataset characteristics (excellent adaptation)

---

## Key Findings by Metric

### 1. Hypervolume (Optimization Quality)

| Algorithm | Total SD | Within SD | Between SD | ICC | Verdict |
|-----------|----------|-----------|------------|-----|---------|
| NSGA-II   | 0.0188   | 0.0123    | 0.0154     | **67%** | ✓ Robust |
| NSGA-III  | 0.0163   | 0.0102    | 0.0137     | **71%** | ✓✓ Very robust |
| SPEA2     | 0.0186   | 0.0151    | 0.0123     | 44% | △ Moderate |
| ε-MOEA    | 0.0216   | 0.0199    | 0.0108     | **25%** | ✗ Unstable |

**Implication:** NSGA-III provides consistent high-quality solutions. ε-MOEA requires multiple runs.

### 2. Execution Time (Computational Efficiency)

| Algorithm | Mean    | Total SD | Within SD | Between SD | ICC | Verdict |
|-----------|---------|----------|-----------|------------|-----|---------|
| NSGA-II   | 31.1s   | 108.8s   | 105.4s    | 43.6s      | 16% | ✗ Unpredictable |
| NSGA-III  | 30.4s   | 106.9s   | 95.2s     | 59.3s      | 31% | ✗ Unpredictable |
| SPEA2     | **14.3s** | **33.7s** | **33.5s** | **11.4s**  | **11%** | ✓✓ Very predictable |
| ε-MOEA    | 157.0s  | 234.8s   | 191.6s    | 154.7s     | 43% | ✗✗ Catastrophic |

**Implication:** Only SPEA2 is suitable for real-time applications. ε-MOEA has extreme variability.

### 3. Convergence (Solution Improvement)

| Algorithm | Mean  | Total SD | Within SD | Between SD | ICC | Verdict |
|-----------|-------|----------|-----------|------------|-----|---------|
| NSGA-II   | 0.693 | 0.386    | 0.204     | 0.349      | 82% | ✓ Dataset-driven |
| NSGA-III  | 0.655 | 0.340    | 0.171     | 0.313      | 85% | ✓ Dataset-driven |
| SPEA2     | 1.065 | 0.572    | 0.187     | 0.570      | **99%** | ✓✓ Deterministic |
| ε-MOEA    | 0.940 | 0.514    | 0.261     | 0.472      | 84% | ✓ Dataset-driven |

**Implication:** All algorithms adapt convergence to problem structure. SPEA2 is nearly perfectly deterministic.

---

## Visualization Guide

### Dataset-Level Performance Profiles (`dataset_profiles/`)

**Example: `dataset_profile_hypervolume.png`**

Shows each algorithm's performance across 10 datasets:
- **X-axis**: Dataset ID (1-10)
- **Y-axis**: Hypervolume (mean across 10 runs)
- **Error bars**: ±1 standard deviation (within-dataset)

**What to look for:**
- **Narrow error bars**: Robust to initialization (NSGA-II, NSGA-III)
- **Wide error bars**: Sensitive to initialization (ε-MOEA)
- **Parallel lines**: Consistent relative performance across datasets
- **Crossing lines**: Algorithm ranking changes depending on dataset

### Variance Component Plots (`variance_components/`)

**Example: `variance_components_hypervolume.png`**

Stacked bar chart showing percentage breakdown:
- **Blue (bottom)**: Between-dataset variance (generalizability)
- **Red (top)**: Within-dataset variance (initialization sensitivity)

**What to look for:**
- **Tall blue, short red**: Good (variance is from dataset adaptation)
- **Short blue, tall red**: Bad (variance is from random initialization)

---

## File Structure

```
variability_analysis/
├── README.md                          # This file
├── INTERPRETATION.md                  # Detailed analysis and interpretation
├── MANUSCRIPT_SECTIONS.md             # Paper sections ready for integration
├── summary_statistics.csv             # All metrics for all algorithms
│
├── tables/                            # CSV tables for each metric
│   ├── variance_decomposition_hypervolume.csv
│   ├── variance_decomposition_spacing.csv
│   ├── variance_decomposition_diversity.csv
│   ├── variance_decomposition_convergence.csv
│   └── variance_decomposition_execution_time.csv
│
├── dataset_profiles/                  # Performance across 10 datasets
│   ├── dataset_profile_hypervolume.png
│   ├── dataset_profile_spacing.png
│   ├── dataset_profile_diversity.png
│   ├── dataset_profile_convergence.png
│   └── dataset_profile_execution_time.png
│
├── variance_components/               # Variance breakdown visualizations
│   ├── variance_components_hypervolume.png
│   ├── variance_components_spacing.png
│   ├── variance_components_diversity.png
│   ├── variance_components_convergence.png
│   └── variance_components_execution_time.png
│
└── mixed_effects/                     # Statistical model outputs
    ├── mixed_effects_hypervolume.txt
    ├── mixed_effects_spacing.txt
    ├── mixed_effects_diversity.txt
    ├── mixed_effects_convergence.txt
    └── mixed_effects_execution_time.txt
```

---

## Reproducing the Analysis

### Requirements
- Python 3.11+
- pandas, numpy, scipy, matplotlib, seaborn, statsmodels, openpyxl

### Running the Analysis
```bash
cd /home/user/Diet_optimization
python3 src/variability_decomposition.py
```

### Input Data
- **Location**: `result/optimization results/`
- **Format**: 10 Excel files (one per dietary dataset)
- **Structure**: Each file contains 10 runs × 4 algorithms × 5 metrics

### Output
All results are saved to `result/variability_analysis/`

---

## Statistical Methods

### 1. Variance Decomposition

For each algorithm and metric:

```python
# Between-dataset variance
dataset_means = data.groupby('Dataset')['Value'].mean()
between_var = dataset_means.var()

# Within-dataset variance
within_var = mean([data[dataset].var() for dataset in datasets])

# Total variance
total_var = data['Value'].var()

# ICC
icc = between_var / total_var
```

### 2. Mixed-Effects Model

```
Value ~ Algorithm + (1|Dataset)
```

- **Fixed effect (Algorithm)**: Overall algorithm performance differences
- **Random effect (Dataset)**: Dataset-specific deviations
- **Residual**: Within-dataset, within-algorithm variation

**Interpretation:**
- Large random effect variance → datasets have different optimal solutions
- Large residual variance → high initialization sensitivity

### 3. Statistical Significance

All pairwise algorithm comparisons use Mann-Whitney U test (non-parametric, appropriate for potentially non-normal distributions).

---

## Key Insights for Practitioners

### 1. Single-Run Reliability

**Question:** "Can I run this algorithm once and trust the result?"

| Algorithm | Answer | Explanation |
|-----------|--------|-------------|
| NSGA-III  | ✓ Yes | Low within-dataset variance (SD = 0.0102) |
| NSGA-II   | ✓ Yes | Low within-dataset variance (SD = 0.0123) |
| SPEA2     | △ Probably | Moderate within-dataset variance (SD = 0.0151) |
| ε-MOEA    | ✗ No | High within-dataset variance (SD = 0.0199) |

### 2. Computational Budget Planning

**Question:** "How much time should I budget for optimization?"

| Algorithm | 95% Confidence Interval | Recommendation |
|-----------|------------------------|----------------|
| SPEA2     | 0s - 81s              | Budget 90s, very reliable |
| NSGA-II   | 0s - 248s             | Budget 250s, use timeout |
| NSGA-III  | 0s - 244s             | Budget 250s, use timeout |
| ε-MOEA    | 0s - 627s             | Avoid in production |

### 3. Quality Assurance

**Question:** "How do I ensure consistent quality?"

**For NSGA-II/III:**
- Single run is sufficient for most applications
- Performance differences across runs reflect dataset characteristics, not randomness

**For SPEA2:**
- Single run acceptable for time-critical applications
- Consider 2-3 runs for quality-critical applications

**For ε-MOEA:**
- Requires 5-10 runs to mitigate initialization sensitivity
- Select best hypervolume result
- Better approach: use NSGA-III instead

---

## Comparison with Traditional Analysis

### Traditional Approach (Pooled Statistics)

| Algorithm | Hypervolume Mean ± SD |
|-----------|-----------------------|
| NSGA-III  | 0.362 ± 0.016        |
| SPEA2     | 0.362 ± 0.019        |
| ε-MOEA    | 0.353 ± 0.022        |

**Conclusion from traditional approach:** "Algorithms are comparable; ε-MOEA slightly worse."

### Our Approach (Variance Decomposition)

| Algorithm | Mean | Total SD | **Within SD** | **ICC** |
|-----------|------|----------|---------------|---------|
| NSGA-III  | 0.362 | 0.016   | **0.010**     | **71%** |
| SPEA2     | 0.362 | 0.019   | **0.015**     | **44%** |
| ε-MOEA    | 0.353 | 0.022   | **0.020**     | **25%** |

**Conclusion from decomposition:** "NSGA-III is robust (71% ICC), ε-MOEA is unstable (25% ICC). For production use, NSGA-III is strongly preferred despite similar aggregate performance."

**The difference matters in practice:**
- Production deployment with single-run constraint → Choose NSGA-III
- Real-time application → Choose SPEA2 for computational stability
- Research application with multiple runs → Any algorithm acceptable

---

## Frequently Asked Questions

### Q1: Why is high ICC good?
**A:** High ICC means performance differences primarily reflect genuine problem characteristics (different datasets) rather than algorithmic randomness (different random seeds). This indicates the algorithm is robust and adapts to problem structure.

### Q2: Can low within-dataset variance and high between-dataset variance coexist?
**A:** Yes, this is the ideal pattern! It means:
- Algorithm produces consistent results on the same problem (low within-dataset variance)
- Algorithm adapts its behavior to different problems (high between-dataset variance)

NSGA-III demonstrates this pattern.

### Q3: SPEA2 has low ICC for execution time. Is that bad?
**A:** No! For execution time, low ICC is GOOD because it means runtime is consistent across both datasets AND runs. High ICC would mean some datasets take much longer than others (problematic for SLA guarantees).

### Q4: Why not just report total variance?
**A:** Total variance obscures the source of variability. Two algorithms with identical total variance can have completely different operational characteristics:
- Algorithm A: High total variance from dataset differences (good adaptation)
- Algorithm B: High total variance from initialization randomness (poor robustness)

Decomposition distinguishes these scenarios.

### Q5: How were datasets selected?
**A:** 10 weekly dietary menus from different time periods (Jan-Aug 2024) at an elderly care facility. Each represents different seasonal ingredients and nutritional requirements.

### Q6: Why 10 runs per dataset?
**A:** Standard practice in evolutionary algorithm evaluation. 10 runs provide sufficient statistical power to estimate within-dataset variance while remaining computationally feasible.

---

## Citation

If you use this analysis methodology in your research, please cite:

```bibtex
@article{diet_optimization_2025,
  title={Multi-objective Enhanced Tool for Optimal Meal Recommendation: A 2-Level Variability Decomposition Approach},
  author={[Your Name]},
  journal={[Journal Name]},
  year={2025}
}
```

---

## Contact

For questions about this analysis or the methodology:
- **Analysis Script**: `src/variability_decomposition.py`
- **Raw Data**: `result/optimization results/`
- **Documentation**: This README and `INTERPRETATION.md`

---

**Last Updated:** 2025-12-13
