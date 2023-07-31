import subprocess

scan_output = subprocess.run(['vivtool', 'scan', '-v'], stdout=subprocess.PIPE)
print(scan_output.stdout.decode('utf-8'))
