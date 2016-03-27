__author__ = 'shaun howard'
import unittest

from os import path
import json

from web_jargon import web_jargon as wj
from web_jargon.web_control_mapper.mapper import Mapper
from web_jargon.text_processor.text_processor import TextProcessor
from web_jargon import helpers as h


DIR = path.dirname(__file__)
COMMAND_SAMPLES = DIR + '/data/action_command_samples.txt'


class WebJargonTest(unittest.TestCase):
    mapper = None
    processor = None
    action_commands = None

    def setUp(self):
        self.mapper = Mapper()
        self.processor = TextProcessor()
        self.action_commands = h.load_action_command_samples(COMMAND_SAMPLES)

    def validate_web_actions(self, json_actions, action_key):
        json_actions = json.loads(json_actions)
        self.assertEqual(len(json_actions), 1)
        self.assertEqual(len(json_actions[h.ACTIONS]), 1)
        action = json_actions[h.ACTIONS][0]
        print "returned action: " + action[h.CMD]
        print "desired action: " + action_key
        self.assertEqual(action[h.CMD], action_key)
        self.assertEqual(action[h.ACTION], self.mapper.action_call_map[action_key][h.ACTION])
        for arg in self.mapper.action_call_map[action_key][h.CMD_ARGS]:
            self.assertTrue(arg in action[h.CMD_ARGS].keys())

    def check_all_action_responses(self, action_key):
        if len(self.action_commands[action_key]) > 0:
            for command in self.action_commands[action_key]:
                json_actions = wj.extract_web_actions(command, self.processor, self.mapper)
                print "checking: " + command
                self.validate_web_actions(json_actions, action_key)

    # check all actions
    def test_all_actions(self):
        for action_key in self.action_commands.keys():
            self.check_all_action_responses(action_key)

if __name__ == '__main__':
    unittest.main()
