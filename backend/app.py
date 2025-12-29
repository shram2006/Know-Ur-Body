import os
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .ai_recommender import recommend_alternatives
from .bmi import calculate_bmi, categorize_bmi
from .impact_engine import compute_food_impact
app = FastAPI(title="Know Ur Body API")
FOOD_DB_PATH = os.path.join(os.path.dirname(__file__), "food_db.csv")
food_df = pd.read_csv(FOOD_DB_PATH)
class UserProfile(BaseModel):
    age: int
    gender: str
    height_cm: float
    weight_kg: float
    activity_level: str
class FoodRequest(BaseModel):
    profile: UserProfile
    food_name: str
    quantity_g: float
@app.get("/foods")
def list_foods():
    
    return sorted(food_df["name"].tolist())
@app.post("/analyze")
def analyze_food(req: FoodRequest):

    bmi = calculate_bmi(req.profile.weight_kg, req.profile.height_cm)
    bmi_category = categorize_bmi(bmi)

    ai_recommendations = recommend_alternatives(
        req.food_name,
        bmi_category
)
    row = food_df[food_df["name"].str.lower() == req.food_name.lower()]
    if row.empty:
        raise HTTPException(404, "Food not found in database.")
    food = row.iloc[0].to_dict()
    impact = compute_food_impact(food, req.quantity_g, bmi)
    highlights = []
    if impact["sodium"] > 500:
        highlights.append("💓 High sodium → blood pressure load increases.")
    if impact["carbs"] > 40:
        highlights.append("🩸 High carbs → blood sugar spike likely.")
    if impact["fat"] > 15:
        highlights.append("🧍 Excess fat → belly fat storage increases.")
    if impact["sugar"] > 20:
        highlights.append("⚡ Sugar spike → energy crash expected.")
    if not highlights:
        highlights.append("✅ No major negative body stress detected.")
    return {
        "bmi": bmi,
        "bmi_category": bmi_category,
        "nutrition": {
            "calories": impact["calories"],
            "carbs": impact["carbs"],
            "fat": impact["fat"],
            "protein": impact["protein"],
            "sodium": impact["sodium"],
            "sugar": impact["sugar"],
        },
        "overall_impact": impact["overall"],
        "score_change": impact["score_change"],
        "messages": impact["impact_messages"],
        "highlights": highlights,
        "ai_recommendations": ai_recommendations

    }