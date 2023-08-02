import subprocess
import time

command = ["vivtool", "scan", "-v"]  # Replace with your command and arguments

process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

try:
    # Try to get the output for x seconds
    stdout, stderr = process.communicate(timeout=15)
except subprocess.TimeoutExpired:
    # If the process does not end after x seconds, kill it
    process.kill()
    stdout, stderr = process.communicate()

# Now stdout and stderr will have the output and errors till x seconds after which the process was killed
print(stdout)
print(stderr)
