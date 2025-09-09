FROM python:3.11-slim

WORKDIR /app

# Copy project files
COPY . .

# Install dependencies if present
RUN if [ -f requirements.txt ]; then \
        pip install --no-cache-dir -r requirements.txt; \
    fi

EXPOSE 8000

CMD ["python", "main.py"]
