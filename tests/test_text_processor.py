__author__ = 'shaun howard'
import os
import unittest
from web_jargon.text_processor import text_processor as tp


class TextProcessorTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_create_new_tab_process_web_action_requests_simple(self):
        create_tab = "Create a new tab."
        web_actions = tp.process_web_action_requests(create_tab)
        self.assertEqual(len(web_actions), 1)
        self.assertEqual(web_actions[0][tp.CMD], "Create tab")

    def test_close_tab_process_web_action_requests_simple(self):
        create_tab = "Close the third tab."
        web_actions = tp.process_web_action_requests(create_tab)
        self.assertEqual(len(web_actions), 1)
        self.assertEqual(web_actions[0][tp.CMD], "Close tab")
        self.assertEqual(web_actions[0][tp.CMD_ARGS], [3])

    def test_scroll_updown_process_web_action_requests_simple(self):
        scroll_up = "Scroll up."
        scroll_down = "Scroll down."

        web_actions = tp.process_web_action_requests(scroll_up)
        self.assertEqual(len(web_actions), 1)
        self.assertEqual(web_actions[0][tp.CMD], "Scroll up")

        web_actions = tp.process_web_action_requests(scroll_down)
        self.assertEqual(len(web_actions), 1)
        self.assertEqual(web_actions[0][tp.CMD], "Scroll down")

    def test_scroll_updown_process_web_action_requests_medium(self):
        scroll_up = "Scroll up in the current webpage."
        scroll_down = "Scroll down on the page."

        web_actions = tp.process_web_action_requests(scroll_up)
        self.assertEqual(len(web_actions), 1)
        self.assertTrue("Scroll" in web_actions[0][tp.CMD] and "up" in web_actions[0][tp.CMD])

        web_actions = tp.process_web_action_requests(scroll_down)
        self.assertEqual(len(web_actions), 1)
        self.assertTrue("Scroll" in web_actions[0][tp.CMD] and "down" in web_actions[0][tp.CMD])

    def test_scroll_leftright_process_web_action_requests(self):
        scroll_left = "Scroll left."
        scroll_right = "Scroll right."

        web_actions = tp.process_web_action_requests(scroll_left)
        self.assertEqual(len(web_actions), 1)
        self.assertEqual(web_actions[0][tp.CMD], "Scroll left")

        web_actions = tp.process_web_action_requests(scroll_right)
        self.assertEqual(len(web_actions), 1)
        self.assertEqual(web_actions[0][tp.CMD], "Scroll right")

    def test_scroll_leftright_process_web_action_requests_medium(self):
        scroll_left = "Scroll all the way left."
        scroll_right = "Scroll right all the way."

        web_actions = tp.process_web_action_requests(scroll_left)
        self.assertEqual(len(web_actions), 1)
        self.assertTrue("Scroll" in web_actions[0][tp.CMD] and "left" in web_actions[0][tp.CMD])

        web_actions = tp.process_web_action_requests(scroll_right)
        self.assertEqual(len(web_actions), 1)
        self.assertTrue("Scroll" in web_actions[0][tp.CMD] and "right" in web_actions[0][tp.CMD])


if __name__ == '__main__':
    unittest.main()