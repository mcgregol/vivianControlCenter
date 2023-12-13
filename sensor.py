import asyncio
from bleak import BleakClient

class Sensor:
    def __init__(self, id, uuid):
        self.id = id
        self.uuid = uuid

    async def get_batt(self):
        try:
            BATTERY_SERVICE_UUID = "0000180f-0000-1000-8000-00805f9b34fb"
            BATTERY_LEVEL_CHARACTERISTIC_UUID = "00002a19-0000-1000-8000-00805f9b34fb"

            async with BleakClient(self.uuid) as client:
                if not client.is_connected:
                    raise Exception("Failed to connect to device")

                battery_level = await client.read_gatt_char(BATTERY_LEVEL_CHARACTERISTIC_UUID)
                return str(battery_level[0]) # Assuming battery level is a single byte 0-100%
        except:
            return "n/a"