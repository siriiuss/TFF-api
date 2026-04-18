# System Architecture

The application is built keeping separation of concerns in mind.

## Folder Structure

* `app/api/`: Contains FastAPI route definitions.
* `app/services/`: Contains the core scraping logic (BeautifulSoup4).
* `app/schemas/`: Contains Pydantic models for data validation.
* `tests/`: Contains Pytest files utilizing Respx for mocking external network calls.

## Caching Strategy
We use `fastapi-cache2` with an `InMemoryBackend`. This ensures that if 100 users request the Super League standings within the same minute, only 1 request is actually made to the TFF servers, preventing IP bans.