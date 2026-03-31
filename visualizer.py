import matplotlib.pyplot as plt
import datetime
import utils

def get_last_7_days_data(health_data):
    """Returns sorted dates and data for the last 7 recorded days."""
    dates = sorted(health_data.keys())[-7:]
    
    sleep = []
    water = []
    screen = []
    steps = []
    mood = []
    consumed = []
    burned = []
    
    for d in dates:
        day_data = health_data[d]
        sleep.append(day_data.get('sleep', 0))
        water.append(day_data.get('water', 0))
        screen.append(day_data.get('screen_time', 0))
        steps.append(day_data.get('steps', 0))
        mood.append(day_data.get('mood', 0))
        consumed.append(day_data.get('calories_consumed', 0))
        burned.append(day_data.get('calories_burned', 0))
        
    return dates, sleep, water, screen, steps, mood, consumed, burned

def plot_health_metrics(health_data):
    if not health_data:
        print(utils.color_text("Not enough health data to plot.", "red"))
        return
        
    dates, sleep, water, screen, steps, mood, _, _ = get_last_7_days_data(health_data)
    
    if not dates:
        print("No recent data.")
        return
        
    fig, axs = plt.subplots(5, 1, figsize=(8, 12), sharex=True)
    fig.suptitle('Health Metrics (Last 7 Days)', fontsize=16)
    
    axs[0].plot(dates, sleep, marker='o', color='purple')
    axs[0].set_ylabel('Sleep (hrs)')
    
    axs[1].plot(dates, water, marker='o', color='blue')
    axs[1].set_ylabel('Water (L)')
    
    axs[2].plot(dates, screen, marker='o', color='orange')
    axs[2].set_ylabel('Screen Time (hrs)')
    
    axs[3].plot(dates, steps, marker='o', color='green')
    axs[3].set_ylabel('Steps')
    
    axs[4].plot(dates, mood, marker='o', color='red')
    axs[4].set_ylabel('Mood (1-5)')
    axs[4].set_ylim([1, 5])
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.subplots_adjust(top=0.95)
    plt.show(block=False)
    # block=False to prevent halting CLI application indefinitely 

def plot_calorie_trend(health_data):
    if not health_data:
        print(utils.color_text("Not enough calorie data to plot.", "red"))
        return
        
    dates, _, _, _, _, _, consumed, burned = get_last_7_days_data(health_data)
    
    if not dates:
        print("No recent calorie data.")
        return
        
    fig, ax = plt.subplots(figsize=(8, 6))
    x = range(len(dates))
    width = 0.35
    
    ax.bar(x, consumed, width, label='Consumed', color='orange')
    ax.bar([i + width for i in x], burned, width, label='Burned', color='red')
    
    ax.set_ylabel('Calories')
    ax.set_title('Calorie Intake vs Burned (Last 7 Days)')
    ax.set_xticks([i + width/2 for i in x])
    ax.set_xticklabels(dates, rotation=45)
    ax.legend()
    
    plt.tight_layout()
    plt.show(block=False)

def plot_cycle_trends(periods_data):
    if len(periods_data) < 2:
        print(utils.color_text("Need at least 2 cycles to plot trends.", "red"))
        return
        
    lengths = []
    cycles = []
    
    for i, c in enumerate(periods_data):
        if "duration" in c and c["duration"]:
             # Calculate cycle length between starts if available
             if i < len(periods_data) - 1:
                 # valid full cycle
                 d1 = datetime.datetime.strptime(c["start_date"], "%Y-%m-%d")
                 d2 = datetime.datetime.strptime(periods_data[i+1]["start_date"], "%Y-%m-%d")
                 length = (d2 - d1).days
                 lengths.append(length)
                 cycles.append(f"Cycle {i+1}")
                 
    if not lengths:
        print("Not enough full cycle data.")
        return
        
    avg = sum(lengths) / len(lengths)
    
    plt.figure(figsize=(8, 6))
    plt.plot(cycles, lengths, marker='o', color='magenta', label='Cycle Length')
    plt.axhline(y=avg, color='r', linestyle='--', label=f'Avg: {avg:.1f} days')
    
    plt.ylabel('Days')
    plt.title('Menstrual Cycle Length Trends')
    plt.legend()
    plt.tight_layout()
    plt.show(block=False)
