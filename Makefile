.PHONY: help run test-local install clean

help:
	@echo "MQTT Publisher - Available commands:"
	@echo ""
	@echo "  make run          - Run with default settings (localhost)"
	@echo "  make test-local   - Run with local Mosquitto broker"
	@echo "  make install      - Install uv (if not already installed)"
	@echo "  make clean        - Remove virtual environment"
	@echo ""
	@echo "Using uv for isolated development - no global packages installed!"

run:
	uv run mqtt_publisher.py --broker localhost --topic robot/data --file data/sampledata.csv

test-local:
	@echo "Make sure Mosquitto is running: mosquitto -v"
	@echo "Subscribe in another terminal: mosquitto_sub -h localhost -t robot/data -v"
	@echo ""
	uv run mqtt_publisher.py --broker localhost --topic robot/data --file data/sampledata.csv --interval 0.5

install:
	@command -v uv >/dev/null 2>&1 || { \
		echo "Installing uv..."; \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
	}
	@echo "✓ uv is installed"

clean:
	rm -rf .venv
	@echo "✓ Virtual environment removed"
