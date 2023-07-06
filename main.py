from appJar import gui
import tkinter.filedialog

# creates and sets save_path variable to contents of save_path.txt
f = open("save-path.txt", "r")
save_path = f.read()

# updates startDate and endDate variables
def setDates():
    startDate = app.getDatePicker("dp1")
    endDate = app.getDatePicker("dp2")
    print(startDate, endDate)

# triggers updating of save_path variable
def press(setFilePath):
    save_path = tkinter.filedialog.askdirectory()
    with open('save-path.txt', 'w') as file:
        file.write(save_path)
    app.setLabel("file_path", "Saving to: " + "\'" + save_path + "\'")

app = gui("vivtoolFetch")

app.setBg("orange", override=True)
app.setOnTop(stay=True)

app.startLabelFrame("Beginning date of data")
app.addDatePicker("dp1")
app.stopLabelFrame()
app.startLabelFrame("Ending date of data")
app.addDatePicker("dp2")
app.stopLabelFrame()
app.setDatePickerRange("dp1", 2010, 2050)
app.setDatePickerRange("dp2", 2010, 2050)
app.setDatePicker("dp1")
app.setDatePicker("dp2")
app.addButton("Set Save Location", press)
app.addLabel("file_path", "Saving to: \'" + save_path + "\'")
app.addButton("Retrieve Data", setDates)

app.go()
