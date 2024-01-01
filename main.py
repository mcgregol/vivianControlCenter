import tkinter as tk
from sensor import Sensor
from tkinter import ttk, messagebox, PhotoImage, filedialog, ttk
from tkcalendar import Calendar
import asyncio, os, subprocess, time
from datetime import datetime

start_date = ''
end_date = ''
sensors_list = []

def set_date_range():
    def set_range():
        global start_date, end_date
        start_date = start_calendar.get_date()
        end_date = end_calendar.get_date()
        print(start_date, end_date)
        date_popup.destroy()

    if is_custom_time.get() == 0:
        return
    today = datetime.today().date()
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

    progress_popup = tk.Toplevel(root)
    progress_popup.geometry("400x250")
    progress_popup.title("Clearing files...")
    #  eventually add sensor id here instead of static text
    current_label = tk.Label(progress_popup, text='Current sensor')
    current_var = tk.IntVar()
    current_bar = ttk.Progressbar(progress_popup,
        variable=current_var,
        mode='determinate',
        maximum=200,
        length=300)
    total_label = tk.Label(progress_popup, text='Total')
    total_var = tk.IntVar()
    #  need to move this to access file_list
    total_bar = ttk.Progressbar(progress_popup,
        variable=total_var,
        mode='determinate',
        maximum=len(selected_sensors),
        length=300)

    current_label.pack(side='top', pady=20)
    current_bar.pack(side='top')
    total_bar.pack(side='bottom', pady=20)
    total_label.pack(side='bottom')

    # Fetch files from the each sensor
    for sensor in selected_sensors:
        current_label.config(text=sensor.id)
        current_var.set(0)
        progress_popup.update()

        files_list = []
        ls = subprocess.run('./vivtool ls --uuid ' + sensor.uuid, shell=True, capture_output=True, text=True)
        ls_lines = ls.stdout.splitlines()
        for line in ls_lines:
            files_list.append(line)
            current_bar['maximum'] = len(files_list)
        for item in files_list:
            subprocess.run('./vivtool rm --uuid ' + sensor.uuid + " " + item, shell=True)
            current_var.set(current_var.get() + 1)
            progress_popup.update()
        total_var.set(total_var.get() + 1)
        progress_popup.update()
    progress_popup.destroy()
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
        date = subprocess.run('./vivtool date -h -s now --uuid ' + sensor.uuid, shell=True)
    date_button['text'] = 'Sync Clocks'
    root.update()
    messagebox.showinfo("Done!", "Selected sensor clocks now synced.")

def get_data():
    global start_date, end_date
    run_export(start_date, end_date)

