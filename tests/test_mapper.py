__author__ = 'shaun howard'

import os
import unittest
from text2web.text_processor import text_processor as tp


class MapperTest(unittest.TestCase):

    def setUp(self):
        os.chdir('../text2web/')

    def test_scroll_updown_create_web_actions_simple(self):
        scroll_up = "Scroll up."
        scroll_down = "Scroll down."

        web_actions = tp.process_web_action_requests(scroll_up)
        self.assertEqual(len(web_actions), 1)
        self.assertEqual(web_actions[0][tp.CMD], "Scroll up")

        web_actions = tp.process_web_action_requests(scroll_down)
        self.assertEqual(len(web_actions), 1)
        self.assertEqual(web_actions[0][tp.CMD], "Scroll down")

    def test_scroll_updown_create_web_actions_medium(self):
        scroll_up = "Scroll up in the current webpage."
        scroll_down = "Scroll down on the page."

        web_actions = tp.process_web_action_requests(scroll_up)
        self.assertEqual(len(web_actions), 1)
        self.assertTrue("Scroll" in web_actions[0][tp.CMD] and "up" in web_actions[0][tp.CMD])

        web_actions = tp.process_web_action_requests(scroll_down)
        self.assertEqual(len(web_actions), 1)
        self.assertTrue("Scroll" in web_actions[0][tp.CMD] and "down" in web_actions[0][tp.CMD])
