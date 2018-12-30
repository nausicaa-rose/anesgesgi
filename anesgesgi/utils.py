from yaml import load as yaml_load

__name__ = "utils"
__package__ = "anesgesgi"


def get_ext(path):
    """Get file extension.

    Finds a file's extension and returns it.

    Parameters
    ----------
    path : str
        The path to a file.

    Returns
    -------
    str
        The file extension including leading "."
    """
    return path[path.rfind(".") :]


def load_yaml(yf):
    """Load YAML file.

    Returns a parsed YAML file from a given path.

    Parameters
    ----------
    yf : str
        The path to a file.

    Returns
    -------
    dict
        The parsed YAML file.
    """
    with open(yf, "r", encoding="utf8") as fh:
        yf_content = fh.read()

    return yaml_load(yf_content)
