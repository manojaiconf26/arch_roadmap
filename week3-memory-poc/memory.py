import json


class SharedMemory:
    def __init__(self):
        self.store = {}

    def read(self, key):
        return self.store.get(key)

    def write(self, key, value):
        self.store[key] = value
        print(f"SharedMemory stored: {key}")

    def dump(self):
        return self.store


class LongTermMemory:
    def __init__(self, file_path="long_term_memory.json"):
        self.file_path = file_path
        try:
            with open(self.file_path, "r") as f:
                self.store = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.store = {}

    def read(self, key):
        return self.store.get(key)

    def write(self, key, value):
        self.store[key] = value
        with open(self.file_path, "w") as f:
            json.dump(self.store, f, indent=2)
        print(f"LongTermMemory stored: {key}")
