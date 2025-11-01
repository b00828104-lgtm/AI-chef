from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/recipes")
def get_recipes(ingredients: str = Query(...)):
    ingredient_list = [i.strip() for i in ingredients.split(",")]

    recipes = []
    for ingredient in ingredient_list:
        r = requests.get(f"https://www.themealdb.com/api/json/v1/1/filter.php?i={ingredient}", timeout=10)
        data = r.json()
        if data.get("meals"):
            for meal in data["meals"]:
                recipes.append({
                    "title": meal["strMeal"],
                    "image": meal["strMealThumb"],
                    "id": meal["idMeal"]
                })

    return {"recipes": list({r["id"]: r for r in recipes}.values())}