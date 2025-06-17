import pandas as pd
from Diet_class import Meal, Diet

def diet_to_dataframe(diet, title: str) -> pd.DataFrame:
    meals_dict = {f'Day {i+1}': [] for i in range(7)}
    
    for i in range(7):
        day_meals = {
            'Breakfast': "",
            'Lunch': "",
            'Dinner': ""
        }
        for meal in diet.meals[i*3:(i+1)*3]: 
            menu_names = "\n".join([
                f"({menu.category}) {menu.name} ({menu.serving_ratio:.1f}배)" 
                for menu in meal.menus
            ])
            day_meals[meal.meal_type.capitalize()] = menu_names
        
        meals_dict[f'Day {i+1}'].extend([day_meals['Breakfast'], day_meals['Lunch'], day_meals['Dinner']])
    
    df = pd.DataFrame(meals_dict, index=['Breakfast', 'Lunch', 'Dinner'])
    df.columns.name = title 
    
    return df

def count_menu_changes(initial_diet, optimized_diet):
    changes = {}
    for initial_meal, optimized_meal in zip(initial_diet.meals, optimized_diet.meals):
        if not initial_meal.menus or not optimized_meal.menus:
            continue
            
        for initial_menu, optimized_menu in zip(initial_meal.menus, optimized_meal.menus):
            category = initial_menu.category or "기타"
            if category not in changes:
                changes[category] = {'total': 0, 'changed': 0}
            changes[category]['total'] += 1
            if initial_menu.name != optimized_menu.name:
                changes[category]['changed'] += 1
    return changes

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