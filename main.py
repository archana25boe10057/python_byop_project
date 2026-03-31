import datetime
import utils
import calorie_tracker
import period_tracker
import visualizer

HEALTH_FILE = "health_data.json"
PERIOD_FILE = "periods.json"

def log_today_health_data(date, health_data):
    print(utils.color_text(f"\n--- Log Health Data for {date} ---", "cyan"))
    
    if date in health_data:
        overwrite = input(utils.color_text(f"Data for {date} already exists. Overwrite? (y/n): ", "yellow")).strip().lower()
        if overwrite != 'y':
            print("Action cancelled.")
            return

    sleep = utils.get_valid_float("Enter sleep hours: ", min_val=0, max_val=24)
    water = utils.get_valid_float("Enter water intake (liters): ", min_val=0)
    screen = utils.get_valid_float("Enter screen time (hours): ", min_val=0, max_val=24)
    steps = utils.get_valid_int("Enter steps walked: ", min_val=0)
    mood = utils.get_valid_int("Enter mood (1-5 scale, 1 is bad, 5 is great): ", min_val=1, max_val=5)
    
    # Preserve existing calorie data if present and just updating health metrics
    existing_data = health_data.get(date, {})
    
    health_data[date] = {
        "sleep": sleep,
        "water": water,
        "screen_time": screen,
        "steps": steps,
        "mood": mood,
        "calories_consumed": existing_data.get("calories_consumed", 0),
        "calories_burned": existing_data.get("calories_burned", 0),
        "meals": existing_data.get("meals", []),
        "exercise": existing_data.get("exercise", []),
        "calorie_goal": existing_data.get("calorie_goal", 0)
    }
    print(utils.color_text(f"Health data logged successfully for {date}.", "green"))


def view_all_logged_entries(health_data):
    print(utils.color_text("\n=== All Logged Health Entries ===", "magenta"))
    if not health_data:
        print("No daily entries found.")
        return
        
    print(f"{'Date':<12} | {'Sleep (h)':<9} | {'Water (L)':<9} | {'Screen (h)':<10} | {'Steps':<8} | {'Mood':<4} | {'Net Cals'}")
    print("-" * 80)
    
    for date in sorted(health_data.keys()):
        d = health_data[date]
        sleep = d.get('sleep', 0)
        water = d.get('water', 0)
        screen = d.get('screen_time', 0)
        steps = d.get('steps', 0)
        mood = d.get('mood', 0)
        net_cals = calorie_tracker.calculate_net_calories(d)
        
        print(f"{date:<12} | {sleep:<9} | {water:<9} | {screen:<10} | {steps:<8} | {mood:<4} | {net_cals}")


def calculate_health_score(date, health_data):
    if date not in health_data:
        print(utils.color_text(f"No health metrics logged for {date} to calculate score.", "red"))
        return
        
    d = health_data[date]
    score = 0
    
    # Sleep: 8 hrs = 20 pts (proportional, max 20)
    sleep = d.get('sleep', 0)
    score += min(20, (sleep / 8.0) * 20)
    
    # Water: 2.5L = 20 pts
    water = d.get('water', 0)
    score += min(20, (water / 2.5) * 20)
    
    # Screen time: under 4 hrs = 20 pts
    screen = d.get('screen_time', 24) # default high if missing? No, default 0 if tracking is active
    if screen <= 4:
         score += 20
    else:
         # Penalty for going over 4, zero at maybe 10 hours
         score += max(0, 20 - ((screen - 4) * 3))
         
    # Steps: 8000 = 20 pts
    steps = d.get('steps', 0)
    score += min(20, (steps / 8000.0) * 20)
    
    # Mood: 5 = 20 pts (mood * 4)
    mood = d.get('mood', 0)
    score += (mood * 4)
    
    # Calorie bonus: within 200 of goal = +5 pts
    bonus = 0
    goal = d.get('calorie_goal', 0)
    if goal > 0:
        net = calorie_tracker.calculate_net_calories(d)
        if abs(net - goal) <= 200:
             bonus = 5
             
    total_score = round(score + bonus)
    print(utils.color_text(f"\n=== Health Score for {date} ===", "cyan"))
    print(f"Calculated Score: {round(score)}/100")
    if bonus > 0:
        print(utils.color_text(f"Calorie Goal Bonus! +{bonus} pts", "green"))
    print(utils.color_text(f"Total: {total_score}/105", "bold"))


