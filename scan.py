import subprocess
import time

scan_output = subprocess.run(['vivtool', 'scan', '-v'], stdout=subprocess.PIPE)

for i in range(30):
    print(scan_output.stdout.decode('utf-8'))
    time.sleep(1)
