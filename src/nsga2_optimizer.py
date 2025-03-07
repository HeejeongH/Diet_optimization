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
        """최적화 관련 초기화"""
        self.fitness_cache = {}
        self.dominance_cache = {}
        self.thread_pool = ThreadPoolExecutor(max_workers=4)
        self.batch_size = 100

    def _get_cached_fitness(self, diet: Diet, diet_db: Diet) -> np.ndarray:
        """캐시된 적합도 값을 반환하거나 계산하여 캐시"""
        diet_hash = hash(str([meal.menus for meal in diet.meals]))
        if diet_hash not in self.fitness_cache:
            self.fitness_cache[diet_hash] = np.array(self.fitness(diet_db, diet))
        return self.fitness_cache[diet_hash]

    def _batch_process_fitness(self, population: List[Diet], diet_db: Diet) -> np.ndarray:
        """배치 처리된 적합도 계산"""
        futures = []
        for i in range(0, len(population), self.batch_size):
            batch = population[i:i + self.batch_size]
            for diet in batch:
                futures.append(self.thread_pool.submit(self._get_cached_fitness, diet, diet_db))
        
        return np.array([f.result() for f in futures])

    def _compute_dominance_matrix(self, fitnesses: np.ndarray) -> np.ndarray:
        """효율적인 도미넌스 행렬 계산"""
        n = len(fitnesses)
        dominance = np.zeros((n, n), dtype=bool)
        
        # 벡터화된 도미넌스 체크
        for i in range(n):
            dominance[i] = np.all(fitnesses[i] >= fitnesses, axis=1) & \
                          np.any(fitnesses[i] > fitnesses, axis=1)
            dominance[i, i] = False
            
        return dominance

    def _fast_non_dominated_sort(self, population: List[Diet], 
                               fitnesses: np.ndarray) -> List[List[int]]:
        """최적화된 비지배 정렬"""
        if len(population) == 0:
            return [[]]

        # 캐시된 도미넌스 행렬 사용 또는 계산
        cache_key = hash(fitnesses.tobytes())
        if cache_key in self.dominance_cache:
            dominance_matrix = self.dominance_cache[cache_key]
        else:
            dominance_matrix = self._compute_dominance_matrix(fitnesses)
            self.dominance_cache[cache_key] = dominance_matrix

        # 지배당하는 수와 지배하는 해들 계산
        domination_counts = np.sum(dominance_matrix.T, axis=0)
        dominated_solutions = [np.where(row)[0].tolist() for row in dominance_matrix]

        # 프론트 계산
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
        """벡터화된 군집 거리 계산"""
        n_points = len(fitnesses)
        if n_points <= 2:
            return np.full(n_points, np.inf)
            
        n_objectives = fitnesses.shape[1]
        distances = np.zeros(n_points)
        
        for obj in range(n_objectives):
            sorted_idx = np.argsort(fitnesses[:, obj])
            obj_range = fitnesses[sorted_idx[-1], obj] - fitnesses[sorted_idx[0], obj]
            
            if obj_range > 1e-10:
                # 경계 포인트에 무한대 거리 할당
                distances[sorted_idx[0]] = np.inf
                distances[sorted_idx[-1]] = np.inf
                
                # 중간 포인트들의 거리 계산
                if n_points > 2:
                    norm_diffs = np.diff(fitnesses[sorted_idx, obj]) / obj_range
                    distances[sorted_idx[1:-1]] += norm_diffs[:-1] + norm_diffs[1:]
        
        return distances

    def selection(self, population: List[Diet], fitnesses: np.ndarray) -> List[Diet]:
        """최적화된 선택 연산자"""
        if len(population) < 2:
            return population[:]
            
        target_size = self.population_size
        fronts = self._fast_non_dominated_sort(population, fitnesses)
        selected = []
        current_front = 0

        # 프론트별 선택
        while current_front < len(fronts) and len(selected) + len(fronts[current_front]) <= target_size:
            selected.extend(fronts[current_front])
            current_front += 1

        if len(selected) < target_size and current_front < len(fronts):
            # 마지막 프론트에서 군집 거리 기반 선택
            last_front = fronts[current_front]
            last_front_fitnesses = fitnesses[last_front]
            crowding_distances = self._calculate_crowding_distance(last_front_fitnesses)
            
            # 군집 거리로 정렬하여 필요한 만큼 선택
            sorted_indices = np.argsort(crowding_distances)[::-1]
            remaining = target_size - len(selected)
            selected.extend([last_front[i] for i in sorted_indices[:remaining]])

        return [population[i] for i in selected]

    def _create_offspring_batch(self, parents: List[Diet], 
                              mutation_prob: float) -> List[Diet]:
        """배치 처리된 자손 생성"""
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

    def optimize(self, diet_db: Diet, initial_diet: Diet, generations: int = 100) -> List[Diet]:
        """최적화된 메인 최적화 루프"""
        # 초기화
        population = [initial_diet]
        self.fitness_cache.clear()
        self.dominance_cache.clear()
        
        # 초기 집단 생성
        futures = []
        for _ in range(self.population_size - 1):
            futures.append(self.thread_pool.submit(
                lambda: self.mutate(self.mutate(initial_diet)) 
                if np.random.random() < 0.3 else self.mutate(initial_diet)
            ))
        population.extend([f.result() for f in futures])

        initial_fitness = self._get_cached_fitness(initial_diet, diet_db)
        best_fitness = float('-inf')
        patience = 10
        no_improvement_count = 0

        for generation in range(generations):
            # 배치 처리된 적합도 계산
            fitnesses = self._batch_process_fitness(population, diet_db)
            
            # 현재 세대 최고 적합도 확인
            current_best = np.max(fitnesses[:, 0])
            if current_best > best_fitness:
                best_fitness = current_best
                no_improvement_count = 0
            else:
                no_improvement_count += 1

            # 종료 조건 확인
            if self.check_termination(initial_fitness, population, diet_db):
                print(f"Termination condition met at generation {generation}")
                return self._select_diverse_solutions(population, fitnesses)
            
            # 적응적 돌연변이 확률
            mutation_prob = self.mutation_prob * (1 + 0.5 * (no_improvement_count / patience))

            # 선택 및 자손 생성
            selected_population = self.selection(population, fitnesses)
            
            # 배치 처리된 자손 생성
            offspring_population = []
            for i in range(0, len(selected_population), self.batch_size):
                batch = selected_population[i:i + self.batch_size]
                offspring_batch = self._create_offspring_batch(batch, mutation_prob)
                offspring_population.extend(offspring_batch)
            
            # 다음 세대 구성
            population = selected_population + offspring_population[:self.population_size - len(selected_population)]

            # 주기적 캐시 정리
            if generation % 10 == 0:
                if len(self.fitness_cache) > 1000:
                    self.fitness_cache.clear()
                if len(self.dominance_cache) > 1000:
                    self.dominance_cache.clear()

        print(f"Maximum generations reached. Found {len(population)} solutions.")
        return self._select_diverse_solutions(population, fitnesses)

    def _select_diverse_solutions(self, population: List[Diet], 
                                fitnesses: np.ndarray, 
                                n_solutions: int = 5) -> List[Diet]:
        """최적화된 다양한 해 선택"""
        fronts = self._fast_non_dominated_sort(population, fitnesses)
        
        if not fronts[0]:
            return population[:n_solutions]
            
        first_front = fronts[0]
        front_fitnesses = fitnesses[first_front]
        distances = self._calculate_crowding_distance(front_fitnesses)
        
        sorted_indices = np.argsort(distances)[::-1]
        selected_indices = sorted_indices[:n_solutions]
        
        return [population[first_front[i]] for i in selected_indices]