#!/bin/bash

# Define the range of ports to check
START_PORT=1024
END_PORT=1400

# Initialize a counter for found ports
FOUND_PORTS=0

# Variables to store the found ports
SENDER_PORT=""
EMULATOR_SENDER_PORT=""
RECEIVER_PORT=""
EMULATOR_RECEIVER_PORT=""

# Iterate through the port range
for ((port=START_PORT; port<=END_PORT; port++)); do
  echo "Checking $port"
    # Check if the port is in use
    if ! lsof -i:$port > /dev/null 2>&1; then
        # Port is not in use, store it in the next available variable
        if [ -z "$SENDER_PORT" ]; then
            SENDER_PORT=$port
        elif [ -z "$EMULATOR_SENDER_PORT" ]; then
            EMULATOR_SENDER_PORT=$port
        elif [ -z "$RECEIVER_PORT" ]; then
            RECEIVER_PORT=$port
        elif [ -z "$EMULATOR_RECEIVER_PORT" ]; then
            EMULATOR_RECEIVER_PORT=$port
            # We have found 4 ports, no need to continue
            break
        fi
        # Increment the counter
        ((FOUND_PORTS++))
    fi
done

# Build and echo the commands
echo "Run the following commands:"
echo "python3 network_emulator.py $EMULATOR_SENDER_PORT 127.0.0.1 $RECEIVER_PORT $EMULATOR_RECEIVER_PORT 127.0.0.1 $SENDER_PORT 100 0.8 1"
echo "python3 receiver.py 127.0.0.1 $EMULATOR_RECEIVER_PORT $RECEIVER_PORT hello.txt"
echo "python3 sender.py 127.0.0.1 $EMULATOR_SENDER_PORT $SENDER_PORT 1000 to.txt"
