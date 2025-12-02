# Figure Generation for Research Paper

This directory contains scripts to generate publication-quality figures for the diet optimization research paper.

## Quick Start

```bash
# Install dependencies
pip install -r ../requirements.txt

# Generate all figures
python generate_figures.py
```

## Generated Figures

### Figure 1: Performance Radar Chart
- **File**: `figure1_radar_chart.png` / `.pdf`
- **Purpose**: Multi-dimensional performance comparison across 5 metrics
- **Usage**: Results section introduction, abstract visual

### Figure 2: Hypervolume Box Plots
- **File**: `figure2_hypervolume_boxplots.png` / `.pdf`
- **Purpose**: Shows distribution and no significant differences
- **Key Finding**: Kruskal-Wallis p = 0.642 (no significant differences)

### Figure 3: Spacing Comparison Bar Chart
- **File**: `figure3_spacing_comparison.png` / `.pdf`
- **Purpose**: Demonstrates NSGA-II's superiority
- **Key Finding**: NSGA-II significantly better (p = 0.001 vs SPEA2)

### Figure 4: Diversity vs Convergence Scatter
- **File**: `figure4_diversity_convergence.png` / `.pdf`
- **Purpose**: Shows exploration-exploitation trade-off
- **Key Finding**: SPEA2 (high convergence) vs ε-MOEA (high diversity)

### Figure 5: Execution Time Comparison
- **File**: `figure5_execution_time.png` / `.pdf`
- **Purpose**: Computational efficiency comparison
- **Key Finding**: SPEA2 fastest (992.1s), 1.90× faster than ε-MOEA

### Figure 6: Statistical Significance Heatmap
- **File**: `figure6_significance_heatmap.png` / `.pdf`
- **Purpose**: Comprehensive p-value matrix
- **Key Finding**: Execution time and convergence show strongest differentiation

## Output Formats

Each figure is generated in two formats:
- **PNG** (300 DPI) - For Microsoft Word documents
- **PDF** (vector) - For LaTeX documents

## Customization

### Change Figure Style

Edit the script to modify:
```python
# Color scheme
colors = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12']

# Figure size
fig, ax = plt.subplots(figsize=(10, 8))

# DPI for PNG export
plt.savefig('output.png', dpi=300)  # Change to 600 for higher quality
```

### Add New Figures

1. Create new function in `generate_figures.py`:
```python
def figure7_new_analysis(output_dir):
    """Your figure description"""
    # Your plotting code here
    pass
```

2. Call in `generate_all_figures()`:
```python
figure7_new_analysis(output_dir)
```

## Data Source

All data comes from `final_comparison.xlsx`:
- 10 independent runs per algorithm
- 4 algorithms (NSGA-II, NSGA-III, SPEA2, ε-MOEA)
- 5 performance metrics

## Dependencies

```bash
pip install numpy pandas matplotlib seaborn scipy
```

## Troubleshooting

### "No module named 'matplotlib'"
```bash
pip install matplotlib seaborn
```

### "Permission denied" when saving
```bash
# Create figures directory manually
mkdir -p figures
chmod 755 figures
```

### Figures look blurry in Word
- Increase DPI: Change `dpi=300` to `dpi=600`
- Use PDF instead: Import `.pdf` files in Word (Insert > Pictures)

## For Paper Submission

### Recommended Format
- **Journal submission**: Use PDF (vector graphics)
- **Conference submission**: Use PNG at 300 DPI minimum
- **Presentation slides**: Use PNG at 150 DPI

### Size Guidelines
- **Single column**: width ≤ 3.5 inches (900 pixels @ 300 DPI)
- **Double column**: width ≤ 7 inches (2100 pixels @ 300 DPI)
- **Full page**: width ≤ 7 inches, height ≤ 9 inches

Current figures are optimized for double-column layout.

## Citation

If you use these visualization methods, please cite:
```
Visualization code from Diet Optimization Project
https://github.com/HeejeongH/Diet_optimization
```
