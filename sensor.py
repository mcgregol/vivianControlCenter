class Sensor:
    def __init__(self, id, name, uuid):
        self.id = id
        self.name = name
        self.uuid = uuid

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_uuid(self):
        return str(self.uuid)
