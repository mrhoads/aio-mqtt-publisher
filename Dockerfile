FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml ./
COPY mqtt_publisher.py ./
COPY data/ ./data/

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Install dependencies using uv
RUN uv pip install --system -r pyproject.toml

# Set default command (can be overridden)
ENTRYPOINT ["python", "mqtt_publisher.py"]

# Default arguments (can be overridden at runtime)
CMD ["--broker", "localhost", "--topic", "robot/data", "--file", "data/sampledata.csv"]
