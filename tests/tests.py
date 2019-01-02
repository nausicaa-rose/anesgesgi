import filecmp
from os.path import exists
from shutil import rmtree
import unittest

from anesgesgi.utils import get_ext, load_yaml
from anesgesgi.build.blog import parse_page, render_template
from anesgesgi.build.site import build_site


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
    input_dir = "tests/test_site/src"
    output_dir = "tests/test_site/output"
    base_line = "tests/test_site/base_line"

    def _filecmp(self, file_path):
        return filecmp.cmp(
            f"{self.output_dir}/{file_path}",
            f"{self.base_line}/{file_path}",
            shallow=False,
        )

    def _delete_directory(self, dir_path):
        if exists(dir_path):
            rmtree(dir_path)

    def setUp(self):
        self._delete_directory(self.output_dir)

    def tearDown(self):
        self._delete_directory(self.output_dir)

    def test_build_site(self):
        build_site(self.input_dir, self.output_dir)
        self.assertTrue(self._filecmp("index.html"))
        self.assertTrue(self._filecmp("about.html"))
        self.assertTrue(self._filecmp("blog/index.html"))
        self.assertTrue(self._filecmp("blog/index1.html"))
        self.assertTrue(self._filecmp("blog/index2.html"))
        self.assertTrue(self._filecmp("blog/post1.html"))
        self.assertTrue(self._filecmp("blog/post2.html"))
        self.assertTrue(self._filecmp("blog/post3.html"))
        self.assertTrue(self._filecmp("blog/post4.html"))
        self.assertTrue(self._filecmp("blog/post5.html"))

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

    def test_render_template(self):
        site = {"lang": "en", "charset": "UTF-8", "blog": {"name": "Banana Blog"}}

        page = {
            "headline": "Banana",
            "page_html": "<h1>Banana</h1>\n<p>Bananas are a fruit.</p>",
        }

        template = "tests/test_template.html"

        render_template(template, site, page)
