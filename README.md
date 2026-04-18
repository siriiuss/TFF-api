# TFF Leagues Scraper

An asynchronous REST API to scrape real-time standings and fixtures from the official Turkish Football Federation (TFF) website.


## ⚠️ Legal Disclaimer & Data Usage Terms
1. **Intellectual Property:** All data retrieved through this tool is the exclusive property of the **Turkish Football Federation (TFF)**. This software does not grant any rights, titles, or licenses over the retrieved data.
2. **Terms of Service:** Users are strictly required to comply with the [TFF Terms of Use](https://www.tff.org/Default.aspx?pageID=179). The commercial use, redistribution, or permanent storage of TFF data without explicit written permission from the federation is strictly prohibited.
3. **Priority of Terms:** While this software is licensed under **GPLv3**, this license applies **ONLY to the source code** of the scraper. TFF’s data usage policies and legal terms take absolute precedence over any permissions granted by the GPLv3 regarding the data itself.
4. **Limitation of Liability:** The author (**Ahmet DURAN**) shall not be held responsible for any misuse of this tool or any legal consequences arising from the violation of TFF's terms. Users are solely responsible for their own actions and the legality of how they utilize the retrieved data.

---


## Tech Stack
- **Framework:** FastAPI
- **Scraping:** BeautifulSoup4 & HTTPX
- **Caching:** FastAPI-Cache (In-memory)
- **Testing:** Pytest & Respx

## Installation

1. Clone the repository:
   ```bash
   git clone git clone https://github.com/yourusername/tff-leagues-scraper.git
   cd tff-leagues-api
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

## Usage

Docs: https://siriiuss.github.io/TFF-Leagues-Scraper/

Start the server:
```bash
uvicorn app.main:app --reload
```

### API Endpoints

- `GET /`: Health check
- `GET /api/standings/{league_name}`: Get standings for simple leagues
- `GET /api/multi-standings/{league_name}/{group_index}`: Get standings for multi-group leagues
- `GET /api/fixture/{league_name}`: Get fixture/match results

Documentation is available at `http://localhost:8000/docs`.

## Testing

Run the test suite:
```bash
pytest tests/ -v
```

## License
MIT
