from abc import ABC, abstractmethod
from Diet_class import Meal, Diet
from typing import List
import numpy as np
from evaluation_function import evaluate_nutrition, evaluate_cost, evaluate_harmony, evaluate_diversity

class DietOptimizer(ABC):
    def __init__(self, all_menus, nutrient_constraints, harmony_matrix):
        self.all_menus = all_menus
        self.nutrient_constraints = nutrient_constraints
        self.harmony_matrix = harmony_matrix
        # 표준화된 매개변수 설정
        self.population_size = 150
        self.archive_size = 100
        self.mutation_prob = 0.3
        self.mutation_menu_prob = 0.7
        self.crossover_prob = 0.8

    @abstractmethod
    def optimize(self, diet_db: Diet, initial_diet: Diet, generations: int = 100) -> List[Diet]:
        pass

    def _dominates(self, a: List[float], b: List[float]) -> bool:
        return all(x >= y for x, y in zip(a, b)) and any(x > y for x, y in zip(a, b))

    def crossover(self, parent1: Diet, parent2: Diet) -> Diet:
        if np.random.random() > self.crossover_prob:
            return parent1  # 교차가 일어나지 않으면 parent1 반환
            
        max_attempts = 10  # 최대 시도 횟수
        
        for _ in range(max_attempts):
            child_meals = []
            for meal1, meal2 in zip(parent1.meals, parent2.meals):
                child_menus = []
                for menu1, menu2 in zip(meal1.menus, meal2.menus):
                    child_menus.append(menu1 if np.random.random() < 0.5 else menu2)
                child_meals.append(Meal(child_menus, meal1.date, meal1.meal_type))
            
            child = Diet(child_meals)
            
            # 제약조건 검증
            if self.validate_nutrient_constraints(child):
                return child
        
        # 최대 시도 횟수 초과시 부모 중 하나 반환
        return parent1 if np.random.random() < 0.5 else parent2

    def mutate(self, diet: Diet) -> Diet:
        max_attempts = 10  # 최대 시도 횟수
        
        for _ in range(max_attempts):
            mutated_meals = []
            for meal in diet.meals:
                if np.random.random() < self.mutation_prob:
                    mutated_menus = []
                    for menu in meal.menus:
                        if np.random.random() < self.mutation_menu_prob:
                            new_menu = np.random.choice(self.all_menus)
                            mutated_menus.append(new_menu)
                        else:
                            mutated_menus.append(menu)
                    mutated_meals.append(Meal(mutated_menus, meal.date, meal.meal_type))
                else:
                    mutated_meals.append(meal)
                    
            mutated_diet = Diet(mutated_meals)
            
            # 제약조건 검증
            if self.validate_nutrient_constraints(mutated_diet):
                return mutated_diet
        
        # 최대 시도 횟수 초과시 원본 반환
        return diet

    def validate_nutrient_constraints(self, weeklydiet: Diet) -> bool:
        days = len(weeklydiet.meals) // 3
        
        for day in range(days):
            daily_nutrients = {nutrient: 0 for nutrient in self.nutrient_constraints.min_values}
            start_idx = day * 3
            for meal in weeklydiet.meals[start_idx:start_idx + 3]:
                for menu in meal.menus:
                    for nutrient, amount in menu.nutrients.items():
                        daily_nutrients[nutrient] += amount
            
            # 영양소 제약조건 검증
            for nutrient, amount in daily_nutrients.items():
                min_value = self.nutrient_constraints.min_values[nutrient]
                max_value = self.nutrient_constraints.max_values[nutrient]
                
                # 탄수화물, 단백질, 지방에 대해서만 엄격한 제약 적용
                if nutrient in ['탄수화물(g)', '단백질(g)', '지방(g)']:
                    if amount < min_value or amount > max_value:
                        return False
        
        return True

    def fitness(self, diet_db: Diet, weeklydiet: Diet) -> List[float]:
        if not self.validate_nutrient_constraints(weeklydiet):
            return [-float('inf'), -float('inf'), -float('inf'), -float('inf')]
        
        nutrition_score = evaluate_nutrition(weeklydiet, self.nutrient_constraints)
        cost_score = evaluate_cost(diet_db, weeklydiet)
        harmony_score = evaluate_harmony(diet_db, weeklydiet)
        diversity_score = evaluate_diversity(weeklydiet)
        return [nutrition_score, cost_score, harmony_score, diversity_score]
        
    def check_termination(self, initial_fitness: List[float], 
                         current_solutions: List[Diet], 
                         diet_db: Diet) -> bool:
        improved_count = 0
        for diet in current_solutions:
            current_fitness = self.fitness(diet_db, diet)
            if sum(1 for init, curr in zip(initial_fitness, current_fitness) 
                  if curr > init) >= 3:
                improved_count += 1
            if improved_count >= 3:
                return True
        return False
