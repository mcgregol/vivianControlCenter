import tkinter as tk
import os, subprocess, time
from sensor import Sensor

def on_select():
    selected_indices = listbox.curselection()
    selected_items = [listbox.get(i) for i in selected_indices]
    print("Selected items:", selected_items)

def get_sensors():
    listbox.delete(0, tk.END)  # Clear the current Listbox items

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

    sensors_list = []
    for key, value in dictionary.items():
        key = key[1:-1]
        value = value[1:-1]
        sensor = Sensor(key, value)
        sensors_list.append(sensor)

    # Add sensors to the Listbox
    for sensor in sensors_list:
        listbox.insert(tk.END, sensor.id)

root = tk.Tk()
root.title("Select Sensors to Use")
root.geometry("400x400")

# Listbox to display sensors
listbox = tk.Listbox(root, selectmode=tk.MULTIPLE)
listbox.pack(pady=20, padx=20)

# Button to retrieve selected items
scan_button = tk.Button(root, text="Scan", command=get_sensors)
scan_button.pack(pady=20)

confirm_button = tk.Button(root, text="Confirm", command=on_select)
confirm_button.pack(pady=20)

root.mainloop()

