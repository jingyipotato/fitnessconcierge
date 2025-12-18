"""Meal planning tools."""


def calculate_daily_calories(
    weight_kg: float,
    age: int,
    sex: str,
    activity_level: str,
    goal: str
) -> dict:
    """Calculate daily calorie and macro needs.

    Args:
        weight_kg: Body weight in kg
        age: Age in years
        sex: 'male' or 'female'
        activity_level: sedentary, light, moderate, active, very_active
        goal: weight_loss, maintain, muscle_gain

    Returns:
        Dict with calories and macros
    """
    if sex.lower() == "male":
        bmr = 10 * weight_kg + 6.25 * 175 - 5 * age + 5
    else:
        bmr = 10 * weight_kg + 6.25 * 165 - 5 * age - 161

    # Activity multiplier
    multipliers = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725,
        "very_active": 1.9
    }

    tdee = bmr * multipliers.get(activity_level.lower(), 1.55)

    # Goal adjustments
    if goal.lower() == "weight_loss":
        calories = tdee - 500
    elif goal.lower() == "muscle_gain":
        calories = tdee + 300
    else:
        calories = tdee

    # Calculate macros
    protein_g = round(weight_kg * 2.2)
    fats_g = round(calories * 0.30 / 9)
    carbs_g = round((calories - (protein_g * 4) - (fats_g * 9)) / 4)

    return {
        "daily_calories": round(calories),
        "protein_grams": protein_g,
        "carbs_grams": carbs_g,
        "fats_gram": fats_g
    }
