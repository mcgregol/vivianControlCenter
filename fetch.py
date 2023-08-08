from sensor import Sensor
import subprocess, time

# Start 'vivtool scan' as a subprocess
scan = subprocess.Popen('vivtool scan', shell=True, stdout=subprocess.PIPE)

# Allow the scan command to run for 5 seconds, then attempt to stop it
time.sleep(5)
if scan.poll() is None:
    scan.terminate()
    time.sleep(0.5)
    if scan.poll() is None:
        scan.kill()

# Get the output from the scan subprocess and decode it from bytes to a string
scan_output, _ = scan.communicate()
pretty_string = scan_output.decode('utf-8')

# Split the string into lines and initialize a dictionary for storing the parsed output
lines = pretty_string.splitlines()
dictionary = {}

# Parse each line into a key-value pair and store it in the dictionary, skipping the first two lines of output
for line in lines[2:]:
    key, value = line.split()
    dictionary[key] = value

# Initialize a list for storing Sensor objects
sensors_list = []

# Convert each key-value pair in the dictionary into a Sensor object and add it to the list
for key, value in dictionary.items():
    key = key[1:-1]
    value = value[1:-1]
    sensor = Sensor(key, value)
    sensors_list.append(sensor)

# Print the details of each sensor
for sensor in sensors_list:
    print(sensor.list() + "\n")