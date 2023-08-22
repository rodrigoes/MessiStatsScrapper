import json
from fastapi import FastAPI

app = FastAPI()

@app.get("/goals")
async def read_goal_data():
    with open("goal_data.json", "r") as file:
        data = json.load(file)
    return data

@app.get("/aggregated")
async def read_aggregated_data():
    with open("aggregated_data.json", "r") as file:
        data = json.load(file)
    return data

@app.get("/games")
async def read_game_data_e0xpanded():
    with open("game_data_expanded.json", "r") as file:
        data = json.load(file)
    return data
