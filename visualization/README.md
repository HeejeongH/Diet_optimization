# Visualization Tools

Tools for generating publication-quality figures for the research paper.

---

## 📊 Figure Generation

### Quick Start

```bash
cd visualization
python generate_figures.py
```

This will generate all 6 figures in both PNG (300 DPI) and PDF (vector) formats.

---

## 🖼️ Generated Figures

### Figure 1: Performance Radar Chart
**File:** `figures/figure1_radar_chart.png` (606 KB)

Multi-dimensional performance comparison showing all 5 metrics for 4 algorithms.

**Metrics displayed:**
- Hypervolume (0-1, higher better)
- Spacing (inverted, lower better)
- Diversity (0-10, higher better)
- Convergence (0-1, higher better)
- Time (inverted, faster better)

### Figure 2: Hypervolume Box Plots
**File:** `figures/figure2_hypervolume_boxplots.png` (172 KB)

Distribution of hypervolume values across 10 runs for each algorithm.

**Shows:**
- Median, quartiles, and outliers
- Statistical comparison between algorithms
- Consistency of each algorithm

### Figure 3: Spacing Comparison
**File:** `figures/figure3_spacing_comparison.png` (163 KB)

Bar chart with error bars showing spacing metric performance.

**Highlights:**
- NSGA-II superiority (0.604 ± 0.985)
- Statistical significance markers
- 8.96x difference vs ε-MOEA

### Figure 4: Diversity vs Convergence
**File:** `figures/figure4_diversity_convergence.png` (400 KB)

Scatter plot showing trade-off between diversity and convergence.

**Insights:**
- ε-MOEA: High diversity, moderate convergence
- SPEA2: Balanced performance
- Trade-off visualization

### Figure 5: Execution Time Comparison
**File:** `figures/figure5_execution_time.png` (199 KB)

Bar chart showing computational efficiency.

**Key finding:**
- SPEA2 fastest: 992.1 ± 576.1 seconds (16.5 min)
- 1.90x speedup vs ε-MOEA
- Statistical significance (p < 0.001)

### Figure 6: Statistical Significance Heatmap
**File:** `figures/figure6_significance_heatmap.png` (272 KB)

Heatmap showing p-values from Mann-Whitney U pairwise tests.

**Color coding:**
- Green: Not significant (p ≥ 0.05)
- Yellow: Significant (0.01 ≤ p < 0.05)
- Orange: Highly significant (0.001 ≤ p < 0.01)
- Red: Very highly significant (p < 0.001)

---

## 🔧 Customization

### Modify Figure Parameters

Edit `generate_figures.py` to customize:

```python
# Figure size
fig, ax = plt.subplots(figsize=(12, 8))  # Width x Height in inches

# DPI (resolution)
plt.savefig('figure.png', dpi=300, bbox_inches='tight')

# Color scheme
colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D']

# Font sizes
plt.rcParams['font.size'] = 12
plt.rcParams['axes.titlesize'] = 16
```

### Add New Figures

1. Load data from `final_comparison.xlsx`
2. Create your plot using matplotlib/seaborn
3. Save in both PNG and PDF formats
4. Update this README

Example:
```python
import pandas as pd
import matplotlib.pyplot as plt

# Load data
data = pd.read_excel('../data/final_comparison.xlsx', sheet_name='HYPERVOLUME')

# Create figure
fig, ax = plt.subplots(figsize=(10, 6))
# ... your plotting code ...

# Save
plt.savefig('figures/my_figure.png', dpi=300, bbox_inches='tight')
plt.savefig('figures/my_figure.pdf', bbox_inches='tight')
```

---

## 📋 Requirements

The figure generation script requires:

```bash
pip install numpy pandas matplotlib seaborn scipy openpyxl
```

All dependencies are included in the main `requirements.txt`.

---

## 🎨 Style Guide

Figures follow these style guidelines:

1. **Color Palette**
   - NSGA-II: `#2E86AB` (Blue)
   - NSGA-III: `#A23B72` (Purple)
   - SPEA2: `#F18F01` (Orange)
   - ε-MOEA: `#C73E1D` (Red)

2. **Font**
   - Family: DejaVu Sans
   - Title: 16pt bold
   - Labels: 12pt
   - Ticks: 10pt

3. **Format**
   - PNG: 300 DPI (for Word/PowerPoint)
   - PDF: Vector format (for LaTeX)
   - White background
   - Tight bounding box

4. **Size**
   - Standard: 12" × 8"
   - Large: 14" × 10"
   - Adjust for specific journal requirements

---

## 📁 Directory Structure

```
visualization/
├── generate_figures.py      # Main script
├── figures/                 # Output directory (auto-created)
│   ├── figure1_radar_chart.png
│   ├── figure1_radar_chart.pdf
│   ├── figure2_hypervolume_boxplots.png
│   ├── figure2_hypervolume_boxplots.pdf
│   └── ...
└── README.md               # This file
```

---

## 🔄 Updating Figures

When experimental results change:

1. Update `final_comparison.xlsx` with new data
2. Run `python generate_figures.py`
3. All figures will be regenerated automatically
4. Check output in `figures/` directory

---

## 📊 Data Source

All figures use data from:
- **File:** `../data/final_comparison.xlsx`
- **Sheets:** HYPERVOLUME, SPACING, DIVERSITY, CONVERGENCE, EXECUTION_TIME
- **Format:** 10 runs × 4 algorithms

---

## 💡 Tips

1. **High-Resolution Figures**
   - Use 600 DPI for journal submissions
   - Increase figure size for better readability

2. **Color-Blind Friendly**
   - Consider using patterns/textures
   - Use high contrast colors

3. **Vector Formats**
   - PDF preferred for publications
   - Scalable without quality loss

4. **File Size**
   - PNG files can be large (100-600 KB)
   - Reduce DPI if file size is an issue

---

## 📧 Support

For issues or questions:
- GitHub Issues: [Report a problem](https://github.com/HeejeongH/Diet_optimization/issues)
- Documentation: See main [README](../README.md)
