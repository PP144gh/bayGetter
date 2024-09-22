[200~#!/bin/bash

# Start the Tor service
echo "Starting Tor..."
tor &

# Get the process ID of the Tor process
TOR_PID=$!

# Wait a few seconds to ensure Tor is fully started
echo "Waiting for Tor to fully start..."
sleep 10  # You can adjust the sleep time if needed

# Check if Tor is running
if ps -p $TOR_PID > /dev/null
then
	   echo "Tor is running. Now starting the Python script."

	      # Run the Python script (replace with the correct path to bayGetterScript.py)
	         python3 bayGetterScript.py

		    # Optionally, kill Tor after the script finishes
		       echo "Stopping Tor..."
		          kill $TOR_PID
		  else
			     echo "Failed to start Tor."
fi

