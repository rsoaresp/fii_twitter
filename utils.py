from typing import Dict
import yaml


def config_loader(config_name: str) -> Dict[str, str]:
    with open(config_name) as file:
        return yaml.load(file, Loader=yaml.FullLoader)