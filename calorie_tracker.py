import utils

FOOD_DICT = {
    "rice (1 cup)": 206,
    "banana": 89,
    "egg": 78,
    "milk (1 glass)": 150,
    "roti": 100,
    "apple": 95,
    "chicken breast (100g)": 165
}

def log_meal(selected_date, daily_data):
    print(utils.color_text("\n--- Log Meal ---", "cyan"))
    print("Available foods:")
    for food, cals in FOOD_DICT.items():
        print(f"- {food}: {cals} cals")
    
    choice = input("Enter a food from the list or type 'custom' for a new entry: ").strip().lower()
    
    food_name = ""
    calories = 0
    
    if choice == 'custom':
        food_name = input("Enter custom food name: ").strip()
        calories = utils.get_valid_int("Enter calories: ", min_val=0)
    else:
        # Check if the food is in our dict
        matched = False
        for f, c in FOOD_DICT.items():
            if f.lower().startswith(choice) or choice in f.lower():
                food_name = f
                calories = c
                matched = True
                break
        
        if not matched:
            print(utils.color_text("Food not found in default list. Adding as custom.", "yellow"))
            food_name = choice
            calories = utils.get_valid_int("Enter calories: ", min_val=0)
    
    quantity = input(f"Enter quantity for {food_name}: ").strip()
    # It might be 2 bananas, etc. We just multiply if they enter a number, else keep it simple and just use base cals
    multiplier = 1
    try:
        multiplier = float(quantity)
    except ValueError:
        print(utils.color_text(f"Non-numeric quantity entered, assuming 1 serving.", "yellow"))
        quantity = "1"
    
    total_cals = int(calories * multiplier)
    
    meal_entry = {
        "food": food_name,
        "quantity": quantity,
        "calories": total_cals
    }
    daily_data.setdefault("meals", []).append(meal_entry)
    daily_data["calories_consumed"] = daily_data.get("calories_consumed", 0) + total_cals
    
    print(utils.color_text(f"Logged: {quantity}x {food_name} ({total_cals} cals)", "green"))


def log_exercise(selected_date, daily_data):
    print(utils.color_text("\n--- Log Exercise ---", "cyan"))
    ex_type = input("Enter exercise type (e.g., Running, Yoga): ").strip()
    duration = utils.get_valid_int("Enter duration (minutes): ", min_val=1)
    calories = utils.get_valid_int("Enter estimated calories burned: ", min_val=0)
    
    ex_entry = {
        "type": ex_type,
        "duration_mins": duration,
        "calories_burned": calories
    }
    daily_data.setdefault("exercise", []).append(ex_entry)
    daily_data["calories_burned"] = daily_data.get("calories_burned", 0) + calories
    
    print(utils.color_text(f"Logged: {ex_type} for {duration} mins ({calories} cals burned)", "green"))


def set_daily_goal(selected_date, daily_data):
    print(utils.color_text("\n--- Set Calorie Goal ---", "cyan"))
    goal = utils.get_valid_int("Enter your daily calorie goal: ", min_val=0)
    daily_data["calorie_goal"] = goal
    print(utils.color_text(f"Goal set to {goal} calories for {selected_date}.", "green"))


def calculate_net_calories(daily_data):
    consumed = daily_data.get("calories_consumed", 0)
    burned = daily_data.get("calories_burned", 0)
    return consumed - burned


def view_daily_summary(selected_date, daily_data):
    print(utils.color_text(f"\n=== Calorie Summary for {selected_date} ===", "magenta"))
    consumed = daily_data.get("calories_consumed", 0)
    burned = daily_data.get("calories_burned", 0)
    net = calculate_net_calories(daily_data)
    goal = daily_data.get("calorie_goal", 0)
    
    print(f"Calories Consumed: {consumed}")
    print(f"Calories Burned:   {burned}")
    print(f"Net Calories:      {net}")
    if goal > 0:
        print(f"Daily Goal:        {goal}")
        
        # Recommendations
        if net > goal + 200:
            print(utils.color_text(f"Warning: You exceeded your calorie goal by {net - goal} calories.", "red"))
        elif net < goal - 500:
            print(utils.color_text(f"Warning: Your calorie intake is too low ({goal - net} below goal).", "yellow"))
        else:
            print(utils.color_text("Great job! You are within a healthy range of your goal.", "green"))
    else:
        print(utils.color_text("No daily goal set. Set one to get recommendations.", "yellow"))
    
    print("\nMeals Logged:")
    for m in daily_data.get("meals", []):
        print(f" - {m['quantity']}x {m['food']}: {m['calories']} cals")
    if not daily_data.get("meals"):
         print(" - None")
         
    print("\nExercise Logged:")
    for e in daily_data.get("exercise", []):
         print(f" - {e['type']} ({e['duration_mins']} mins): {e['calories_burned']} cals")
    if not daily_data.get("exercise"):
         print(" - None")
    input("\Press Enter to return...")

def calorie_tracker_menu(selected_date, daily_data):
    while True:
        utils.clear_screen()
        print(utils.color_text(f"=== CALORIE TRACKER ({selected_date}) ===", "bold"))
        print("1. Log Meal")
        print("2. Log Exercise")
        print("3. View Daily Summary")
        print("4. Set Daily Calorie Goal")
        print("5. Return to Main Menu")
        
        choice = input("Select an option: ").strip()
        
        if choice == '1':
            log_meal(selected_date, daily_data)
        elif choice == '2':
            log_exercise(selected_date, daily_data)
        elif choice == '3':
            view_daily_summary(selected_date, daily_data)
        elif choice == '4':
            set_daily_goal(selected_date, daily_data)
        elif choice == '5':
            break
        else:
            print(utils.color_text("Invalid Option", "red"))
