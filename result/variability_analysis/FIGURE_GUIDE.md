# Visualization Guide for 2-Level Variability Decomposition

This guide explains each visualization and how to use it in your paper/presentation.

---

## Core Visualizations (Primary Analysis)

### 1. Dataset-Level Performance Profiles (`dataset_profiles/`)

**Files:**
- `dataset_profile_hypervolume.png`
- `dataset_profile_spacing.png`
- `dataset_profile_diversity.png`
- `dataset_profile_convergence.png`
- `dataset_profile_execution_time.png`

**What it shows:**
- X-axis: 10 different dietary datasets
- Y-axis: Performance metric (mean across 10 runs per dataset)
- Error bars: Within-dataset standard deviation (±1 SD)

**Key insights:**
- **Narrow error bars** = robust to initialization (NSGA-II, NSGA-III)
- **Wide error bars** = sensitive to initialization (ε-MOEA)
- **Parallel lines** = consistent relative performance
- **Crossing lines** = algorithm ranking depends on dataset

**Best for:** Results section (5.2.2), showing robustness differences

**Recommended figure for paper:**
- `dataset_profile_hypervolume.png` (most important metric)
- `dataset_profile_execution_time.png` (shows SPEA2 stability vs ε-MOEA chaos)

---

### 2. Variance Component Plots (`variance_components/`)

**Files:**
- `variance_components_hypervolume.png`
- `variance_components_spacing.png`
- `variance_components_diversity.png`
- `variance_components_convergence.png`
- `variance_components_execution_time.png`

**What it shows:**
- Stacked bar chart (100% total variance)
- Blue (bottom): Between-dataset variance (generalizability)
- Red (top): Within-dataset variance (initialization sensitivity)
- Percentages labeled on each segment

**Key insights:**
- **Tall blue, short red** = good (dataset-adaptive, initialization-robust)
- **Short blue, tall red** = bad (ignores dataset, initialization-dependent)

**Example interpretations:**
- NSGA-III hypervolume: 71% blue → adapts to dataset characteristics
- ε-MOEA hypervolume: 75% red → dominated by random initialization
- SPEA2 execution time: 89% red (but low total variance, so this is good!)

**Best for:** Results section (5.2.2), Discussion (explaining ICC concept visually)

