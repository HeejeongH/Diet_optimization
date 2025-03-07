from Diet_class import Menu, Diet, NutrientConstraints
import numpy as np
from collections import Counter

def evaluate_nutrition(weeklydiet: Diet, nutrient_constraints: NutrientConstraints) -> float:
    days = len(weeklydiet.meals) // 3
    total_score = 0
    
    for day in range(days):
        daily_nutrients = {nutrient: 0 for nutrient in nutrient_constraints.min_values}
        start_idx = day * 3
        for meal in weeklydiet.meals[start_idx:start_idx + 3]:
            for menu in meal.menus:
                for nutrient, amount in menu.nutrients.items():
                    daily_nutrients[nutrient] += amount
        
        day_score = 100  # 시작점수 100
        nutrient_count = len(daily_nutrients)
        max_penalty_per_nutrient = 100 / nutrient_count
        
        for nutrient, C_n in daily_nutrients.items():
            L_n = nutrient_constraints.min_values[nutrient]  # 최소 기준값
            U_n = nutrient_constraints.max_values[nutrient]  # 최대 기준값
            W_n = nutrient_constraints.weights[nutrient]  # 중요도 가중치

            M_n = L_n if C_n < L_n else U_n if C_n > U_n else C_n

            P_n = min(max_penalty_per_nutrient, abs((C_n - M_n) / M_n) * W_n * max_penalty_per_nutrient)

            #print(f"{nutrient}: amount={C_n:.2f}, min={L_n}, max={U_n}, weight={W_n}, penalty={P_n:.2f}")

            day_score -= P_n

        day_score = max(0, day_score)  # 점수는 최소 0으로 제한
        #print(f"Day {day+1} Score: {day_score:.2f}")
        total_score += day_score

    final_score = total_score / days
    #print(f"\nFinal Average Score: {final_score:.2f}")

    normalized_score = max(0, min(100, final_score))
    #print(f"Normalized Score: {normalized_score:.2f}")

    return normalized_score

def evaluate_cost(diet_db: Diet, weeklydiet: Diet) -> float:
    total_cost = 0
    for meal in weeklydiet.meals:
        for menu in meal.menus:
            total_cost += sum(ingredient.price for ingredient in menu.ingredients)

    cost_db = []
    for meal in diet_db.meals:
        meal_cost = 0
        for menu in meal.menus:
            meal_cost += sum(ingredient.price for ingredient in menu.ingredients)
        cost_db.append(meal_cost)
    sorted_cost_db = sorted(cost_db)
    min_cost = sum(sorted_cost_db[:21])
    max_cost = sum(sorted_cost_db[-21:])

    normalized_cost = (total_cost - min_cost) / (max_cost - min_cost) * 100

    return -normalized_cost # -100 ~ 0

def calculate_harmony_matrix(diet_db: Diet):
    all_menus = set()
    menu_counts = Counter()
    for meal in diet_db.meals:
        meal_menus = [menu.name for menu in meal.menus]
        all_menus.update(meal_menus)
        menu_counts.update(meal_menus)
    
    all_menus = sorted(all_menus)
    menu_to_index = {menu: i for i, menu in enumerate(all_menus)}
    
    n_menus = len(all_menus)
    harmony_matrix = np.zeros((n_menus, n_menus), dtype=int)
    
    for meal in diet_db.meals:
        menu_names = [menu.name for menu in meal.menus]
        for i, menu1 in enumerate(menu_names):
            for menu2 in menu_names[i+1:]:
                idx1, idx2 = menu_to_index[menu1], menu_to_index[menu2]
                harmony_matrix[idx1, idx2] += 1
                harmony_matrix[idx2, idx1] += 1
    
    for menu, count in menu_counts.items():
        idx = menu_to_index[menu]
        harmony_matrix[idx, idx] = count
    
    return harmony_matrix, all_menus, menu_counts, menu_to_index

def evaluate_harmony(diet_db: Diet, weeklydiet: Diet) -> float:
    harmony_matrix, all_menus, _, menu_to_index = calculate_harmony_matrix(diet_db)
    
    min_harmony = np.min(harmony_matrix)
    max_harmony = np.max(harmony_matrix)
    if max_harmony == min_harmony:
        return 0
    
    harmony_score = 0
    max_possible_harmony_score = 0
    
    all_menus_weekly = []
    for meal in weeklydiet.meals:
        all_menus_weekly.extend(menu.name for menu in meal.menus)
    
    for i in range(len(all_menus_weekly)):
        for j in range(i+1, len(all_menus_weekly)):
            idx1 = menu_to_index.get(all_menus_weekly[i])
            idx2 = menu_to_index.get(all_menus_weekly[j])
            if idx1 is not None and idx2 is not None:
                harmony_value = harmony_matrix[idx1, idx2]
                if max_harmony > min_harmony:
                    normalized_value = (harmony_value - min_harmony) / (max_harmony - min_harmony)
                    harmony_score += normalized_value
                max_possible_harmony_score += 1
    
    return harmony_score / max_possible_harmony_score * 100 if max_possible_harmony_score > 0 else 0

def get_top_n_harmony_pairs(harmony_matrix, menus, n=5):
    harmony_matrix_no_diag = harmony_matrix - np.diag(np.diag(harmony_matrix))
    top_pairs = []
    for i in range(len(menus)):
        for j in range(i+1, len(menus)):
            if harmony_matrix_no_diag[i, j] > 0:
                top_pairs.append((menus[i], menus[j], harmony_matrix_no_diag[i, j]))
    return sorted(top_pairs, key=lambda x: x[2], reverse=True)[:n]

def evaluate_diversity(weeklydiet: Diet) -> float:
    menu_occurrences = {}
    n_meals = len(weeklydiet.meals)
    
    for i, meal in enumerate(weeklydiet.meals):
        for menu in meal.menus:
            if menu.name not in menu_occurrences:
                menu_occurrences[menu.name] = []
            menu_occurrences[menu.name].append(i)
    
    diversity_scores = []
    
    for occurrences in menu_occurrences.values():
        if len(occurrences) > 1:
            distances = [occurrences[i+1] - occurrences[i] for i in range(len(occurrences)-1)]
            variance = np.var(distances)
            min_distance = min(distances)

            normalized_variance = (variance - 0) / (n_meals**2 / 4) 
            normalized_min_distance = (min_distance - 1) / (n_meals - 1) 

            diversity_score = 100 * (-normalized_variance + normalized_min_distance)
            diversity_scores.append(diversity_score)
    
    return np.mean(diversity_scores) if diversity_scores else 0 # 0 ~ 100