from sensor import Sensor
import subprocess, time

scan = subprocess.Popen('vivtool scan', shell=True, stdout=subprocess.PIPE)

# change to 10-15 for irl use
time.sleep(5)

if scan.poll() is None:
    scan.terminate()
    time.sleep(0.5)
    if scan.poll() is None:
        scan.kill()

scan_output, _ = scan.communicate()

pretty_string = scan_output.decode('utf-8')

lines = pretty_string.splitlines()

dictionary = {}

for line in lines[2:]:
    key, value = line.split(' ')
    dictionary[key] = value

print(dictionary)
