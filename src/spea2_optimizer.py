from optimizer_base import DietOptimizer
import numpy as np
from typing import List, Tuple, Dict
from Diet_class import Diet, Meal
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict

class LRUCache:
    """Least Recently Used 캐시"""
    def __init__(self, capacity: int):
        self.capacity = capacity
        self._cache = {}
        self._access_count = {}
        self._total_access = 0
        
    def get(self, key):
        if key in self._cache:
            self._access_count[key] = self._total_access
            self._total_access += 1
            return self._cache[key]
        return None
        
    def put(self, key, value):
        if len(self._cache) >= self.capacity:
            min_key = min(self._access_count.items(), key=lambda x: x[1])[0]
            del self._cache[min_key]
            del self._access_count[min_key]
        self._cache[key] = value
        self._access_count[key] = self._total_access
        self._total_access += 1
        
    def clear(self):
        self._cache.clear()
        self._access_count.clear()

class SPEA2Optimizer(DietOptimizer):
    def __init__(self, all_menus, nutrient_constraints, harmony_matrix):
        super().__init__(all_menus, nutrient_constraints, harmony_matrix)
        self._initialize_optimization()

    def _initialize_optimization(self):
        """최적화 관련 초기화"""
        self.archive = []
        self.fitness_cache = LRUCache(1000)
        self.distance_cache = LRUCache(1000)
        self.strength_cache = LRUCache(1000)
        self.thread_pool = ThreadPoolExecutor(max_workers=4)
        self.batch_size = 16

    def _get_cached_fitness(self, diet: Diet, diet_db: Diet) -> np.ndarray:
        """캐시된 적합도 값"""
        diet_hash = hash(str([meal.menus for meal in diet.meals]))
        cached = self.fitness_cache.get(diet_hash)
        if cached is None:
            cached = np.array(self.fitness(diet_db, diet))
            self.fitness_cache.put(diet_hash, cached)
        return cached

    def _compute_dominance_relations(self, fitnesses: np.ndarray) -> np.ndarray:
        """효율적인 도미넌스 관계 계산"""
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
        """강도값 계산 최적화"""
        # 캐시 확인
        cache_key = hash(fitnesses.tobytes())
        cached = self.strength_cache.get(cache_key)
        if cached is not None:
            return cached

        dominance = self._compute_dominance_relations(fitnesses)
        strength = np.sum(dominance, axis=1)
        self.strength_cache.put(cache_key, strength)
        
        return strength

    def _calculate_raw_fitness(self, fitnesses: np.ndarray, strength: np.ndarray) -> np.ndarray:
        """효율적인 raw fitness 계산"""
        dominance = self._compute_dominance_relations(fitnesses)
        raw_fitness = np.zeros(len(fitnesses))
        
        for i in range(len(fitnesses)):
            dominated_by = np.where(dominance[:, i])[0]
            raw_fitness[i] = np.sum(strength[dominated_by])
            
        return raw_fitness

    def _calculate_distances(self, fitnesses: np.ndarray) -> np.ndarray:
        """효율적인 거리 계산"""
        cache_key = hash(fitnesses.tobytes())
        cached = self.distance_cache.get(cache_key)
        if cached is not None:
            return cached

        n = len(fitnesses)
        distances = np.zeros((n, n))
        
        # 유클리드 거리 계산 최적화
        for i in range(n):
            diff = fitnesses[i] - fitnesses
            distances[i] = np.sqrt(np.sum(diff * diff, axis=1))
            distances[i, i] = np.inf  # 자기 자신과의 거리는 무한대
            
        self.distance_cache.put(cache_key, distances)
        return distances

    def _calculate_density(self, distances: np.ndarray) -> np.ndarray:
        """효율적인 밀도 계산"""
        k = int(np.sqrt(len(distances)))
        density = np.zeros(len(distances))
        
        # k-nearest neighbor 거리 계산
        for i in range(len(distances)):
            kth_distance = np.partition(distances[i], k)[k]
            density[i] = 1.0 / (kth_distance + 2.0)
            
        return density

    def _environmental_selection(self, population: List[Diet], 
                               fitnesses: np.ndarray) -> List[Diet]:
        """효율적인 환경 선택"""
        if not population:
            return []

        # 강도값 계산
        strength = self._calculate_strength(fitnesses)
        
        # Raw fitness 계산
        raw_fitness = self._calculate_raw_fitness(fitnesses, strength)
        
        # 거리 및 밀도 계산
        distances = self._calculate_distances(fitnesses)
        density = self._calculate_density(distances)
        
        # 최종 적합도
        fitness = raw_fitness + density
        
        # 비지배 해 선택
        non_dominated_mask = raw_fitness == 0
        non_dominated_indices = np.where(non_dominated_mask)[0]
        
        if len(non_dominated_indices) == self.archive_size:
            return [population[i] for i in non_dominated_indices]
        
        elif len(non_dominated_indices) < self.archive_size:
            # fitness 기반 선택
            sorted_indices = np.argsort(fitness)
            return [population[i] for i in sorted_indices[:self.archive_size]]
        
        else:
            # 군집 절단
            selected = list(non_dominated_indices)
            while len(selected) > self.archive_size:
                # 가장 가까운 이웃 거리가 최소인 해 제거
                min_distance = float('inf')
                to_remove = None
                
                for i, idx1 in enumerate(selected):
                    dist_to_nearest = np.min([distances[idx1, idx2] 
                                           for j, idx2 in enumerate(selected) if i != j])
                    if dist_to_nearest < min_distance:
                        min_distance = dist_to_nearest
                        to_remove = i
                
                if to_remove is not None:
                    selected.pop(to_remove)
            
            return [population[i] for i in selected]

    def optimize(self, diet_db: Diet, initial_diet: Diet, generations: int = 100) -> List[Diet]:
        """최적화된 메인 최적화 루프"""
        # 초기화
        population = [initial_diet]
        self.archive = []
        
        # 병렬 초기 집단 생성
        futures = []
        for _ in range(self.population_size - 1):
            futures.append(self.thread_pool.submit(
                lambda: self.mutate(initial_diet)
            ))
        population.extend([f.result() for f in futures])

        # 세대별 최적화
        for generation in range(generations):
            # 배치 처리된 적합도 계산
            all_solutions = population + self.archive
            fitnesses = []
            for i in range(0, len(all_solutions), self.batch_size):
                batch = all_solutions[i:i + self.batch_size]
                batch_futures = [self.thread_pool.submit(self._get_cached_fitness, diet, diet_db)
                               for diet in batch]
                fitnesses.extend([f.result() for f in batch_futures])
            fitnesses = np.array(fitnesses)
            
            # 환경 선택
            self.archive = self._environmental_selection(all_solutions, fitnesses)
            
            # 종료 조건 체크
            if self.check_termination(self._get_cached_fitness(initial_diet, diet_db), 
                                    self.archive, diet_db):
                print(f"Termination condition met at generation {generation}")
                return self.archive

            # 새로운 세대 생성
            new_population = []
            while len(new_population) < self.population_size:
                # 부모 선택
                parents = np.random.choice(
                    self.archive if self.archive else population, 
                    size=2, replace=False
                )
                
                # 자손 생성
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

            # 주기적 캐시 정리
            if generation % 10 == 0:
                self.fitness_cache.clear()
                self.distance_cache.clear()
                self.strength_cache.clear()

        return self.archive