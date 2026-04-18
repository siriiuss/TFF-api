# API Endpoints

Base URL: `http://localhost:8000/api`

---

## 1. Health Check
Checks if the API is running correctly.

* **URL:** `/`
* **Method:** `GET`
* **Success Response:** `{"status": "Online", "message": "TFF Leagues API is running."}`

---

## 2. Simple Standings
Fetches the current standings for standard, single-group leagues.

* **URL:** `/standings/{league_name}`
* **Method:** `GET`
* **URL Parameters:**
    * `league_name` (string): The slug of the league.

### Supported Simple Leagues
You can use the following slugs for the `league_name` parameter:

| League Name | Slug (`league_name`) |
| :--- | :--- |
| Trendyol Süper Lig | `trendyol-super-league` |
| Trendyol 1. Lig | `trendyol-1-league` |
| Turkcell Kadın Futbol Süper Ligi | `turkcell-womens-super-league` |
| Türk Telekom e-Süper Lig | `turk-telekom-e-super-league` |

**Example Request:**
```http
GET /api/standings/trendyol-super-league
```

---

## 3. Multi-Group Standings
Fetches standings for leagues that are divided into multiple groups (e.g., White Group, Red Group).

* **URL:** `/multi-standings/{league_name}/{group_index}`
* **Method:** `GET`
* **URL Parameters:**
    * `league_name` (string): The slug of the multi-group league.
    * `group_index` (integer): The zero-based index of the specific group.

### Supported Multi-Group Leagues
| League Name | Slug (`league_name`) | Total Groups |
| :--- | :--- | :--- |
| Nesine 2. Lig | `nesine-2-league` | 2 Groups (White & Red) |
| Nesine 3. Lig | `nesine-3-league` | 4 Groups |
| Bölgesel Amatör Lig (BAL) | `regional-amateur-league-bal` | Multiple Groups |

### How to use `group_index`?
The TFF website uses different internal IDs for each group. Our API simplifies this by using a zero-based index (`0`, `1`, `2`, etc.).

**For Nesine 2. League:**
* `0`: Beyaz Grup (White Group)
* `1`: Kırmızı Grup (Red Group)

**For Nesine 3. League:**
* `0`: 1. Grup
* `1`: 2. Grup
* `2`: 3. Grup
* `3`: 4. Grup

**Example Requests:**
```http
# Fetch Nesine 2. League - Beyaz Grup (White Group)
GET /api/multi-standings/nesine-2-league/0

# Fetch Nesine 3. League - 4. Grup
GET /api/multi-standings/nesine-3-league/3
```

---

## 4. Fixtures (Coming Soon)
Fetches the match results and upcoming fixtures for a given league.

* **URL:** `/fixture/{league_name}`
* **Method:** `GET`
