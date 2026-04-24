from data_store import DIET_PLANS

def run_diet_expert_system(user_data):
    # 1. Inputs and BMI Calculation
    weight = user_data['weight']
    height = user_data['height'] / 100
    bmi = round(weight / (height ** 2), 1)
    
    goal = user_data['goal']
    condition = user_data['condition']
    activity = user_data['activity']

    plan_key = ""
    reasoning = ""

    # 2. Forward Chaining Logic (Rules)
    
    # Priority 1: Health Conditions
    if condition == "Diabetes":
        plan_key = "Diabetes_Plan"
        reasoning = "This plan was chosen because diabetic patients need foods that do not cause sharp spikes in blood sugar."
    
    elif condition in ["PCOS", "Insulin Resistance"]:
        plan_key = "Insulin_PCOS_Plan"
        reasoning = "These conditions require reducing carbohydrates to improve insulin sensitivity and reduce inflammation."

    # Priority 2: Goal and BMI
    elif goal == "Weight Loss":
        plan_key = "Weight_Loss_Plan"
        reasoning = f"Since your goal is weight loss and your BMI is {bmi}, you need a plan focused on fat burning via calorie deficit."

    elif goal == "Weight Gain":
        plan_key = "Weight_Gain_Plan"
        reasoning = f"To gain weight from a BMI of {bmi}, you must consume more calories than you burn with a focus on protein."

    else:
        plan_key = "Maintenance_Plan"
        reasoning = "Your current weight is proportional to your height, so the goal is to maintain a healthy and balanced lifestyle."

    # 3. Final Output Generation
    final_plan = DIET_PLANS[plan_key]
    
    return {
        "bmi": bmi,
        "diet_type": final_plan['name'],
        "reasoning": reasoning,
        "suggested_meals": final_plan['meals'],
        "suggested_exercises": final_plan['exercises'],
        "general_advice": final_plan['advice']
    }

# --- Testing the System ---
example_user = {
    "weight": 85,
    "height": 165,
    "activity": "Low",
    "condition": "PCOS",
    "goal": "Weight Loss"
}

result = run_diet_expert_system(example_user)

# Print results to the Terminal
print(f"--- Smart Analysis Result ---")
print(f"BMI: {result['bmi']}")
print(f"Diet Type: {result['diet_type']}")
print(f"Reasoning: {result['reasoning']}")
print(f"Meals: {', '.join(result['suggested_meals'])}")
print(f"Exercises: {', '.join(result['suggested_exercises'])}")
print(f"Advice: {result['general_advice']}")