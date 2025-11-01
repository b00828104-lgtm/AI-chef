# app.py
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI(title="AI Chef API", version="1.0.0")

# 先放开跨域，等前端稳定后再收紧到你的 *.streamlit.app 域名
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "AI Chef API is running", "endpoints": ["/health", "/recipes"]}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/recipes")
def get_recipes(ingredients: str = Query(..., description="Comma separated ingredients")):
    ing_list = [i.strip() for i in ingredients.split(",") if i.strip()]

    candidates = []
    for ing in ing_list:
        r = requests.get(f"https://www.themealdb.com/api/json/v1/1/filter.php?i={ing}", timeout=10)
        data = r.json()
        for meal in (data.get("meals") or []):
            candidates.append({
                "title": meal["strMeal"],
                "image": meal["strMealThumb"],
                "id": meal["idMeal"]
            })

    # 去重
    unique = list({m["id"]: m for m in candidates}.values())
    return {"recipes": unique}