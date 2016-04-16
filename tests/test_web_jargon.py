__author__ = 'shaun howard'
import unittest
import json

from os import path
from web_jargon import web_jargon as wj
from mapper import Mapper
from text_processor import TextProcessor
from web_jargon import helpers as h


DIR = path.dirname(__file__)
COMMAND_SAMPLES = DIR + '/data/action_command_samples.txt'


class WebJargonTest(unittest.TestCase):
    """
    Tests the overall Web Jargon back end in a functional way.
    Tests both the text processor and the mapper together in series.
    """
    mapper = None
    processor = None
    action_commands = None

    def setUp(self):
        self.mapper = Mapper()
        self.processor = TextProcessor()
        self.action_commands = h.load_action_command_samples(COMMAND_SAMPLES)

    def validate_web_actions(self, json_actions, action_key):
        # load json actions
        json_actions = json.loads(json_actions)
        print json_actions
        # assert one is returned
        self.assertEqual(len(json_actions), 2)
        self.assertEqual(len(json_actions[h.ACTION]), 4)
        action = json_actions[h.ACTION]
        print "returned action: " + action[h.CMD]
        print "desired action: " + action_key
        # assert the correct action token was interpreted
        self.assertEqual(action[h.CMD], action_key)
        # assert that the action returned matches the action it should be
        self.assertEqual(action[h.ACTION], self.mapper.action_call_map[action_key][h.ACTION])
        # assert that the arguments return are in fact provided in the response dictionary
        for arg in self.mapper.action_call_map[action_key][h.CMD_ARGS_DICT]:
            self.assertTrue(arg in action[h.CMD_ARGS_DICT].keys())

    def check_all_action_responses(self, action_key):
        """
        Runs through all sample action commands with arguments for the provided action key/token and validates
        that they return the correct action responses.
        :param action_key: the action token to test all the command samples for
        """
        possible_url = h.get_url_for_context(action_key)
        if len(self.action_commands[action_key]) > 0:
            # iterate through all possible action command samples
            for command in self.action_commands[action_key]:
                request_dict = {"command": command, "session_id": "ADFW#R$#$%$452354345345e23@#FSDFASFw3r",
                                "url": possible_url}
                # get the json action response and validate it
                json_actions = wj.extract_web_actions(request_dict, self.processor, self.mapper)
                print "checking: " + command
                self.validate_web_actions(json_actions, action_key)

    # test and assert all action requests are serviced correctly
    def test_all_actions(self):
        for action_key in self.action_commands.keys():
            self.check_all_action_responses(action_key)

if __name__ == '__main__':
    unittest.main()
