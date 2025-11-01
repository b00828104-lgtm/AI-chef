import streamlit as st
import requests

# === Streamlit 页面设置 ===
st.set_page_config(page_title="AI Chef", page_icon="🍳")
st.title("🍳 AI Chef")
st.write("Enter ingredients you have, and I'll recommend recipes using our FastAPI backend.")

# === 你的 Render 后端地址 ===
BACKEND_URL = "https://ai-chef-14yn.onrender.com/recipes"

# === 输入栏 ===
ingredients = st.text_input("Ingredients (comma separated)", "chicken, rice, onion")

# === 调用 FastAPI 的函数 ===
def get_recipes_from_api(ingredients):
    try:
        response = requests.get(BACKEND_URL, params={"ingredients": ingredients}, timeout=20)
        response.raise_for_status()
        return response.json().get("recipes", [])
    except Exception as e:
        st.error(f"❌ Backend error: {e}")
        return None

# === 按钮触发 ===
if st.button("Find Recipes"):
    with st.spinner("Cooking up suggestions... 🍽️"):
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