# Application Architecture

This project follows a layered architecture for separation of concerns:

1.  **API Layer (`app/api/`)**
    * Handles incoming HTTP requests via FastAPI `APIRouter`.
    * Uses Pydantic schemas (`app/schemas/`) for request validation and response serialization.
    * Relies on FastAPI's dependency injection (`app/api/deps.py`) for common needs like database sessions or authentication.
    * Delegates business logic execution to the Service Layer.
    * Endpoints should be "thin" and primarily handle request/response formatting and calling services.
    * Organized by version (`v1/`) and feature (`endpoints/`).

2.  **Service Layer (`app/services/`)**
    * Contains the core business logic of the application.
    * Orchestrates operations, performs calculations, interacts with external services (via clients/SDKs).
    * Calls CRUD layer functions for database persistence.
    * Keeps business logic separate from API routing and raw database access.

3.  **CRUD Layer (`app/crud/`)**
    * Handles direct database interactions (Create, Read, Update, Delete).
    * Functions operate on SQLAlchemy ORM models (`app/models/`).
    * Takes Pydantic schemas or basic types as input, returns ORM model instances or basic types.
    * Isolates database-specific query logic.

4.  **Data Model Layer (`app/models/`)**
    * Defines database table structures using SQLAlchemy ORM models.

5.  **Schema Layer (`app/schemas/`)**
    * Defines data shapes for API input/output using Pydantic models. Decoupled from database models.

6.  **Database Layer (`app/db/`)**
    * Manages database connection setup (SQLAlchemy engine, session factory).

7.  **Core Layer (`app/core/`)**
    * Handles application-wide configuration and core utilities (e.g., security helpers).

**Data Flow (Typical Read Request):**
`Client -> FastAPI Router (@app.get) -> Service Function -> CRUD Function -> SQLAlchemy Model -> Database -> SQLAlchemy Model -> CRUD Function -> Service Function -> Pydantic Schema -> FastAPI Router -> Client (JSON)`

**Data Flow (Typical Create Request):**
`Client (JSON) -> FastAPI Router (@app.post) -> Pydantic Schema (Validation) -> Service Function -> Pydantic Schema -> CRUD Function -> SQLAlchemy Model -> Database -> SQLAlchemy Model -> CRUD Function -> Service Function -> Pydantic Schema -> FastAPI Router -> Client (JSON)`