from math import ceil
import os

from jinja2 import Template
from markdown import markdown
from yaml import load as yaml_load

from anesgesgi.utils import load_yaml, get_ext, save_page

__name__ = 'blog'
__package__ = 'anesgesi'

def build_blog(input_dir, output_dir):
    """Build blog.

    Loads the settings and metadata from the site.yml file in
    the root source directory, and iterates over the files in
    the source directory, converting Markdown files to HTML
    and copying other file types to the output directory.

    Parameters
    ----------
    input_dir : str
        A string containing the path to the input directory
        for the blog being built.
    output_dir : str
        A string containing the path to the output directory
        for the blog being built.

    Returns
    -------
    Nothing.
    """
    posts = []
    site_data = load_yaml(os.path.join(input_dir, 'site.yml'))
    site_data['output_dir'] = output_dir
    site_data['input_dir'] = input_dir
    site_data['blog_path'] = os.path.join(site_data['input_dir'], site_data['blog_dir'])
    site_data['template_path'] = os.path.join(site_data['input_dir'], site_data['template_dir'])
    blog_data = load_yaml(os.path.join(site_data['blog_path'], 'blog.yml'))
    for file_ in os.listdir(site_data['blog_path']):
        if file_.endswith('.md'):
            with open(os.path.join(site_data['blog_path'], file_), 'r', encoding='utf8') as fh:
                post = fh.read()
            posts.append(build_post(site_data, blog_data, post))

    posts.sort(key=lambda post: post['datePublished'], reverse=True)

    build_indices(site_data, blog_data, posts)


def build_indices(site_data, blog_data, posts):
    blog_data['continue'] = False
    max_posts = blog_data['max_posts']
    num_of_posts = len(posts)
    num_of_indices = ceil(num_of_posts / max_posts)
    
    build_index(site_data, blog_data, posts)

    if num_of_indices > 1:
        for i in range(1, num_of_indices):
            blog_data['continue'] = i
            build_index(site_data, blog_data, posts[max_posts * i + 1:])

        
def build_index(site_data, blog_data, posts):
    template = os.path.join(site_data['template_path'], blog_data['template'])
    ext = get_ext(template)
    page = render_template(template, site_data, blog_data, posts)
    if blog_data['continue']:
        path = os.path.join(site_data['output_dir'], site_data['blog_dir'], 
                            f"index{blog_data['continue']}{ext}")
    else:
        path = os.path.join(site_data['output_dir'], site_data['blog_dir'], f"index{ext}")
    save_page(page, path)


def build_post(site_data, blog_data, blogpost):
    """Build post.

    Loads the settings and metadata from the site.yml file in
    the root source directory, and iterates over the files in
    the source directory, converting Markdown files to HTML
    and copying other file types to the output directory.

    Parameters
    ----------
    site_data : dict
        A dictionary built from the site's site.yml file.
    blog_data : dict
        A dictionary built from the site's blog.yml file.
    blogpost : str
        A string containing the contents of a Markdown file.

    Returns
    -------
    Nothing.
    """
    post_data = parse_post(blogpost)
    template = os.path.join(site_data['template_path'], post_data['template'])
    ext = get_ext(template)
    page = render_template(template, site_data, blog_data, post_data)
    path = os.path.join(site_data['output_dir'], site_data['blog_dir'], f"{post_data['slug']}{ext}")
    save_page(page, path)

    return post_data


def render_template(template, site_data, blog_data, post_data):
    """Render template.

    Renders a Jinja2 template using site- and page-level data.

    Parameters
    ----------
    template : str
        A string containing the path to a Jinja2 template.
    site_data : dict
        A dictionary containing site-level data for the
        template.
    blog_data : dict
        A dictionary built from the site's blog.yml file.
    post_data : dict
        A dictionary containing page-level data for the
        template.

    Returns
    -------
    str
        A rendered template.
    """
    with open(template, 'r', encoding='utf-8') as fh:
        temp = Template(fh.read())

    return temp.render(site=site_data, blog=blog_data, post=post_data)


def parse_post(yaml_md):
    yaml_, md = yaml_md.split('---')
    data = yaml_load(yaml_)
    data['post_text'], data['post_html'] = md.replace("\n", " "), markdown(md)

    return data

