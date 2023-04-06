from fastapi import FastAPI, Response
import os
import json

import requests
import pandas as pd
from bs4 import BeautifulSoup

app = FastAPI()

url = "https://www.tff.org/default.aspx?pageID=198"

def tff_data(data_type):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("table", {"class": "s-table"})

    teams = []  # Tüm takımları saklayacak bir liste oluşturun

    rows = table.findAll("tr")[1:]

    for row in rows:

        cells = row.findAll("td")
        team_data = {
            "name": cells[0].text.strip().split(".", 1)[-1].strip(),
            "played": int(cells[1].text.strip()),
            "wins": int(cells[2].text.strip()),
            "draws": int(cells[3].text.strip()),
            "losses": int(cells[4].text.strip()),
            "goals_for": int(cells[5].text.strip()),
            "goals_against": int(cells[6].text.strip()),
            "average": int(cells[7].text.strip()),
            "points": int(cells[8].text.strip())
        }
        teams.append(team_data)


    with open("table.json", "w", encoding="utf-8") as f:
        json.dump(teams, f, ensure_ascii=False, indent=4)
    f.close()

    with open('table.json', 'r', encoding="utf-8") as json_file:
        json_object = json.load(json_file)

    if data_type == "json_file":
        return json_object
    elif data_type == "live":
        return teams


@app.get("/")
async def root():
    json_str = json.dumps(tff_data("live"), indent = 4, default = str, ensure_ascii=False)
    return Response(content=json_str, media_type='application/json')
