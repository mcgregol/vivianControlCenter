import tkinter as tk
from tkcalendar import DateEntry

def on_select_range():
	start_date = start_date_entry.get_date()
	end_date = end_date_entry.get_date()
	print(f"Selected Date Range: {start_date} to {end_date}")
	root.destroy()

root = tk.Tk()
root.title("Date Range Picker")

start_date_label = tk.Label(root, text="Start Date: ")
start_date_label.pack(pady=10)

start_date_entry = DateEntry(root)
start_date_label.pack(pady=10)

end_date_label = tk.Label(root, text="End Date: ")
end_date_label.pack(pady=10)

end_date_entry = DateEntry(root)
end_date_label.pack(pady=10)

select_button = tk.Button(root, text="Select Date Range", command=on_select_range)
select_button.pack(pady=20)

root.mainloop()