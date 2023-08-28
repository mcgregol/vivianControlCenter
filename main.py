import tkinter as tk
from sensor import Sensor
from tkinter import messagebox
import asyncio, os, subprocess, time

sensors_list = []

def clock_sync():
    selected_indices = listbox.curselection()
    selected_ids = [listbox.get(i) for i in selected_indices]
    selected_sensors = []
    for sensor_id in selected_ids:
        #   remove battery percentage from listbox id
        whole = sensor_id.split()
        only_id = whole[0]
        for sensor in sensors_list:
            if sensor.id == only_id:
                selected_sensors.append(sensor)
    for sensor in selected_sensors:
        print(sensor.id + ": ")
        date = subprocess.run('vivtool date -h -s now --uuid ' + sensor.uuid, shell=True)
        print("Clocks now synced!")


def on_select():
    selected_indices = listbox.curselection()
    selected_ids = [listbox.get(i) for i in selected_indices]
    selected_sensors = []
    for sensor_id in selected_ids:
        #   remove battery percentage from listbox id
        whole = sensor_id.split()
        only_id = whole[0]
        for sensor in sensors_list:
            if sensor.id == only_id:
                selected_sensors.append(sensor)
    # Fetch files from the each sensor
    for sensor in selected_sensors:
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
    messagebox.showinfo("Done!", "Success! Files located in \'outputs\' folder on the Desktop.")
    root.destroy()

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

    for key, value in dictionary.items():
        key = key[1:-1]
        value = value[1:-1]
        sensor = Sensor(key, value)
        sensors_list.append(sensor)

    # Check if sensors found
    if sensors_list:
        loop = asyncio.get_event_loop()
        # Add sensors to the Listbox
        for sensor in sensors_list:
            battery_level = loop.run_until_complete(sensor.get_batt())
            listbox.insert(tk.END, sensor.id + " {" + battery_level + "%}")
        confirm_button.config(state=tk.NORMAL)
        date_button.config(state=tk.NORMAL)
    else:
        listbox.insert(tk.END, "No sensors found...")
        listbox.insert(tk.END, "Is bluetooth on?")


    listbox.select_set(0, tk.END)
    messagebox.showinfo("Sensor Selection", "Use \'CTRL + click\' to deslect a sensor. Use \'CTRL + drag\' to select multiple sensors. All sensors are selected by default.")

root = tk.Tk()
root.title("Select Sensors to Use")
root.geometry("800x600")

# Button to retrieve selected items
scan_button = tk.Button(root, text="Scan", command=get_sensors)
scan_button.pack(pady=20)

# Listbox to display sensors
listbox = tk.Listbox(root, selectmode=tk.EXTENDED)
listbox.pack(pady=20, padx=20)
listbox.insert(tk.END, "TIP: scan to find sensors")

confirm_button = tk.Button(root, text="Get Data", command=on_select, state=tk.DISABLED)
confirm_button.pack(pady=20)

date_button = tk.Button(root, text="Sync Clocks", command=clock_sync, state=tk.DISABLED)
date_button.pack(pady=20)

root.mainloop()