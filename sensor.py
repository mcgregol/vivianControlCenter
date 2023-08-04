class Sensor:
    def __init__(self, id, uuid):
        self.id = id
        self.uuid = uuid

    def list(self):
        return "Sensor ID: " + self.id + "\nUUID: " + self.uuid