import json

class ConfigLoad:

    @staticmethod
    def load_config() -> str:
        with open("./config/config.json") as config_file:
            data = json.load(config_file)
            MONGO_ENV = data["MONGO_DB_ENV"]

        return MONGO_ENV
