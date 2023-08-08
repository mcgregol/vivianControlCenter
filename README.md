# VivianControlCenter
A graphic user interface to easily transfer data from Viiiiva heart rate monitor to MacBook.

### WARNING: still in early stages of development

## Details
🚀 Presenting the Vivian Control Center! 🚀

Unlock the full potential of in-depth athletic analytics with Vivian Control Center, a groundbreaking tool designed specifically for managing 4iiii Viiiiva sensors worn by elite athletes.

The Vivian Control Center is not just an application - it's a revolution, leveraging the power of Python scripting to provide a seamless, powerful interface for sensor management and data collection.

🏋️ Unearth the depth of your performance, with insights from your sensor data! 🏋️‍♀️

The Vivian Control Center communicates directly with 4iiii Viiiiva sensors, extracting valuable real-time data and facilitating unprecedented insights into athlete performance.

🔑 Key Features:

1️⃣ Automated Sensor Scanning: The tool initiates a vivtool scan subprocess that automatically detects all active Viiiiva sensors in the vicinity. This is followed by an intelligent termination process that ensures no resource leakage, even with a large number of sensors.

2️⃣ Real-time Data Parsing: Vivian Control Center then interprets the raw byte data from each sensor scan, decoding and splitting it into a manageable format. It discards unnecessary information and extracts the essence - the sensor id and uuid, which are crucial for subsequent steps.

3️⃣ Smart Sensor Object Management: Our tool converts the parsed data into user-friendly Sensor objects. Each sensor is given a unique identity in the system with its id and uuid, creating a detailed sensor inventory for easy management.

4️⃣ Instant File Retrieval: Using each sensor's uuid, the application runs the vivtool ls --uuid command to list files associated with each sensor. This means you have immediate access to essential training data at your fingertips!

5️⃣ Seamless Data Export: Vivian Control Center goes a step further by offering an automated data export function. It copies the files associated with each sensor to a specific location of your choice for further analysis.

In the high-stakes world of athletic performance, every heartbeat counts. With Vivian Control Center, you can tap into the rhythm of your performance, translate raw sensor data into meaningful insights, and push beyond the boundaries of your potential.

Harness the power of data and elevate your performance with Vivian Control Center. The journey to peak performance begins here.

Note: The use of the Vivian Control Center requires a compatible 4iiii Viiiiva sensor.
