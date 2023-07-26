#!/bin/bash



# Decode the Python script from base64
python_script=$(base64 -d <<< "{{python_script}}")

# Check if the script can be executed by Bash
if command -v python3 &> /dev/null; then
    # If Python 3 is available, call Python to execute the script
    python3 - <<EOF
$python_script
EOF
else
    # If Python 3 is not available, display an error message
    echo "Python 3 is required to execute this script."
    exit 1
fi