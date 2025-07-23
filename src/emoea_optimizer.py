from optimizer_base import DietOptimizer
import numpy as np
from typing import List
from Diet_class import Diet
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict, OrderedDict
import threading
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()
        self._lock = threading.Lock()
        
    def get(self, key):
        with self._lock:
            if key in self.cache:
                self.cache.move_to_end(key)
                return self.cache[key]
            return None
        
    def put(self, key, value):
        with self._lock:
            if key in self.cache:
                self.cache.move_to_end(key)
            else:
                if len(self.cache) >= self.capacity:
                    self.cache.popitem(last=False)
            self.cache[key] = value
            
class EpsilonMOEAOptimizer(DietOptimizer):
    def __init__(self, all_menus, nutrient_constraints, harmony_matrix):
        super().__init__(all_menus, nutrient_constraints, harmony_matrix)
        self._initialize()

    def _initialize(self):
        self.epsilon = np.array([5.0, 5.0, 5.0, 5.0])  # [nutrition, cost, harmony, diversity]
        self.archive = {}
        self.fitness_cache = LRUCache(1000)
        self.box_cache = LRUCache(1000)
        self.thread_pool = ThreadPoolExecutor(max_workers=4)
        self.batch_size = 16
        self.ideal_point = None
        self.nadir_point = None

    def _get_cached_fitness(self, diet: Diet, diet_db: Diet) -> np.ndarray:
        diet_hash = hash(str([(meal.menus, [menu.serving_ratio for menu in meal.menus]) for meal in diet.meals]))
        cached = self.fitness_cache.get(diet_hash)
        if cached is None:
            cached = np.array(self.fitness(diet_db, diet))
            self.fitness_cache.put(diet_hash, cached)
        return cached

    def _batch_compute_fitness(self, population: List[Diet], diet_db: Diet) -> np.ndarray:
        fitnesses = []
        for i in range(0, len(population), self.batch_size):
            batch = population[i:i + self.batch_size]
            futures = [self.thread_pool.submit(self._get_cached_fitness, diet, diet_db)
                      for diet in batch]
            fitnesses.extend([f.result() for f in futures])
        return np.array(fitnesses)

    def _get_hyperbox_indices(self, fitnesses: np.ndarray) -> np.ndarray:
        eps_scaled = np.floor_divide(fitnesses, self.epsilon)
        return eps_scaled.astype(np.int64)

    def _update_archive_efficient(self, population: List[Diet], fitnesses: np.ndarray) -> None:
        box_indices = self._get_hyperbox_indices(fitnesses)
        
        box_groups = defaultdict(list)
        for i, box_idx in enumerate(map(tuple, box_indices)):
            box_groups[box_idx].append((i, fitnesses[i]))
        
        for box_idx, solutions in box_groups.items():
            if box_idx not in self.archive:
                best_idx, best_fitness = solutions[0]
                self.archive[box_idx] = (population[best_idx], best_fitness)
                continue
            
            existing_fitness = self.archive[box_idx][1]
            box_center = (np.array(box_idx) + 0.5) * self.epsilon
            
            min_dist = float('inf')
            best_solution = None
            
            for idx, fitness in solutions:
                if self._dominates(fitness, existing_fitness):
                    dist = np.sum((fitness - box_center) ** 2)
                    if dist < min_dist:
                        min_dist = dist
                        best_solution = (population[idx], fitness)
            
            if best_solution is not None:
                self.archive[box_idx] = best_solution

    def _clean_archive(self):
        if len(self.archive) <= self.archive_size:
            return

        boxes = list(self.archive.keys())
        fitnesses = np.array([self.archive[box][1] for box in boxes])
        
        dominated = np.zeros(len(boxes), dtype=bool)
        for i in range(len(boxes)):
            for j in range(i + 1, len(boxes)):
                if self._dominates(fitnesses[i], fitnesses[j]):
                    dominated[j] = True
                elif self._dominates(fitnesses[j], fitnesses[i]):
                    dominated[i] = True
        
        non_dominated = ~dominated
        if np.sum(non_dominated) > self.archive_size:
            distances = np.zeros((len(boxes), len(boxes)))
            for i in range(len(boxes)):
                if non_dominated[i]:
                    for j in range(i + 1, len(boxes)):
                        if non_dominated[j]:
                            dist = np.sum((fitnesses[i] - fitnesses[j]) ** 2)
                            distances[i, j] = distances[j, i] = dist
            
            selected = []
            remaining = list(np.where(non_dominated)[0])
            
            first = remaining[np.argmax(np.sum(fitnesses[remaining], axis=1))]
            selected.append(first)
            remaining.remove(first)
            
            while len(selected) < self.archive_size and remaining:
                min_distances = np.min([distances[i, selected] for i in remaining], axis=1)
                next_idx = remaining[np.argmax(min_distances)]
                selected.append(next_idx)
                remaining.remove(next_idx)
            
            new_archive = {}
            for idx in selected:
                box = boxes[idx]
                new_archive[box] = self.archive[box]
            self.archive = new_archive

    def optimize(self, diet_db: Diet, initial_diet: Diet, generations: int = 100) -> List[Diet]:
        # 초기화
        self.good_solutions_archive.clear()
        self.backup_solutions.clear()
        self.constraint_solutions.clear()
        
        population = [initial_diet]
        for _ in range(self.population_size - 1):
            mutated = self.mutate(initial_diet)
            for meal in mutated.meals:
                for menu in meal.menus:
                    menu.serving_ratio = np.random.uniform(0.6, 0.9)
            population.append(mutated)
        self.archive.clear()

        initial_fitness = self._get_cached_fitness(initial_diet, diet_db)
        
        for generation in range(generations):
            print(f"=== Generation {generation + 1}/{generations} ===")
            fitnesses = self._batch_compute_fitness(population, diet_db)
            self._update_archive_efficient(population, fitnesses)
            self._clean_archive()

            # 종료 조건 체크
            current_solutions = [diet for diet, _ in self.archive.values()]
            if self.check_termination(initial_fitness, current_solutions, diet_db):
                print(f"Termination condition met at generation {generation}")
                return self.get_final_solutions(diet_db)

            # 새로운 세대 생성
            new_population = []
            archive_solutions = [diet for diet, _ in self.archive.values()]
            
            while len(new_population) < self.population_size:
                if np.random.random() < self.crossover_prob:
                    parent1 = np.random.choice(archive_solutions) if archive_solutions else np.random.choice(population)
                    parent2 = np.random.choice(population)
                    
                    futures = [
                        self.thread_pool.submit(self._create_offspring, parent1, parent2),
                        self.thread_pool.submit(self._create_offspring, parent2, parent1)
                    ]
                    
                    new_population.extend([f.result() for f in futures])
                else:
                    parent = np.random.choice(archive_solutions) if archive_solutions else np.random.choice(population)
                    new_population.append(parent)
            
            population = new_population[:self.population_size]

            if generation % 10 == 0:
                self.fitness_cache = LRUCache(1000)
                self.box_cache = LRUCache(1000)

        return self.get_final_solutions(diet_db)

    def _create_offspring(self, parent1: Diet, parent2: Diet) -> Diet:
        child = self.crossover(parent1, parent2)
        if np.random.random() < self.mutation_prob:
            child = self.mutate(child)
        return child

    def _dominates(self, fitness1: np.ndarray, fitness2: np.ndarray) -> bool:
        return (np.all(fitness1 >= fitness2) and np.any(fitness1 > fitness2))