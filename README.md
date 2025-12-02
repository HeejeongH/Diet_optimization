# Diet Optimization for Elderly Care Facilities

**Multi-objective Enhanced Tool for Optimal meal Recommendation (METOR)**

A comprehensive multi-objective optimization system for generating balanced, cost-effective, and diverse weekly meal plans for elderly care facilities.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Research Paper](#research-paper)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

This project implements a **multi-objective evolutionary algorithm (MOEA)** framework for optimizing weekly meal plans in elderly care facilities. The system simultaneously optimizes four competing objectives:

1. **Nutritional Adequacy** - Meeting daily nutritional requirements
2. **Cost Effectiveness** - Minimizing food costs while maintaining quality
3. **Menu Harmony** - Ensuring culturally appropriate food combinations
4. **Dietary Diversity** - Providing variety to prevent menu fatigue

### Algorithms Implemented

- **NSGA-II** - Non-dominated Sorting Genetic Algorithm II
- **NSGA-III** - NSGA-III with reference point-based selection
- **SPEA2** - Strength Pareto Evolutionary Algorithm 2
- **ε-MOEA** - Epsilon Multi-Objective Evolutionary Algorithm

---

## ✨ Features

### Core Functionality

- 🍽️ **Multi-objective Optimization** - Simultaneous optimization of 4 objectives
- 📊 **Performance Comparison** - Comprehensive algorithm benchmarking
- 📈 **Statistical Analysis** - Rigorous statistical validation
- 🎨 **Visualization** - Publication-quality figures and charts
- 💾 **Data Export** - Excel reports and CSV outputs

### Advanced Features

- ⚙️ **Flexible Serving Ratios** - Adjustable portion sizes (0.6-1.0)
- 🔄 **Adaptive Termination** - Smart stopping criteria
- 💪 **Parallel Processing** - Multi-threaded fitness evaluation
- 📦 **Caching System** - LRU cache for performance optimization
- 🎯 **Harmony Matrix** - Cultural food pairing validation

---

## 📁 Project Structure

```
diet_optimization/
│
├── src/                          # Source code
│   ├── Diet_class.py             # Core data structures (Menu, Meal, Diet)
│   ├── load_data.py              # Data loading and preprocessing
│   ├── evaluation_function.py   # Objective function implementations
│   ├── optimizer_base.py         # Base optimizer class
│   ├── nsga2_optimizer.py        # NSGA-II implementation
│   ├── nsga3_optimizer.py        # NSGA-III implementation
│   ├── spea2_optimizer.py        # SPEA2 implementation
│   ├── emoea_optimizer.py        # ε-MOEA implementation
│   ├── performance_metrics.py    # Performance evaluation metrics
│   └── app.py                    # Streamlit web application
│
├── visualization/                # Figure generation
│   └── generate_figures.py       # Paper figures generator
│
├── data/                         # Data files
│   ├── menu_db.xlsx              # Menu database (nutrients, ingredients)
│   └── ingredient_prices.xlsx    # Ingredient pricing data
│
├── config/                       # Configuration files
│   └── optimization_config.json  # Algorithm parameters
│
├── results/                      # Optimization results
│   ├── optimization_results.xlsx # Raw performance data
│   └── final_comparison.xlsx     # Statistical analysis
│
├── figures/                      # Generated figures (auto-created)
│   ├── figure1_radar_chart.png
│   ├── figure2_hypervolume_boxplots.png
│   ├── figure3_spacing_comparison.png
│   ├── figure4_diversity_convergence.png
│   ├── figure5_execution_time.png
│   └── figure6_significance_heatmap.png
│
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

---

## 🚀 Installation

### Prerequisites

- Python 3.10 or higher
- pip package manager

### Step 1: Clone the Repository

```bash
git clone https://github.com/HeejeongH/Diet_optimization.git
cd Diet_optimization
```

### Step 2: Create Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Required Packages

```
numpy>=1.24.0
pandas>=2.0.0
matplotlib>=3.7.0
seaborn>=0.12.0
scipy>=1.10.0
openpyxl>=3.1.0
streamlit>=1.28.0  # For web UI
```

---

## 🎬 Quick Start

### Generate All Figures for Paper

```bash
cd visualization
python generate_figures.py
```

This will create 6 publication-quality figures in the `figures/` directory:
- PNG format (300 DPI) for Word documents
- PDF format (vector) for LaTeX documents

### Run Optimization

```python
from src.load_data import load_menu_database, load_diet_database
from src.nsga2_optimizer import NSGA2Optimizer
from src.spea2_optimizer import SPEA2Optimizer

# Load data
menu_db_path = 'data/menu_db.xlsx'
ingredient_db_path = 'data/ingredient_prices.xlsx'
all_menus = load_menu_database(menu_db_path, ingredient_db_path)

# Initialize optimizer
optimizer = SPEA2Optimizer(all_menus, nutrient_constraints, harmony_matrix)

# Run optimization
optimized_diets = optimizer.optimize(diet_db, initial_diet, generations=100)
```

### Launch Web Application

```bash
streamlit run src/app.py
```

Open browser at `http://localhost:8501`

---

## 📖 Usage

### 1. Data Preparation

#### Menu Database Format (`menu_db.xlsx`)

**Sheet: 'ingredient'**
| Menu | Ingredient | Amount_g |
|------|-----------|----------|
| 쌀밥 | 쌀 | 100 |
| 미역국 | 미역 | 20 |

**Sheet: 'nutrient'**
| Menu | 에너지(kcal) | 탄수화물(g) | 단백질(g) | 지방(g) | 식이섬유(g) |
|------|-----------|----------|---------|--------|----------|
| 쌀밥 | 300 | 65 | 6 | 1 | 1.5 |

**Sheet: 'category'**
| Menu | Category |
|------|----------|
| 쌀밥 | main |
| 미역국 | soup |

#### Ingredient Prices Format (`ingredient_prices.xlsx`)

| Ingredient | 단가(원/g) | 용량(g) |
|-----------|----------|--------|
| 쌀 | 5.0 | 5000 |
| 미역 | 15.0 | 100 |

### 2. Configure Optimization

```python
from src.Diet_class import NutrientConstraints

# Set nutritional constraints
nutrient_constraints = NutrientConstraints(
    min_values={
        '에너지(kcal)': 1600,
        '탄수화물(g)': 200,
        '단백질(g)': 50,
        '지방(g)': 35,
        '식이섬유(g)': 20
    },
    max_values={
        '에너지(kcal)': 2000,
        '탄수화물(g)': 280,
        '단백질(g)': 70,
        '지방(g)': 55,
        '식이섬유(g)': 30
    },
    weights={
        '에너지(kcal)': 1.0,
        '탄수화물(g)': 0.8,
        '단백질(g)': 1.0,
        '지방(g)': 0.6,
        '식이섬유(g)': 0.8
    }
)
```

### 3. Run Performance Comparison

```python
from src.performance_metrics import PerformanceEvaluator

# Initialize evaluator
evaluator = PerformanceEvaluator(diet_db, initial_diet, optimizers)

# Run comparison (10 runs per algorithm)
results = evaluator.run_comparison(generations=100, num_runs=10)

# Export results
evaluator.export_to_excel('results/comparison_results.xlsx')
```

### 4. Generate Figures

```bash
cd visualization
python generate_figures.py
```

**Generated Figures:**
- `figure1_radar_chart.png` - Multi-dimensional performance comparison
- `figure2_hypervolume_boxplots.png` - Hypervolume distribution
- `figure3_spacing_comparison.png` - Spacing metric with significance
- `figure4_diversity_convergence.png` - Trade-off analysis
- `figure5_execution_time.png` - Computational efficiency
- `figure6_significance_heatmap.png` - Statistical significance matrix

---

## 📊 Research Paper

### Performance Summary

| Metric | NSGA-II | NSGA-III | SPEA2 | ε-MOEA |
|--------|---------|----------|-------|--------|
| **Hypervolume** | 0.409±0.012 | 0.401±0.008 | **0.426±0.026** | 0.370±0.048 |
| **Spacing** | **0.604±0.985** | 1.367±3.139 | 5.415±5.266 | 4.785±2.343 |
| **Diversity** | 1.132±0.614 | 1.572±2.137 | 6.236±4.556 | **9.449±3.058** |
| **Convergence** | 0.334±0.105 | 0.383±0.115 | **0.703±0.348** | 0.430±0.149 |
| **Time (sec)** | 1423.5±579.5 | 1145.4±26.0 | **992.1±576.1** | 1889.8±477.0 |

**Note:** Bold values indicate best performance for each metric.

### Key Findings

1. **No universal winner** - Each algorithm excels in different dimensions
2. **SPEA2 recommended** for operational deployment due to:
   - Fastest execution time (16.5 minutes)
   - Highest convergence (0.703)
   - Balanced performance across all metrics
3. **NSGA-II superior** for decision support (best spacing: 0.604)
4. **ε-MOEA best** for exploration (highest diversity: 9.449)

### Statistical Validation

- **Hypervolume**: No significant differences (Kruskal-Wallis p = 0.642)
- **Spacing**: Significant differences (p = 0.011), NSGA-II > SPEA2/ε-MOEA
- **Diversity**: Highly significant (p < 0.001), ε-MOEA > all others
- **Convergence**: Highly significant (p < 0.001), SPEA2 > all others
- **Time**: Highly significant (p < 0.001), SPEA2 fastest

---

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines.

### How to Contribute

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Areas for Contribution

- 🐛 Bug fixes and improvements
- 📚 Documentation enhancements
- 🔬 New optimization algorithms
- 🎨 Visualization improvements
- 🧪 Additional test cases

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Authors

- **Heejeong Han** - *Initial work* - [HeejeongH](https://github.com/HeejeongH)

---

## 📧 Contact

For questions or collaborations:
- Email: [your.email@example.com]
- GitHub Issues: [Create an issue](https://github.com/HeejeongH/Diet_optimization/issues)

---

## 🙏 Acknowledgments

- Jeongseon Nursing Home for providing real-world data
- Korean Dietary Reference Intakes (KDRIs) 2020 for nutritional guidelines
- Research team members for their contributions

---

## 📚 Citation

If you use this software in your research, please cite:

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

## 🔄 Version History

- **v1.0.0** (2024-12) - Initial release
  - Four MOEA implementations
  - Performance comparison framework
  - Figure generation tool
  - Web application interface

---

**Happy Optimizing! 🍽️**
