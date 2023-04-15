from fastapi import FastAPI, Response, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
import json
import websockets

from time import sleep

import requests
from bs4 import BeautifulSoup

app = FastAPI()

def tff_data(data_type, url="https://www.tff.org/default.aspx?pageID=198"):

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



    return teams


@app.get("/")
async def root():
    return RedirectResponse("/live")

@app.get("/json")
async def json_type():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
    <title>Unavaible</title>
     <meta http-equiv="refresh" content="10;URL='/live'" />
    </head>
    <body style="background-color: #121212;">
    <p style="color: white; font-size: 14px;">The JSON type is unavailable due to system capacity issues. You will be redirected to Live in 10 seconds. For more detail <a href="" style="color: white;"> check documentation</a>
    </p>
    </body>
    </html>
    """
    return HTMLResponse(html)

@app.get("/live")
async def live():
    json_str = json.dumps(tff_data("live"), indent = 4, default = str, ensure_ascii=False)
    return Response(content=json_str, media_type='application/json')

@app.get("/live/league/{league}")
async def league_select(league):
    if league == "tff-1":
        league_url = "https://www.tff.org/default.aspx?pageID=142"
        json_str = json.dumps(tff_data("live", league_url), indent=4, default=str, ensure_ascii=False)
        return Response(content=json_str, media_type='application/json')
    elif league == "tff-2":
        league_url = "https://www.tff.org/default.aspx?pageID=976"
        json_str = json.dumps(tff_data("live", league_url), indent=4, default=str, ensure_ascii=False)
        return Response(content=json_str, media_type='application/json')
    elif league == "tff-3":
        league_url = "https://www.tff.org/default.aspx?pageID=971"
        json_str = json.dumps(tff_data("live", league_url), indent=4, default=str, ensure_ascii=False)
        return Response(content=json_str, media_type='application/json')
    elif league == "amateur":
        league_url = "https://www.tff.org/default.aspx?pageID=1596"
        json_str = json.dumps(tff_data("live", league_url), indent=4, default=str, ensure_ascii=False)
        return Response(content=json_str, media_type='application/json')