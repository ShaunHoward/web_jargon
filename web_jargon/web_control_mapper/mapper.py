__author__ = 'shaun'
from os import path

from web_jargon import helpers as h


CONTEXT = 'context'
DEFAULT_ACTION_CONTEXT = "default"
DIR = path.dirname(path.dirname(__file__))
DEFAULT_ACTIONS_PATH = DIR + '/templates/action_call_templates.txt'


def insert_args_into_action(args, action):
    # begin bracket of parameters
    up_to_params = action.index("(")
    before_params = action[:up_to_params+1]

    # end bracket of parameters
    after_params_ind = action.index(")")
    after_params = action[after_params_ind-1:]

    # get params and divide them by comma
    params = action[up_to_params+2:after_params_ind-2]
    action_call = action
    if len(params) > 0:
        param_list = params.split(",")
        # clean up any preceding/trailing whitespace
        param_list = [param.strip() for param in param_list]
        # TODO: do something with params
        action_call = ''.join([before_params, ', '.join(param_list), after_params])
    else:
        action_call = action_call[:len(action_call)-2]
    return action_call


# def get_actions_in_context(context):
#     """
#     Load the actions for the specified context given action call
#     template files for various websites that are well-known.
#     By default, return the default available action list.
#     :param context: the context of the web page to control
#     :return: a list of available actions in this context
#     """
#     action_template_mappings = {DEFAULT_ACTION_CONTEXT: DEFAULT_ACTIONS_PATH}
#     if context in action_template_mappings.keys():
#         # try to load a custom action mapping
#         action_map = load_action_template(action_template_mappings[context])
#     else:
#         # load the default action mappings by default
#         action_map = load_action_template(action_template_mappings[DEFAULT_ACTION_CONTEXT])
#     return action_map


class Mapper():
    action_map = dict()

    def __init__(self):
        self.action_map = h.load_web_action_template(DEFAULT_ACTIONS_PATH)

    def create_web_actions(self, action_requests):
        """
        Creates the web action function calls using the
        action call templates.
        :param action_requests: the list of commands to turn into web action sequences
        :return: a list of web actions for the given web action requests
        """
        web_actions = []
        for action_request in action_requests:
            # find the available web page controls as stored in a web control map template
            # these can be determined from the web page context using words and their POS tags
            # action_map = get_actions_in_context(action_request[CONTEXT])

            # search for the correct web action
            for action_key in self.action_map.keys():
                action_split = action_key.split("_")
                count = 0
                for word in action_split:
                    if word.lower() in action_request[h.CMD].lower():
                        count += 1
                if count == len(action_split):
                    args = ', '.join(action_request[h.CMD_ARGS])
                    web_action = insert_args_into_action(args, self.action_map[action_key][0])
                    web_actions.append(web_action)
        return web_actions