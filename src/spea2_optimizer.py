from optimizer_base import DietOptimizer
import numpy as np
from typing import List, Tuple, Dict
from Diet_class import Diet, Meal
from concurrent.futures import ThreadPoolExecutor
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

class SPEA2Optimizer(DietOptimizer):
    def __init__(self, all_menus, nutrient_constraints, harmony_matrix):
        super().__init__(all_menus, nutrient_constraints, harmony_matrix)
        self._initialize_optimization()

    def _initialize_optimization(self):
        self.archive = []
        self.fitness_cache = LRUCache(1000)
        self.distance_cache = LRUCache(1000)
        self.strength_cache = LRUCache(1000)
        self.thread_pool = ThreadPoolExecutor(max_workers=4)
        self.batch_size = 16

    def _get_cached_fitness(self, diet: Diet, diet_db: Diet) -> np.ndarray:
        diet_hash = hash(str([(meal.menus, [menu.serving_ratio for menu in meal.menus]) for meal in diet.meals]))
        cached = self.fitness_cache.get(diet_hash)
        if cached is None:
            cached = np.array(self.fitness(diet_db, diet))
            self.fitness_cache.put(diet_hash, cached)
        return cached

    def _compute_dominance_relations(self, fitnesses: np.ndarray) -> np.ndarray:
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

    def _calculate_strength(self, fitnesses: np.ndarray) -> np.ndarray:
        cache_key = hash(fitnesses.tobytes())
        cached = self.strength_cache.get(cache_key)
        if cached is not None:
            return cached

        dominance = self._compute_dominance_relations(fitnesses)
        strength = np.sum(dominance, axis=1)
        self.strength_cache.put(cache_key, strength)
        
        return strength

    def _calculate_raw_fitness(self, fitnesses: np.ndarray, strength: np.ndarray) -> np.ndarray:
        dominance = self._compute_dominance_relations(fitnesses)
        raw_fitness = np.zeros(len(fitnesses))
        
        for i in range(len(fitnesses)):
            dominated_by = np.where(dominance[:, i])[0]
            raw_fitness[i] = np.sum(strength[dominated_by])
            
        return raw_fitness

    def _calculate_distances(self, fitnesses: np.ndarray) -> np.ndarray:
        cache_key = hash(fitnesses.tobytes())
        cached = self.distance_cache.get(cache_key)
        if cached is not None:
            return cached

        n = len(fitnesses)
        distances = np.zeros((n, n))
        
        for i in range(n):
            diff = fitnesses[i] - fitnesses
            distances[i] = np.sqrt(np.sum(diff * diff, axis=1))
            distances[i, i] = np.inf
            
        self.distance_cache.put(cache_key, distances)
        return distances

    def _calculate_density(self, distances: np.ndarray) -> np.ndarray:
        k = int(np.sqrt(len(distances)))
        density = np.zeros(len(distances))
        
        for i in range(len(distances)):
            kth_distance = np.partition(distances[i], k)[k]
            density[i] = 1.0 / (kth_distance + 2.0)
            
        return density

    def _environmental_selection(self, population: List[Diet], fitnesses: np.ndarray) -> List[Diet]:
        if not population:
            return []

        strength = self._calculate_strength(fitnesses)
        raw_fitness = self._calculate_raw_fitness(fitnesses, strength)
        distances = self._calculate_distances(fitnesses)
        density = self._calculate_density(distances)
        fitness = raw_fitness + density
        non_dominated_mask = raw_fitness == 0
        non_dominated_indices = np.where(non_dominated_mask)[0]
        
        if len(non_dominated_indices) == self.archive_size:
            return [population[i] for i in non_dominated_indices]
        
        elif len(non_dominated_indices) < self.archive_size:
            sorted_indices = np.argsort(fitness)
            return [population[i] for i in sorted_indices[:self.archive_size]]
        
        else:
            selected = list(non_dominated_indices)
            while len(selected) > self.archive_size:
                min_distance = float('inf')
                to_remove = None
                
                for i, idx1 in enumerate(selected):
                    dist_to_nearest = np.min([distances[idx1, idx2] for j, idx2 in enumerate(selected) if i != j])
                    if dist_to_nearest < min_distance:
                        min_distance = dist_to_nearest
                        to_remove = i
                
                if to_remove is not None:
                    selected.pop(to_remove)
            
            return [population[i] for i in selected]

    def _create_initial_individual(self, base_diet):
        mutated = self.mutate(base_diet)
        for meal in mutated.meals:
            for menu in meal.menus:
                menu.serving_ratio = np.random.uniform(0.6, 0.9)
        return mutated

    def optimize(self, diet_db: Diet, initial_diet: Diet, generations: int = 200) -> List[Diet]:
        # 초기화
        self.good_solutions_archive.clear()
        self.backup_solutions.clear()
        self.constraint_solutions.clear()
        
        population = [initial_diet]
        self.archive = []

        initial_fitness = self._get_cached_fitness(initial_diet, diet_db)
        
        futures = []
        for _ in range(self.population_size - 1):
            futures.append(self.thread_pool.submit(self._create_initial_individual, initial_diet))
        population.extend([f.result() for f in futures])

        # 세대별 최적화
        for generation in range(generations):
            print(f"=== Generation {generation + 1}/{generations} ===")
            all_solutions = population + self.archive
            fitnesses = []
            for i in range(0, len(all_solutions), self.batch_size):
                batch = all_solutions[i:i + self.batch_size]
                batch_futures = [self.thread_pool.submit(self._get_cached_fitness, diet, diet_db)
                               for diet in batch]
                fitnesses.extend([f.result() for f in batch_futures])
            fitnesses = np.array(fitnesses)
            
            self.archive = self._environmental_selection(all_solutions, fitnesses)
            
            # 종료 조건 체크
            if self.check_termination(initial_fitness, self.archive, diet_db):
                print(f"Termination condition met at generation {generation}")
                return self.get_final_solutions(diet_db)

            # 새로운 세대 생성
            new_population = []
            while len(new_population) < self.population_size:
                parents = np.random.choice(self.archive if self.archive else population, size=2, replace=False)

                if np.random.random() < self.crossover_prob:
                    child1 = self.crossover(parents[0], parents[1])
                    child2 = self.crossover(parents[1], parents[0])
                    
                    if np.random.random() < self.mutation_prob:
                        child1 = self.mutate(child1)
                    if np.random.random() < self.mutation_prob:
                        child2 = self.mutate(child2)
                        
                    new_population.extend([child1, child2])
                else:
                    new_population.extend(parents)
            
            population = new_population[:self.population_size]

            if generation % 10 == 0:
                self.fitness_cache.clear()
                self.distance_cache.clear()
                self.strength_cache.clear()

        return self.get_final_solutions(diet_db)