**Recommended figure for paper:**
- `variance_components_hypervolume.png` (key metric)
- `variance_components_convergence.png` (shows SPEA2's 99% dataset-driven behavior)

---

## Additional Visualizations (Supplementary/Presentation)

### 3. ICC Radar Comparison (`additional_figures/icc_radar_comparison.png`)

**What it shows:**
- Radar/spider chart with 5 axes (one per metric)
- Each algorithm is a colored line forming a shape
- Larger shape area = higher ICC overall = more robust

**Key insights:**
- **NSGA-II and NSGA-III**: Large, regular shapes → consistently high ICC
- **ε-MOEA**: Small, irregular shape → low ICC, especially for spacing/hypervolume
- **SPEA2**: Medium shape, strong for convergence

**Best for:**
- Presentations (visually striking, easy to grasp)
- Supplementary material (comprehensive comparison)
- Discussion section (overall robustness comparison)

**How to interpret:**
- Points further from center = higher ICC = better robustness
- Look for which algorithms "dominate" (enclose others) for each metric

---

### 4. Combined Performance Summary (`additional_figures/combined_performance_summary.png`)

**What it shows:**
6-panel figure providing comprehensive overview:
- **(A) Optimization Quality**: Hypervolume mean ± SD
- **(B) Computational Efficiency**: Execution time mean ± SD
- **(C) Robustness**: Hypervolume ICC values
- **(D) Initialization Sensitivity**: Within-dataset SD for key metrics
- **(E) Solution Improvement**: Convergence mean ± SD
- **(F) ICC Heatmap**: All metrics × all algorithms

**Key insights:**
- Single figure summarizes entire study
- Panel (A) + (C): NSGA-III has both high quality AND high robustness
- Panel (B): SPEA2 is dramatically faster and more stable
- Panel (F): Color pattern shows NSGA-II/III are robustly green, ε-MOEA is problematically red

**Best for:**
- **Main paper figure**: Perfect as Figure 1 or 2 in Results section
- Gives reviewers immediate understanding of all findings
- Presentations: Can show full figure or extract individual panels

**Recommendation:** Use this as your primary figure in the Results section. It tells the complete story.

---

### 5. Algorithm Ranking Heatmap (`additional_figures/algorithm_ranking_heatmap.png`)

**What it shows:**
- Heatmap of algorithm rankings (1-4) for each metric
- Green = Rank 1 (best), Red = Rank 4 (worst)
- Rankings based on mean performance (higher for quality, lower for time)

**Key insights:**
- **NSGA-III**: Ranks 1st or 2nd for most metrics (consistent excellence)
- **SPEA2**: Ranks 1st for execution time (by far), mid-tier for quality
- **ε-MOEA**: Mostly ranks 3rd-4th (consistently worst)

**Best for:**
- Quick comparison for readers
- Discussion section: "NSGA-III achieved top-2 rankings across 4/5 metrics..."
- Supplementary material

**Note:** Rankings don't account for statistical significance or robustness, only mean values.

---

### 6. Metric Correlation Matrices (`additional_figures/metric_correlations.png`)

**What it shows:**
- 4 correlation matrices (one per algorithm)
- Shows how metrics relate to each other within each algorithm
- Red = positive correlation, Blue = negative correlation

**Key insights:**
- **Hypervolume vs Execution Time**: Generally uncorrelated or weakly correlated
  → Can't predict quality from speed
- **Diversity vs Convergence**: Often positively correlated
  → Algorithms that converge well also spread solutions widely
- **Different patterns per algorithm**: Each algorithm has unique metric relationships

**Best for:**
- Supplementary material
- Discussion: "The weak correlation between hypervolume and execution time (r < 0.3) indicates that computational cost does not reliably predict solution quality..."
- Methodological justification: "Low inter-metric correlations confirm that our metrics capture distinct aspects of performance"

**Advanced interpretation:**
- Strong correlations (|r| > 0.7) suggest redundancy → could use fewer metrics
- Weak correlations suggest metrics are complementary → all are necessary

---

### 7. Box Plot Comparison (`additional_figures/box_plot_comparison.png`)

**What it shows:**
- Box plots for 3 key metrics: Hypervolume, Execution Time, Convergence
- Each box shows:
  - Median (black line)
  - Mean (red diamond)
  - Quartiles (box edges)
  - Outliers (black circles)

**Key insights:**
- **ε-MOEA execution time**: Massive outliers (600+ seconds)
  → Pathological cases on certain datasets
- **SPEA2 hypervolume**: Median ≈ Mean, symmetric distribution
  → Gaussian-like, predictable
- **NSGA-III**: Tight distributions across all metrics
  → Consistent performance

**Best for:**
- Results section: "Box plots reveal that ε-MOEA exhibited extreme execution time outliers exceeding 600 seconds..."
- Statistical validation: Shows distribution shapes (important for non-parametric tests)
- Identifying outliers and asymmetry

**How to read:**
- **Narrow box** = low variance (consistent)
- **Wide box** = high variance (unpredictable)
- **Outliers far from box** = occasional extreme values
- **Median ≠ Mean** = skewed distribution

---

## Recommended Figure Selection for Paper

### Main Text (3-4 figures max)

**Figure 1: Combined Performance Summary**
- File: `additional_figures/combined_performance_summary.png`
- Placement: Results section 5.2
- Rationale: Comprehensive overview, tells complete story

**Figure 2: Dataset-Level Hypervolume Profile**
- File: `dataset_profiles/dataset_profile_hypervolume.png`
- Placement: Results section 5.2.2
- Rationale: Shows robustness differences with error bars

**Figure 3: Variance Components (Hypervolume & Execution Time)**
- Files: `variance_components_hypervolume.png` + `variance_components_execution_time.png`
- Placement: Results section 5.2.2 and 5.3.1
- Rationale: Visualizes ICC concept, shows contrasting patterns

**Figure 4: Box Plot Comparison**
- File: `additional_figures/box_plot_comparison.png`
- Placement: Results section 5.3 or Supplementary
- Rationale: Shows distributions and outliers

### Supplementary Material

- ICC Radar Comparison
- Algorithm Ranking Heatmap
- Metric Correlation Matrices
- All other dataset-level profiles
- All other variance component plots

### Presentation Slides

**Slide 1: Problem Statement**
- No visualization (text only)

**Slide 2: Methodology Overview**
- Use: `variance_components_hypervolume.png` (simplified)
- Annotate: "Blue = Dataset differences, Red = Initialization randomness"

**Slide 3: Main Results**
- Use: `additional_figures/combined_performance_summary.png`
- Highlight panels (A), (B), and (C)

**Slide 4: Robustness Comparison**
- Use: `additional_figures/icc_radar_comparison.png`
- Very visual, easy to understand at a glance

**Slide 5: Practical Implications**
- Use: `dataset_profiles/dataset_profile_execution_time.png`
- Annotate: "SPEA2 = predictable, ε-MOEA = catastrophic"

**Slide 6: Recommendations**
- Use: `additional_figures/algorithm_ranking_heatmap.png`
- Clear visual summary of which algorithm wins for what

---

## Figure Quality Guidelines

All figures are saved at **300 DPI** (publication quality).

**For paper submission:**
- ✓ 300 DPI PNG format (suitable for most journals)
- ✓ Large fonts (12-16pt) for readability
- ✓ Color-blind friendly palettes (blue/orange/green/red)
- ✓ Black borders and grid lines for clarity

**If journal requires vector graphics:**
Modify the save lines in the Python scripts to:
```python
plt.savefig(save_path.replace('.png', '.pdf'), format='pdf', bbox_inches='tight')
```

**For presentations:**
- Current 300 DPI PNGs are perfect
- High resolution ensures clarity on projectors/screens

---

## Common Questions

### Q: Which figure best shows that NSGA-III is the best algorithm?

**A:** Combine:
1. **Panel (A) of Combined Summary**: Shows NSGA-III has competitive hypervolume
2. **Panel (C) of Combined Summary**: Shows NSGA-III has highest ICC (0.71)
3. **ICC Radar Chart**: Shows NSGA-III has large, consistent shape across metrics

**Narrative:** "While NSGA-III's aggregate hypervolume (0.362 ± 0.016) appears similar to NSGA-II and SPEA2, its superior robustness (ICC = 0.71) indicates that this performance is reliable across different random initializations."

### Q: Which figure best shows that SPEA2 is best for real-time applications?

**A:** Combine:
1. **Execution Time Dataset Profile**: Shows SPEA2's flat, low profile with tiny error bars
2. **Execution Time Variance Components**: Shows SPEA2's low total variance
3. **Panel (B) of Combined Summary**: Shows SPEA2's 14.3s vs others' 30-157s

**Narrative:** "SPEA2's exceptional computational stability (SD = 33.69s) and low ICC (11.4%) indicate predictable execution time regardless of dataset complexity or initialization, making it ideal for latency-sensitive applications."

### Q: Which figure best shows that ε-MOEA is problematic?

**A:** Use:
1. **Box Plot (Execution Time panel)**: Shows massive outliers
2. **Hypervolume Variance Components**: Shows 75% red (initialization-dominated)
3. **Algorithm Ranking Heatmap**: Shows mostly rank 3-4 across metrics

**Narrative:** "ε-MOEA exhibited the worst performance across all dimensions: lowest hypervolume (0.353), poorest robustness (ICC = 0.25), and catastrophic execution time variability (SD = 234.76s with outliers exceeding 600s)."

### Q: Which figures should I show to non-technical stakeholders?

**A:** Use:
1. **ICC Radar Chart**: Very intuitive "bigger shape = better"
2. **Algorithm Ranking Heatmap**: Simple color coding (green = good, red = bad)
3. **Panel (B) of Combined Summary**: Bar chart showing SPEA2 is 10× faster than ε-MOEA

Avoid: Variance component plots (requires understanding of ICC concept)

---

## File Naming Convention

All files follow consistent naming:
- Core analysis: `{analysis_type}_{metric}.{ext}`
  - Example: `dataset_profile_hypervolume.png`
- Additional figures: `{figure_type}.{ext}`
  - Example: `icc_radar_comparison.png`
- Tables: `variance_decomposition_{metric}.csv`

This makes it easy to find specific visualizations and reference them in text.

---

## Accessibility Notes

**Color-blind friendly:**
- Uses Blue-Orange-Green-Red palette (distinguishable in deuteranopia/protanopia)
- Supplemented with patterns, markers, and labels

**Black-and-white printing:**
- All figures use distinct line styles and markers
- Heatmaps include numerical annotations
- Variance component plots include percentage labels

**Screen readers:**
- All data available in CSV format (`tables/` directory)
- Summary statistics in `summary_statistics.csv`

---

## Next Steps

1. **Review all figures**: Ensure they tell your intended story
2. **Select 3-4 for main text**: Based on journal page limits
3. **Prepare figure captions**: 2-3 sentences each, explain what reader should see
4. **Create supplementary PDF**: Combine remaining figures
5. **Reference in text**: "As shown in Figure X, NSGA-III..."

All figures are ready for direct inclusion in your manuscript!
