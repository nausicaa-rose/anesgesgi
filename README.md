# anesgesgi 0.1

## Overview

`anesgesgi`, named after the Cherokee word for builder (ᎠᏁᏍᎨᏍᎩ),
is a utility for building out skeleton webpages/websites and
generating static websites.

`anesgesgi` builds sites configured with YAML files, with content
written in Markdown, and layout defined by Jinja2 templates.

`anesgesgi` is currently alpha-level software and is not recommended
for production use. For now, check out [Pelican][1] or [Nikola][2]
if your looking for a stable, Python-based static site generators.

## Usage

To build a site with or without a blog.
`anesgesgi build site <input dir> <output dir>`
To build a stand-alone blog or a blog that's part of a larger site.
`anesgesgi build blog <input dir> <output dir>`

To set up a site to be built with `anesgesgi`, you'll need to create
a `site.yml` file, a `blog.yml` file, if including a blog and Markdown
files with YAML headers.

`site.yml` must include:

    blog_active: yes
    blog_dir: blog
    template_dir: templates

Values for `blog_active` can be `yes` or `no`. `blog_dir` can be blank
if there is no blog or the blog directory is the same as the site's root
directory. `template_dir` shouldn't be blank and is relative to the root
source directory. It should not begin with a slash. Additional metadata
of any sort can be added to `site.yml` and it will be passed to page
templates.

`blog.yml` must include:

    url: blog
    template: blog_index.html
    max_posts: 6

`url` is the blog's directory and is relative to the site's root source
directory. It should not begin with a slash. `template` is the path to
the template that will be used to render the blog index. The path is
relative to the `site.yml` `template_dir` and should not begin with
a slash. `max_posts` is the number of posts to have per index page.
Additional metadata of any sort can be added to `blog.yml` and it will
be passed to page templates.

Page headers must include:

    slug: anesgesgi
    template: blog_post.html

and must end with three hyphens (`---`), so a simple web page or blog post
might look like:

    slug: firstpage
    template: basic.html
    ---
    # My first page

    This is my first page.

`slug` will be the name of the page. It will be combined with the extension
of the template used to render it, so in the above example, the page would
be `firstpage.html`. `template` is the path to the template used to render
the page. The path is relative to the template directory in `site.yml` and
should not begin with a slash. Additional metadata of any sort can be added
to the page header and it will be passed to page template.

[1]: https://blog.getpelican.com/
[2]: https://getnikola.com/