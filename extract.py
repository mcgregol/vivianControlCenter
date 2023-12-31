from sensor import Sensor
import os, subprocess, time

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

# Fetch files from the each sensor
for sensor in sensors_list:
    files_list = []
    if not os.path.isdir('/Users/achieve/Desktop/outputs/' + sensor.id):
        print("creating /Users/achieve/Desktop/outputs/" + sensor.id)
        os.makedirs('/Users/achieve/Desktop/outputs/' + sensor.id)
        ls = subprocess.run('vivtool ls --uuid ' + sensor.uuid, shell=True, capture_output=True, text=True)
        ls_lines = ls.stdout.splitlines()
        for line in ls_lines:
            files_list.append(line)
        for item in files_list:
            print("    moving " + item + " to /Users/achieve/Desktop/outputs/" + sensor.id + "...")
            subprocess.run('vivtool cp --uuid ' + sensor.uuid + ' ' + item + ' /Users/achieve/Desktop/outputs/' + sensor.id, shell=True)
    else:
        print("/Users/achieve/Desktop/outputs/" + sensor.id + " already exists")
        ls = subprocess.run('vivtool ls --uuid ' + sensor.uuid, shell=True, capture_output=True, text=True)
        ls_lines = ls.stdout.splitlines()
        for line in ls_lines:
            files_list.append(line)
        for item in files_list:
            print("    moving " + item + " to /Users/achieve/Desktop/outputs/" + sensor.id + "...")
            subprocess.run('vivtool cp --uuid ' + sensor.uuid + ' ' + item + ' /Users/achieve/Desktop/outputs/' + sensor.id, shell=True)

print("done!")
    
