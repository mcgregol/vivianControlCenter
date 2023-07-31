import subprocess

scan = subprocess.Popen('vivtool scan -v', stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

while True:
    scan_output = scan.stdout.readline().decode()
    
    if scan_output == '' and process.poll() is not None:
        break
        
    if scan_output:
        print(scan_output.strip())
        
rc = process.poll()