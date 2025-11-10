# Docker Usage Guide

## Quick Start with Docker Compose (Recommended)

The easiest way to run the MQTT publisher with a local broker:

```bash
# Start both the publisher and Mosquitto broker
docker compose up

# Run in background
docker compose up -d

# View logs
docker compose logs -f

# Stop everything
docker compose down
```

This will:
- Start a Mosquitto MQTT broker on port 1883
- Start the publisher in loop mode
- Automatically connect them together

## Using Dockerfile Only

### Build the Image

```bash
docker build -t mqtt-publisher .
```

### Run the Container

**Basic usage (connect to external broker):**
```bash
docker run mqtt-publisher \
  --broker mqtt.example.com \
  --topic robot/data \
  --file data/sampledata.csv
```

**With loop mode:**
```bash
docker run mqtt-publisher \
  --broker mqtt.example.com \
  --topic robot/data \
  --file data/sampledata.csv \
  --loop
```

**With custom interval:**
```bash
docker run mqtt-publisher \
  --broker mqtt.example.com \
  --topic robot/data \
  --file data/sampledata.csv \
  --interval 0.5 \
  --loop
```

**With authentication:**
```bash
docker run mqtt-publisher \
  --broker mqtt.example.com \
  --topic robot/data \
  --file data/sampledata.csv \
  --username myuser \
  --password mypass
```

### Connect to Host Network

To connect to a broker running on your host machine:

**macOS/Windows:**
```bash
docker run mqtt-publisher \
  --broker host.docker.internal \
  --topic robot/data \
  --file data/sampledata.csv
```

**Linux:**
```bash
docker run --network host mqtt-publisher \
  --broker localhost \
  --topic robot/data \
  --file data/sampledata.csv
```

## Using Your Own CSV File

Mount your own CSV file as a volume:

```bash
docker run -v /path/to/your/data.csv:/app/data/custom.csv mqtt-publisher \
  --broker mqtt.example.com \
  --topic robot/data \
  --file data/custom.csv
```

## Docker Compose Configuration

The `docker-compose.yml` includes:

- **mqtt-publisher**: Your Python publisher running in loop mode
- **mosquitto**: MQTT broker accessible on port 1883

### Customize docker-compose.yml

Edit the `command` section to change publisher settings:

```yaml
command: >
  --broker mosquitto
  --topic your/topic
  --file data/sampledata.csv
  --interval 0.5
  --loop
```

### View Mosquitto Logs

```bash
docker compose logs mosquitto
```

### Subscribe to Messages

From your host machine:

```bash
# If you have mosquitto_sub installed
mosquitto_sub -h localhost -t robot/data -v

# Or use Docker
docker run -it --rm --network ignite-2025-mqtt_mqtt-network eclipse-mosquitto mosquitto_sub -h mosquitto -t robot/data -v
```

## Troubleshooting

**Container exits immediately:**
- Check logs: `docker compose logs mqtt-publisher`
- Verify CSV file exists: `docker run mqtt-publisher ls -la data/`

**Can't connect to broker:**
- Verify broker is running: `docker compose ps`
- Check network connectivity: `docker compose logs mosquitto`
- Try using broker IP instead of hostname

**Permission denied on volumes:**
```bash
# Create directories with proper permissions
mkdir -p mosquitto/data mosquitto/log
chmod -R 777 mosquitto/
```

## Production Tips

1. **Don't use `allow_anonymous true` in production** - configure proper authentication
2. **Use secrets for passwords** - don't hardcode them
3. **Set resource limits** in docker-compose.yml
4. **Use specific image tags** instead of `latest`
5. **Enable TLS** for secure connections
