# Usage Guide

Complete guide for using the Diet Optimization System.

---

## 🚀 Quick Start

### 1. Installation

```bash
# Clone repository
git clone https://github.com/HeejeongH/Diet_optimization.git
cd Diet_optimization

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run Web Application

```bash
streamlit run src/app.py
```

Open browser at: `http://localhost:8501`

---

## 📊 Generate Paper Figures

```bash
cd visualization
python generate_figures.py
```

Figures will be saved in `visualization/figures/` in both PNG (300 DPI) and PDF formats.

---

## 🔬 Run Optimization Experiments

### Example: SPEA2 Optimization

```python
from src.load_data import load_and_process_data, create_nutrient_constraints, load_all_menus
from src.spea2_optimizer import SPEA2Optimizer
from src.Diet_class import set_servings

# Set number of servings (default: 55)
set_servings(55)

# Load data
diet_db_path = 'data/sarang_DB/processed_DB/DIET_jeongseong.xlsx'
menu_db_path = 'data/sarang_DB/processed_DB/Menu_ingredient_nutrient_jeongseong.xlsx'
ingredient_db_path = 'data/sarang_DB/processed_DB/Ingredient_Price_jeongseong.xlsx'

diet_db, initial_diet, harmony_matrix = load_and_process_data(
    diet_db_path, menu_db_path, ingredient_db_path
)

all_menus = load_all_menus(menu_db_path, ingredient_db_path)
nutrient_constraints = create_nutrient_constraints()

# Initialize optimizer
optimizer = SPEA2Optimizer(
    all_menus=all_menus,
    nutrient_constraints=nutrient_constraints,
    harmony_matrix=harmony_matrix,
    population_size=150,
    archive_size=100
)

# Run optimization
result_diets = optimizer.optimize(
    diet_db=diet_db,
    initial_diet=initial_diet,
    generations=100
)

print(f"Generated {len(result_diets)} optimized diets")
```

---

## 🎯 Algorithm Comparison

### Run All Algorithms

```python
from src.nsga2_optimizer import NSGA2Optimizer
from src.nsga3_optimizer import NSGA3Optimizer
from src.spea2_optimizer import SPEA2Optimizer
from src.emoea_optimizer import EpsilonMOEAOptimizer
from src.performance_metrics import PerformanceEvaluator

# Initialize all optimizers
optimizers = {
    'NSGA-II': NSGA2Optimizer(all_menus, nutrient_constraints, harmony_matrix),
    'NSGA-III': NSGA3Optimizer(all_menus, nutrient_constraints, harmony_matrix),
    'SPEA2': SPEA2Optimizer(all_menus, nutrient_constraints, harmony_matrix),
    'ε-MOEA': EpsilonMOEAOptimizer(all_menus, nutrient_constraints, harmony_matrix)
}

# Run comparison (10 runs per algorithm)
evaluator = PerformanceEvaluator(diet_db, initial_diet, optimizers)
results = evaluator.run_comparison(generations=100, num_runs=10)

# Export results
evaluator.export_to_excel('results/comparison.xlsx')
```

---

## 📁 Data Format

### Diet Database (DIET_jeongseong.xlsx)

**Columns:**
- `week_num`: Week number (1-13)
- `day`: Day of week (월, 화, 수, 목, 금, 토, 일)
- `밥, 국, 찌개, 반찬1-5`: Menu items for each meal component

**Example:**
```
week_num | day | 밥    | 국      | 반찬1    | ...
---------|-----|-------|---------|----------|----
1        | 월  | 쌀밥  | 미역국  | 계란찜   | ...
```

### Menu Database (Menu_ingredient_nutrient_jeongseong.xlsx)

**Sheet 1: 'ingredient'**
- `Menu`: Menu item name
- `Ingredient`: Ingredient name
- `Amount_g`: Amount in grams

**Sheet 2: 'nutrient'**
- `Menu`: Menu item name
- `에너지(kcal)`, `탄수화물(g)`, `단백질(g)`, etc.

**Sheet 3: 'category'**
- `Menu`: Menu item name
- `Category`: Menu category (main, soup, side, etc.)

### Ingredient Prices (Ingredient_Price_jeongseong.xlsx)

**Columns:**
- `재료`: Ingredient name
- `단가(원/g)`: Price per gram
- `용량(g)`: Package size in grams

---

## 🔧 Configuration

### Nutritional Constraints

Modify constraints in your code:

```python
from src.Diet_class import NutrientConstraints

constraints = NutrientConstraints(
    min_values={
        '에너지(kcal)': 1600,
        '탄수화물(g)': 200,
        '단백질(g)': 50,
        '지방(g)': 35,
        '식이섬유(g)': 20,
        # Add more nutrients...
    },
    max_values={
        '에너지(kcal)': 2000,
        '탄수화물(g)': 280,
        '단백질(g)': 70,
        '지방(g)': 55,
        '식이섬유(g)': 30,
        # Add more nutrients...
    },
    weights={
        '에너지(kcal)': 1.0,
        '탄수화물(g)': 0.8,
        '단백질(g)': 1.0,
        # Add more nutrients...
    }
)
```

### Algorithm Parameters

```python
optimizer = SPEA2Optimizer(
    all_menus=all_menus,
    nutrient_constraints=nutrient_constraints,
    harmony_matrix=harmony_matrix,
    population_size=150,      # Population size
    archive_size=100,          # Archive size
    mutation_prob=0.1,         # Mutation probability
    crossover_prob=0.9,        # Crossover probability
    early_stopping_patience=20 # Early stopping patience
)
```

---

## 📊 Performance Metrics

The system evaluates solutions using:

1. **Hypervolume** - Volume of objective space dominated
2. **Spacing** - Uniformity of solution distribution
3. **Diversity** - Variety using Simpson index
4. **Convergence** - Improvement from initial population
5. **Execution Time** - Computational efficiency

---

## 🐛 Troubleshooting

### Common Issues

**Issue:** `FileNotFoundError` when loading data
```bash
# Make sure you're in the correct directory
cd Diet_optimization
python src/app.py
```

**Issue:** Import errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

**Issue:** Memory error during optimization
```python
# Reduce population size
optimizer = SPEA2Optimizer(
    ...,
    population_size=100,  # Reduced from 150
    archive_size=75       # Reduced from 100
)
```

---

## 📚 Additional Resources

- [Main README](../README.md) - Project overview
- [Paper Documentation](paper/README.md) - Research results
- [GitHub Issues](https://github.com/HeejeongH/Diet_optimization/issues) - Report problems

---

**Need Help?** Create an issue on GitHub or contact the development team.
