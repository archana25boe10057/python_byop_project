import json
import os
import datetime

# ANSI Color Codes
COLORS = {
    'green': '\033[92m',
    'red': '\033[91m',
    'yellow': '\033[93m',
    'cyan': '\033[96m',
    'magenta': '\033[95m',
    'bold': '\033[1m',
    'reset': '\033[0m'
}

def color_text(text, color):
    """Returns text wrapped in the specified ANSI color code."""
    color_code = COLORS.get(color.lower(), COLORS['reset'])
    return f"{color_code}{text}{COLORS['reset']}"

def clear_screen():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def load_json(filepath, default_data):
    """Loads JSON data from file, or returns default if file doesn't exist."""
    if not os.path.exists(filepath):
        # Create empty file with default data
        save_json(filepath, default_data)
        return default_data
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(color_text(f"Error reading {filepath}. Starting fresh.", 'red'))
        return default_data

def save_json(filepath, data):
    """Saves data dictionary to JSON file safely."""
    try:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
    except IOError as e:
        print(color_text(f"Error saving data to {filepath}: {e}", 'red'))

def get_valid_int(prompt, min_val=None, max_val=None):
    """Prompts for an integer and handles invalid inputs with optional bounds."""
    while True:
        try:
            val = int(input(prompt))
            if min_val is not None and val < min_val:
                print(color_text(f"Please enter a value >= {min_val}", 'yellow'))
                continue
            if max_val is not None and val > max_val:
                print(color_text(f"Please enter a value <= {max_val}", 'yellow'))
                continue
            return val
        except ValueError:
            print(color_text("Invalid input. Please enter a whole number.", 'red'))

def get_valid_float(prompt, min_val=None, max_val=None):
    """Prompts for a float and handles invalid inputs with optional bounds."""
    while True:
        try:
            val = float(input(prompt))
            if min_val is not None and val < min_val:
                print(color_text(f"Please enter a value >= {min_val}", 'yellow'))
                continue
            if max_val is not None and val > max_val:
                print(color_text(f"Please enter a value <= {max_val}", 'yellow'))
                continue
            return val
        except ValueError:
            print(color_text("Invalid input. Please enter a number.", 'red'))

def get_valid_date(prompt):
    """Prompts for a date string in YYYY-MM-DD format."""
    while True:
        date_str = input(prompt)
        try:
            datetime.datetime.strptime(date_str, "%Y-%m-%d")
            return date_str
        except ValueError:
            print(color_text("Invalid date format. Please use YYYY-MM-DD.", 'yellow'))
