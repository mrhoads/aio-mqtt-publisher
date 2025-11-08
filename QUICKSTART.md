# Quick Start with uv

## What is uv?

`uv` is an extremely fast Python package installer and resolver that creates isolated environments automatically. You don't need to install packages globally or manage virtual environments manually.

## Installation

If you don't have uv installed:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Run the MQTT Publisher

Just use `uv run` - it handles everything:

```bash
uv run mqtt_publisher.py --broker localhost --topic robot/data --file data/sampledata.csv
```

The first time you run this, `uv` will:
1. Create an isolated environment
2. Install the required dependencies (paho-mqtt)
3. Run your script

Subsequent runs will be much faster since the environment is cached.

## Common Commands

### Run with different options

```bash
# Custom interval (0.5 seconds between messages)
uv run mqtt_publisher.py --broker localhost --topic robot/data --file data/sampledata.csv --interval 0.5

# With authentication
uv run mqtt_publisher.py --broker mqtt.example.com --topic sensors/robot1 --file data/sampledata.csv --username user --password pass
```

### Check what's installed

```bash
uv pip list
```

### Update dependencies

```bash
uv sync
```

## Benefits of using uv

- ✓ **No global package pollution** - Everything is isolated
- ✓ **Fast** - 10-100x faster than pip
- ✓ **Automatic** - No need to create/activate virtual environments
- ✓ **Reproducible** - Consistent environments across machines
- ✓ **Clean** - Easy to remove (just delete the `.venv` folder)

## Cleanup

If you want to remove the environment:

```bash
rm -rf .venv
```

That's it! Next time you run `uv run`, it will recreate it.
