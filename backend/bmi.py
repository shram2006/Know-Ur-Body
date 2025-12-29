def calculate_bmi(weight_kg : float, height_cm : float) -> float:
    height_m = height_cm / 100
    if height_m <= 0:
        return 0
    return round(weight_kg / (height_m ** 2), 2)
def categorize_bmi(bmi: float) -> str :
    if bmi == 0:
        return "Invalid BMI"
    if bmi < 18.5:
        return "Underweight"
    if bmi < 25:
        return "Normal"
    if bmi < 30:
        return "Overweight"
    else:
        return "Obese"