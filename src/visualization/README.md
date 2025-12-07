# METOR Visualization Scripts

This directory contains all visualization scripts for the METOR project.

## Main Script

**`generate_all_figures.py`** - Master script that generates ALL figures
```bash
python src/visualization/generate_all_figures.py
```

## Individual Scripts

1. **`generate_figures.py`** - Main paper figures (Figure 1-8, Table 1)
   - Figure 1: Convergence Plot (Hypervolume over generations)
   - Figure 2: 3D Pareto Front (SPEA2 solutions)
   - Figure 3: Radar Chart (4-objective comparison)
   - Table 1: Performance Summary
   - Figure 4-7: Detailed analysis (Box, Bar, Scatter, Time)
   - Figure 8: Statistical Heatmap (p-values)

2. **`visualize_4d_alternatives.py`** - Alternative 4D visualization methods
   - Method 1: 3D + Color Mapping
   - Method 2: Pairwise Scatter Matrix
   - Method 3: Parallel Coordinates
   - Method 4: Heatmap Matrix

3. **`visualize_metric_comparison.py`** - Performance metrics explanation
   - Comprehensive comparison figure (6 metrics)
   - Detailed Hypervolume explanation
   - METOR results summary

4. **`additional_figures.py`** - Supplementary figures
   - Figure 7: 3D Pareto Front (alternative version)
   - Figure 8: Convergence Plot (alternative version)

## Output Directory

All figures are saved to: `results/figures/`

## Dependencies

- numpy
- matplotlib
- seaborn
- pandas
- scipy
