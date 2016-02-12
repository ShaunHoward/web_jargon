__author__ = 'shaun howard'
import unittest
from web_jargon import web_jargon as tw


class Text2WebText(unittest.TestCase):

    def setUp(self):
        pass

    def test_scroll_up_text2web(self):
        json_actions = tw.web_jargon("Scroll up in the current webpage.")
        self.assertGreater(len(json_actions), 0)
        lower_actions = json_actions.lower()
        self.assertTrue("scroll" in lower_actions)
        self.assertTrue("up" in lower_actions)

    def test_scroll_down_text2web(self):
        json_actions = tw.web_jargon("Scroll down a page.")
        self.assertGreater(len(json_actions), 0)
        lower_actions = json_actions.lower()
        self.assertTrue("scroll" in lower_actions)
        self.assertTrue("down" in lower_actions)

if __name__ == '__main__':
    unittest.main()
