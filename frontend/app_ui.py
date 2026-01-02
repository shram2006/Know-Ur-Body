import streamlit as st
import sys
import os
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Know Ur Body – Smart Nutrition Check",
    page_icon="🥗",
    layout="wide"
)

# ---------------- FONT + UI ----------------
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@200;300;400;600;700&display=swap" rel="stylesheet">

<style>
html, body, .stApp, .block-container, [class*="css"], p, div, span, input, select, button {
    font-family: 'JetBrains Mono', monospace !important;
}

h1 { font-size: 2.4rem !important; }
h2 { font-size: 1.6rem !important; }

.stButton>button {
    font-weight: 600 !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------- BACKEND LOGIC IMPORTS ----------------
sys.path.append(os.path.abspath("backend"))

from bmi import calculate_bmi, categorize_bmi
from impact_engine import compute_food_impact
from ai_recommender import recommend_alternatives

# ---------------- LOAD FOOD DATABASE ----------------
@st.cache_data
def load_food_db():
    return pd.read_csv("backend/food_db.csv")

FOOD_DB = load_food_db()
FOODS = sorted(FOOD_DB["name"].tolist())

# ---------------- TITLE ----------------
st.title("🥗 Know Ur Body – Smart Nutrition Check")
st.caption("AI-powered nutrition analysis with BMI-based health insights")

# ---------------- USER PROFILE ----------------
st.header("👤 User Profile")

age = st.number_input("Age", 10, 90, 20)
gender = st.selectbox("Gender", ["male", "female"])
height = st.number_input("Height (cm)", 100, 250, 170)
weight = st.number_input("Weight (kg)", 20.0, 200.0, 65.0)
activity = st.selectbox("Activity Level", ["low", "moderate", "high"])

# ---------------- FOOD SELECTION ----------------
st.header("🍜 Food Selection")

food_name = st.selectbox("Select Food Item", FOODS)
quantity = st.number_input("Quantity (grams)", 10, 2000, 100)

# ---------------- ANALYZE BUTTON ----------------
# ---------------- ANALYZE BUTTON ----------------
if st.button("Analyze Impact"):

    # ---- BMI ----
    bmi = calculate_bmi(weight, height)
    bmi_category = categorize_bmi(bmi)

    # ---- FOOD IMPACT ----
    food_row = FOOD_DB[FOOD_DB["name"] == food_name].iloc[0].to_dict()

    impact = compute_food_impact(
        food=food_row,
        quantity_g=quantity,
        bmi=bmi
    )

    # ---- AI RECOMMENDATIONS (SMART) ----
    ai_recommendations = recommend_alternatives(
        food_name,
        bmi_category,
        impact
    )

    st.success("Analysis Complete!")

    # ---------------- BMI RESULT ----------------
    st.subheader("📊 BMI Information")
    st.write(f"**BMI:** {round(bmi, 2)}")
    st.info(f"Category: **{bmi_category}**")

    # ---------------- NUTRITION CHART ----------------
    st.subheader("🔥 Nutrition Breakdown")

    macro_df = pd.DataFrame({
        "Nutrient": ["Calories", "Carbs", "Fat", "Protein", "Sugar"],
        "Value": [
            impact["calories"],
            impact["carbs"],
            impact["fat"],
            impact["protein"],
            impact["sugar"]
        ]
    })

    st.bar_chart(macro_df.set_index("Nutrient"))

    # ---------------- IMPACT MESSAGES ----------------
    st.subheader("⚠️ Health Impact Messages")
    for msg in impact["impact_messages"]:
        st.write("•", msg)

    # ---------------- AI RECOMMENDATIONS ----------------
    st.subheader("🤖 AI-Based Healthier Alternatives")
    for rec in ai_recommendations:
        st.write("👉", rec)

    # ---------------- OVERALL RESULT ----------------
    st.subheader("🏁 Overall Impact")
    st.write(f"### {impact['overall']}")
