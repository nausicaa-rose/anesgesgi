import os
import shutil

from anesgesgi.build import build_page, parse_page, render_template, save_page
from anesgesgi.utils import load_yaml, get_ext
from anesgesgi.build.blog import build_blog

__name__ = "site"
__package__ = "anesgesi"


def build_site(input_dir, output_dir):
    """Build site.

    Loads the settings and metadata from the site.yml file in
    the root source directory, and iterates over the files in
    the source directory, converting Markdown files to HTML
    and copying other file types to the output directory.

    Parameters
    ----------
    input_dir : str
        A string containing the path to the input directory
        for the site being built.
    output_dir : str
        A string containing the path to the output directory
        for the site being built.

    Returns
    -------
    None
    """
    site_data = load_yaml(os.path.join(input_dir, "site.yml"))
    site_data["output_dir"] = output_dir
    site_data["input_dir"] = input_dir
    site_data["template_path"] = os.path.join(
        site_data["input_dir"], site_data["template_dir"]
    )
    page_dir_offset = len(input_dir) + 1
    for dir_path, _, file_names in os.walk(input_dir):
        site_data["page_dir"] = dir_path[page_dir_offset:]
        full_path = os.path.join(site_data["output_dir"], site_data["page_dir"])
        if not dir_path == site_data["template_path"]:
            if not os.path.exists(full_path):
                os.makedirs(full_path)

            if site_data["page_dir"] == site_data["blog_dir"]:
                if site_data["blog_active"]:
                    build_blog(input_dir, output_dir)
            elif (
                dir_path == site_data["template_dir"]
                or dir_path.endswith("site.yml")
                or dir_path.endswith("blog.yml")
            ):
                continue
            else:
                for file_name in file_names:
                    input_path = os.path.join(site_data["input_dir"], file_name)
                    full_path = os.path.join(
                        site_data["output_dir"], site_data["page_dir"], file_name
                    )
                    if os.path.isfile(input_path):
                        if input_path.endswith(".md"):
                            with open(input_path, "r", encoding="utf8") as fh:
                                page = fh.read()
                            build_page(site_data, page)
                        else:
                            shutil.copyfile(
                                os.path.join(dir_path, input_path), full_path
                            )
                    elif os.path.isdir(file_name):
                        os.makedirs(full_path)
