__author__ = 'shaun howard'
import os
import unittest
from text2web.text_processor import text_processor as tp


class TextProcessorTest(unittest.TestCase):

    def setUp(self):
        os.chdir('../text2web/')

    def test_scrollupdown_text2web(self):
        scroll_up = "Scroll up."
        scroll_down = "Scroll down."

        web_actions = tp.process_web_action_requests(scroll_up)
        self.assertEqual(len(web_actions), 1)
        self.assertEqual(web_actions[0][tp.CMD], "Scroll up")

        web_actions = tp.process_web_action_requests(scroll_down)
        self.assertEqual(len(web_actions), 1)
        self.assertEqual(web_actions[0][tp.CMD], "Scroll down")

if __name__ == '__main__':
    unittest.main()