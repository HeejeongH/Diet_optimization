# METOR Project Structure

## 📁 Directory Organization

```
diet_optimization_clean/
│
├── src/                          # Source code
│   ├── visualization/            # ✨ All visualization scripts
│   │   ├── generate_all_figures.py           # 🎯 Master script (run this!)
│   │   ├── generate_figures.py               # Main figures (1-8, Table 1)
│   │   ├── visualize_4d_alternatives.py      # 4D visualization methods
│   │   ├── visualize_metric_comparison.py    # Metrics explanation
│   │   ├── additional_figures.py             # Supplementary figures
│   │   └── README.md                         # Visualization guide
│   │
│   ├── Diet_class.py             # Diet representation
│   ├── evaluation_function.py    # Objective functions
│   ├── load_data.py              # Data loading
│   ├── optimizer_base.py         # Base optimizer class
│   ├── nsga2_optimizer.py        # NSGA-II implementation
│   ├── nsga3_optimizer.py        # NSGA-III implementation
│   ├── spea2_optimizer.py        # SPEA2 implementation
│   ├── emoea_optimizer.py        # ε-MOEA implementation
│   ├── performance_metrics.py    # Performance evaluation
│   ├── statistical_analysis.py   # Statistical tests
│   ├── food_mapper.py            # Food mapping utilities
│   ├── diet_converter.py         # Diet conversion
│   ├── utils.py                  # Helper functions
│   └── app.py                    # Web application
│
├── results/                      # 📊 All output files
│   └── figures/                  # ✨ All generated figures
│       ├── figure1.png/pdf       # Convergence Plot
│       ├── figure2.png/pdf       # 3D Pareto Front
│       ├── figure3.png/pdf       # Radar Chart
│       ├── table1.png/pdf        # Performance Table
│       ├── figure4.png/pdf       # Hypervolume Box Plots
│       ├── figure5.png/pdf       # Spacing Bar Chart
│       ├── figure6.png/pdf       # Diversity vs Convergence
│       ├── figure7.png/pdf       # Execution Time
│       ├── figure8.png/pdf       # Statistical Heatmap
│       ├── 4d_visualization/     # Alternative 4D methods
│       │   ├── method1_3d_color_mapping.png/pdf
│       │   ├── method2_pairwise_scatter.png/pdf
│       │   ├── method3_parallel_coordinates.png/pdf
│       │   └── method4_heatmap_matrix.png/pdf
│       └── metric_examples/      # Performance metrics explanation
│           ├── comprehensive_metrics_comparison.png/pdf
│           ├── hypervolume_detailed.png/pdf
│           └── README_METRICS.md
│
├── docs/                         # Documentation
│   └── paper/                    # Paper-related documents
│       ├── results_section_v2.md             # Results section
│       ├── performance_metrics_explained.md  # Metrics guide
│       └── literature_visualization_comparison.md
│
├── data/                         # Data files
│   ├── food_data.csv             # Food database
│   └── nutrition_requirements.json
│
├── optimization_comparison_results.xlsx  # Experiment results
├── README.md                     # Main README
├── requirements.txt              # Python dependencies
└── .gitignore                    # Git ignore rules
```

## 🎨 Generating Figures

### Quick Start (Recommended)

**Generate ALL figures at once:**
```bash
python src/visualization/generate_all_figures.py
```

This will create:
- `results/figures/figure1-8.png/pdf` - Main paper figures
- `results/figures/table1.png/pdf` - Performance table
- `results/figures/4d_visualization/` - Alternative 4D methods
- `results/figures/metric_examples/` - Metrics explanation

### Individual Scripts

**1. Main Paper Figures (Figure 1-8, Table 1):**
```bash
python src/visualization/generate_figures.py
```

**2. 4D Visualization Alternatives:**
```bash
python src/visualization/visualize_4d_alternatives.py
```

**3. Performance Metrics Explanation:**
```bash
python src/visualization/visualize_metric_comparison.py
```

**4. Supplementary Figures:**
```bash
python src/visualization/additional_figures.py
```

## 📊 Figure Description

### Main Figures (for Paper)

| Figure | Description | Section |
|--------|-------------|---------|
| **Figure 1** | Convergence Plot (Hypervolume over generations) | 3.1 Optimization Process |
| **Figure 2** | 3D Pareto Front (SPEA2 solutions) | 3.2 Solution Distribution |
| **Figure 3** | Radar Chart (4-objective comparison) | 3.3 Overall Performance |
| **Table 1** | Performance Summary Table | 3.3 Overall Performance |
| **Figure 4** | Hypervolume Box Plots | 3.4.1 Optimization Quality |
| **Figure 5** | Spacing Bar Chart | 3.4.2 Solution Distribution |
| **Figure 6** | Diversity vs Convergence Scatter | 3.4.3 Trade-off Analysis |
| **Figure 7** | Execution Time Bar Chart | 3.4.4 Computational Efficiency |
| **Figure 8** | Statistical Heatmap (p-values) | 3.5 Statistical Validation |

### Supplementary Figures

| Directory/Figure | Description | Purpose |
|------------------|-------------|---------|
| **4d_visualization/** | 4 alternative 4D visualization methods | Methodological comparison |
| **metric_examples/** | Performance metrics explanation figures | Educational/Tutorial |

## 🔬 Running Experiments

**1. Run optimization comparison:**
```bash
python src/optimizer_comparison.py
```

**2. Analyze results:**
```bash
python src/statistical_analysis.py
```

**3. Generate all figures:**
```bash
python src/visualization/generate_all_figures.py
```

## 📦 Dependencies

Main dependencies (see `requirements.txt` for full list):
- Python 3.8+
- numpy
- pandas
- matplotlib
- seaborn
- scipy
- openpyxl

**Install all dependencies:**
```bash
pip install -r requirements.txt
```

## 📝 Key Files

### Code Organization

- **Core Algorithms**: `src/*_optimizer.py`
- **Evaluation**: `src/evaluation_function.py`, `src/performance_metrics.py`
- **Visualization**: `src/visualization/`
- **Analysis**: `src/statistical_analysis.py`

### Results

- **Figures**: `results/figures/`
- **Raw Data**: `optimization_comparison_results.xlsx`

### Documentation

- **Paper**: `docs/paper/results_section_v2.md`
- **Metrics Guide**: `docs/paper/performance_metrics_explained.md`
- **Visualization Guide**: `src/visualization/README.md`

## 🎯 Quick Reference

**Most Important Commands:**

```bash
# Generate all figures
python src/visualization/generate_all_figures.py

# View results
ls results/figures/

# Check figure quality
open results/figures/figure1.png  # macOS
xdg-open results/figures/figure1.png  # Linux
```

## 📊 Output Locations

**All generated content goes to:**
- Figures: `results/figures/`
- Data: `optimization_comparison_results.xlsx`
- Logs: Standard output

**No figures should be in:**
- ❌ `src/figures/` (removed)
- ❌ `docs/paper/metric_examples/` (moved)
- ❌ Root directory (cleaned)

---

**Project**: METOR (Multi-objective Enhanced Tool for Optimal meal Recommendation)  
**GitHub**: https://github.com/HeejeongH/Diet_optimization  
**Updated**: 2025-12-07
