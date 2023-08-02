import subprocess, time

scan = subprocess.Popen('vivtool scan', shell=True, stdout=subprocess.PIPE)

time.sleep(5)

if scan.poll() is None:
    scan.terminate()
    time.sleep(0.5)
    if scan.poll() is None:
        scan.kill()
        
scan_output, _ = scan.communicate()

#print(str(scan_output).replace('b', ''))
print(scan_output.decode('utf-8'))