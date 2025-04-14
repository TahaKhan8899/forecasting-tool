# Database Migrations Workflow (Alembic)

This document outlines the standard process for making and applying database schema changes using Alembic in this project.

## Standard Workflow

1.  **Modify SQLAlchemy Models:**
    * Make the necessary changes to your model classes defined in `app/models/`. This could involve adding/removing models, adding/removing/modifying columns or constraints, etc.
    * Ensure the models correctly inherit from `Base` defined in `app.db.session` (or `app.db.base`).

2.  **Generate Migration Script:**
    * Open your terminal in the project root directory.
    * Make sure your Poetry virtual environment is active (`poetry shell` or ensure commands are prefixed with `poetry run`).
    * Run the `revision` command with `--autogenerate`. Provide a short, descriptive message about the change using the `-m` flag:
      ```bash
      poetry run alembic revision --autogenerate -m "Add last_login column to user table"
      ```
    * Alembic will connect to the database (using the `DATABASE_URL` from your `.env` file via `alembic.ini` and `env.py`), compare your models' current state (`Base.metadata`) to the database's recorded schema version, and generate a new migration script in `alembic/versions/`.

3.  **Review Generated Script (CRITICAL STEP):**
    * **Always** open the newly generated migration script file located in `alembic/versions/`.
    * Carefully review the Python code within the `upgrade()` and `downgrade()` functions.
    * Ensure the generated operations (`op.create_table`, `op.add_column`, `op.drop_column`, etc.) accurately reflect the changes you intended to make to your models.
    * Autogenerate isn't perfect; sometimes you may need to manually edit the script for complex changes (e.g., data migrations, specific constraint naming, complex type changes).

4.  **Apply the Migration:**
    * If the migration script looks correct after review, apply it to the database using the `upgrade` command:
      ```bash
      poetry run alembic upgrade head
      ```
      *(`head` applies all migrations up to the latest one).*
    * This command executes the `upgrade()` function in the new migration script(s).

5.  **Verify Changes in Database:**
    * Connect to your Supabase database (using the Supabase Studio UI, `psql`, or another DB tool).
    * Verify that the schema changes (new table, new column, altered type, etc.) have been applied correctly.

6.  **Commit Changes to Git:**
    * Stage the changes you made to your models (`app/models/`), the new migration script (`alembic/versions/`), and potentially `alembic.ini` if needed.
    * Commit these related changes together:
      ```bash
      git add app/models/your_changed_model.py alembic/versions/your_new_migration_script.py
      git commit -m "feat: Add last_login column to User model and migration"
      ```
      *(Adjust commit message type like `feat:`, `fix:`, `refactor:` as appropriate).*

## Other Useful Alembic Commands

* **Check Current Revision:** `poetry run alembic current`
* **View Migration History:** `poetry run alembic history` or `poetry run alembic history --verbose`
* **Downgrade (Revert) Last Migration:** `poetry run alembic downgrade -1`
* **Downgrade to a Specific Revision:** `poetry run alembic downgrade <revision_id>`
* **Downgrade all Migrations (Empty DB):** `poetry run alembic downgrade base`

---

Remember to reference this file (`@project_context/migrations_workflow.md`) when asking Cursor to perform tasks that involve database schema changes!