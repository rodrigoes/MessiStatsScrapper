import csv
import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup

def str_to_date(date_str):
    return datetime.strptime(date_str, '%d-%m-%Y')

def make_request(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.content

def parse_html(html):
    soup = BeautifulSoup(html, "html.parser")
    form = soup.find("form", {"action": "/index.php"})
    if form is None:
        raise ValueError("Form not found")
    section = form.find("section", {"class": "results"})
    if section is None:
        raise ValueError("Section not found")
    div = section.find("div", {"class": "wrap"})
    if div is None:
        raise ValueError("Div not found")
    table = div.find("table", {"class": "nextlevel"})
    if table is None:
        raise ValueError("Table not found")
    return table

def extract_games(table):
    data = []
    rows = table.find_all("tr")
    for row in rows:
        cells = row.find_all("td")
        if cells:
            data.append({
                "Game": cells[0].text.strip(),
                "Date": cells[1].text.strip(),
                "Competition": cells[2].text.split("\n")[-1].strip(),
                "Home team": cells[3].text.strip(),
                "Result": cells[4].text.strip(),
                "Away team": cells[5].text.strip(),
                "Lineup": cells[6].text.split("\n")[-1].strip(),
                "Minutes": cells[7].text.strip(),
                "Goals": cells[8].text.strip(),
                "Assists": cells[9].text.strip(),
                "Cards": cells[10].text.strip(),
                "Jersey": cells[11].text.strip(),
            })
    return data

def extract_goals(table):
    data = []
    rows = table.find_all("tr")
    for row in rows:
        cells = row.find_all("td")
        if cells:
            data.append({
                "Number": cells[0].text.strip(),
                "Date": cells[1].text.strip(),
                "Competiton": cells[2].text.split("\n")[-1].strip(),
                "Home team": cells[3].text.strip(),
                "Result": cells[4].text.strip(),
                "Away team": cells[5].text.strip(),
                "Minute": cells[6].text.strip(),
                "Score": cells[7].text.strip(),
                "Whats": cells[8].text.strip(),
                "How": cells[9].text.strip(),
                "Jersey": cells[10].text.strip(),
            })
    return data

def save_data_to_json(data, filename):
    with open(filename, "w", encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False)
    print(f"Data saved to {filename}")

def calculate_stats(data, filename):
    aggregated_data = {
        "Games": len(data),
        "Goals": sum([int(game["Goals"]) for game in data]),
        "Assists": sum([int(game["Assists"]) for game in data]),
        "Cards": sum([int(game["Cards"]) for game in data]),
        "Minutes": sum([int(game["Minutes"]) for game in data]),
        "Goals + Assists": sum([int(game["Goals"]) + int(game["Assists"]) for game in data]),
        "Goals per game": round(sum([int(game["Goals"]) for game in data]) / len(data),2),
        "National Team Goals": sum([int(game["Goals"]) for game in data if game["Away team"] == "Argentina" or game["Home team"] == "Argentina"])
    }

    club_goals = {
        "total": sum([int(game["Goals"]) for game in data if game["Away team"] != "Argentina" and game["Home team"] != "Argentina"]),
        "FC Barcelona": sum([int(game["Goals"]) if str_to_date(game["Date"])<= str_to_date("10-08-2021") else 0 for game in data if game["Away team"] == "FC Barcelona" or game["Home team"] == "FC Barcelona"]),
        "Paris Saint-Germain": sum([int(game["Goals"]) if str_to_date(game["Date"])> str_to_date("10-08-2021") else 0 for game in data if game["Away team"] == "Paris Saint-Germain" or game["Home team"] == "Paris Saint-Germain"]),
        "Inter Miami CF":  sum([int(game["Goals"]) for game in data if game["Away team"] == "Inter Miami CF" or game["Home team"] == "Inter Miami CF"]),
    }
    
    aggregated_data["Club Goals"] = club_goals

    
    jersey_data = {}
    for game in data:
        jersey = int(game["Jersey"])
        if jersey in jersey_data:
            jersey_data[jersey] += 1
        else:
            jersey_data[jersey] = 1
    aggregated_data["Jersey"] = jersey_data
    
   
    goal_types = {}
    with open('goal_data.json', 'r') as f:
        goal_data = json.load(f)
    for goal in goal_data:
        goal_type = goal["How"]
        if goal_type in goal_types:
            goal_types[goal_type] += 1
        else:
            goal_types[goal_type] = 1
    aggregated_data["Goal Types"] = goal_types
    
    with open(filename, "w", encoding='utf-8') as outfile:
        json.dump(aggregated_data, outfile, ensure_ascii=False)
    print(f"Data saved to {filename}")

def save_data_to_csv(data, filename):
    with open(filename, "w", newline="") as outfile:
        writer = csv.writer(outfile)
        writer.writerow(["Game", "Date", "Competition", "Home team", "Result", "Away team", "Lineup", "Minutes", "Goals", "Assists", "Cards", "Jersey"])
        for item in data:
            writer.writerow([item["Game"], item["Date"], item["Competition"], item["Home team"], item["Result"], item["Away team"], item["Lineup"], item["Minutes"], item["Goals"], item["Assists"], item["Cards"], item["Jersey"]])
    print(f"Data saved to {filename}")

def compare_goals():

    with open('game_data.json', 'r') as f:
        table_data = json.load(f)

    with open('goal_data.json', 'r') as f:
        goal_data = json.load(f)

    game_data = {}

    for game in table_data:
        date = game['Date']
        game_data[date] = game.copy()
        game_data[date]['Goals'] = []

    for goal in goal_data:
        date = goal['Date']
        if date in game_data:
            game_data[date]['Goals'].append(goal)

    with open('game_data_expanded.json', 'w', encoding='utf-8') as f:
        json.dump(list(game_data.values()), f, indent=4, ensure_ascii=False)
        
if __name__ == "__main__":
    
    urlGames = "https://messi.starplayerstats.com/en/games/0/0/all/0/0/0/t/0/0/0/1"
    urlGoals = "https://messi.starplayerstats.com/en/goals/0/0/all/0/0/0/t/all/all/0/0/1"

    try:
        html_games = make_request(urlGames)
        html_goals = make_request(urlGoals)
        table_games = parse_html(html_games)
        table_goals = parse_html(html_goals)
        data_games = extract_games(table_games)
        data_goals = extract_goals(table_goals)
        save_data_to_json(data_games, "game_data.json")
        save_data_to_json(data_goals, "goal_data.json")
        save_data_to_csv(data_games, "game_data.csv")
        #save_data_to_csv(data_goals, "goal_data.csv")
        totals_json = calculate_stats(data_games,'aggregated_data.json')
        compare_goals()
        print("""
    __  ___               _    _____                                      
   /  |/  /__  __________(_)  / ___/______________ _____  ____  ___  _____
  / /|_/ / _ \/ ___/ ___/ /   \__ \/ ___/ ___/ __ `/ __ \/ __ \/ _ \/ ___/
 / /  / /  __(__  |__  ) /   ___/ / /__/ /  / /_/ / /_/ / /_/ /  __/ /    
/_/  /_/\___/____/____/_/   /____/\___/_/   \__,_/ .___/ .___/\___/_/     
                                                /_/   /_/   
                                                        
            Data Source: https://messi.starplayerstats.com
""")
   

    except Exception as e:
        print(f"Error: {e}")



