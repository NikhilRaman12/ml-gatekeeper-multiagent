# Use official lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the validator source code
COPY validation_agent.py .

# Expose port 8080 (Cloud Run default)
EXPOSE 8080

# Run FastAPI app with Uvicorn
CMD ["uvicorn", "validation_agent:app", "--host", "0.0.0.0", "--port", "8080"]