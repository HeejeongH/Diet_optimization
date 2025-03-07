from optimizer_base import DietOptimizer
import numpy as np
from typing import List, Tuple, Dict
from Diet_class import Diet, Meal
from concurrent.futures import ThreadPoolExecutor
import heapq
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

class NSGA3Optimizer(DietOptimizer):
    def __init__(self, all_menus, nutrient_constraints, harmony_matrix):
        super().__init__(all_menus, nutrient_constraints, harmony_matrix)
        self.n_objectives = 4
        self._initialize_optimization()
        
    def _initialize_optimization(self):
        """최적화 관련 초기화"""
        self.fitness_cache = LRUCache(1000)
        self.dominance_cache = LRUCache(1000)
        self.thread_pool = ThreadPoolExecutor(max_workers=4)
        self.batch_size = 16
        self.reference_points = self._generate_reference_points(4)
        self.ideal_point = None
        self.nadir_point = None

    def _generate_reference_points(self, divisions: int) -> np.ndarray:
        """안정적인 참조점 생성"""
        def generate_recursive(remaining_sum: float, n_remaining: int, curr_point: List[float]) -> List[List[float]]:
            if n_remaining == 1:
                return [curr_point + [remaining_sum]]
            
            points = []
            step = 1.0 / divisions
            for i in range(int(remaining_sum / step) + 1):
                value = i * step
                if value <= remaining_sum + 1e-10:
                    points.extend(generate_recursive(remaining_sum - value, 
                                                  n_remaining - 1, 
                                                  curr_point + [value]))
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
        """캐시된 적합도 값"""
        diet_hash = hash(str([meal.menus for meal in diet.meals]))
        cached = self.fitness_cache.get(diet_hash)
        if cached is None:
            cached = np.array(self.fitness(diet_db, diet))
            self.fitness_cache.put(diet_hash, cached)
        return cached

    def _compute_dominance_matrix(self, fitnesses: np.ndarray) -> np.ndarray:
        """효율적인 도미넌스 행렬 계산"""
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
        """안정적인 비지배 정렬 구현"""
        n = len(fitnesses)
        if n == 0:
            return [[]]

        # 도미넌스 관계 계산
        dominance_matrix = np.zeros((n, n), dtype=bool)
        domination_count = np.zeros(n, dtype=int)
        dominated_solutions = [[] for _ in range(n)]

        # 도미넌스 관계와 지배당하는 수 계산
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

        # 프론트 구성
        fronts = []
        current_front = []
        
        # 첫 번째 프론트 찾기
        for i in range(n):
            if domination_count[i] == 0:
                current_front.append(i)
        
        if not current_front:  # 해가 없는 경우
            return [[]]
            
        fronts.append(current_front)
        current = 0

        # 나머지 프론트 찾기
        while True:
            next_front = []
            for i in fronts[current]:
                for j in dominated_solutions[i]:
                    domination_count[j] -= 1
                    if domination_count[j] == 0:
                        next_front.append(j)
            
            if not next_front:  # 더 이상 프론트가 없으면 종료
                break
                
            fronts.append(next_front)
            current += 1

        return fronts

    def _normalize_objectives(self, fitnesses: np.ndarray) -> np.ndarray:
        """효율적인 목적 함수 정규화"""
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
        """효율적인 참조점 연관성 계산"""
        if len(normalized_objectives) == 0:
            return np.zeros(len(self.reference_points)), np.array([])

        # 정규화된 해와 참조점 간의 거리 계산
        distances = np.zeros((len(normalized_objectives), len(self.reference_points)))
        for i in range(len(normalized_objectives)):
            for j in range(len(self.reference_points)):
                diff = normalized_objectives[i] - self.reference_points[j]
                distances[i, j] = np.sum(diff * diff)

        # 각 해를 가장 가까운 참조점에 할당
        associations = np.argmin(distances, axis=1)
        niche_counts = np.bincount(associations, minlength=len(self.reference_points))
        
        return niche_counts, distances

    def selection(self, population: List[Diet], fitnesses: np.ndarray) -> List[Diet]:
        """안정적인 선택 연산자"""
        if len(population) < 2:
            return population[:]
            
        target_size = self.population_size
        fronts = self._fast_non_dominated_sort(fitnesses)
        
        if not fronts[0]:  # 프론트가 비어있는 경우
            return population[:target_size]
            
        selected = []
        front_idx = 0
        
        # 프론트별 선택
        while front_idx < len(fronts) and len(selected) + len(fronts[front_idx]) <= target_size:
            selected.extend(fronts[front_idx])
            front_idx += 1
            
        if len(selected) < target_size and front_idx < len(fronts):
            # 마지막 프론트에서 추가 선택 필요
            remaining = target_size - len(selected)
            last_front = fronts[front_idx]
            
            # 마지막 프론트의 해들 정규화
            last_front_fitnesses = fitnesses[last_front]
            normalized = self._normalize_objectives(last_front_fitnesses)
            
            # 참조점 기반 선택
            niche_counts, distances = self._associate_to_references(normalized)
            
            # 선택할 해의 수가 남은 자리보다 적으면 모두 선택
            if len(last_front) <= remaining:
                selected.extend(last_front)
            else:
                # 니치 기반 선택
                selected_from_last = []
                while len(selected_from_last) < remaining:
                    min_count = np.min(niche_counts)
                    min_niches = np.where(niche_counts == min_count)[0]
                    
                    for niche in min_niches:
                        if len(selected_from_last) >= remaining:
                            break
                            
                        # 현재 니치에서 가장 가까운 해 선택
                        candidates = []
                        for idx, sol_idx in enumerate(last_front):
                            if idx not in selected_from_last and \
                               np.argmin(distances[idx]) == niche:
                                candidates.append((distances[idx, niche], idx))
                        
                        if candidates:
                            # 가장 가까운 해 선택
                            best_idx = min(candidates, key=lambda x: x[0])[1]
                            selected_from_last.append(best_idx)
                            niche_counts[niche] += 1
                
                selected.extend([last_front[i] for i in selected_from_last])

        return [population[i] for i in selected]


    def optimize(self, diet_db: Diet, initial_diet: Diet, generations: int = 100) -> List[Diet]:
        """최적화된 메인 최적화 루프"""
        # 초기화
        population = [initial_diet]
        
        # 병렬 초기 집단 생성
        futures = []
        for _ in range(self.population_size - 1):
            futures.append(self.thread_pool.submit(
                lambda: self.mutate(initial_diet)
            ))
        population.extend([f.result() for f in futures])

        for generation in range(generations):
            # 배치 처리된 적합도 계산
            fitnesses = []
            for i in range(0, len(population), self.batch_size):
                batch = population[i:i + self.batch_size]
                batch_futures = [self.thread_pool.submit(self._get_cached_fitness, diet, diet_db)
                               for diet in batch]
                fitnesses.extend([f.result() for f in batch_futures])
            fitnesses = np.array(fitnesses)

            # 선택
            selected = self.selection(population, fitnesses)
            
            # 자손 생성
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
        return [population[i] for i in fronts[0][:5]]  # 최상위 프론트에서 5개 선택