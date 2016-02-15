__author__ = 'shaun howard'
import unittest
from web_jargon import web_jargon as wj
from web_jargon.web_control_mapper.mapper import Mapper
from web_jargon.text_processor.text_processor import TextProcessor


class Text2WebText(unittest.TestCase):
    mapper = None
    processor = None

    def setUp(self):
        self.mapper = Mapper()
        self.processor = TextProcessor()

    def test_scroll_up_text2web(self):
        json_actions = wj.extract_web_actions("Scroll up in the current webpage.", self.processor, self.mapper)
        self.assertGreater(len(json_actions), 0)
        lower_actions = json_actions.lower()
        self.assertTrue("scroll" in lower_actions)
        self.assertTrue("up" in lower_actions)

    def test_scroll_down_text2web(self):
        json_actions = wj.extract_web_actions("Scroll down a page.", self.processor, self.mapper)
        self.assertGreater(len(json_actions), 0)
        lower_actions = json_actions.lower()
        self.assertTrue("scroll" in lower_actions)
        self.assertTrue("down" in lower_actions)

if __name__ == '__main__':
    unittest.main()
