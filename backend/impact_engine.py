from typing import Dict
def compute_food_impact(food : Dict, quantity_g: float, bmi: float) -> Dict:
    impact_messages = []
    factor = quantity_g / 100.0
    calories = food["calories"] * factor
    carbs = food["carbs"] * factor
    fat = food["fat"] * factor
    protein = food["protein"] * factor
    sodium = food["sodium"] * factor
    sugar = food["sugar"] * factor
    category = food["category"]
    impact_message = []
    score_change = 0
    if calories > 300:
        impact_messages.append("High calorie intake - may lead to weight gain.")
        score_change -= 10
    elif calories > 150:
        impact_messages.append("Moderate calories - okay if within daily limit.")
        score_change -= 3
    else:
        impact_messages.append("Low-to-moderate calories - light on the stomach.")
        score_change += 2
    if carbs > 40:
        impact_messages.append("High carbs - may cause a blood sugar spike.")
        score_change -= 6
    if fat > 15:
        impact_messages.append("High fat - increases fat storage risk.")
        score_change -= 6
    if protein > 15:
        impact_messages.append("Good protein amount - supports muscles.")
        score_change += 5
    if sodium > 800:
        impact_messages.append("Very high sodium - increases blood pressure load.")
        score_change -= 12
    elif sodium > 400:
        impact_messages.append("Moderate sodium - monitor intake today.")
        score_change -= 4
    if sugar > 20:
        impact_messages.append("High sugar - quick energy spike then crash.")
        score_change -= 8
    elif sugar > 5:
        impact_messages.append("Some sugar - okay in moderation.")
    else:
        impact_messages.append("Low sugar - stable energy.")
    if category == "processed":
        impact_messages.append("Processed food - contains additives/preservatives.")
        score_change -= 5
    elif category == "fruit":
        impact_messages.append("Natural fruit - good vitamins and fiber.")
        score_change += 4
    elif category == "veggie":
        impact_messages.append("Vegetable-based - great for digestion.")
        score_change += 5
    if bmi >= 25:
        impact_messages.append("Higher BMI - more likely to store excess calories as fat.")
        score_change -= 5
    elif bmi < 18.5:
        impact_messages.append("Low BMI - calories may help healthy weight gain.")
    if score_change <= -15:
        overall = "High Negative Impact"
    elif score_change <= -5:
        overall = "Moderate Negative Impact"
    elif score_change < 5:
        overall = "Neutral Impact"
    else:
        overall = "Positive Impact"
    return {
        "calories": round(calories, 1),
        "carbs": round(carbs, 1),
        "fat": round(fat, 1),
        "protein": round(protein, 1),
        "sodium": round(sodium, 1),
        "sugar": round(sugar, 1),
        "impact_messages": impact_messages,
        "score_change": score_change,
        "overall": overall
    }