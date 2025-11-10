#!/usr/bin/env python3
"""
MQTT Publisher for Robot Data
Reads CSV data and publishes it to an MQTT broker
"""

import csv
import json
import time
import argparse
from datetime import datetime
import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc, properties=None):
    """Callback for when the client connects to the broker"""
    if rc == 0:
        print(f"✓ Connected to MQTT broker successfully")
    else:
        print(f"✗ Connection failed with code {rc}")


def on_publish(client, userdata, mid, reason_code=None, properties=None):
    """Callback for when a message is published"""
    pass  # Removed verbose logging per message


def publish_csv_data(broker_host, broker_port, topic, csv_file, interval=1.0, username=None, password=None, loop=False):
    """
    Read CSV file and publish each row to MQTT broker
    
    Args:
        broker_host: MQTT broker hostname or IP
        broker_port: MQTT broker port (default 1883)
        topic: MQTT topic to publish to
        csv_file: Path to CSV file
        interval: Delay between messages in seconds
        username: Optional MQTT username
        password: Optional MQTT password
        loop: If True, continuously loop through CSV file
    """
    
    # Create MQTT client with callback API version 2
    client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_publish = on_publish
    
    # Set credentials if provided
    if username and password:
        client.username_pw_set(username, password)
        print(f"Using authentication with username: {username}")
    
    try:
        # Connect to broker
        print(f"Connecting to MQTT broker at {broker_host}:{broker_port}...")
        client.connect(broker_host, broker_port, 60)
        client.loop_start()
        
        # Give connection time to establish
        time.sleep(1)
        
        # Read and publish CSV data
        print(f"\nReading data from: {csv_file}")
        print(f"Publishing to topic: {topic}")
        print(f"Interval between messages: {interval}s")
        if loop:
            print("Mode: Continuous loop (Press Ctrl+C to stop)")
        else:
            print("Mode: Single pass through file")
        print()
        
        row_count = 0
        iteration = 0
        
        while True:
            iteration += 1
            if loop and iteration > 1:
                print(f"\n--- Starting iteration {iteration} ---\n")
            
            with open(csv_file, 'r') as file:
                csv_reader = csv.DictReader(file)
                
                for row in csv_reader:
                    # Convert row to JSON
                    message = json.dumps(row)
                    
                    # Publish message
                    result = client.publish(topic, message, qos=1)
                    
                    row_count += 1
                    print(f"[{row_count}] Published row at {row.get('Robot1_SourceTimestamp', 'N/A')}")
                    
                    # Wait before sending next message
                    time.sleep(interval)
            
            # Exit loop if not in continuous mode
            if not loop:
                break
        
        print(f"\n✓ Successfully published {row_count} messages")
        
    except FileNotFoundError:
        print(f"✗ Error: CSV file not found: {csv_file}")
    except ConnectionRefusedError:
        print(f"✗ Error: Could not connect to MQTT broker at {broker_host}:{broker_port}")
        print("  Make sure the broker is running and accessible")
    except KeyboardInterrupt:
        print("\n\n⚠ Publishing interrupted by user")
    except Exception as e:
        print(f"✗ Error: {e}")
    finally:
        # Cleanup
        client.loop_stop()
        client.disconnect()
        print("Disconnected from broker")


def main():
    parser = argparse.ArgumentParser(
        description='Publish CSV data to MQTT broker',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Publish to local broker (single pass)
  python mqtt_publisher.py --broker localhost --topic robot/data --file data/sampledata.csv
  
  # Continuously loop through CSV
  python mqtt_publisher.py --broker localhost --topic robot/data --file data/sampledata.csv --loop
  
  # Publish with authentication and custom interval
  python mqtt_publisher.py --broker mqtt.example.com --topic sensors/robot1 \\
                           --file data/sampledata.csv --interval 0.5 \\
                           --username myuser --password mypass
        """
    )
    
    parser.add_argument('--broker', required=True, help='MQTT broker hostname or IP address')
    parser.add_argument('--port', type=int, default=1883, help='MQTT broker port (default: 1883)')
    parser.add_argument('--topic', required=True, help='MQTT topic to publish to')
    parser.add_argument('--file', required=True, help='Path to CSV file')
    parser.add_argument('--interval', type=float, default=1.0, 
                       help='Delay between messages in seconds (default: 1.0)')
    parser.add_argument('--username', help='MQTT username (optional)')
    parser.add_argument('--password', help='MQTT password (optional)')
    parser.add_argument('--loop', action='store_true',
                       help='Continuously loop through CSV file (default: false)')
    
    args = parser.parse_args()
    
    # Publish data
    publish_csv_data(
        broker_host=args.broker,
        broker_port=args.port,
        topic=args.topic,
        csv_file=args.file,
        interval=args.interval,
        username=args.username,
        password=args.password,
        loop=args.loop
    )


if __name__ == '__main__':
    main()
