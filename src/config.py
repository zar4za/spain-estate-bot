import json


def load_config(path: str):
    dev_path = path.replace(".json", ".development.json")
    paths = [dev_path, path]

    for p in paths:
        try:
            with open(p, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            continue
    else:
        raise FileNotFoundError("A configuration file named appsettings.json was not found")
