import streamlit as st
import requests
st.set_page_config(
    page_title="Know Ur Body – Smart Nutrition Check",
    page_icon="🥗",
    layout="wide"
)
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
BACKEND_URL = "http://127.0.0.1:8000"
st.title("🥗 Know Ur Body – Smart Nutrition Check")
st.write("Understand how your food choices affect your body.")
st.header("👤 User Profile")
age = st.number_input("Age", 10, 90, 20)
gender = st.selectbox("Gender", ["male", "female"])
height = st.number_input("Height (cm)", 100, 250, 170)
weight = st.number_input("Weight (kg)", 20.0, 200.0, 65.0)
activity = st.selectbox("Activity Level", ["low", "moderate", "high"])
foods = requests.get(f"{BACKEND_URL}/foods").json()
st.header("🍜 Food Selection")
food_name = st.selectbox("Select Food Item", foods)
quantity = st.number_input("Quantity (grams)", 10, 2000, 100)
if st.button("Analyze Impact"):
    payload = {
        "profile": {
            "age": age,
            "gender": gender,
            "height_cm": height,
            "weight_kg": weight,
            "activity_level": activity
        },
        "food_name": food_name,
        "quantity_g": quantity
    }
    response = requests.post(f"{BACKEND_URL}/analyze", json=payload)
    if response.status_code == 200:
        data = response.json()
        st.success("Analysis Complete!")
        st.subheader("📊 BMI Information")
        st.write(f"**BMI:** {data['bmi']} — *{data['bmi_category']}*")
        st.subheader("🔥 Nutrition Breakdown")
        st.json(data["nutrition"])
        st.subheader("⚠️ Impact Messages")
        for msg in data["messages"]:
            st.write("• " + msg)
        st.subheader("🔍 Body Highlights")
        for h in data["highlights"]:
            st.markdown(f"**{h}**")
        st.subheader("🏁 Overall Impact")
        st.write(f"### {data['overall_impact']}")
        st.subheader("🤖 AI-Recommended Healthier Alternatives")
        for item in data["ai_recommendations"]:
            st.write(f"👉 {item}")
    else:
        st.error("Backend Error: Could not analyze food. Check server.")