#  checks if checkbox is ticked inside method and condensed so only one is needed
#  if is_custom_time.get() == 1 then check if in date range
def run_export(init_start, init_end):
    #  takes ISO 8601 format and returns normal
    def parse_date(input_date):
        parsed_date = datetime.fromisoformat(input_date)
        formatted_date = parsed_date.strftime('%m/%d/%y')
        return formatted_date

    def check_size(input_size):
        try:
            #  convert bytes to kb
            if (input_size / 1000) >= int(min_filesize_sp.get()):
                return True
            else:
                return False
        except:
            return True

    def check_date(input_date):
        #  convert strings to datetime objects
        mod_input_date = datetime.fromisoformat(input_date)
        mod_input_date_str = datetime.strftime(mod_input_date, '%m/%d/%y')
        input_date_obj = datetime.strptime(mod_input_date_str, '%m/%d/%y')
        start_date_obj = datetime.strptime(init_start, '%m/%d/%y')
        end_date_obj = datetime.strptime(init_end, '%m/%d/%y')

        #  returns True if date is within range
        print(datetime.strftime)
        return start_date_obj <= input_date_obj <= end_date_obj

    if get_save_path() == "Saving to: config required/ViiiivaOutput":
        messagebox.showwarning("Warning!", "Please set save path...")
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

    progress_popup = tk.Toplevel(root)
    progress_popup.geometry("400x250")
    progress_popup.title("Transferring data...")
    #  eventually add sensor id here instead of static text
    current_label = tk.Label(progress_popup, text='Current sensor')
    current_var = tk.IntVar()
    current_bar = ttk.Progressbar(progress_popup,
        variable=current_var,
        mode='determinate',
        maximum=200,
        length=300)
    total_label = tk.Label(progress_popup, text='Total')
    total_var = tk.IntVar()
    #  need to move this to access file_list
    total_bar = ttk.Progressbar(progress_popup,
        variable=total_var,
        mode='determinate',
        maximum=len(selected_sensors),
        length=300)

    current_label.pack(side='top', pady=20)
    current_bar.pack(side='top')
    total_bar.pack(side='bottom', pady=20)
    total_label.pack(side='bottom')

    # Fetch files from the each sensor
    for sensor in selected_sensors:
        current_label.config(text=sensor.id)
        current_var.set(0)
        progress_popup.update()

        file_list = []
        if not os.path.isdir(get_save_path() + "/" + sensor.id):
            print("creating " + get_save_path() + "/" + sensor.id)
            os.makedirs(get_save_path() + '/' + sensor.id)
            ls = subprocess.run('./vivtool ls -l --uuid ' + sensor.uuid, shell=True, capture_output=True, text=True)
            lines = ls.stdout.splitlines()
            for line in lines:
                parts = line.split()
                if len(parts) == 3:
                    file_info = {
                        "file_size": int(parts[0]),
                        "timestamp": parse_date(parts[1]),
                        "filename": parts[2]
                    }
                    file_list.append(file_info)
            current_bar['maximum'] = len(file_list)
            for file_info in file_list:
                if check_size(file_info['file_size']):
                    if is_custom_time.get() == 1:
                        if check_date(file_info["timestamp"]):         
                            print("    moving " + file_info["filename"] + " to " + get_save_path() + "/" + sensor.id + "...")
                            subprocess.run('./vivtool cp --uuid ' + sensor.uuid + ' ' + file_info["filename"] + ' \"' + get_save_path() + "/" + sensor.id + "\"", shell=True)
                    else:
                        print("    moving " + file_info["filename"] + " to " + get_save_path() + "/" + sensor.id + "...")
                        subprocess.run('./vivtool cp --uuid ' + sensor.uuid + ' ' + file_info["filename"] + ' \"' + get_save_path() + "/" + sensor.id + "\"", shell=True)
                current_var.set(current_var.get() + 1)
                progress_popup.update()
        else:
            print(get_save_path() + "/" + sensor.id + " already exists")
            ls = subprocess.run('./vivtool ls -l --uuid ' + sensor.uuid, shell=True, capture_output=True, text=True)
            lines = ls.stdout.splitlines()
            for line in lines:
                parts = line.split()
                if len(parts) == 3:
                    file_info = {
                        "file_size": int(parts[0]),
                        "timestamp": parts[1],
                        "filename": parts[2]
                    }
                    file_list.append(file_info)
            current_bar['maximum'] = len(file_list)
            for file_info in file_list:
                if check_size(file_info['file_size']):
                    if is_custom_time.get() == 1:
                        if check_date(file_info["timestamp"]):
                            print("    moving " + file_info["filename"] + " to " + get_save_path() + "/" + sensor.id + "...")
                            subprocess.run('./vivtool cp --uuid ' + sensor.uuid + ' ' + file_info["filename"] + ' \"' + get_save_path() + "/" + sensor.id + "\"", shell=True)
                    else:
                        print("    moving " + file_info["filename"] + " to " + get_save_path() + "/" + sensor.id + "...")
                        subprocess.run('./vivtool cp --uuid ' + sensor.uuid + ' ' + file_info["filename"] + ' \"' + get_save_path() + "/" + sensor.id + "\"", shell=True)
                current_var.set(current_var.get() + 1)
                progress_popup.update()
        total_var.set(total_var.get() + 1)
        progress_popup.update()

    root.update()
    confirm_button['text'] = 'Get Data'
    messagebox.showinfo("Done!", "Success! Files located in " + get_save_path() + "...")
    progress_popup.destroy()

def get_sensors():
    #  free up some oh-so-good memory
    if sensors_list:
        for sensor in sensors_list:
            sensors_list.remove(sensor)
            del sensor
    scan_button['text'] = 'Scanning...'
    listbox.delete(0, tk.END)  # Clear the current Listbox items
    root.update()

    # Start 'vivtool scan' as a subprocess
    scan = subprocess.Popen('./vivtool scan', shell=True, stdout=subprocess.PIPE)

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
        key, value = line.split(maxsplit=1)
        dictionary[key] = value

    for key, value in dictionary.items():
        key = key[1:-1]
        value = value[1:-1]
        new_sensor = Sensor(key, value)

        #  check for repeats
        existing_sensor = next((sensor for sensor in sensors_list if sensor.id == new_sensor.id), None)
        if not existing_sensor:
            sensors_list.append(new_sensor)

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

is_custom_time = tk.IntVar()
toggle_custom_time = tk.Checkbutton(root,
    text="Specify custom date range?",
    variable = is_custom_time,
    onvalue=1,
    offvalue=0,
    command=set_date_range)
toggle_custom_time.pack(pady=10)

min_filesize_label = tk.Label(root, text="Min filesize filter (kb)\n0 for none")
min_filesize_label.pack()

min_filesize_sp = tk.Spinbox(root, value=0, from_=0)
min_filesize_sp.pack()

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
save_path_label.pack(pady=10)

confirm_button = tk.Button(root, text="Get Data", command=get_data, state=tk.DISABLED)
confirm_button.pack(pady=20)

separator = ttk.Separator(root, orient='horizontal')
separator.pack(pady=5, fill='x')

date_button = tk.Button(root, text="Sync Clocks", command=clock_sync, state=tk.DISABLED)
date_button.pack(pady=20)

erase_button = tk.Button(root, text="Erase Data", command=erase, state=tk.DISABLED)
erase_button.pack(pady=10)

logo = PhotoImage(file='logo.png')
logo_label = tk.Label(image=logo)
logo_label.pack(side='right', padx=40)

root.mainloop()