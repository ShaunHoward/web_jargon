__author__ = 'Shaun Howard'

import unittest

from text2web.text_processor import text_processor

good_web_commands = ["Navigate to my Facebook friends and search for John Doe",
                     "Find the article named Web Jargon API docs on the Web Jargon homepage"]
bad_web_commands = ["Get me pizza",
                    "Look for my spouse in the honors list"]

success_statuses = {text_processor.SUCCESS}
failure_statuses = {text_processor.FAIL}


class TextProcessorTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_parse_good_input(self):
        for test_command in good_web_commands:
            controls, status = text_processor.parse_web_commands(test_command)
            self.validate_controls(controls)
            self.assertTrue(status in success_statuses)

    def test_parse_bad_input(self):
        for test_command in bad_web_commands:
            controls, status = text_processor.parse_web_commands(test_command)
            self.assertEqual(len(controls), 0)
            self.assertTrue(status in failure_statuses)

    def validate_controls(self, controls):
        """
        Checks that the provided controls list are valid controls.
        :param controls: the controls list
        """
        self.assertGreater(len(controls), 0)
        for control in controls:
            self.assertEqual(type(control), str)
            self.assertGreater(len(control), 0)


if __name__ == '__main__':
    unittest.main()
