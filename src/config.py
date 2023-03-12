import json
import logging
from json import JSONDecodeError

logger = logging.getLogger(__name__)


def load_config(path: str = "../appsettings.json"):
    dev_path = path.replace(".json", ".development.json")
    paths = [dev_path, path]

    for p in paths:
        try:
            with open(p, "r") as file:
                config = json.load(file)
                logger.info(f"Loaded configuration from file {p.split('/')[-1]}.")
                return config
        except JSONDecodeError:
            raise FileNotFoundError(f"Configuration file named {p.split('/')[-1]} can not be parsed.")
        except:
            logger.warning(f"Configuration file {p.split('/')[-1]} was not found, trying next one.")
            continue
    else:
        raise FileNotFoundError(f"Configuration file named {path.split('/')[-1]} was not found.")
