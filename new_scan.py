import subprocess
import time

process = subprocess.Popen('vivtool scan', stdout=subprocess.PIPE, shell=True)

try:
    # Try to get the output for 15 seconds
    stdout = process.communicate(timeout=5)
except subprocess.TimeoutExpired:
    # If the process does not end after 15 seconds, kill it
    process.kill()
    stdout = process.communicate()

# Now stdout will have the output and errors till 15 seconds after which the process was killed
print(stdout)
