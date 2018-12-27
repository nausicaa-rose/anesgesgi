from yaml import load

__name__ = "utils"
__package__ = "anesgesgi"


def load_yaml(yf):
    with open(yf, "r", encoding="utf8") as fh:
        yf_content = fh.read()

    return load(yf_content)


def get_ext(path):
    return path[path.rfind(".") :]


def save_page(page, path):
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(page)
