# Use Python 3.13 slim image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv for dependency management
RUN pip install uv

# Copy dependency files
COPY pyproject.toml ./

# Install dependencies (without lock file to avoid platform compatibility issues)
RUN uv sync

# Copy source code
COPY . .

# Expose port 8000
EXPOSE 8000

# Run the application
CMD ["uv", "run", "python", "main.py"]
