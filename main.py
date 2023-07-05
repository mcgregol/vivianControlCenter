from appJar import gui

def setDates():
    startDate = app.getDatePicker("dp1")
    endDate = app.getDatePicker("dp2")
    print(startDate, endDate)

app = gui()

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
app.addButton("Retrieve Data", setDates)

app.go()
