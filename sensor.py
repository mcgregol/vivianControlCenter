class Sensor:
    def __init__(self, id, name, uuid):
        self.id = id
        self.name = name
        self.uuid = uuid

    def list(self):
        return "Player Name: " + self.name + "\nDevice ID: " + self.id + "\nUUID: " + self.uuid
