from sensor import Sensor

dylan = Sensor("DL43", "Dylan Larkin", 543543543543543)

print("Player Name: " + dylan.get_name())
print("Device ID: " + dylan.get_id())
print("UUID: " + dylan.get_uuid())
