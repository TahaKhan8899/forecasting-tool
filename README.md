# AI-Powered Forecasting Tool

## Project Description

A robust backend API system built with FastAPI to automate the collection, calculation, and forecasting of key business metrics for e-commerce businesses using Shopify. This tool replaces manual spreadsheet-based forecasting with an automated solution that provides timely, accurate data and predictive insights to support strategic decision-making.

### Core Features

- Automated data collection from Shopify (multiple stores) and major ad platforms (Meta, Google, TikTok, Amazon)
- Calculation of key e-commerce metrics (aMER, AOV, repeat rates, etc.)
- AI-powered predictive forecasting for spend, revenue, and profitability
- "What-if" scenario analysis capabilities
- Database persistence for historical data

## Technology Stack

- **Backend Framework:** FastAPI
- **Language:** Python (Version 3.11+)
- **Database:** Supabase (PostgreSQL)
- **Data Validation:** Pydantic V2
- **Database ORM:** SQLAlchemy 2.0 (async API)
- **Testing:** Pytest
- **API Specification:** OpenAPI 3+
- **Environment Variables:** python-dotenv
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