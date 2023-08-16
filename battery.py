import asyncio
from bleak import BleakClient

BATTERY_SERVICE_UUID = "0000180f-0000-1000-8000-00805f9b34fb"
BATTERY_LEVEL_CHARACTERISTIC_UUID = "00002a19-0000-1000-8000-00805f9b34fb"

async def get_battery_level(address):
    async with BleakClient(address) as client:
        if not client.is_connected:
            raise Exception("Failed to connect to device")

        battery_level = await client.read_gatt_char(BATTERY_LEVEL_CHARACTERISTIC_UUID)
        return battery_level[0]  # Assuming battery level is a single byte 0-100%

device_address = "1234"  # Replace with device's uuid

battery = asyncio.run(get_battery_level(device_address))
print(f"Device Battery Level: {battery}%")
