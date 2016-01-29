__author__ = 'shaun howard'

import os
import unittest
from text2web.text_processor import text_processor as tp
from text2web.web_control_mapper import mapper as mp

# TODO read in these functions from dict or something
SCROLL_UP = 'function scrollUp()'
SCROLL_DOWN = 'function scrollDown()'


class MapperTest(unittest.TestCase):

    def setUp(self):
        os.chdir('../text2web/')

    def test_scroll_updown_create_web_actions_simple(self):
        scroll_up = "Scroll up."
        scroll_down = "Scroll down."

        web_actions = mp.create_web_actions(tp.process_web_action_requests(scroll_up))
        self.assertEqual(len(web_actions), 1)
        self.assertEqual(web_actions[0], SCROLL_UP)

        web_actions = mp.create_web_actions(tp.process_web_action_requests(scroll_down))
        self.assertEqual(len(web_actions), 1)
        self.assertEqual(web_actions[0], SCROLL_DOWN)

    def test_scroll_updown_create_web_actions_medium(self):
        scroll_up = "Scroll up in the current webpage."
        scroll_down = "Scroll down on the page."

        web_actions = mp.create_web_actions(tp.process_web_action_requests(scroll_up))
        self.assertEqual(len(web_actions), 1)
        self.assertEqual(web_actions[0], SCROLL_UP)

        web_actions = mp.create_web_actions(tp.process_web_action_requests(scroll_down))
        self.assertEqual(len(web_actions), 1)
        self.assertEqual(web_actions[0], SCROLL_DOWN)
