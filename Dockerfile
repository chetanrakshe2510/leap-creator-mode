FROM node:20-slim AS frontend-builder

WORKDIR /app/frontend

# Copy frontend files
COPY frontend/package*.json ./
RUN npm install

COPY frontend/ ./
RUN npm run build

# Backend stage
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for Manim
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libcairo2-dev \
    libpango1.0-dev \
    texlive \
    texlive-latex-extra \
    texlive-fonts-extra \
    texlive-latex-recommended \
    texlive-science \
    tipa \
    libffi-dev \
    build-essential \
    pkg-config \
    sox \
    fonts-noto \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Update font cache
RUN fc-cache -fv

# Copy backend requirements and install
COPY backend/requirements.txt /app/backend/
WORKDIR /app/backend

# First upgrade pip and install build tools (setuptools<72 needed for pkg_resources)
RUN pip install --upgrade pip "setuptools==70.0.0" wheel

# Install requirements
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ /app/backend/

# Create necessary directories
RUN mkdir -p /app/backend/generated/media/videos /app/backend/generated/logs

# Copy frontend build to the correct location
COPY --from=frontend-builder /app/frontend/dist/ /app/frontend/dist/

# Set environment variables
ENV PYTHONPATH=/app
ENV PORT=8000

# Expose the port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "leap.api_server:app", "--host", "0.0.0.0", "--port", "8000"]
