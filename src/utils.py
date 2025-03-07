import pandas as pd

def diet_to_dataframe(diet, title: str) -> pd.DataFrame:
    meals_dict = {f'{i+1}일': [] for i in range(7)}
    
    for i in range(7):
        day_meals = {
            '아침': "",
            '점심': "",
            '저녁': ""
        }
        for meal in diet.meals[i*3:(i+1)*3]: 
            menu_names = "\n".join([f"({menu.category}) {menu.name}" for menu in meal.menus])
            day_meals[meal.meal_type.capitalize()] = menu_names
        
        meals_dict[f'{i+1}일'].extend([day_meals['아침'], day_meals['점심'], day_meals['저녁']])
    
    df = pd.DataFrame(meals_dict, index=['아침', '점심', '저녁'])
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
