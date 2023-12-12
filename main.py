import tkinter as tk
from dateutil import parser
from sensor import Sensor
from tkinter import messagebox, PhotoImage, filedialog, ttk
from tkcalendar import Calendar
import asyncio, datetime, os, subprocess, time

start_date = ''
end_date = ''
sensors_list = []

def parse_date(input_date):
    datey = parser.parse(input_date)
    formatted_date = datey.strftime('%Y-%m-%d')
    return(formatted_date)

def get_date_range():
    def set_range():
        start_date = start_calendar.get_date()
        end_date = end_calendar.get_date()
        print(start_date, end_date)
        date_popup.destroy()

    if is_custom_time.get() == 0:
        return
    today = datetime.date.today()
    date_popup = tk.Toplevel(root)
    date_popup.geometry("800x400")
    date_popup.title("Select Date Range")
    start_date_label = tk.Label(date_popup, text="Select start date:")
    end_date_label = tk.Label(date_popup, text="Select end date:")
    start_date_label.grid(column=0, row=0, padx=60, pady=40)
    end_date_label.grid(column=2, row=0, padx=80, pady=40)
    start_calendar = Calendar(date_popup,
        selectmode='day',
        year=today.year,
        month=today.month,
        day=today.day)
    start_calendar.grid(column=0, row=1, padx=60)
    end_calendar = Calendar(date_popup,
        selectmode='day',
        year=today.year,
        month=today.month,
        day=today.day)
    end_calendar.grid(column=2, row=1, padx=80)
    confirm_range_button = tk.Button(date_popup, text='Confirm', command=set_range)
    confirm_range_button.grid(column=1, row=2, pady=40)

def get_save_path():
    with open('save_path.conf', 'r') as file:
        return file.read() + "/ViiiivaOutput"

def set_save_path():
    directory = filedialog.askdirectory()
    if directory:
        with open('save_path.conf', 'w') as file:
            file.write(directory)
        save_path_label.config(text="Saving to: " + directory + "/ViiiivaOutput")

def erase():
    if not messagebox.askokcancel("Caution", "You will not be able to recover files from these sensors. Are you sure you want to continue?"):
        return
    erase_button['text'] = 'Erasing...'
    root.update()
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
        ls = subprocess.run('vivtool ls --uuid ' + sensor.uuid, shell=True, capture_output=True, text=True)
        ls_lines = ls.stdout.splitlines()
        for line in ls_lines:
            files_list.append(line)
        for item in files_list:
            subprocess.run('vivtool rm --uuid ' + sensor.uuid + " " + item, shell=True)
        erase_button['text'] = 'Erase Data'
        root.update()
        messagebox.showinfo("Done!", "Selected sensors now erased.")

def clock_sync():
    date_button['text'] = 'Syncing...'
    root.update()
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
    date_button['text'] = 'Sync Clocks'
    root.update()
    messagebox.showinfo("Done!", "Selected sensor clocks now synced.")

def get_data():
    if is_custom_time.get() == 0:
        on_select()
    elif is_custom_time.get() == 1:
        on_select(start_date, end_date)
    else:
        return

#  method used if custom date is selected
def on_select(init_start, init_end):
    pass

# method used if unspecified
def on_select():
    if get_save_path() == "Saving to: config required/ViiiivaOutput":
        messagebox.showwarning("Warning!", "Please set save path...")
        return
    if is_custom_time.get() == 1:
        print("now go to popup calendar")
        return
    confirm_button['text'] = 'Retrieving...'
    root.update()
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
        if not os.path.isdir(get_save_path() + "/" + sensor.id):
            print("creating " + get_save_path() + "/" + sensor.id)
            os.makedirs(get_save_path() + '/' + sensor.id)
            ls = subprocess.run('vivtool ls --uuid ' + sensor.uuid, shell=True, capture_output=True, text=True)
            ls_lines = ls.stdout.splitlines()
            for line in ls_lines:
                files_list.append(line)
            for item in files_list:
                print("    moving " + item + " to " + get_save_path() + "/" + sensor.id + "...")
                subprocess.run('vivtool cp --uuid ' + sensor.uuid + ' ' + item + ' \"' + get_save_path() + "/" + sensor.id + "\"", shell=True)
        else:
            print(get_save_path() + "/" + sensor.id + " already exists")
            ls = subprocess.run('vivtool ls --uuid ' + sensor.uuid, shell=True, capture_output=True, text=True)
            ls_lines = ls.stdout.splitlines()
            for line in ls_lines:
                files_list.append(line)
            for item in files_list:
                print("    moving " + item + " to " + get_save_path() + "/" + sensor.id + "...")
                subprocess.run('vivtool cp --uuid ' + sensor.uuid + ' ' + item + ' \"' + get_save_path() + "/" + sensor.id + "\"", shell=True)
    root.update()
    confirm_button['text'] = 'Get Data'
    messagebox.showinfo("Done!", "Success! Files located in " + get_save_path() + "...")

def get_sensors():
    scan_button['text'] = 'Scanning...'
    root.update()
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
        erase_button.config(state=tk.NORMAL)
        save_path_button.config(state=tk.NORMAL)
    else:
        listbox.insert(tk.END, "No sensors found...")
        listbox.insert(tk.END, "Is bluetooth on?")

    listbox.select_set(0, tk.END)
    messagebox.showinfo("Sensor Selection", "Use \'CTRL + click\' to deslect a sensor. Use \'CTRL + drag\' to select multiple sensors. All sensors are selected by default.")
    scan_button['text'] = 'Scan'

root = tk.Tk()
root.title("Select Sensors to Use")
root.geometry("800x800")

# Button to retrieve selected items
scan_button = tk.Button(root, text="Scan", command=get_sensors)
scan_button.pack(pady=20)

# Listbox to display sensors
listbox = tk.Listbox(root, selectmode=tk.EXTENDED)
listbox.pack(pady=20, padx=20)
listbox.insert(tk.END, "TIP: scan to find sensors")

save_path_button = tk.Button(root, text="Set Save Path", command=set_save_path, state=tk.DISABLED)
save_path_button.pack(pady=20)

save_path_label = tk.Label(root, text=get_save_path())
save_path_label.pack(pady=20)

is_custom_time = tk.IntVar()
toggle_custom_time = tk.Checkbutton(root,
    text="Specify custom date range?",
    variable = is_custom_time,
    onvalue=1,
    offvalue=0,
    command=get_date_range)
toggle_custom_time.pack(pady=20)

confirm_button = tk.Button(root, text="Get Data", command=on_select, state=tk.DISABLED)
confirm_button.pack(pady=20)

separator = ttk.Separator(root, orient='horizontal')
separator.pack(pady=5, fill='x')

date_button = tk.Button(root, text="Sync Clocks", command=clock_sync, state=tk.DISABLED)
date_button.pack(pady=20)

erase_button = tk.Button(root, text="Erase Data", command=erase, state=tk.DISABLED)
erase_button.pack(pady=20)

logo = PhotoImage(file='logo.png')
logo_label = tk.Label(image=logo)
logo_label.pack(side='right', padx=40)

root.mainloop()