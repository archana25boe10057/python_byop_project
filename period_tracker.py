import utils
import datetime

def calculate_cycle_stats(data_list):
    """Calculates average cycle length and predicts next period."""
    if not data_list:
        return 28, None 
    
    valid_lengths = []
    
    for i in range(len(data_list) - 1):
        try:
            d1 = datetime.datetime.strptime(data_list[i]["start_date"], "%Y-%m-%d")
            d2 = datetime.datetime.strptime(data_list[i+1]["start_date"], "%Y-%m-%d")
            length = (d2 - d1).days
            valid_lengths.append(length)
            
            
            if "end_date" in data_list[i] and data_list[i]["end_date"]:
                end = datetime.datetime.strptime(data_list[i]["end_date"], "%Y-%m-%d")
                data_list[i]["duration"] = (end - d1).days
                
        except ValueError:
            pass
            
    
    recent_lengths = valid_lengths[-3:] if len(valid_lengths) >= 3 else valid_lengths
    
    avg_length = 28
    if recent_lengths:
         avg_length = sum(recent_lengths) // len(recent_lengths)
         
    
    try:
         last_start = datetime.datetime.strptime(data_list[-1]["start_date"], "%Y-%m-%d")
         next_period = last_start + datetime.timedelta(days=avg_length)
         prediction = next_period.strftime("%Y-%m-%d")
    except ValueError:
         prediction = None
         
    return avg_length, prediction


def period_tracker_menu(periods_data):
    while True:
        utils.clear_screen()
        print(utils.color_text("=== PERIOD TRACKER ===", "bold"))
        print("1. Log Period Start Date")
        print("2. Log Period End Date")
        print("3. Log Symptoms")
        print("4. View Cycle History")
        print("5. Predict Next Period & Phase Info")
        print("6. Return to Main Menu")
        
        choice = input("Select an option: ").strip()
        
        if choice == '1':
            start = utils.get_valid_date("Enter period start date (YYYY-MM-DD): ")
            periods_data.append({
                "start_date": start,
                "end_date": None,
                "duration": None,
                "cycle_length": None,
                "symptoms": []
            })
            print(utils.color_text("Start date logged.", "green"))
            input("\nPress Enter to continue...")
            
        elif choice == '2':
            if not periods_data:
                print(utils.color_text("No period data exists. Log a start date first.", "red"))
            else:
                end = utils.get_valid_date("Enter period end date (YYYY-MM-DD): ")
                periods_data[-1]["end_date"] = end
                try:
                    start_dt = datetime.datetime.strptime(periods_data[-1]["start_date"], "%Y-%m-%d")
                    end_dt = datetime.datetime.strptime(end, "%Y-%m-%d")
                    periods_data[-1]["duration"] = (end_dt - start_dt).days + 1
                except ValueError:
                    pass
                print(utils.color_text("End date logged.", "green"))
            input("\nPress Enter to continue...")
            
        elif choice == '3':
            if not periods_data:
                 print(utils.color_text("No period data exists. Log a start date first.", "red"))
            else:
                 print("\nSymptoms: 1. cramps, 2. headache, 3. bloating, 4. fatigue, 5. mood swings")
                 s_choice = input("Enter symptom numbers separated by comma (e.g., 1,3): ").strip()
                 symptom_map = {"1": "cramps", "2": "headache", "3": "bloating", "4": "fatigue", "5": "mood swings"}
                 selected = [symptom_map[c.strip()] for c in s_choice.split(",") if c.strip() in symptom_map]
                 
                 current = periods_data[-1].get("symptoms", [])
                 for s in selected:
                     if s not in current:
                         current.append(s)
                 periods_data[-1]["symptoms"] = current
                 print(utils.color_text(f"Logged symptoms: {', '.join(selected)}", "green"))
            input("\nPress Enter to continue...")
            
        elif choice == '4':
             print(utils.color_text("\n=== Cycle History ===", "magenta"))
             if not periods_data:
                 print("No data logged.")
             else:
                 for i, cycle in enumerate(periods_data):
                     start = cycle.get('start_date', 'N/A')
                     end = cycle.get('end_date', 'Ongoing')
                     duration = cycle.get('duration', 'N/A')
                     symptoms = ', '.join(cycle.get('symptoms', []))
                     print(f"Cycle {i+1}: Start: {start} | End: {end} | Duration: {duration} days")
                     if symptoms:
                         print(f"  Symptoms: {symptoms}")
             input("\nPress Enter to continue...")
             
        elif choice == '5':
             avg_len, next_d = calculate_cycle_stats(periods_data)
             print(utils.color_text(f"\nAverage Cycle Length: {avg_len} days", "cyan"))
             if next_d:
                 print(utils.color_text(f"Predicted Next Period: {next_d}", "magenta"))
                 
                 if avg_len < 21 or avg_len > 35:
                     print(utils.color_text("Warning: Your average cycle is flagged as irregular (<21 or >35 days). Consider consulting a doctor.", "red"))
                 
                 try:
                     last_start = datetime.datetime.strptime(periods_data[-1]["start_date"], "%Y-%m-%d")
                     today = datetime.datetime.now()
                     day_of_cycle = (today - last_start).days + 1
                     
                     print(f"\nCurrent Day of Cycle: {day_of_cycle}")
                     print(utils.color_text("\n=== Recommendations Based on Phase ===", "yellow"))
                     
                     if day_of_cycle <= 5:
                         print("Phase: Menstrual (Day 1-5)")
                         print("Tip: Eat iron-rich foods, prioritize rest and hydration.")
                     elif 5 < day_of_cycle <= 13:
                         print("Phase: Follicular (Day 6-13)")
                         print("Tip: Great time for cardio and high-energy workouts.")
                     elif 14 <= day_of_cycle <= 16:
                         print("Phase: Ovulation (Day 14-16)")
                         print("Tip: Peak energy. Ideal for strength training.")
                         print(utils.color_text("Note: Currently in fertile window.", "magenta"))
                     else:
                         print(f"Phase: Luteal (Day 17-{avg_len})")
                         print("Tip: Focus on yoga, light exercise, and reduce caffeine.")
                         
                 except ValueError:
                     pass
                     
             else:
                 print("Not enough data to make predictions.")
             input("\nPress Enter to continue...")
             
        elif choice == '6':
             break
        else:
             print(utils.color_text("Invalid Option", "red"))
             input("\nPress Enter to try again...")
