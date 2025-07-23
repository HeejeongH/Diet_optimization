from optimizer_base import DietOptimizer
import numpy as np
from typing import List, Tuple, Dict
from Diet_class import Diet, Meal
from concurrent.futures import ThreadPoolExecutor
import heapq
from collections import defaultdict
import threading

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self._cache = {}
        self._access_count = {}
        self._total_access = 0
        self._lock = threading.Lock()  # 스레드 락 추가
        
    def get(self, key):
        with self._lock:  # 락으로 보호
            if key in self._cache:
                self._access_count[key] = self._total_access
                self._total_access += 1
                return self._cache[key]
            return None
        
    def put(self, key, value):
        with self._lock:  # 락으로 보호
            if len(self._cache) >= self.capacity:
                items_copy = list(self._access_count.items())
                min_key = min(items_copy, key=lambda x: x[1])[0]
                del self._cache[min_key]
                del self._access_count[min_key]
            self._cache[key] = value
            self._access_count[key] = self._total_access
            self._total_access += 1
            
    def clear(self):
        with self._lock:  # 락으로 보호
            self._cache.clear()
            self._access_count.clear()

class NSGA3Optimizer(DietOptimizer):
    def __init__(self, all_menus, nutrient_constraints, harmony_matrix):
        super().__init__(all_menus, nutrient_constraints, harmony_matrix)
        self.n_objectives = 4
        self._initialize_optimization()
        
    def _initialize_optimization(self):
        self.fitness_cache = LRUCache(1000)
        self.dominance_cache = LRUCache(1000)
        self.thread_pool = ThreadPoolExecutor(max_workers=4)
        self.batch_size = 16
        self.reference_points = self._generate_reference_points(4)
        self.ideal_point = None
        self.nadir_point = None

    def _generate_reference_points(self, divisions: int) -> np.ndarray:
        def generate_recursive(remaining_sum: float, n_remaining: int, curr_point: List[float]) -> List[List[float]]:
            if n_remaining == 1:
                return [curr_point + [remaining_sum]]
            
            points = []
            step = 1.0 / divisions
            for i in range(int(remaining_sum / step) + 1):
                value = i * step
                if value <= remaining_sum + 1e-10:
                    points.extend(generate_recursive(remaining_sum - value, n_remaining - 1, curr_point + [value]))
            return points

        # 참조점 생성
        points = generate_recursive(1.0, self.n_objectives, [])
        ref_points = np.array(points, dtype=np.float64)
        
        # 정규화
        norms = np.linalg.norm(ref_points, axis=1)
        zero_norm_mask = norms < 1e-10
        norms[zero_norm_mask] = 1.0
        ref_points = ref_points / norms[:, np.newaxis]
        
        return ref_points

    def _get_cached_fitness(self, diet: Diet, diet_db: Diet) -> np.ndarray:
        diet_hash = hash(str([(meal.menus, [menu.serving_ratio for menu in meal.menus]) for meal in diet.meals]))
        cached = self.fitness_cache.get(diet_hash)
        if cached is None:
            cached = np.array(self.fitness(diet_db, diet))
            self.fitness_cache.put(diet_hash, cached)
        return cached

    def _compute_dominance_matrix(self, fitnesses: np.ndarray) -> np.ndarray:
        n = len(fitnesses)
        dominance = np.zeros((n, n), dtype=bool)
        
        for i in range(n):
            for j in range(i + 1, n):
                i_dom_j = True
                j_dom_i = True
                
                for k in range(len(fitnesses[i])):
                    if fitnesses[i][k] < fitnesses[j][k]:
                        i_dom_j = False
                    if fitnesses[j][k] < fitnesses[i][k]:
                        j_dom_i = False
                    if not i_dom_j and not j_dom_i:
                        break
                        
                if i_dom_j and any(fitnesses[i] > fitnesses[j]):
                    dominance[i, j] = True
                elif j_dom_i and any(fitnesses[j] > fitnesses[i]):
                    dominance[j, i] = True
        
        return dominance

    def _fast_non_dominated_sort(self, fitnesses: np.ndarray) -> List[List[int]]:
        n = len(fitnesses)
        if n == 0:
            return [[]]

        dominance_matrix = np.zeros((n, n), dtype=bool)
        domination_count = np.zeros(n, dtype=int)
        dominated_solutions = [[] for _ in range(n)]

        for i in range(n):
            for j in range(i + 1, n):
                i_dominates = True
                j_dominates = True
                
                for k in range(len(fitnesses[i])):
                    if fitnesses[i][k] < fitnesses[j][k]:
                        i_dominates = False
                    if fitnesses[j][k] < fitnesses[i][k]:
                        j_dominates = False
                    if not i_dominates and not j_dominates:
                        break
                        
                if i_dominates and not j_dominates:
                    dominance_matrix[i, j] = True
                    domination_count[j] += 1
                    dominated_solutions[i].append(j)
                elif j_dominates and not i_dominates:
                    dominance_matrix[j, i] = True
                    domination_count[i] += 1
                    dominated_solutions[j].append(i)

        fronts = []
        current_front = []
        
        for i in range(n):
            if domination_count[i] == 0:
                current_front.append(i)
        
        if not current_front:
            return [[]]
            
        fronts.append(current_front)
        current = 0

        while True:
            next_front = []
            for i in fronts[current]:
                for j in dominated_solutions[i]:
                    domination_count[j] -= 1
                    if domination_count[j] == 0:
                        next_front.append(j)
            
            if not next_front:
                break
                
            fronts.append(next_front)
            current += 1

        return fronts

    def _normalize_objectives(self, fitnesses: np.ndarray) -> np.ndarray:
        if self.ideal_point is None:
            self.ideal_point = np.min(fitnesses, axis=0)
            self.nadir_point = np.max(fitnesses, axis=0)
        else:
            self.ideal_point = np.minimum(self.ideal_point, np.min(fitnesses, axis=0))
            self.nadir_point = np.maximum(self.nadir_point, np.max(fitnesses, axis=0))

        normalized = fitnesses.copy()
        normalized -= self.ideal_point
        
        denom = self.nadir_point - self.ideal_point
        denom[denom < 1e-10] = 1.0
        normalized /= denom
        
        return np.clip(normalized, 0, 1)

    def _associate_to_references(self, normalized_objectives: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        if len(normalized_objectives) == 0:
            return np.zeros(len(self.reference_points)), np.array([])

        distances = np.zeros((len(normalized_objectives), len(self.reference_points)))
        for i in range(len(normalized_objectives)):
            for j in range(len(self.reference_points)):
                diff = normalized_objectives[i] - self.reference_points[j]
                distances[i, j] = np.sum(diff * diff)

        associations = np.argmin(distances, axis=1)
        niche_counts = np.bincount(associations, minlength=len(self.reference_points))
        
        return niche_counts, distances

    def selection(self, population: List[Diet], fitnesses: np.ndarray) -> List[Diet]:
        if len(population) < 2:
            return population[:]
            
        target_size = self.population_size
        fronts = self._fast_non_dominated_sort(fitnesses)
        
        if not fronts[0]:
            return population[:target_size]
            
        selected = []
        front_idx = 0
        
        while front_idx < len(fronts) and len(selected) + len(fronts[front_idx]) <= target_size:
            selected.extend(fronts[front_idx])
            front_idx += 1
            
        if len(selected) < target_size and front_idx < len(fronts):
            remaining = target_size - len(selected)
            last_front = fronts[front_idx]
            
            last_front_fitnesses = fitnesses[last_front]
            normalized = self._normalize_objectives(last_front_fitnesses)
            
            niche_counts, distances = self._associate_to_references(normalized)
            
            if len(last_front) <= remaining:
                selected.extend(last_front)
            else:
                selected_from_last = []
                while len(selected_from_last) < remaining:
                    min_count = np.min(niche_counts)
                    min_niches = np.where(niche_counts == min_count)[0]
                    
                    for niche in min_niches:
                        if len(selected_from_last) >= remaining:
                            break
                            
                        candidates = []
                        for idx, sol_idx in enumerate(last_front):
                            if idx not in selected_from_last and \
                               np.argmin(distances[idx]) == niche:
                                candidates.append((distances[idx, niche], idx))
                        
                        if candidates:
                            best_idx = min(candidates, key=lambda x: x[0])[1]
                            selected_from_last.append(best_idx)
                            niche_counts[niche] += 1
                
                selected.extend([last_front[i] for i in selected_from_last])

        return [population[i] for i in selected]

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
        
        futures = []
        for _ in range(self.population_size - 1):
            futures.append(self.thread_pool.submit(self._create_initial_individual, initial_diet))
        population.extend([f.result() for f in futures])

        initial_fitness = self._get_cached_fitness(initial_diet, diet_db)

        for generation in range(generations):
            print(f"=== Generation {generation + 1}/{generations} ===")
            fitnesses = []
            for i in range(0, len(population), self.batch_size):
                batch = population[i:i + self.batch_size]
                batch_futures = [self.thread_pool.submit(self._get_cached_fitness, diet, diet_db) for diet in batch]
                fitnesses.extend([f.result() for f in batch_futures])
            fitnesses = np.array(fitnesses)

            # 종료 조건 체크 
            if self.check_termination(initial_fitness, population, diet_db):
                print(f"Termination condition met at generation {generation}")
                return self.get_final_solutions(diet_db)

            selected = self.selection(population, fitnesses)
            offspring = []
            for i in range(0, len(selected), 2):
                parent1 = selected[i]
                parent2 = selected[min(i + 1, len(selected) - 1)]
                
                child1 = self.crossover(parent1, parent2)
                child2 = self.crossover(parent2, parent1)
                
                if np.random.random() < self.mutation_prob:
                    child1 = self.mutate(child1)
                if np.random.random() < self.mutation_prob:
                    child2 = self.mutate(child2)
                    
                offspring.extend([child1, child2])

            population = selected + offspring[:self.population_size - len(selected)]

            # 주기적 캐시 정리
            if generation % 10 == 0:
                self.fitness_cache = LRUCache(1000)
                self.dominance_cache = LRUCache(1000)

        # 최종 해 선택
        fitnesses = np.array([self._get_cached_fitness(diet, diet_db) for diet in population])
        fronts = self._fast_non_dominated_sort(fitnesses)
        final_solutions = [population[i] for i in fronts[0][:5]]
        return self.get_final_solutions(diet_db)