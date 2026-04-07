FROM python:3.10-slim

WORKDIR /app

# Essential build tools for lightweight dependency compilation
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Pre-install core framework dependencies
RUN pip install --no-cache-dir openenv-core>=0.2.3 fastapi uvicorn pydantic openai pyyaml

# Set up a new user named "user" with user ID 1000 for Hugging Face Spaces compatibility
RUN useradd -m -u 1000 user

# Set home to the user's home directory
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

# Copy minimal project files required for the environment
COPY --chown=user env.py .
COPY --chown=user openenv.yaml .
COPY --chown=user pyproject.toml .
COPY --chown=user README.md .
COPY --chown=user inference.py .
COPY --chown=user server/app.py ./app.py

# Switch to the "user" user to avoid HF permission errors
USER user

# Set default env variables for HF Spaces compatibility
ENV API_BASE_URL=https://router.huggingface.co/v1
ENV MODEL_NAME=meta-llama/Llama-3-8B-Instruct
ENV PORT=7860

# Expose standard HF Space port
EXPOSE 7860

# Fast Cold Start: Run uvicorn directly with optimized worker count
# Pointing to the new server/app.py location required by openenv-core
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
