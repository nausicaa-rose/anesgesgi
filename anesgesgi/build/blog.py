from math import ceil
import os

from anesgesgi.build import build_page, parse_page, render_template, save_page
from anesgesgi.utils import load_yaml, get_ext

__name__ = "blog"
__package__ = "anesgesi"


def build_blog(input_dir, output_dir):
    """Build blog.

    Loads the settings and metadata from the site.yml file in
    the root source directory, and iterates over the files in
    the source directory, converting Markdown files to HTML
    and copying other file types to the output directory.

    Parameters
    ----------
    input_dir : str
        The path to the input directory for the blog being built.
    output_dir : str
        The path to the output directory for the blog being built.

    Returns
    -------
    None
    """
    posts = []
    site_data = load_yaml(os.path.join(input_dir, "site.yml"))
    site_data["output_dir"] = output_dir
    site_data["input_dir"] = input_dir
    site_data["blog_path"] = os.path.join(site_data["input_dir"], site_data["blog_dir"])
    site_data["page_dir"] = site_data["blog_dir"]
    site_data["template_path"] = os.path.join(
        site_data["input_dir"], site_data["template_dir"]
    )
    site_data["blog"] = load_yaml(os.path.join(site_data["blog_path"], "blog.yml"))
    for file_ in os.listdir(site_data["blog_path"]):
        if file_.endswith(".md"):
            with open(
                os.path.join(site_data["blog_path"], file_), "r", encoding="utf8"
            ) as fh:
                post = fh.read()
            posts.append(build_page(site_data, post))

    posts.sort(key=lambda post: post["datePublished"], reverse=True)

    build_indices(site_data, posts)


def build_indices(site_data, posts):
    """Build indices.

    Parameters
    ----------
    site_data : dict
        Site- and blog-level data.
    posts : list
        A list of dictionaries of page data.

    Returns
    -------
    None
    """
    site_data["blog"]["continue"] = None
    max_posts = site_data["blog"]["max_posts"]
    num_of_posts = len(posts)
    site_data["blog"]["num_of_indices"] = ceil(num_of_posts / max_posts)

    if num_of_posts > max_posts:
        index_num = 0
        for i in range(0, num_of_posts, max_posts):
            site_data["blog"]["continue"] = index_num
            index_num += 1
            build_index(site_data, posts[i : max_posts + i])
    else:
        build_index(site_data, posts)


def build_index(site_data, posts):
    """Build index.

    Builds an index page from the given site data and list
    of posts.

    Parameters
    ----------
    site_data : dict
        Site- and blog-level data.
    posts : list
        A list of dictionaries of page data.

    Returns
    -------
    None
    """
    template = os.path.join(site_data["template_path"], site_data["blog"]["template"])
    ext = get_ext(template)
    page = render_template(template, site_data, posts)
    if not site_data["blog"]["continue"] or site_data["blog"]["continue"] == 0:
        path = os.path.join(
            site_data["output_dir"], site_data["blog_dir"], f"index{ext}"
        )
    else:
        path = os.path.join(
            site_data["output_dir"],
            site_data["blog_dir"],
            f"index{site_data['blog']['continue']}{ext}",
        )
    save_page(page, path)
