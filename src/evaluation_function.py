from Diet_class import Menu, Diet, NutrientConstraints, get_servings
import numpy as np
import math
from collections import Counter, defaultdict

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
            L_n = nutrient_constraints.min_values[nutrient]
            U_n = nutrient_constraints.max_values[nutrient]
            W_n = nutrient_constraints.weights[nutrient]

            M_n = L_n if C_n < L_n else U_n if C_n > U_n else C_n
            P_n = min(max_penalty_per_nutrient, abs((C_n - M_n) / M_n) * W_n * max_penalty_per_nutrient)
            day_score -= P_n

        day_score = max(0, day_score)
        total_score += day_score

    final_score = total_score / days
    normalized_score = max(0, min(100, final_score))
    return normalized_score

def calculate_actual_cost(diet: Diet, servings: int = None) -> float:
    if servings is None:
        servings = get_servings()
        
    ingredient_total = defaultdict(float)
    ingredient_info = {}
    
    for meal in diet.meals:
        for menu in meal.menus:
            adjusted_ingredients = menu.get_adjusted_ingredients()
            for ing in adjusted_ingredients:
                ingredient_total[ing.name] += ing.amount_g * servings
                if ing.name not in ingredient_info:
                    ingredient_info[ing.name] = {
                        'package_size': ing.package_size,
                        'package_price': ing.package_price
                    }
    
    total_cost = 0
    for ingredient_name, needed_amount in ingredient_total.items():
        if ingredient_name in ingredient_info:
            package_size = ingredient_info[ingredient_name]['package_size']
            package_price = ingredient_info[ingredient_name]['package_price']
            
            packages_needed = math.ceil(needed_amount / package_size)
            total_cost += packages_needed * package_price

    return total_cost

def evaluate_cost(diet_db: Diet, weekly_diet: Diet) -> float:
    from Diet_class import Menu, Diet, Meal
    
    servings = get_servings()
    weekly_cost = calculate_actual_cost(weekly_diet, servings)
    
    # 모든 메뉴 수집 및 중복 제거
    all_menus = []
    for meal in diet_db.meals:
        all_menus.extend(meal.menus)
    
    unique_menus = {}
    for menu in all_menus:
        if menu.name not in unique_menus:
            unique_menus[menu.name] = menu
    all_menus = list(unique_menus.values())
    
    # 카테고리별 메뉴 분류
    menu_by_category = {}
    for menu in all_menus:
        category = menu.category
        if category not in menu_by_category:
            menu_by_category[category] = []
        menu_by_category[category].append(menu)
    
    # 카테고리별 최저가/최고가 메뉴 찾기
    category_cheapest = {}
    category_expensive = {}
    
    for category, menus in menu_by_category.items():
        min_cost = float('inf')
        max_cost = 0
        cheapest_menu = None
        expensive_menu = None
        
        for menu in menus:
            temp_menu_min = Menu(menu.name, menu.nutrients, menu.ingredients, menu.category, 0.6)
            temp_meal_min = Meal([temp_menu_min], "temp", "temp")
            temp_diet_min = Diet([temp_meal_min])
            cost_min = calculate_actual_cost(temp_diet_min, servings)
            
            temp_menu_max = Menu(menu.name, menu.nutrients, menu.ingredients, menu.category, 1.0)
            temp_meal_max = Meal([temp_menu_max], "temp", "temp")
            temp_diet_max = Diet([temp_meal_max])
            cost_max = calculate_actual_cost(temp_diet_max, servings)
            
            if cost_min < min_cost:
                min_cost = cost_min
                cheapest_menu = menu
            
            if cost_max > max_cost:
                max_cost = cost_max
                expensive_menu = menu
        
        category_cheapest[category] = cheapest_menu
        category_expensive[category] = expensive_menu
    
    categories = ['밥', '국', '주찬', '부찬', '부찬', '김치']
    
    # 최저가 식단 생성
    min_meals = []
    for day in range(1, 8):
        for meal_type in ['Breakfast', 'Lunch', 'Dinner']:
            min_menus = []
            for category in categories:
                if category in category_cheapest:
                    cheapest = category_cheapest[category]
                    min_menu = Menu(cheapest.name, cheapest.nutrients, 
                                  cheapest.ingredients, cheapest.category, 0.6)
                    min_menus.append(min_menu)
            min_meals.append(Meal(min_menus, str(day), meal_type))
    
    min_diet = Diet(min_meals)
    min_cost = calculate_actual_cost(min_diet, servings)
    
    # 최고가 식단 생성
    max_meals = []
    for day in range(1, 8):
        for meal_type in ['Breakfast', 'Lunch', 'Dinner']:
            max_menus = []
            for category in categories:
                if category in category_expensive:
                    expensive = category_expensive[category] 
                    max_menu = Menu(expensive.name, expensive.nutrients,
                                  expensive.ingredients, expensive.category, 1.0)
                    max_menus.append(max_menu)
            max_meals.append(Meal(max_menus, str(day), meal_type))
    
    max_diet = Diet(max_meals)
    max_cost = calculate_actual_cost(max_diet, servings)
    
    if weekly_cost <= min_cost:
        cost_score = 100.0
    elif weekly_cost >= max_cost:
        cost_score = 0.0
    else:
        normalized_cost = (weekly_cost - min_cost) / (max_cost - min_cost)
        cost_score = (1 - normalized_cost) * 100
    
    return max(0, min(100, cost_score))

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