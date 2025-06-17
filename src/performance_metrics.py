import numpy as np
import pandas as pd
from typing import List, Dict, Any
from Diet_class import Diet
from optimizer_base import DietOptimizer
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.chart import BarChart, Reference, LineChart, ScatterChart
from openpyxl.chart.label import DataLabelList

class PerformanceEvaluator:
    def __init__(self, diet_db: Diet, initial_diet: Diet, optimizers: Dict[str, DietOptimizer]):
        self.diet_db = diet_db
        self.initial_diet = initial_diet
        self.optimizers = optimizers
        self.metrics = ['hypervolume', 'spacing', 'diversity', 'convergence', 'execution_time']

    def calculate_hypervolume(self, solutions: List[Diet], optimizer: DietOptimizer) -> float:
        reference_point = np.array([-100, -100, 0, 0])
        fitnesses = np.array([optimizer.fitness(self.diet_db, solution) for solution in solutions])
        normalized_fitnesses = (fitnesses - reference_point) / (np.array([0, 0, 100, 100]) - reference_point)
        sorted_points = normalized_fitnesses[np.lexsort(normalized_fitnesses.T)]
        volume = 0
        for i in range(len(sorted_points)):
            if i == 0:
                volume += np.prod(sorted_points[i])
            else:
                volume += np.prod(np.maximum(0, sorted_points[i] - sorted_points[i-1]))
        return volume

    def calculate_spacing(self, solutions: List[Diet], optimizer: DietOptimizer) -> float:
        if len(solutions) < 2:
            return 0.0
        fitnesses = np.array([optimizer.fitness(self.diet_db, solution) for solution in solutions])
        distances = []
        for i in range(len(fitnesses)):
            min_dist = float('inf')
            for j in range(len(fitnesses)):
                if i != j:
                    dist = np.linalg.norm(fitnesses[i] - fitnesses[j])
                    min_dist = min(min_dist, dist)
            distances.append(min_dist)
        mean_dist = np.mean(distances)
        return np.sqrt(np.sum((distances - mean_dist)**2) / (len(distances) - 1))

    def calculate_diversity(self, solutions: List[Diet], optimizer: DietOptimizer) -> float:
        if len(solutions) < 2:
            return 0.0
        fitnesses = np.array([optimizer.fitness(self.diet_db, solution) for solution in solutions])
        max_spread = np.max(fitnesses, axis=0) - np.min(fitnesses, axis=0)
        return np.mean(max_spread)

    def calculate_convergence(self, solutions: List[Diet], optimizer: DietOptimizer) -> float:
        initial_fitness = np.array(optimizer.fitness(self.diet_db, self.initial_diet))
        final_fitnesses = np.array([optimizer.fitness(self.diet_db, solution) for solution in solutions])
        improvements = np.maximum(0, final_fitnesses - initial_fitness)
        return np.mean(improvements)

    def perform_statistical_analysis(self, results: Dict[str, Dict[str, List[float]]]) -> Dict:
        statistical_results = {}
        
        for metric in self.metrics:
            statistical_results[metric] = {
                'normality': {},
                'overall_test': {},
                'pairwise_tests': {}
            }
            
            algorithm_data = {name: results[name][metric] for name in self.optimizers.keys()}
            
            # 1. Normality test (Shapiro-Wilk)
            for alg_name, data in algorithm_data.items():
                statistic, p_value = stats.shapiro(data)
                statistical_results[metric]['normality'][alg_name] = {
                    'statistic': statistic,
                    'p_value': p_value
                }
            
            # 2. Overall test (Kruskal-Wallis)
            all_data = [data for data in algorithm_data.values()]
            h_statistic, p_value = stats.kruskal(*all_data)
            statistical_results[metric]['overall_test'] = {
                'test': 'Kruskal-Wallis',
                'statistic': h_statistic,
                'p_value': p_value
            }
            
            # 3. Pairwise comparisons (Mann-Whitney U)
            alg_names = list(self.optimizers.keys())
            for i in range(len(alg_names)):
                for j in range(i+1, len(alg_names)):
                    alg1, alg2 = alg_names[i], alg_names[j]
                    statistic, p_value = stats.mannwhitneyu(
                        algorithm_data[alg1],
                        algorithm_data[alg2],
                        alternative='two-sided'
                    )
                    statistical_results[metric]['pairwise_tests'][f'{alg1} vs {alg2}'] = {
                        'statistic': statistic,
                        'p_value': p_value
                    }
        
        return statistical_results

    def save_results_to_excel(self, results: Dict, statistics: Dict, statistical_analysis: Dict,
                            filename: str = 'optimization_results.xlsx'):
        wb = Workbook()
        
        # 1. Raw Results Sheet
        ws_raw = wb.active
        ws_raw.title = 'Raw Results'
        
        row = 1
        for metric in self.metrics:
            ws_raw.cell(row=row, column=1, value=metric.upper())
            row += 1
            
            # Headers
            headers = ['Algorithm'] + [f'Run {i+1}' for i in range(len(next(iter(results.values()))[metric]))]
            for col, header in enumerate(headers, 1):
                ws_raw.cell(row=row, column=col, value=header)
            
            # Data
            for alg_name in self.optimizers.keys():
                row += 1
                ws_raw.cell(row=row, column=1, value=alg_name)
                for col, value in enumerate(results[alg_name][metric], 2):
                    ws_raw.cell(row=row, column=col, value=value)
            
            row += 2

        # 2. Statistical Analysis Sheet
        ws_stats = wb.create_sheet('Statistical Analysis')
        
        row = 1
        for metric in self.metrics:
            # Metric title
            ws_stats.cell(row=row, column=1, value=f"{metric.upper()} Analysis")
            row += 1
            
            # Normality test results
            ws_stats.cell(row=row, column=1, value="Normality Test (Shapiro-Wilk)")
            row += 1
            
            for alg_name, results in statistical_analysis[metric]['normality'].items():
                ws_stats.cell(row=row, column=1, value=alg_name)
                ws_stats.cell(row=row, column=2, value=f"p-value: {results['p_value']:.4f}")
                row += 1
            
            row += 1
            
            # Overall test results
            ws_stats.cell(row=row, column=1, value="Overall Test (Kruskal-Wallis)")
            ws_stats.cell(row=row, column=2, 
                         value=f"p-value: {statistical_analysis[metric]['overall_test']['p_value']:.4f}")
            row += 2
            
            # Pairwise comparison results
            ws_stats.cell(row=row, column=1, value="Pairwise Comparisons (Mann-Whitney U)")
            row += 1
            
            for pair, results in statistical_analysis[metric]['pairwise_tests'].items():
                ws_stats.cell(row=row, column=1, value=pair)
                ws_stats.cell(row=row, column=2, value=f"p-value: {results['p_value']:.4f}")
                row += 1
            
            row += 2

        # 3. Summary Statistics Sheet
        ws_summary = wb.create_sheet('Summary Statistics')
        
        row = 1
        for metric in self.metrics:
            ws_summary.cell(row=row, column=1, value=metric.upper())
            row += 1
            
            # Headers
            headers = ['Algorithm', 'Mean', 'Std', 'Min', 'Max']
            for col, header in enumerate(headers, 1):
                ws_summary.cell(row=row, column=col, value=header)
            
            # Data
            for alg_name in self.optimizers.keys():
                row += 1
                stats = statistics[alg_name][metric]
                ws_summary.cell(row=row, column=1, value=alg_name)
                ws_summary.cell(row=row, column=2, value=stats['mean'])
                ws_summary.cell(row=row, column=3, value=stats['std'])
                ws_summary.cell(row=row, column=4, value=stats['min'])
                ws_summary.cell(row=row, column=5, value=stats['max'])
            
            row += 2
                    
        wb.save(filename)

    def run_comparison(self, generations: int = 100, num_runs: int = 30) -> None:
        results = {name: {metric: [] for metric in self.metrics} 
                  for name in self.optimizers.keys()}
        
        for name, optimizer in self.optimizers.items():
            print(f"\nEvaluating {name}...")
            
            for run in range(num_runs):
                import time
                start_time = time.time()
                
                solutions = optimizer.optimize(self.diet_db, self.initial_diet, generations)
                execution_time = time.time() - start_time
                
                results[name]['hypervolume'].append(
                    self.calculate_hypervolume(solutions, optimizer))
                results[name]['spacing'].append(
                    self.calculate_spacing(solutions, optimizer))
                results[name]['diversity'].append(
                    self.calculate_diversity(solutions, optimizer))
                results[name]['convergence'].append(
                    self.calculate_convergence(solutions, optimizer))
                results[name]['execution_time'].append(execution_time)
                
                print(f"Run {run + 1}/{num_runs} completed")

        # Calculate statistics
        statistics = {}
        for name in self.optimizers.keys():
            statistics[name] = {
                metric: {
                    'mean': np.mean(results[name][metric]),
                    'std': np.std(results[name][metric]),
                    'min': np.min(results[name][metric]),
                    'max': np.max(results[name][metric])
                }
                for metric in self.metrics
            }

        # Perform statistical analysis
        statistical_analysis = self.perform_statistical_analysis(results)

        # Save results
        self.save_results_to_excel(results, statistics, statistical_analysis)