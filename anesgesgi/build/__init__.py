import os

from yaml import load as yaml_load

from jinja2 import Template
from markdown import markdown

from anesgesgi.utils import get_ext

__all__ = ["build_page", "parse_page", "render_template", "save_page", "blog", "site"]
__package__ = "anesgesgi"
__name__ = "build"


def build_page(site_data, page):
    """Build page.

    Loads the settings and metadata from the site.yml file in
    the root source directory, and iterates over the files in
    the source directory, converting Markdown files to HTML
    and copying other file types to the output directory.

    Parameters
    ----------
    site_data : dict
        Data from the site's site.yml file.
    page : str
        The contents of a Markdown file.

    Returns
    -------
    dict
        Page data.
    """
    page_data = parse_page(page)
    template = os.path.join(site_data["template_path"], page_data["template"])
    ext = get_ext(template)
    page = render_template(template, site_data, page_data)
    path = os.path.join(
        site_data["output_dir"], site_data["page_dir"], f"{page_data['slug']}{ext}"
    )
    save_page(page, path)

    return page_data


def parse_page(yaml_md):
    """Parse page string.

    Parse the content of a Markdown file by seperating
    the YAML header metadata and the Markdown page content.
    The YAML header is parsed into a dictionary, the 
    Markdown is rendered as HTML and both the original
    Markdown text and the rendered HTML to the dictionary
    and returns the dictionary.

    Parameters
    ----------
    yaml_md : str
        The contents of a Markdown file.

    Returns
    -------
    dict
        Data from a page's Markdown file.
    """
    yaml_, md = yaml_md.split("---")
    data = yaml_load(yaml_)
    data["page_text"], data["page_html"] = md.strip().replace("\n", " "), markdown(md)

    return data


def render_template(template, site_data, page_data):
    """Render template.

    Renders a Jinja2 template using site- and page-level data.

    Parameters
    ----------
    template : str
        The path to a Jinja2 template.
    site_data : dict
        Site-level data for the template.
    page_data : dict
        Page-level data for the template.

    Returns
    -------
    str
        A rendered template.
    """
    with open(template, "r", encoding="utf-8") as fh:
        temp = Template(fh.read(), trim_blocks=True, lstrip_blocks=True)

    return temp.render(site=site_data, page=page_data)


def save_page(page, path):
    """Save page.

    Saves a page to a given path.

    Parameters
    ----------
    page : str
        The page text to save.
    path : str
        The path to save the page to.

    Returns
    -------
    None
    """
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(page)
