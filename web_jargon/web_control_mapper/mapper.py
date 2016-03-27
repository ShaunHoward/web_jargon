__author__ = 'shaun'
from os import path

import web_jargon.helpers as h


CONTEXT = 'context'
DEFAULT_ACTION_CONTEXT = "default"
DIR = path.dirname(path.dirname(__file__))
DEFAULT_ACTIONS_PATH = DIR + '/templates/action_call_templates.txt'


class Mapper():
    action_call_map = dict()

    def __init__(self):
        self.action_call_map = h.load_web_action_template(DEFAULT_ACTIONS_PATH)

    def create_web_actions(self, action_requests):
        """
        Creates the web action function calls using the
        action call templates.
        :param action_requests: the list of commands to turn into web action sequences
        :return: a list of web actions for the given web action requests
        """
        web_actions = []
        for action_request in action_requests:

            # get correct web action call template
            action_call_template = self.action_call_map[action_request[h.CMD]]

            # add arguments to action call
            action_call_template[h.CMD_ARGS_DICT] = action_request[h.CMD_ARGS_DICT]
            action_call_template[h.CMD_ARGS_LIST] =\
                [action_request[h.CMD_ARGS_DICT][x] for x in action_request[h.CMD_ARGS_DICT].keys()]

            # append to web action call list
            web_actions.append(action_call_template)
        return web_actions