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
                adjusted_nutrients = menu.get_adjusted_nutrients()
                for nutrient, amount in adjusted_nutrients.items():
                    daily_nutrients[nutrient] += amount
        
        day_score = 100
        nutrient_count = len(daily_nutrients)
        max_penalty_per_nutrient = 100 / nutrient_count
        
        for nutrient, C_n in daily_nutrients.items():
            L_n = nutrient_constraints.min_values[nutrient]  # 최소 기준값
            U_n = nutrient_constraints.max_values[nutrient]  # 최대 기준값
            W_n = nutrient_constraints.weights[nutrient]  # 중요도 가중치

            M_n = L_n if C_n < L_n else U_n if C_n > U_n else C_n

            P_n = min(max_penalty_per_nutrient, abs((C_n - M_n) / M_n) * W_n * max_penalty_per_nutrient)

            day_score -= P_n

        day_score = max(0, day_score)  # 점수는 최소 0으로 제한
        total_score += day_score

    final_score = total_score / days

    normalized_score = max(0, min(100, final_score))

    return normalized_score

def evaluate_cost(diet_db: Diet, weekly_diet: Diet) -> float:
    total_cost = sum(menu.get_adjusted_price() for meal in weekly_diet.meals for menu in meal.menus)

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
    cost_score = 100 - normalized_cost

    return max(0, min(100, cost_score))  # 0 ~ 100

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
    harmony_matrix, _, _, menu_to_index = calculate_harmony_matrix(diet_db)
    
    weekly_menus = [menu.name for meal in weeklydiet.meals for menu in meal.menus]
    total_pairs = 0
    harmony_sum = 0
    
    for i in range(len(weekly_menus)):
        for j in range(i+1, len(weekly_menus)):
            menu1, menu2 = weekly_menus[i], weekly_menus[j]
            if menu1 in menu_to_index and menu2 in menu_to_index:
                idx1, idx2 = menu_to_index[menu1], menu_to_index[menu2]
                harmony_sum += harmony_matrix[idx1, idx2]
                total_pairs += 1
    
    if total_pairs == 0:
        return 0
    
    avg_harmony = harmony_sum / total_pairs
    max_harmony = np.max(harmony_matrix)
    
    return (avg_harmony / max_harmony * 100) if max_harmony > 0 else 0

def get_top_n_harmony_pairs(harmony_matrix, menus, n=5):
    harmony_matrix_no_diag = harmony_matrix - np.diag(np.diag(harmony_matrix))
    top_pairs = []
    for i in range(len(menus)):
        for j in range(i+1, len(menus)):
            if harmony_matrix_no_diag[i, j] > 0:
                top_pairs.append((menus[i], menus[j], harmony_matrix_no_diag[i, j]))
    return sorted(top_pairs, key=lambda x: x[2], reverse=True)[:n]

def evaluate_diversity(weeklydiet: Diet) -> float:
    menu_counts = Counter()
    total_menus = 0
    
    for meal in weeklydiet.meals:
        for menu in meal.menus:
            menu_counts[menu.name] += 1
            total_menus += 1
    
    if total_menus == 0:
        return 0
    
    simpson_index = sum((count / total_menus) ** 2 for count in menu_counts.values())
    simpson_diversity = 1 - simpson_index
    
    return simpson_diversity * 100

def validate_weekly_constraints_detailed(weeklydiet: Diet, nutrient_constraints: NutrientConstraints):
    days = len(weeklydiet.meals) // 3
    total_nutrients = {nutrient: 0 for nutrient in nutrient_constraints.min_values}
    
    for meal in weeklydiet.meals:
        for menu in meal.menus:
            adjusted_nutrients = menu.get_adjusted_nutrients()
            for nutrient, amount in adjusted_nutrients.items():
                total_nutrients[nutrient] += amount
    
    violations = []
    for nutrient, total_amount in total_nutrients.items():
        daily_avg = total_amount / days
        min_val = nutrient_constraints.min_values[nutrient]
        max_val = nutrient_constraints.max_values[nutrient]
        
        if daily_avg < min_val:
            violations.append(f"{nutrient}: {daily_avg:.1f} < {min_val} (부족)")
        elif daily_avg > max_val:
            violations.append(f"{nutrient}: {daily_avg:.1f} > {max_val} (과다)")
    
    is_valid = len(violations) == 0
    return is_valid, violations

def validate_weekly_constraints(weeklydiet: Diet, nutrient_constraints: NutrientConstraints) -> bool:
    is_valid, _ = validate_weekly_constraints_detailed(weeklydiet, nutrient_constraints)
    return is_valid