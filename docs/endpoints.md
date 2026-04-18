# API Endpoints

Base URL: `http://localhost:8000/api`

## 1. Health Check
Checks if the API is running correctly.

* **URL:** `/`
* **Method:** `GET`
* **Success Response:** `{"status": "Online", "message": "..."}`

---

## 2. Simple Standings
Fetches the current standings for standard, single-group leagues.

* **URL:** `/standings/{league_name}`
* **Method:** `GET`
* **URL Parameters:**
    * `league_name` (string): The slug of the league (e.g., `trendyol-super-league`)
* **Success Response:** HTTP 200 with JSON list of teams.
* **Error Response:** HTTP 404 (League not found) or HTTP 502 (Upstream error).

---

## 3. Multi-Group Standings
Fetches standings for leagues divided into multiple groups (e.g., Nesine 2. League).

* **URL:** `/multi-standings/{league_name}/{group_index}`
* **Method:** `GET`
* **URL Parameters:**
    * `league_name` (string): The slug of the league.
    * `group_index` (integer): Zero-based index of the group (0 for Group 1, 1 for Group 2).