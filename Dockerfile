FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml ./
COPY mqtt_publisher.py ./
COPY data/ ./data/

# Install dependencies directly with pip (more reliable than uv in containers)
RUN pip install --no-cache-dir paho-mqtt>=1.6.1

# Set default command (can be overridden)
ENTRYPOINT ["python", "mqtt_publisher.py"]

# Default arguments (can be overridden at runtime)
CMD ["--broker", "localhost", "--topic", "robot/data", "--file", "data/sampledata.csv"]
