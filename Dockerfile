FROM python:3.10-slim

WORKDIR /app

# Ensure we have essential build tools if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY env.py .
COPY inference.py .
COPY openenv.yaml .

# Set default env variables (can be overridden)
ENV API_BASE_URL=https://router.huggingface.co/v1
ENV MODEL_NAME=meta-llama/Llama-3-8B-Instruct

# Execution command as specified for OpenEnv
CMD ["python", "inference.py"]
