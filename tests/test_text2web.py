__author__ = 'shaun howard'
import unittest
from text2web import text2web as tw


class Text2WebText(unittest.TestCase):

    def setUp(self):
        pass

    def test_scroll_up_text2web(self):
        json_actions = tw.text2web("Scroll up in the current webpage.")
        self.assertGreater(len(json_actions), 0)
        lower_actions = json_actions.lower()
        self.assertTrue("scroll" in lower_actions)
        self.assertTrue("up" in lower_actions)

    def test_scroll_down_text2web(self):
        json_actions = tw.text2web("Scroll down a page.")
        self.assertGreater(len(json_actions), 0)
        lower_actions = json_actions.lower()
        self.assertTrue("scroll" in lower_actions)
        self.assertTrue("down" in lower_actions)

if __name__ == '__main__':
    unittest.main()
