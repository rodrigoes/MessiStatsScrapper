import requests
from bs4 import BeautifulSoup
import json


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
                "CMP": cells[2].text.split("\n")[-1].strip(),
                "Home team": cells[3].text.strip(),
                "Result": cells[4].text.strip(),
                "Away team": cells[5].text.strip(),
                "LU": cells[6].text.split("\n")[-1].strip(),
                "MI": cells[7].text.strip(),
                "GO": cells[8].text.strip(),
                "AS": cells[9].text.strip(),
                "CA": cells[10].text.strip(),
                "JS": cells[11].text.strip(),
            })
    return data


def save_data_to_file(data, filename):
    with open(filename, "w") as outfile:
        json.dump(data, outfile)
    print(f"Data saved to {filename}")


if __name__ == "__main__":
    url = "https://messi.starplayerstats.com/en/games/0/0/all/0/0/0/t/0/0/0/1"

    try:
        html = make_request(url)
        table = parse_html(html)
        data = extract_table_data(table)
        save_data_to_file(data, "table_data.json")
    except Exception as e:
        print(f"Error: {e}")
