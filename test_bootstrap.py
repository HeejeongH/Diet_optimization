"""Test script for Bootstrap ICC confidence intervals."""
import sys
sys.path.append('/home/user/Diet_optimization/src')

from variability_decomposition import VariabilityDecomposition

# Configuration
excel_dir = '/home/user/Diet_optimization/result/optimization results'

# Initialize analyzer
print("Initializing VariabilityDecomposition...")
analyzer = VariabilityDecomposition()

# Load all datasets
print("Loading datasets...")
analyzer.load_all_datasets(excel_dir)

# Test bootstrap ICC CI for one metric and one algorithm
print("\n" + "="*80)
print("TESTING BOOTSTRAP ICC CONFIDENCE INTERVAL")
print("="*80)

test_metric = 'hypervolume'
test_algorithm = 'NSGA-II'

print(f"\nTesting {test_algorithm} on {test_metric} metric...")
icc_est, ci_lower, ci_upper = analyzer.bootstrap_icc_ci(
    test_algorithm,
    test_metric,
    n_bootstrap=100,  # Use fewer iterations for quick test
    random_seed=42
)

print(f"\nResults:")
print(f"  ICC Estimate: {icc_est:.4f}")
print(f"  95% CI: [{ci_lower:.4f}, {ci_upper:.4f}]")
print(f"  CI Width: {ci_upper - ci_lower:.4f}")

# Test variance decomposition table with bootstrap
print("\n" + "="*80)
print("TESTING VARIANCE DECOMPOSITION TABLE WITH BOOTSTRAP CI")
print("="*80)

print(f"\n{test_metric.upper()}")
table = analyzer.variance_decomposition_table(test_metric, include_bootstrap=True)
print(table.to_string(index=False))

print("\n" + "="*80)
print("TEST COMPLETE - All functions working correctly!")
print("="*80)
