from fastapi import FastAPI, Query
import requests

app = FastAPI()

@app.get("/recipes")
def get_recipes(ingredients: str = Query(..., description="Comma separated ingredients")):
    ingredient_list = [i.strip() for i in ingredients.split(",")]

    recipes = []
    for ingredient in ingredient_list:
        response = requests.get(f"https://www.themealdb.com/api/json/v1/1/filter.php?i={ingredient}")
        data = response.json()
        if data.get("meals"):
            for meal in data["meals"]:
                recipes.append({
                    "title": meal["strMeal"],
                    "image": meal["strMealThumb"],
                    "id": meal["idMeal"]
                })

    unique_recipes = {r["id"]: r for r in recipes}.values()

    return {"recipes": list(unique_recipes)}