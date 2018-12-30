import unittest

from anesgesgi.utils import get_ext, load_yaml
from anesgesgi.build.blog import parse_page, render_template


class UtilsTests(unittest.TestCase):
    def test_get_ext(self):
        test_path = "test/path/to/page/page.md"
        self.assertEqual(get_ext(test_path), ".md")

    def test_load_yaml(self):
        test_yaml = "tests/test_yaml.yml"
        loaded_yaml = load_yaml(test_yaml)

        self.assertEqual(
            loaded_yaml,
            {"blog_active": True, "blog_dir": "blog", "template_dir": "templates"},
        )


class BuildTests(unittest.TestCase):
    def test_render_template(self):
        site = {"lang": "en", "charset": "UTF-8", "blog": {"name": "Banana Blog"}}

        page = {
            "headline": "Banana",
            "page_html": "<h1>Banana</h1>\n<p>Bananas are a fruit.</p>",
        }

        template = "tests/test_template.html"

        render_template(template, site, page)

    def test_parse_page(self):
        test_page = """headline: Banana
slug: banana
template: basic.html
---
# Banana

Bananas are a fruit.
"""

        parsed_page = parse_page(test_page)

        self.assertEqual(parsed_page["headline"], "Banana")
        self.assertEqual(parsed_page["slug"], "banana")
        self.assertEqual(parsed_page["template"], "basic.html")
        self.assertEqual(parsed_page["page_text"], "# Banana  Bananas are a fruit.")
        self.assertEqual(
            parsed_page["page_html"], "<h1>Banana</h1>\n<p>Bananas are a fruit.</p>"
        )
