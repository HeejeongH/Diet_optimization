from optimizer_base import DietOptimizer
import numpy as np
from typing import List, Tuple, Dict, Set
from Diet_class import Diet, Meal
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor

class NSGA2Optimizer(DietOptimizer):
    def __init__(self, all_menus, nutrient_constraints, harmony_matrix):
        super().__init__(all_menus, nutrient_constraints, harmony_matrix)
        self._initialize_optimization()
        
    def _initialize_optimization(self):
        self.fitness_cache = {}
        self.dominance_cache = {}
        self.thread_pool = ThreadPoolExecutor(max_workers=4)
        self.batch_size = 100

    def _get_cached_fitness(self, diet: Diet, diet_db: Diet) -> np.ndarray:
        diet_hash = hash(str([(meal.menus, [menu.serving_ratio for menu in meal.menus]) for meal in diet.meals]))
        if diet_hash not in self.fitness_cache:
            self.fitness_cache[diet_hash] = np.array(self.fitness(diet_db, diet))
        return self.fitness_cache[diet_hash]

    def _batch_process_fitness(self, population: List[Diet], diet_db: Diet) -> np.ndarray:
        futures = []
        for i in range(0, len(population), self.batch_size):
            batch = population[i:i + self.batch_size]
            for diet in batch:
                futures.append(self.thread_pool.submit(self._get_cached_fitness, diet, diet_db))
        
        return np.array([f.result() for f in futures])

    def _compute_dominance_matrix(self, fitnesses: np.ndarray) -> np.ndarray:
        n = len(fitnesses)
        dominance = np.zeros((n, n), dtype=bool)
        
        for i in range(n):
            dominance[i] = np.all(fitnesses[i] >= fitnesses, axis=1) & np.any(fitnesses[i] > fitnesses, axis=1)
            dominance[i, i] = False
            
        return dominance

    def _fast_non_dominated_sort(self, population: List[Diet], fitnesses: np.ndarray) -> List[List[int]]:
        if len(population) == 0:
            return [[]]

        cache_key = hash(fitnesses.tobytes())
        if cache_key in self.dominance_cache:
            dominance_matrix = self.dominance_cache[cache_key]
        else:
            dominance_matrix = self._compute_dominance_matrix(fitnesses)
            self.dominance_cache[cache_key] = dominance_matrix

        domination_counts = np.sum(dominance_matrix.T, axis=0)
        dominated_solutions = [np.where(row)[0].tolist() for row in dominance_matrix]

        fronts = [[]]
        fronts[0] = np.where(domination_counts == 0)[0].tolist()
        
        current = 0
        while fronts[current]:
            next_front = []
            for i in fronts[current]:
                for j in dominated_solutions[i]:
                    domination_counts[j] -= 1
                    if domination_counts[j] == 0:
                        next_front.append(j)
            current += 1
            fronts.append(next_front)

        if not fronts[-1]:
            fronts.pop()

        return fronts

    def _calculate_crowding_distance(self, fitnesses: np.ndarray) -> np.ndarray:
        n_points = len(fitnesses)
        if n_points <= 2:
            return np.full(n_points, np.inf)
            
        n_objectives = fitnesses.shape[1]
        distances = np.zeros(n_points)
        
        for obj in range(n_objectives):
            sorted_idx = np.argsort(fitnesses[:, obj])
            obj_range = fitnesses[sorted_idx[-1], obj] - fitnesses[sorted_idx[0], obj]
            
            if obj_range > 1e-10:
                distances[sorted_idx[0]] = np.inf
                distances[sorted_idx[-1]] = np.inf
                
                if n_points > 2:
                    norm_diffs = np.diff(fitnesses[sorted_idx, obj]) / obj_range
                    distances[sorted_idx[1:-1]] += norm_diffs[:-1] + norm_diffs[1:]
        
        return distances

    def selection(self, population: List[Diet], fitnesses: np.ndarray) -> List[Diet]:
        if len(population) < 2:
            return population[:]
            
        target_size = self.population_size
        fronts = self._fast_non_dominated_sort(population, fitnesses)
        selected = []
        current_front = 0

        while current_front < len(fronts) and len(selected) + len(fronts[current_front]) <= target_size:
            selected.extend(fronts[current_front])
            current_front += 1

        if len(selected) < target_size and current_front < len(fronts):
            last_front = fronts[current_front]
            last_front_fitnesses = fitnesses[last_front]
            crowding_distances = self._calculate_crowding_distance(last_front_fitnesses)
            
            sorted_indices = np.argsort(crowding_distances)[::-1]
            remaining = target_size - len(selected)
            selected.extend([last_front[i] for i in sorted_indices[:remaining]])

        return [population[i] for i in selected]

    def _create_offspring_batch(self, parents: List[Diet],  mutation_prob: float) -> List[Diet]:
        offspring = []
        for i in range(0, len(parents), 2):
            parent1 = parents[i]
            parent2 = parents[min(i + 1, len(parents) - 1)]
            
            child1 = self.crossover(parent1, parent2)
            child2 = self.crossover(parent2, parent1)
            
            if np.random.random() < mutation_prob:
                child1 = self.mutate(child1)
            if np.random.random() < mutation_prob:
                child2 = self.mutate(child2)
                
            offspring.extend([child1, child2])
        return offspring

    def _create_initial_individual(self, base_diet):
        mutated = self.mutate(base_diet)
        for meal in mutated.meals:
            for menu in meal.menus:
                menu.serving_ratio = np.random.uniform(0.6, 0.9)
        return mutated

    def optimize(self, diet_db: Diet, initial_diet: Diet, generations: int = 100) -> List[Diet]:
        # 초기화
        self.good_solutions_archive.clear()
        self.backup_solutions.clear()
        self.constraint_solutions.clear()
        
        population = [initial_diet]
        self.fitness_cache.clear()
        self.dominance_cache.clear()
        
        futures = []
        for _ in range(self.population_size - 1):
            futures.append(self.thread_pool.submit(self._create_initial_individual, initial_diet))
        population.extend([f.result() for f in futures])

        initial_fitness = self._get_cached_fitness(initial_diet, diet_db)
        best_fitness = float('-inf')
        patience = 10
        no_improvement_count = 0

        for generation in range(generations):
            print(f"=== Generation {generation + 1}/{generations} ===")
            fitnesses = self._batch_process_fitness(population, diet_db)
            
            current_best = np.max(fitnesses[:, 0])
            if current_best > best_fitness:
                best_fitness = current_best
                no_improvement_count = 0
            else:
                no_improvement_count += 1

            # 종료 조건 확인
            if self.check_termination(initial_fitness, population, diet_db):
                print(f"Termination condition met at generation {generation}")
                return self.get_final_solutions(diet_db)
            
            mutation_prob = self.mutation_prob * (1 + 0.5 * (no_improvement_count / patience))
            selected_population = self.selection(population, fitnesses)
            offspring_population = []
            for i in range(0, len(selected_population), self.batch_size):
                batch = selected_population[i:i + self.batch_size]
                offspring_batch = self._create_offspring_batch(batch, mutation_prob)
                offspring_population.extend(offspring_batch)
            population = selected_population + offspring_population[:self.population_size - len(selected_population)]

            if generation % 10 == 0:
                if len(self.fitness_cache) > 1000:
                    self.fitness_cache.clear()
                if len(self.dominance_cache) > 1000:
                    self.dominance_cache.clear()

        print(f"Maximum generations reached. Found {len(population)} solutions.")
        return self.get_final_solutions(diet_db)

    def _select_diverse_solutions(self, population: List[Diet], fitnesses: np.ndarray, n_solutions: int = 5) -> List[Diet]:
        fronts = self._fast_non_dominated_sort(population, fitnesses)
        
        if not fronts[0]:
            return population[:n_solutions]
            
        first_front = fronts[0]
        front_fitnesses = fitnesses[first_front]
        distances = self._calculate_crowding_distance(front_fitnesses)
        
        sorted_indices = np.argsort(distances)[::-1]
        selected_indices = sorted_indices[:n_solutions]
        
        return [population[first_front[i]] for i in selected_indices]