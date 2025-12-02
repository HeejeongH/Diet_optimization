# Research Paper Documentation

## 📄 Paper Information

**Title:** Multi-objective Enhanced Tool for Optimal meal Recommendation (METOR)

**Status:** Under Review

---

## 📊 Generated Figures

All figures for the paper are located in `../../visualization/figures/`:

### Main Figures

1. **Figure 1: Performance Radar Chart** (`figure1_radar_chart.png`)
   - Multi-dimensional performance comparison
   - Shows all 5 metrics for 4 algorithms

2. **Figure 2: Hypervolume Box Plots** (`figure2_hypervolume_boxplots.png`)
   - Distribution of hypervolume across 10 runs
   - Statistical comparison

3. **Figure 3: Spacing Comparison** (`figure3_spacing_comparison.png`)
   - Solution distribution quality
   - Highlights NSGA-II superiority

4. **Figure 4: Diversity vs Convergence** (`figure4_diversity_convergence.png`)
   - Trade-off analysis between two objectives
   - Shows Pareto frontier characteristics

5. **Figure 5: Execution Time Comparison** (`figure5_execution_time.png`)
   - Computational efficiency
   - Demonstrates SPEA2's speed advantage

6. **Figure 6: Statistical Significance Heatmap** (`figure6_significance_heatmap.png`)
   - P-values from Mann-Whitney U tests
   - Shows pairwise algorithm comparisons

---

## 🔄 Regenerating Figures

To regenerate all figures:

```bash
cd ../../visualization
python generate_figures.py
```

Figures will be created in both formats:
- **PNG** (300 DPI) - For Word documents
- **PDF** (vector) - For LaTeX documents

---

## 📈 Key Results

### Performance Summary (Mean ± Std)

| Metric | NSGA-II | NSGA-III | SPEA2 | ε-MOEA |
|--------|---------|----------|-------|--------|
| **Hypervolume** | 0.409±0.012 | 0.401±0.008 | **0.426±0.026** | 0.370±0.048 |
| **Spacing** | **0.604±0.985** | 1.367±3.139 | 5.415±5.266 | 4.785±2.343 |
| **Diversity** | 1.132±0.614 | 1.572±2.137 | 6.236±4.556 | **9.449±3.058** |
| **Convergence** | 0.334±0.105 | 0.383±0.115 | **0.703±0.348** | 0.430±0.149 |
| **Time (sec)** | 1423.5±579.5 | 1145.4±26.0 | **992.1±576.1** | 1889.8±477.0 |

**Bold:** Best performance for each metric

### Statistical Significance

- **Hypervolume**: p = 0.642 (no significant difference)
- **Spacing**: p = 0.011 (NSGA-II significantly better)
- **Diversity**: p < 0.001 (ε-MOEA significantly better)
- **Convergence**: p < 0.001 (SPEA2 significantly better)
- **Time**: p < 0.001 (SPEA2 significantly faster)

---

## 🎯 Algorithm Recommendations

### For Operational Deployment
**Recommendation: SPEA2**
- Fastest execution (16.5 minutes)
- Highest convergence (0.703)
- Balanced performance

### For Decision Support
**Recommendation: NSGA-II**
- Best solution distribution (spacing: 0.604)
- Stable and reliable
- Well-studied algorithm

### For Exploratory Analysis
**Recommendation: ε-MOEA**
- Highest diversity (9.449)
- Explores wider solution space
- Good for research purposes

---

## 📝 Citation

```bibtex
@article{han2024diet,
  title={Multi-objective Enhanced Tool for Optimal meal Recommendation},
  author={Han, Heejeong and others},
  journal={Journal Name},
  year={2024},
  note={Under review}
}
```

---

## 📧 Contact

For questions about the paper or results:
- GitHub Issues: [Create an issue](https://github.com/HeejeongH/Diet_optimization/issues)
