#!/bin/bash

# Check if Tor is already running by attempting to connect to the default Tor SOCKS port (127.0.0.1:9050)
if lsof -Pi :9050 -sTCP:LISTEN -t >/dev/null ; then
    echo "Tor is already running. Proceeding to run the Python script."
else
    # Start the Tor service if it's not running
    echo "Starting Tor..."
    tor &

    # Get the process ID of the Tor process
    TOR_PID=$!

    # Wait a few seconds to ensure Tor is fully started
    echo "Waiting for Tor to fully start..."
    sleep 10  # You can adjust the sleep time if needed

    # Check if Tor started successfully
    if ps -p $TOR_PID > /dev/null; then
        echo "Tor is running."
    else
        echo "Failed to start Tor."
        exit 1
    fi
fi

# Run the Python script (replace with the correct path to bayGetterScript.py)
echo "Now starting the Python script."
python3 bayGetterScript.py

# Optionally, stop Tor if we started it (only if $TOR_PID is set)
if [[ ! -z "$TOR_PID" ]]; then
    echo "Stopping Tor..."
    kill $TOR_PID
fi