def show_health_recommendations(date, health_data, periods_data):
    if date not in health_data:
        print(utils.color_text(f"No daily metrics logged for {date} to offer health recommendations.", "red"))
    else:
        print(utils.color_text(f"\n=== Health Recommendations ({date}) ===", "yellow"))
        d = health_data[date]
        
        sleep = d.get('sleep', 0)
        water = d.get('water', 0)
        screen = d.get('screen_time', 0)
        steps = d.get('steps', 0)
        mood = d.get('mood', 0)
        goal = d.get('calorie_goal', 0)
        net_cals = calorie_tracker.calculate_net_calories(d)
        
        if sleep < 7:
            print("- Sleep: You got less than 7 hours. Try to go to bed earlier tonight.")
        if water < 2:
            print("- Water: You drank less than 2L. Drink a glass of water right now!")
        if screen > 5:
            print("- Screen Time: Over 5 hours of screen time. Remember the 20-20-20 rule to rest your eyes.")
        if steps < 5000:
            print("- Steps: Less than 5000 steps. Take a short 15-minute walk today.")
        if mood < 3:
            print("- Mood: Your mood is low. Consider some stress relief activities or journaling.")
            
        if goal > 0 and net_cals > goal + 200:
             print("- Calories: You are consistently exceeding your calorie goal. Focus on portion control.")
             
    print(utils.color_text("\n=== Cycle-based Recommendations ===", "yellow"))
    if not periods_data:
        print("No cycle data logged to provide recommendations.")
    else:
         avg_len, next_d = period_tracker.calculate_cycle_stats(periods_data)
         if avg_len < 21 or avg_len > 35:
             print(utils.color_text("- Medical: Irregular cycle detected. Consider consulting a doctor.", "red"))
             
         try:
             last_start = datetime.datetime.strptime(periods_data[-1]["start_date"], "%Y-%m-%d")
             today = datetime.datetime.now()
             day_of_cycle = (today - last_start).days + 1
             
             if day_of_cycle <= 5:
                 print("- Cycle Phase (Menstrual): Eat iron-rich foods, prioritize rest and hydration.")
             elif 5 < day_of_cycle <= 13:
                 print("- Cycle Phase (Follicular): Great time for cardio and high-energy workouts.")
             elif 14 <= day_of_cycle <= 16:
                 print("- Cycle Phase (Ovulation): Peak energy levels. Ideal for strength training.")
             else:
                 print(f"- Cycle Phase (Luteal): Focus on yoga, light exercise, and reduce caffeine.")
         except ValueError:
             print("- Cycle start date is invalid, cannot determine phase.")


def main():
    utils.clear_screen()
    print(utils.color_text("Starting Student Health Tracker...", "bold"))
    
    # Load Data
    health_data = utils.load_json(HEALTH_FILE, {})
    periods_data = utils.load_json(PERIOD_FILE, [])
    
    today_date = datetime.datetime.now().strftime("%Y-%m-%d")
    
    while True:
        utils.clear_screen()
        print(utils.color_text(f"=== STUDENT HEALTH TRACKER ({today_date}) ===", "bold"))
        print("1. Log today's health data")
        print("2. View all logged entries")
        print("3. View weekly health score")
        print("4. Show health recommendations")
        print("5. Visualize data plots")
        print("6. Calorie Tracker Menu")
        print("7. Period Tracker Menu")
        print("8. Exit")
        
        choice = input("Select an option: ").strip()
        
        if choice == '1':
            custom_date = input(f"Press Enter to log for today ({today_date}) or enter YYYY-MM-DD: ").strip()
            date_to_log = today_date
            if custom_date:
                try:
                     datetime.datetime.strptime(custom_date, "%Y-%m-%d")
                     date_to_log = custom_date
                except ValueError:
                     print(utils.color_text("Invalid date format. Using today's date instead.", "yellow"))
            log_today_health_data(date_to_log, health_data)
            utils.save_json(HEALTH_FILE, health_data)
            input("\nPress Enter to continue...")
            
        elif choice == '2':
             view_all_logged_entries(health_data)
             input("\nPress Enter to continue...")
             
        elif choice == '3':
             custom_date = input(f"Press Enter for today ({today_date}) or enter YYYY-MM-DD: ").strip()
             date_to_calc = custom_date if custom_date else today_date
             calculate_health_score(date_to_calc, health_data)
             input("\nPress Enter to continue...")
             
        elif choice == '4':
             show_health_recommendations(today_date, health_data, periods_data)
             input("\nPress Enter to continue...")
             
        elif choice == '5':
             print(utils.color_text("\nVisualizations open in separate windows. Close them to continue.", "cyan"))
             visualizer.plot_health_metrics(health_data)
             visualizer.plot_calorie_trend(health_data)
             visualizer.plot_cycle_trends(periods_data)
             input("\nPress Enter to return to main menu...")
             
        elif choice == '6':
             # Ensure daily entry exists before going to tracker menu
             if today_date not in health_data:
                 health_data[today_date] = {}
             calorie_tracker.calorie_tracker_menu(today_date, health_data[today_date])
             utils.save_json(HEALTH_FILE, health_data)
             
        elif choice == '7':
             period_tracker.period_tracker_menu(periods_data)
             utils.save_json(PERIOD_FILE, periods_data)
             
        elif choice == '8':
             print(utils.color_text("Saving data and exiting. Stay healthy!", "green"))
             utils.save_json(HEALTH_FILE, health_data)
             utils.save_json(PERIOD_FILE, periods_data)
             break
        else:
             print(utils.color_text("Invalid Option", "red"))
             input("\nPress Enter to try again...")

if __name__ == "__main__":
    main()
