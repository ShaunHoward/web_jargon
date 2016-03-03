__author__ = 'shaun'
from os import path

import helpers as h


CONTEXT = 'context'
DEFAULT_ACTION_CONTEXT = "default"
DIR = path.dirname(path.dirname(__file__))
DEFAULT_ACTIONS_PATH = DIR + '/templates/action_call_templates.txt'


# def insert_args_into_action_call(action_request, args, action_call):
#     # begin bracket of parameters
#     up_to_params = action_request.index("(")
#     before_params = action_request[:up_to_params+1]
#
#     # end bracket of parameters
#     after_params_ind = action_request.index(")")
#     after_params = action_request[after_params_ind-1:]
#
#     # get params and divide them by comma
#     params = action_request[up_to_params+2:after_params_ind-2]
#     if len(params) > 0:
#         param_list = params.split(",")
#         # clean up any preceding/trailing whitespace
#         param_list = [param.strip() for param in param_list]
#         # TODO: do something with params
#         action_call = ''.join([before_params, ', '.join(param_list), after_params])
#     else:
#         action_call = action_call[:len(action_call)-2]
#     return action_call


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
            action_call_template[h.CMD_ARGS] = action_request[h.CMD_ARGS]

            # append to web action call list
            web_actions.append(action_call_template)
        return web_actions