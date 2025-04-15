# AI-Powered Forecasting Tool

## Project Description

A robust backend API system built with FastAPI to automate the collection, calculation, and forecasting of key business metrics for e-commerce businesses using Shopify. This tool replaces manual spreadsheet-based forecasting with an automated solution that provides timely, accurate data and predictive insights to support strategic decision-making.

### Core Features

- Automated data collection from Shopify (multiple stores) and major ad platforms (Meta, Google, TikTok, Amazon)
- Calculation of key e-commerce metrics (aMER, AOV, repeat rates, etc.)
- AI-powered predictive forecasting for spend, revenue, and profitability
- "What-if" scenario analysis capabilities
- Database persistence for historical data
- Structured JSON logging for observability

## Technology Stack

- **Backend Framework:** FastAPI
- **Language:** Python (Version 3.11+)
- **Database:** Supabase (PostgreSQL)
- **Data Validation:** Pydantic V2
- **Database ORM:** SQLAlchemy 2.0 (async API)
- **Testing:** Pytest
- **API Specification:** OpenAPI 3+
- **Environment Variables:** python-dotenv
- **Logging:** Structlog + python-json-logger
- **Server:** Uvicorn
- **Version Control:** Git / GitHub

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Git
- Supabase account (for PostgreSQL database)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```

2. Navigate to the project directory:
   ```bash
   cd ai-powered-forecasting-tool
   ```

3. Install Poetry (if you haven't already):
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

4. Install dependencies using Poetry:
   ```bash
   poetry install
   ```

5. Set up environment variables:
   - Copy the example environment file:
     ```bash
     cp .env.example .env
     ```
   - Open the `.env` file and update the `DATABASE_URL` with your Supabase PostgreSQL connection string
   - Fill in any other required environment variables

## Running the Application Locally

Start the development server with:

```bash
poetry run uvicorn app.main:app --reload
```

The API will be available at http://127.0.0.1:8000

## Running with Docker (Recommended)

This is the recommended way to run the application consistently, mirroring a production-like environment.

### Prerequisites

- Docker installed and running.

### Dependency Workflow (Crucial!)

The Docker image relies on a `requirements.txt` file for Python dependencies. This file is generated locally using Poetry and **must be kept up-to-date and committed to Git** whenever dependencies change.

**When adding/updating/removing dependencies in `pyproject.toml`:**

1.  Modify your `pyproject.toml` file.
2.  Update the lock file:
    ```bash
    poetry lock
    ```
3.  Ensure the `poetry-plugin-export` is installed locally (one-time or per environment check):
    *Check if needed/installed:*
    ```bash
    poetry plugin show 
    ```
    *Install if needed (for Poetry 2.0+):*
    ```bash
    poetry self add poetry-plugin-export
    ```
4.  Export dependencies to `requirements.txt`:
    ```bash
    poetry export --without dev --format requirements.txt --output requirements.txt
    ```
5.  Verify `requirements.txt` was updated (`cat requirements.txt`).
6.  Commit *all three* files (`pyproject.toml`, `poetry.lock`, `requirements.txt`):
    ```bash
    git add pyproject.toml poetry.lock requirements.txt
    git commit -m "Update project dependencies"
    ```

### Building the Docker Image

Ensure you have completed the dependency workflow above if dependencies have changed.

```bash
docker build -t forecasting-api:latest .
```

### Environment Variables for Docker

The container requires environment variables to run correctly (e.g., database connection strings, external API keys). These should be defined in a `.env` file (based on `.env.example`) in your project root. The docker run command will load these using the `--env-file` flag. Make sure your `.env` file contains all necessary runtime variables.

### Running the Container

Use the image built previously. Ensure your `.env` file is configured.

```bash
# Run in detached mode (background)
docker run -d -p 8000:8000 --env-file .env --name forecasting-api-container forecasting-api:latest
```

- `-d`: Run container in the background (detached).
- `-p 8000:8000`: Map port 8000 on your host machine to port 8000 inside the container.
- `--env-file .env`: Load environment variables from your local `.env` file into the container.
- `--name forecasting-api-container`: Assign a convenient name to the running container.
- `forecasting-api:latest`: The name and tag of the image to run.

### Accessing the API (via Docker)

Once the container is running:

- API Base URL: http://localhost:8000
- Swagger UI Docs: http://localhost:8000/docs
- ReDoc Docs: http://localhost:8000/redoc

### Managing the Container

**View Logs:**
```bash
docker logs forecasting-api-container
```

Add `-f` to follow logs in real-time:
```bash
docker logs -f forecasting-api-container
```

**Stop Container:**
```bash
docker stop forecasting-api-container
```

**Remove Container (after stopping):**
```bash
docker rm forecasting-api-container
```

## API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

These documentation pages allow you to explore the available endpoints and test them directly from your browser.

## Running Tests

To run the test suite:

```bash
poetry run pytest
```

## License

MIT 