# TFF Leagues Scraper

An asynchronous REST API to scrape real-time standings and fixtures from the official Turkish Football Federation (TFF) website.

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
