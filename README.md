# Messi Stats Scrapper

![BG](https://user-images.githubusercontent.com/36699060/229926354-0572d805-ae8b-43b3-b129-bdceab7043e9.png)

Messi Stats Scrapper is a project that collects statistics of the football player Lionel Messi using a Python scrapper with the BeautifulSoup library, and processes them into JSON files. In addition, a FastAPI API is created to provide access to the collected information.

Match and goal data were taken from the site: http://messi.starplayerstats.com/en/, aggregated data were made in the code itself.

## 📋 Requirements

To run the Messi Stats Scrapper, you need to have the following software installed:

- Python 3.7 or higher
- Beautiful Soup 4
- Requests
- FastAPI
- Uvicorn

## 💾 Installation

1. Clone the repository:

```
git clone https://github.com/rodrigoes/MessiDashboard.git
```

2. Install the required dependencies: For this step you need Git installed, but you can just download the zip file instead by clicking the button at the top of this page ☝️

```
pip install -r requirements.txt
```

## 💻 Usage

To collect the statistics, run the Scrapper.py script with the following command:

```
python Scrapper.py
```

This script will download the data from the website and process it into JSON files that will be stored in the data directory.

To start the FastAPI API, run the Main.py script with the following command:

```
uvicorn Main:app --reload
```

This command will start the API server at http://localhost:8000/, and you can access the endpoints using a web browser or a HTTP client.

## 🌐 API endpoints

The Messi Stats API provides the following endpoints:

### 🏳 Games

**/games**: Returns a JSON object with all matches played by Messi, with information such as the date, opponent, competition, score, etc.

Example response:

```
 {
    "Game": "1017",
    "Date": "24-03-2023",
    "Competition": "International friendly",
    "Home team": "Argentina",
    "Result": "2-0",
    "Away team": "Panama",
    "Lineup": "Starter",
    "Minutes": "90",
    "Goals": [
      {
        "Number": "800",
        "Date": "24-03-2023",
        "Competiton": "International friendly",
        "Home team": "Argentina",
        "Result": "2-0",
        "Away team": "Panama",
        "Minute": "89",
        "Score": "2-0",
        "Whats": "Free kick",
        "How": "Left foot",
        "Jersey": "10"
      }
    ],
    "Assists": "0",
    "Cards": "0",
    "Jersey": "10"
  },
```

### ⚽ Goals

**/goals**:Returns a JSON object with all goals scored by Messi, with information such as the match, date, Competition, Jersey, etc.

Example response:

```
{
   "Number": "800",
   "Date": "24-03-2023",
   "Competiton": "International friendly",
   "Home team": "Argentina",
   "Result": "2-0",
   "Away team": "Panama",
   "Minute": "89",
   "Score": "2-0",
   "Whats": "Free kick",
   "How": "Left foot",
   "Jersey": "10"
 },
```

### 🧾 Aggregated

**/aggregated**: Returns a JSON object with various aggregated statistics for Lionel Messi, including total goals, assists, cards, and minutes played, as well as a breakdown of goals by type and jersey number.

Example response:

```
{
  "Games": 1032,
  "Goals": 814,
  "Assists": 358,
  "Cards": 96,
  "Minutes": 84814,
  "Goals + Assists": 1172,
  "Goals per game": 0.79,
  "National Team Goals": 103,
  "Club Goals": {
    "total": 711,
    "FC Barcelona": 672,
    "Paris Saint-Germain": 32,
    "Inter Miami CF": 7
  },
  "Jersey": {
    "0": 1,
    "10": 811,
    "30": 108,
    "18": 24,
    "19": 88 },
  "Goal Types": {
    "Left foot": 680,
    "Right foot": 105,
    "Head": 26,
    "Hip": 1,
    "Chest": 1,
    "Hand": 1
  }
}

```
