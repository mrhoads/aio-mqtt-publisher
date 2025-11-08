# MQTT Publisher for CSV Data

This script reads robot sensor data from a CSV file and publishes it to an MQTT broker.

## Setup

### Using uv (Recommended)

[uv](https://github.com/astral-sh/uv) provides fast, isolated Python environments without installing packages globally.

1. Install uv if you haven't already:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. That's it! uv will automatically manage dependencies when you run the script.

### Using pip (Alternative)

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Using uv (Recommended)

Run the script directly with uv - it will automatically create an isolated environment and install dependencies:

```bash
uv run mqtt_publisher.py --broker localhost --topic robot/data --file data/sampledata.csv
```

### Using Python directly

If you installed dependencies with pip:

```bash
python mqtt_publisher.py --broker localhost --topic robot/data --file data/sampledata.csv
```

## Examples

### Basic: Publish to local broker

```bash
uv run mqtt_publisher.py --broker localhost --topic robot/data --file data/sampledata.csv
```

### With Authentication

Publish to a broker that requires authentication:

```bash
uv run mqtt_publisher.py \
  --broker mqtt.example.com \
  --topic sensors/robot1 \
  --file data/sampledata.csv \
  --username myuser \
  --password mypass
```

### Custom Interval

Adjust the delay between messages (in seconds):

```bash
uv run mqtt_publisher.py \
  --broker localhost \
  --topic robot/data \
  --file data/sampledata.csv \
  --interval 0.5
```

### Custom Port

Use a non-standard MQTT port:

```bash
uv run mqtt_publisher.py \
  --broker localhost \
  --port 1884 \
  --topic robot/data \
  --file data/sampledata.csv
```

## Arguments

- `--broker` (required): MQTT broker hostname or IP address
- `--port`: MQTT broker port (default: 1883)
- `--topic` (required): MQTT topic to publish to
- `--file` (required): Path to CSV file
- `--interval`: Delay between messages in seconds (default: 1.0)
- `--username`: MQTT username (optional)
- `--password`: MQTT password (optional)

## Data Format

Each row from the CSV is published as a JSON message. For example:
```json
{
  "KeepAliveTag_SourceTimestamp": "2025-09-24 15:13:28.3682827",
  "KeepAliveTag_Value": "363,249",
  "Robot1_Value_Compliant4": "FALSE",
  "Robot1_Value_Joint1Posn": "-203.02754",
  ...
}
```

## Testing with Local Broker

If you need a local MQTT broker for testing, you can use Mosquitto:

### Install Mosquitto (macOS)

```bash
brew install mosquitto
```

### Start Mosquitto

```bash
mosquitto -v
```

### Subscribe to messages (in another terminal)

```bash
mosquitto_sub -h localhost -t robot/data -v
```

### Publish data

```bash
uv run mqtt_publisher.py --broker localhost --topic robot/data --file data/sampledata.csv
```

## Troubleshooting

- **Connection Refused**: Make sure your MQTT broker is running and accessible
- **Authentication Failed**: Verify your username and password are correct
- **File Not Found**: Check the path to your CSV file is correct
