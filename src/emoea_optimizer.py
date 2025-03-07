from optimizer_base import DietOptimizer
import numpy as np
from typing import List, Tuple, Dict
from Diet_class import Diet, Meal
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict, OrderedDict

class LRUCache:
    """Least Recently Used 캐시"""
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()
        
    def get(self, key):
        if key in self.cache:
            self.cache.move_to_end(key)
            return self.cache[key]
        return None
        
    def put(self, key, value):
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
        """초기화 및 최적화 관련 설정"""
        self.epsilon = np.array([5.0, 5.0, 5.0, 5.0])  # [nutrition, cost, harmony, diversity]
        self.archive = {}
        self.fitness_cache = LRUCache(1000)
        self.box_cache = LRUCache(1000)
        self.thread_pool = ThreadPoolExecutor(max_workers=4)
        self.batch_size = 16
        self.ideal_point = None
        self.nadir_point = None

    def _get_cached_fitness(self, diet: Diet, diet_db: Diet) -> np.ndarray:
        """캐시된 적합도 값"""
        diet_hash = hash(str([meal.menus for meal in diet.meals]))
        cached = self.fitness_cache.get(diet_hash)
        if cached is None:
            cached = np.array(self.fitness(diet_db, diet))
            self.fitness_cache.put(diet_hash, cached)
        return cached

    def _batch_compute_fitness(self, population: List[Diet], diet_db: Diet) -> np.ndarray:
        """배치 처리된 적합도 계산"""
        fitnesses = []
        for i in range(0, len(population), self.batch_size):
            batch = population[i:i + self.batch_size]
            futures = [self.thread_pool.submit(self._get_cached_fitness, diet, diet_db)
                      for diet in batch]
            fitnesses.extend([f.result() for f in futures])
        return np.array(fitnesses)

    def _get_hyperbox_indices(self, fitnesses: np.ndarray) -> np.ndarray:
        """효율적인 하이퍼박스 인덱스 계산"""
        eps_scaled = np.floor_divide(fitnesses, self.epsilon)
        return eps_scaled.astype(np.int64)

    def _update_archive_efficient(self, population: List[Diet], 
                                fitnesses: np.ndarray) -> None:
        """효율적인 아카이브 업데이트"""
        box_indices = self._get_hyperbox_indices(fitnesses)
        
        # 하이퍼박스별 해 그룹화
        box_groups = defaultdict(list)
        for i, box_idx in enumerate(map(tuple, box_indices)):
            box_groups[box_idx].append((i, fitnesses[i]))
        
        # 각 하이퍼박스에서 최적 해 선택
        for box_idx, solutions in box_groups.items():
            if box_idx not in self.archive:
                # 새로운 하이퍼박스
                best_idx, best_fitness = solutions[0]
                self.archive[box_idx] = (population[best_idx], best_fitness)
                continue
            
            existing_fitness = self.archive[box_idx][1]
            box_center = (np.array(box_idx) + 0.5) * self.epsilon
            
            # 현재 하이퍼박스 내 최적 해 선택
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
        """효율적인 아카이브 정리"""
        if len(self.archive) <= self.archive_size:
            return

        # 아카이브의 해들을 도미넌스와 거리 기준으로 평가
        boxes = list(self.archive.keys())
        fitnesses = np.array([self.archive[box][1] for box in boxes])
        
        # 도미넌스 관계 계산
        dominated = np.zeros(len(boxes), dtype=bool)
        for i in range(len(boxes)):
            for j in range(i + 1, len(boxes)):
                if self._dominates(fitnesses[i], fitnesses[j]):
                    dominated[j] = True
                elif self._dominates(fitnesses[j], fitnesses[i]):
                    dominated[i] = True
        
        # 비지배 해 선택
        non_dominated = ~dominated
        if np.sum(non_dominated) > self.archive_size:
            # 거리 기반 선택
            distances = np.zeros((len(boxes), len(boxes)))
            for i in range(len(boxes)):
                if non_dominated[i]:
                    for j in range(i + 1, len(boxes)):
                        if non_dominated[j]:
                            dist = np.sum((fitnesses[i] - fitnesses[j]) ** 2)
                            distances[i, j] = distances[j, i] = dist
            
            # 가장 멀리 떨어진 해들 선택
            selected = []
            remaining = list(np.where(non_dominated)[0])
            
            # 첫 번째 해 선택
            first = remaining[np.argmax(np.sum(fitnesses[remaining], axis=1))]
            selected.append(first)
            remaining.remove(first)
            
            # 나머지 해 선택
            while len(selected) < self.archive_size and remaining:
                min_distances = np.min([distances[i, selected] for i in remaining], axis=1)
                next_idx = remaining[np.argmax(min_distances)]
                selected.append(next_idx)
                remaining.remove(next_idx)
            
            # 아카이브 업데이트
            new_archive = {}
            for idx in selected:
                box = boxes[idx]
                new_archive[box] = self.archive[box]
            self.archive = new_archive

    def optimize(self, diet_db: Diet, initial_diet: Diet, generations: int = 100) -> List[Diet]:
        """최적화된 메인 최적화 루프"""
        # 초기화
        population = [initial_diet] + [self.mutate(initial_diet) 
                                     for _ in range(self.population_size - 1)]
        self.archive.clear()
        
        for generation in range(generations):
            # 배치 처리된 적합도 계산
            fitnesses = self._batch_compute_fitness(population, diet_db)
            
            # 아카이브 업데이트
            self._update_archive_efficient(population, fitnesses)
            
            # 아카이브 크기 관리
            self._clean_archive()
            
            # 종료 조건 체크
            current_solutions = [diet for diet, _ in self.archive.values()]
            if self.check_termination(self._get_cached_fitness(initial_diet, diet_db), 
                                    current_solutions, diet_db):
                print(f"Termination condition met at generation {generation}")
                return current_solutions

            # 새로운 세대 생성
            new_population = []
            archive_solutions = [diet for diet, _ in self.archive.values()]
            
            # 효율적인 자손 생성
            while len(new_population) < self.population_size:
                if np.random.random() < self.crossover_prob:
                    # 병렬 자손 생성
                    parent1 = np.random.choice(archive_solutions) if archive_solutions else \
                             np.random.choice(population)
                    parent2 = np.random.choice(population)
                    
                    futures = [
                        self.thread_pool.submit(self._create_offspring, parent1, parent2),
                        self.thread_pool.submit(self._create_offspring, parent2, parent1)
                    ]
                    
                    new_population.extend([f.result() for f in futures])
                else:
                    parent = np.random.choice(archive_solutions) if archive_solutions else \
                            np.random.choice(population)
                    new_population.append(parent)
            
            population = new_population[:self.population_size]

            # 주기적 캐시 정리
            if generation % 10 == 0:
                self.fitness_cache = LRUCache(1000)
                self.box_cache = LRUCache(1000)

        return list(diet for diet, _ in self.archive.values())

    def _create_offspring(self, parent1: Diet, parent2: Diet) -> Diet:
        """효율적인 자손 생성"""
        child = self.crossover(parent1, parent2)
        if np.random.random() < self.mutation_prob:
            child = self.mutate(child)
        return child

    def _dominates(self, fitness1: np.ndarray, fitness2: np.ndarray) -> bool:
        """효율적인 도미넌스 체크"""
        return (np.all(fitness1 >= fitness2) and np.any(fitness1 > fitness2))