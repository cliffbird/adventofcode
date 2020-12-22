from main import BaseProcessor
import re

class D21Processor(BaseProcessor):
    def run1(self):
        self.foods = set()
        with open(self.path, "r") as f:
            for line in f:
                line = line.strip()
                f = Food(line)
                self.foods.add(f)

        all_ingredients = set()
        self.a_to_i = {}

        for f in self.foods:
            for ingredient in f.ingredients:
                all_ingredients.add(ingredient)

            for allergen in f.allergens:
                if allergen not in self.a_to_i:
                    self.a_to_i[allergen] = set(f.ingredients)
                else:
                    self.a_to_i[allergen] = self.a_to_i[allergen].intersection(set(f.ingredients))


        with_allergens = set()
        for allergen, ingredients in self.a_to_i.items():
            with_allergens = with_allergens.union(set(ingredients))
        self.with_allergens = with_allergens

        without_allergens = all_ingredients.difference(with_allergens)

        without_appearances_count = 0
        for f in self.foods:
            for ingredient in f.ingredients:
                if ingredient in without_allergens:
                    without_appearances_count += 1

        print(f"part1: {without_appearances_count}")

    def run2(self):
        confirmed = []

        num_ingredients = len(self.with_allergens)
        while len(confirmed) < num_ingredients:
            ingredient_to_remove = None
            for allergen, ingredients in self.a_to_i.items():
                if len(ingredients) == 1:
                    ingredient_to_remove = ingredients.pop()
                    break
            assert ingredient_to_remove
            confirmed.append((allergen, ingredient_to_remove))

            del self.a_to_i[allergen]
            for allergen, ingredients in self.a_to_i.items():
                if ingredient_to_remove in ingredients:
                    ingredients.remove(ingredient_to_remove)

        confirmed.sort(key=lambda x: x[0])

        ingredients_sorted = []
        for allergen,ingredient in confirmed:
            ingredients_sorted.append(ingredient)
        print(f"part2: {','.join(ingredients_sorted)}")

class Food:
    def __init__(self, line):
        m = re.match("^(.+?) \(contains (.+)\)$", line)
        self.ingredients = m.group(1).split()
        self.allergens = m.group(2).split(", ")
