__author__ = 'shaun'
from os import path

import helpers as h


CONTEXT = 'context'
DEFAULT_ACTION_CONTEXT = "default"
DIR = path.dirname(path.dirname(__file__))
DEFAULT_ACTIONS_PATH = DIR + '/templates/action_call_templates.txt'


class Mapper():
    """
    The Mapper class maps action requests and arguments to action calls.
    Action calls are function calls that can be invoked by adding parentheses
    and the necessary function arguments. Many functions have default arguments
    set in the action call templates or action command templates files.
    For each action request sequence, a list of action call templates and parsed
    arguments are returned to the browser plugin.
    """
    action_call_map = dict()

    def __init__(self):
        self.action_call_map = h.load_web_action_template(DEFAULT_ACTIONS_PATH)

    def create_web_action(self, action_request):
        """
        Creates the web action function call using the
        action call templates.
        :param action_request: the command to turn into a web action sequence
        :return: a web action for the given web action request
        """
        web_actions = None
        if action_request is not None:
            # get correct web action call template
            action_call_template = self.action_call_map[action_request[h.CMD]].copy()

            # add arguments to action call
            action_call_template[h.CMD_ARGS_LIST] = []
            for arg_type in action_call_template[h.CMD_ARGS_DICT].keys():
                # try to match expected arguments in input text
                if arg_type in action_request[h.CMD_ARGS_DICT].keys():
                    value = action_request[h.CMD_ARGS_DICT][arg_type]
                    # set value if an actual arg value was given with the expected type
                    if value is not None:
                        action_call_template[h.CMD_ARGS_DICT][arg_type] = value
                        action_call_template[h.CMD_ARGS_LIST].append(value)
                else:
                    # use the default value for this argument type from the action call template
                    action_call_template[h.CMD_ARGS_LIST].append(action_call_template[h.CMD_ARGS_DICT][arg_type])
            # append to web action call list
            web_actions = action_call_template
        return web_actions