import streamlit as st
import requests

# === Streamlit 页面设置 ===
st.set_page_config(page_title="AI Chef", page_icon="🍳")
st.title("🍳 AI Chef")
st.write("Enter ingredients you have, and I'll recommend recipes using our FastAPI backend.")

# === 输入栏 ===
ingredients = st.text_input("Ingredients (comma separated)", "chicken, rice, onion")

# === 调用 FastAPI 的函数 ===
def get_recipes_from_api(ingredients):
    url = "http://127.0.0.1:8000/recipes"
    params = {"ingredients": ingredients}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("recipes", [])
    else:
        return None

# === 按钮触发 ===
if st.button("Find Recipes"):
    with st.spinner("Finding yummy dishes... 🍽️"):
        recipes = get_recipes_from_api(ingredients)

        if recipes:
            st.subheader("🍽 Top Recipe Matches")

            for recipe in recipes[:3]:  # 只展示前三个
                st.markdown(f"### {recipe['title']}")
                st.image(recipe["image"], width=250)
                st.write(f"**Meal ID:** {recipe['id']}")
                st.write("---")
        else:
            st.error("No recipes found. Try more common ingredients 👨‍🍳")