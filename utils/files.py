import tomllib
from datetime import datetime
from pathlib import Path


def read_configs(path: Path, service: str, theme: str, location: str):
    """
    Load the targets from a toml file.
    :return:
    """

    with open(path, "rb") as f:
        configs = tomllib.load(f)

    return configs[service][theme][location]


def path_builder(configs: dict, transaction: str, local=True):
    """
    Build the path for the file to be saved
    :param configs:
    :param local:
    :return:
    """
    if local:
        path = Path(
            configs[transaction]
            + f"/{configs['file_name']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{configs['extension']}"
        )
    else:
        path = Path(configs["transaction"])

    return path


def get_lattest_file(folder: Path) -> Path:
    """
    Get the latest file from the folder
    :param folder:
    :param parser_name:
    :param local:
    :return:
    """

    files = list(folder.glob("*"))

    if not files:
        return None

    return sorted(files, key=lambda x: x.stat().st_ctime, reverse=True)[0]
