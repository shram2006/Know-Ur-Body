def recommend_alternatives(food_name: str, bmi_category: str, impact: dict):
    """
    Smart AI-style recommendation logic based on:
    - Food type
    - BMI category
    - Calories, sugar, fat levels
    """

    food_name = food_name.lower()

    calories = impact["calories"]
    sugar = impact["sugar"]
    fat = impact["fat"]

    recommendations = []

    # ---------------- BMI BASED GOALS ----------------
    if bmi_category in ["Overweight", "Obese"]:
        goal = "fat_loss"
    elif bmi_category == "Underweight":
        goal = "weight_gain"
    else:
        goal = "maintenance"

    # ---------------- SMART RULE ENGINE ----------------

    # HIGH CALORIE FOOD
    if calories > 400:
        recommendations.append("Reduce portion size by 30–40%")
        recommendations.append("Avoid late-night consumption")

    # HIGH SUGAR FOOD
    if sugar > 20:
        recommendations.append("Replace with low-sugar alternatives")
        recommendations.append("Pair with fiber-rich food to reduce sugar spike")

    # HIGH FAT FOOD
    if fat > 15:
        recommendations.append("Avoid combining with other fatty meals today")
        recommendations.append("Add light physical activity (walk 20 mins)")

    # ---------------- GOAL-SPECIFIC SUGGESTIONS ----------------
    if goal == "fat_loss":
        recommendations.extend([
            "Vegetable salad with lean protein",
            "Boiled eggs or paneer (small portion)",
            "Oats or millet-based meal"
        ])

    elif goal == "weight_gain":
        recommendations.extend([
            "Banana peanut butter smoothie",
            "Rice + dal + ghee (moderate)",
            "Paneer or egg-based meal"
        ])

    else:  # maintenance
        recommendations.extend([
            "Balanced home-cooked meal",
            "Include protein + vegetables",
            "Stay hydrated"
        ])

    # ---------------- FOOD-SPECIFIC SMART SWAPS ----------------
    if "ice cream" in food_name:
        recommendations.append("Greek yogurt with fruits")
        recommendations.append("Frozen banana smoothie")

    if "maggi" in food_name or "noodles" in food_name:
        recommendations.append("Vegetable oats upma")
        recommendations.append("Whole wheat noodles with veggies")

    if "pizza" in food_name:
        recommendations.append("Homemade wheat pizza")
        recommendations.append("Paneer veggie wrap")

    # ---------------- FINAL CLEANUP ----------------
    # Remove duplicates & limit output
    recommendations = list(dict.fromkeys(recommendations))

    return recommendations[:6]
