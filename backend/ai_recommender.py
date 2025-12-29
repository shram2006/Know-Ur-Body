def recommend_alternatives(food_name: str, bmi_category: str):
    food_name = food_name.lower()

    rules = {
        "maggi": [
            "Oats Upma",
            "Vegetable Poha",
            "Whole Wheat Sandwich"
        ],
        "ice cream (100g)": [
            "Greek Yogurt",
            "Fruit Bowl",
            "Dark Chocolate (small portion)"
        ],
        "pizza": [
            "Homemade Wheat Pizza",
            "Paneer Wrap",
            "Grilled Sandwich"
        ],
        "chips": [
            "Roasted Makhana",
            "Baked Sweet Potato",
            "Handful of Nuts"
        ]
    }

    # BMI-based adjustment
    if bmi_category in ["Overweight", "Obese"]:
        return rules.get(food_name, ["High-protein salad", "Boiled eggs", "Vegetable soup"])
    elif bmi_category == "Underweight":
        return ["Banana with peanut butter", "Milk smoothie", "Paneer sandwich"]
    else:
        return rules.get(food_name, ["Balanced homemade meal"])
