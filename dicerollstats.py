import csv
import re
from bs4 import BeautifulSoup
from dateutil.parser import parse

# Define the path to the HTML file
html_file_path = 'Chat Log for The Forge of Fury.html'

# Mapping for character consolidation
character_map = {
    "Joel K.:": "Bajan",
    "NekLevDev:": "Monty",
    "Jerry:": "Jerry",
    "Monty Mauler:": "Monty",
    "Gronkus Stoneheel:": "Gronkus",
    "Kento GM (GM):": "GM",
    "Montgomery 'Monty' Mauler": "Monty",
    "(To GM):": "GM",
    "Jerry Beaumont:": "Jerry",
    "Gronkus:": "Gronkus",
    "Bajan Boomcask:": "Bajan",
    "Batu": "Bajan"
}

valid_characters = {"Jerry", "Monty", "Gronkus", "GM", "Bajan", "Unknown"}

# Function to parse the HTML file and extract dice rolls
def parse_html_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
    
    # Extract all chat messages
    messages = soup.find_all('div', class_='message')
    
    current_time = None
    timestamps = []
    roll_msgs = []
    has_roll = []

    # Extract timestamps and check for roll messages
    for message in messages:
        tstamp = message.find(class_='tstamp')
        if tstamp:
            current_time = parse(tstamp.string)
        timestamps.append(current_time)
        
        has_roll.append(message.find(class_='inlinerollresult') is not None)
        if has_roll[-1]:
            roll_msgs.append(message)
    
    roll_timestamps = [timestamp for i, timestamp in zip(has_roll, timestamps) if i]
    
    character_rolls = {}
    unknown_messages = []

    roll_re = re.compile(r'">([0-9]+)</span>')

    for message in roll_msgs:
        character = None
        
        # First, check if 'sheet-charname' is present
        charname_div = message.find('div', class_='sheet-charname')
        if charname_div:
            character = charname_div.get_text(strip=True)
        else:
            charname_span = message.find('span', class_='sheet-charname')
            if charname_span:
                character = charname_span.get_text(strip=True)
            elif message.find(class_='by'):
                character = message.find(class_='by').get_text(strip=True)

        # Consolidate characters based on the provided map
        if character in character_map:
            character = character_map[character]

        # Filter out unwanted characters
        if character not in valid_characters:
            unknown_messages.append(str(message))
            character = "Unknown"

        if character not in character_rolls:
            character_rolls[character] = []

        roll_results = message.find_all('span', class_='inlinerollresult')

        for roll_result in roll_results:
            if '1d20' in roll_result['title']:
                match = roll_re.search(roll_result['title'])
                if match:
                    roll = int(match.group(1))
                    character_rolls[character].append(roll)
                else:
                    print(f"Roll not found in roll_result: {roll_result}")

    character_stats = []
    for character, rolls in character_rolls.items():
        total_rolls = len(rolls)
        total_sum = sum(rolls)
        nat_1s = rolls.count(1)
        nat_20s = rolls.count(20)
        average_roll = total_sum / total_rolls if total_rolls > 0 else 0
        character_stats.append([character, total_rolls, average_roll, nat_1s, nat_20s])

    return character_stats, unknown_messages

# Function to save stats to CSV
def save_stats_to_csv(character_stats, output_file_path):
    with open(output_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Character', 'Number of Rolls', 'Average Roll', 'Number of Nat 1s', 'Number of Nat 20s'])
        writer.writerows(character_stats)

# Function to save unknown messages to a separate file
def save_unknown_messages_to_file(unknown_messages, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write("\n".join(unknown_messages))

# Parse the HTML file to get stats and unknown messages
character_stats, unknown_messages = parse_html_file(html_file_path)

# Define the output CSV file path
output_csv_file_path = 'dice_roll_stats.csv'
unknown_messages_file_path = 'unknown_messages.html'

# Save the stats to the CSV file
save_stats_to_csv(character_stats, output_csv_file_path)

# Save the unknown messages to the HTML file
save_unknown_messages_to_file(unknown_messages, unknown_messages_file_path)

print(f'Stats have been saved to {output_csv_file_path}')
print(f'Unknown messages have been saved to {unknown_messages_file_path}')
