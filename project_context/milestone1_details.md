# Milestone 1 Details: Data Automation and Foundational Setup

**Estimated Time:** 1.5 – 2.5 Weeks (40 – 60 Hours)

**Tasks:**

1.  **Backend Service Setup (10-15 hrs)**
    * **Reasoning:** Current MVP is CLI, need a proper API service foundation.
    * **Deliverable:** Stable FastAPI backend structure ready for feature integration. Includes basic app setup, Uvicorn configuration, core settings (`app/core/config.py`).
2.  **Data Storage Setup (5-10 hrs)**
    * **Reasoning:** Need persistent storage for credentials, fetched data, metrics.
    * **Deliverable:** Configured database (Supabase/Postgres) integrated with the FastAPI app. Includes basic SQLAlchemy setup (`app/db/`, `app/models/` structure started).
3.  **Secure Shopify Integration (15-20 hrs)**
    * **Reasoning:** Current MVP is single-store, not scalable or using best practices for auth. Need multi-store capability via OAuth.
    * **Deliverable:** Ability to securely connect via OAuth and pull basic data (e.g., store info) from multiple Shopify stores using the FastAPI service. Includes setting up initial Shopify API client logic within the service structure.
4.  **Core Metric Calculation (10-15 hrs)**
    * **Reasoning:** Automate initial calculations currently done manually.
    * **Deliverable:** Functions within the service (`app/services/`, `app/crud/`) to calculate and store initial key metrics (AOV, Repeat Rates, Churn Rate, etc.) based on fetched Shopify data. Requires defining relevant Pydantic schemas (`app/schemas/`) and database models (`app/models/`).