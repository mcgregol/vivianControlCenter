import subprocess
import time

scan_output = subprocess.run(['vivtool', 'scan', '-v'], stdout=subprocess.PIPE)

for i in range(15):
    time.sleep(2)
    print(scan_output.stdout.decode('utf-8'))
