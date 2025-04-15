# Start directly from the Python base image
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app

# Copy the requirements file generated LOCALLY (using 'poetry export') and committed
COPY requirements.txt .

# Install dependencies using pip (standard and reliable)
RUN pip install --no-cache-dir -r requirements.txt 

# Install gunicorn/uvicorn separately
# (Alternatively, add gunicorn and uvicorn to your main dependencies 
# in pyproject.toml before exporting requirements.txt locally)
RUN pip install --no-cache-dir gunicorn uvicorn

# Copy application code
COPY ./app /app/app

ENV PORT=8000
EXPOSE ${PORT}

# CMD remains the same
CMD ["sh", "-c", "gunicorn -w 2 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:${PORT}"]