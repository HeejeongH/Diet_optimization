from abc import ABC, abstractmethod
from Diet_class import Meal, Diet, Menu
from typing import List
import numpy as np
from evaluation_function import evaluate_nutrition, evaluate_cost, evaluate_harmony, evaluate_diversity, validate_weekly_constraints_detailed, validate_weekly_constraints

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

        self.good_solutions_archive = []
        self.backup_solutions = []  # 3가지 이상 개선된 해들
        self.constraint_solutions = []  # 제약조건만 만족하는 해들

    @abstractmethod
    def optimize(self, diet_db: Diet, initial_diet: Diet, generations: int = 100) -> List[Diet]:
        pass

    def _dominates(self, a: List[float], b: List[float]) -> bool:
        return all(x >= y for x, y in zip(a, b)) and any(x > y for x, y in zip(a, b))

    def crossover(self, parent1: Diet, parent2: Diet) -> Diet:
        if np.random.random() > self.crossover_prob:
            return parent1
            
        child_meals = []
        for meal1, meal2 in zip(parent1.meals, parent2.meals):
            child_menus = []
            for menu1, menu2 in zip(meal1.menus, meal2.menus):
                selected_menu = menu1 if np.random.random() < 0.5 else menu2
                new_ratio = (menu1.serving_ratio + menu2.serving_ratio) / 2 + np.random.normal(0, 0.05)
                new_ratio = np.clip(new_ratio, 0.6, 0.9)
                
                new_menu = Menu(selected_menu.name, selected_menu.nutrients, 
                            selected_menu.ingredients, selected_menu.category, new_ratio)
                child_menus.append(new_menu)
            child_meals.append(Meal(child_menus, meal1.date, meal1.meal_type))
        
        return Diet(child_meals)
    
    def mutate(self, diet: Diet) -> Diet:
        mutated_meals = []
        for meal in diet.meals:
            if np.random.random() < self.mutation_prob:
                mutated_menus = []
                for menu in meal.menus:
                    if np.random.random() < self.mutation_menu_prob:
                        same_category_menus = [m for m in self.all_menus if m.category == menu.category]
                        if same_category_menus:
                            selected_menu = np.random.choice(same_category_menus)
                        else:
                            selected_menu = menu
                        new_menu = Menu(selected_menu.name, selected_menu.nutrients, selected_menu.ingredients, selected_menu.category, np.random.uniform(0.6, 1.0))
                    else:
                        new_menu = Menu(menu.name, menu.nutrients, menu.ingredients, menu.category, np.clip(menu.serving_ratio + np.random.normal(0, 0.1), 0.6, 1.0))
                    mutated_menus.append(new_menu)
                mutated_meals.append(Meal(mutated_menus, meal.date, meal.meal_type))
            else:
                mutated_meals.append(meal)
        return Diet(mutated_meals)

    def fitness(self, diet_db: Diet, weeklydiet: Diet) -> List[float]:
        '''if not self.validate_nutrient_constraints(weeklydiet):
            return [-float('inf'), -float('inf'), -float('inf'), -float('inf')]'''
        
        nutrition_score = evaluate_nutrition(weeklydiet, self.nutrient_constraints)
        cost_score = evaluate_cost(diet_db, weeklydiet)
        harmony_score = evaluate_harmony(diet_db, weeklydiet)
        diversity_score = evaluate_diversity(weeklydiet)
        # Convert all to Python float for consistent output formatting
        return [float(nutrition_score), float(cost_score), float(harmony_score), float(diversity_score)]
        
    def check_termination(self, initial_fitness, current_solutions, diet_db):
            improved_count = 0
            valid_constraint_count = 0
            current_valid_solutions = []
            
            print(f"\n=== 종료 조건 체크 (해 개수: {len(current_solutions)}) ===")

            for i, diet in enumerate(current_solutions):
                current_fitness = self.fitness(diet_db, diet)
                improvements = sum(1 for init, curr in zip(initial_fitness, current_fitness) if curr > init)
                
                constraint_satisfied, violations = validate_weekly_constraints_detailed(diet, self.nutrient_constraints)
                if constraint_satisfied:
                    valid_constraint_count += 1
                    
                print(f"해 {i+1}: {improvements}가지 개선, 제약조건 {'만족' if constraint_satisfied else '위반'} {current_fitness}")
                
                if violations:
                    print(f"  위반사항: {', '.join(violations)}")

                # 3가지 이상 개선된 해는 무조건 backup에 저장 (중복 체크 완화)
                if improvements >= 3:
                    self.backup_solutions.append((diet, improvements, constraint_satisfied))

                # 제약조건 만족하는 모든 해를 저장 (개선 수 상관없이)
                if constraint_satisfied:
                    self.constraint_solutions.append((diet, improvements))

                # 기존 조건: 3가지 이상 개선 + 제약조건 만족
                if improvements >= 3 and constraint_satisfied and not self._is_duplicate(diet):
                    current_valid_solutions.append(diet)
                    improved_count += 1
            
            for diet in current_valid_solutions:
                if not self._is_duplicate(diet):
                    self.good_solutions_archive.append(diet)
            
            self.good_solutions_archive = [
                diet for diet in self.good_solutions_archive if validate_weekly_constraints(diet, self.nutrient_constraints)
            ]
            
            print(f"제약조건 만족 해: {valid_constraint_count}/{len(current_solutions)}")
            print(f"현재 세대 수집된 해: {len(current_valid_solutions)}개")
            print(f"총 수집된 좋은 해: {len(self.good_solutions_archive)}개")
            print(f"백업 해: {len(self.backup_solutions)}개")
            print(f"제약조건 해: {len(self.constraint_solutions)}개")
            
            return len(self.good_solutions_archive) >= 5

    def _is_duplicate_in_backup(self, new_diet):
        new_menus = [meal.menus[0].name for meal in new_diet.meals[:10]]
        for diet, _, _ in self.backup_solutions:
            existing_menus = [meal.menus[0].name for meal in diet.meals[:10]]
            if new_menus == existing_menus:
                return True
        return False

    def _is_duplicate_final(self, new_diet, solution_list):
            new_signature = [(meal.menus[0].name, round(meal.menus[0].serving_ratio, 2)) 
                            for meal in new_diet.meals[:10]]
            for existing_diet in solution_list:
                existing_signature = [(meal.menus[0].name, round(meal.menus[0].serving_ratio, 2)) 
                                    for meal in existing_diet.meals[:10]]
                if new_signature == existing_signature:
                    return True
            return False

    def _is_duplicate_in_constraint(self, new_diet):
        new_menus = [meal.menus[0].name for meal in new_diet.meals[:10]]
        for diet, _ in self.constraint_solutions:
            existing_menus = [meal.menus[0].name for meal in diet.meals[:10]]
            if new_menus == existing_menus:
                return True
        return False

    def get_final_solutions(self, diet_db) -> List[Diet]:
        print(f"\n=== get_final_solutions 시작 ===")
        print(f"good_solutions_archive: {len(self.good_solutions_archive)}개")
        print(f"backup_solutions: {len(self.backup_solutions)}개")
        print(f"constraint_solutions: {len(self.constraint_solutions)}개")
        
        if len(self.good_solutions_archive) >= 5:
            return self.good_solutions_archive[:5]
        
        final_solutions = self.good_solutions_archive[:]
        needed = 5 - len(final_solutions)
        print(f"추가로 필요한 해: {needed}개")
        
        # 1단계: backup_solutions에서 제약조건 만족하는 해 우선 선택
        constraint_satisfied_backup = [(diet, imp, cs) for diet, imp, cs in self.backup_solutions if cs]
        constraint_violated_backup = [(diet, imp, cs) for diet, imp, cs in self.backup_solutions if not cs]
        
        print(f"제약조건 만족 백업해: {len(constraint_satisfied_backup)}개")
        print(f"제약조건 위반 백업해: {len(constraint_violated_backup)}개")
        
        # 제약조건 만족하는 백업해부터 추가
        added_from_backup_satisfied = 0
        for diet, improvements, constraint_satisfied in sorted(constraint_satisfied_backup, key=lambda x: x[1], reverse=True):
            if needed <= 0:
                break
            if not self._is_duplicate_final(diet, final_solutions):
                final_solutions.append(diet)
                needed -= 1
                added_from_backup_satisfied += 1
                print(f"백업(제약만족)에서 추가: {improvements}가지 개선")
            # else:
            #     print(f"중복으로 제외: {improvements}가지 개선")
        
        print(f"제약조건 만족 백업에서 추가된 해: {added_from_backup_satisfied}개")
        
        # 2단계: 여전히 부족하면 제약조건 위반하는 백업해 추가
        added_from_backup_violated = 0
        for diet, improvements, constraint_satisfied in sorted(constraint_violated_backup, key=lambda x: x[1], reverse=True):
            if needed <= 0:
                break
            if not self._is_duplicate_final(diet, final_solutions):
                final_solutions.append(diet)
                needed -= 1
                added_from_backup_violated += 1
                print(f"백업(제약위반)에서 추가: {improvements}가지 개선")
        
        print(f"제약조건 위반 백업에서 추가된 해: {added_from_backup_violated}개")
        
        # 3단계: 여전히 부족하면 제약조건만 만족하는 해로 채우기
        if needed > 0:
            unique_constraint_solutions = []
            for diet, improvements in self.constraint_solutions:
                if not self._is_duplicate_final(diet, final_solutions + [d for d, _ in unique_constraint_solutions]):
                    unique_constraint_solutions.append((diet, improvements))
            
            print(f"유니크한 제약조건 해: {len(unique_constraint_solutions)}개")
            
            added_from_constraint = 0
            for diet, improvements in sorted(unique_constraint_solutions, key=lambda x: x[1], reverse=True):
                if needed <= 0:
                    break
                final_solutions.append(diet)
                needed -= 1
                added_from_constraint += 1
                print(f"제약조건 해에서 추가: {improvements}가지 개선")
            
            print(f"제약조건 해에서 추가된 해: {added_from_constraint}개")
        
        print(f"최종 반환 해 개수: {len(final_solutions)}개")
        return final_solutions
            
    def _is_duplicate(self, new_diet):
        new_signature = [(meal.menus[0].name, round(meal.menus[0].serving_ratio, 2)) 
                        for meal in new_diet.meals[:10]]
        for existing_diet in self.good_solutions_archive:
            existing_signature = [(meal.menus[0].name, round(meal.menus[0].serving_ratio, 2)) 
                                 for meal in existing_diet.meals[:10]]
            if new_signature == existing_signature:
                return True
        return False
