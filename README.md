# Messi Stats Scrapper

![BG](https://user-images.githubusercontent.com/36699060/229386298-5d7140c1-9f76-4ef4-9475-28c3dae788c6.png)

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
2. Install the required dependencies:
You can install these dependencies using the following command:
```
pip install -r requirements.txt
```
## 💻 Usage
To collect the statistics, run the Scrapper.py script with the following command:
python Scrapper.py

This script will download the data from the website and process it into JSON files that will be stored in the data directory.

To start the FastAPI API, run the Main.py script with the following command:

uvicorn Main:app --reload

This command will start the API server at http://localhost:8000/, and you can access the endpoints using a web browser or a HTTP client.

API endpoints
The Messi Stats API provides the following endpoints:

/matches: returns a list of all matches played by Messi, with information such as the date, opponent, competition, and score.
/goals: returns a list of all goals scored by Messi, with information such as the match, minute, type of goal, and assist.
/stats: returns aggregated statistics for Messi, such as the total number of matches, goals, assists, shots, passes, and dribbles.
You can access these endpoints by sending a GET request to the corresponding URL
