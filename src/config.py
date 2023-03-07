import json
from json import JSONDecodeError


def load_config(path: str = "../appsettings.json"):
    dev_path = path.replace(".json", ".development.json")
    paths = [dev_path, path]

    for p in paths:
        try:
            with open(p, "r") as file:
                config = json.load(file)
                print(f"Loaded config {p.split('/')[-1]}")
                return config
        except JSONDecodeError:
            raise FileNotFoundError(f"A configuration file named {p.split('/')[-1]} can not be parsed.")
        except:
            continue
    else:
        raise FileNotFoundError(f"A configuration file named {path.split('/')[-1]} was not found")
