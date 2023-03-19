import requests
from bs4 import BeautifulSoup
import json
import csv


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


def extract_table_data(table):
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


def save_data_to_json(data, filename):
    with open(filename, "w") as outfile:
        json.dump(data, outfile)
    print(f"Data saved to {filename}")


def save_data_to_csv(data, filename):
    with open(filename, "w", newline="") as outfile:
        writer = csv.writer(outfile)
        writer.writerow(["Game", "Date", "Competition", "Home team", "Result", "Away team", "Lineup", "Minutes", "Goals", "Assists", "Cards", "Jersey"])
        for item in data:
            writer.writerow([item["Game"], item["Date"], item["Competition"], item["Home team"], item["Result"], item["Away team"], item["Lineup"], item["Minutes"], item["Goals"], item["Assists"], item["Cards"], item["Jersey"]])
    print(f"Data saved to {filename}")


if __name__ == "__main__":
    url = "https://messi.starplayerstats.com/en/games/0/0/all/0/0/0/t/0/0/0/1"

    try:
        html = make_request(url)
        table = parse_html(html)
        data = extract_table_data(table)
        save_data_to_json(data, "table_data.json")
        save_data_to_csv(data, "table_data.csv")
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


# with open('table_data.json') as json_file:
#     data = json.load(json_file)
#     sum = 0
#     for p in data:
#         sum += int(p['GO'])
#     print(sum)


