from typing import List, Dict

SERVINGS = 55

def set_servings(servings: int):
    global SERVINGS
    SERVINGS = servings

def get_servings() -> int:
    return SERVINGS

class Ingredient:
    def __init__(self, name: str, price_per_g: float, amount_g: float, package_size: float):
        self.name = name
        self.price_per_g = price_per_g 
        self.amount_g = amount_g
        self.package_size = package_size
        self.package_price = price_per_g * package_size

class Menu:
    def __init__(self, name: str, nutrients: Dict[str, float], ingredients: List[Ingredient], category: str, serving_ratio: float = 1.0):
        self.name = name
        self.nutrients = nutrients
        self.ingredients = ingredients
        self.category = category
        self.serving_ratio = serving_ratio  # 0.6, 0.9 범위
    
    def get_adjusted_nutrients(self):
        return {k: v * self.serving_ratio for k, v in self.nutrients.items()}
    
    def get_adjusted_ingredients(self):
        adjusted = []
        for ing in self.ingredients:
            adjusted_ing = Ingredient(
                name=ing.name,
                price_per_g=ing.price_per_g,
                amount_g=ing.amount_g * self.serving_ratio,
                package_size=ing.package_size
            )
            adjusted.append(adjusted_ing)
        return adjusted

class Meal:
    def __init__(self, menus: List[Menu], date: str, meal_type: str):
        self.menus = menus
        self.date = date
        self.meal_type = meal_type

class Diet:
    def __init__(self, meals: List[Meal]):
        self.meals = meals

class WeeklyDiet:
    def __init__(self, diets: List[Diet]):
        self.diets = diets

class NutrientConstraints:
    def __init__(self, min_values: Dict[str, float], max_values: Dict[str, float], weights: Dict[str, float]):
        self.min_values = min_values
        self.max_values = max_values
        self.weights = weights