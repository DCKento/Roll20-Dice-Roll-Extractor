## Overview

This project is a Python script that parses an HTML chat log from a game session and extracts dice roll statistics for various characters. The script consolidates character names, filters valid characters, and calculates statistics such as the number of rolls, average roll, and the number of natural 1s and 20s. The results are saved into a CSV file, and any messages with unknown characters are saved into a separate HTML file.

## Features

-   Parses Roll20 Chat Archive HTML file to extract dice roll information.
-   Consolidates character names based on a predefined map.
-   Calculates statistics for each character:
    -   Total number of rolls
    -   Average roll value
    -   Number of natural 1s
    -   Number of natural 20s
-   Saves the statistics to a CSV file.
-   Saves messages with unknown characters to an HTML file.

## Requirements

-   Python 3.x
-   BeautifulSoup
-   dateutil

## Usage

1.  Place your HTML chat log file in the project directory. You can obtain this by saving the Chat Archive from Roll20
2.  Update the `html_file_path` variable in the script with the name of your HTML file:
    `html_file_path = 'Chat Log for The Forge of Fury.html'` 
3.  Run the script:
    `python parse_dice_rolls.py` 
4.  The script will generate two output files:
    -   `dice_roll_stats.csv`: Contains the dice roll statistics for each character.
    -   `unknown_messages.html`: Contains the messages with unknown characters.

## Configuration

### Character Mapping

The script uses a predefined character map to consolidate character names. You can update the `character_map` dictionary in the script to include new mappings or modify existing ones

### Valid Characters

You can update the set of valid characters in the `valid_characters` set

## File Descriptions

-   `parse_dice_rolls.py`: The main script that parses the HTML file and generates the output files.
-   `dice_roll_stats.csv`: The CSV file containing dice roll statistics.
-   `unknown_messages.html`: The HTML file containing messages with unknown characters.
