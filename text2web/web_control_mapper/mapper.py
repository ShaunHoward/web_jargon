__author__ = 'shaun'
from os import path
from text2web.text_processor.text_processor import CMD, CMD_ARGS, CONTEXT, DEFAULT_ACTION_CONTEXT

DIR = path.dirname(path.dirname(__file__))
DEFAULT_ACTIONS_PATH = DIR + '/templates/action_call_templates.txt'


def create_web_actions(action_requests):
    """
    Creates the web action function calls using the
    action call templates.
    :param action_requests: the list of commands to turn into web action sequences
    :return:
    """

    for action_request in action_requests:
        # find the available web page controls as stored in a web control map template
        # these can be determined from the webpage context using words and their POS tags
        possible_actions = get_actions_in_webpage(action_request[CONTEXT])

        web_actions = []
        # search for web action requests in the sentence
        for action in possible_actions:
            action_split = action.split("_")
            count = 0
            for action_request in action_requests:
                for word in action_split:
                    if word in action_request:
                        count += 1
                if count == len(action_split):
                    web_actions.append((action_request, action))


def get_actions_in_webpage(context):
    actions = actions_in_context(context)
    return actions


def actions_in_context(context):
    """
    Load the actions for the specified context given action call
    template files for various websites that are well-known.
    By default, return the default available action list.
    :param context:
    :return:
    """
    action_template_mappings = {DEFAULT_ACTION_CONTEXT: DEFAULT_ACTIONS_PATH}
    if context in action_template_mappings.keys():
        available_actions_list = load_action_template(action_template_mappings[context])
    default_action_list = load_action_template(DEFAULT_ACTIONS_PATH)
    return default_action_list


def load_action_template(template_path):
    # read actions file
    with open(template_path, 'r') as f:
        actions_string = f.read()

    # determine each of the actions from string
    actions = actions_string.split('\n')

    # filter out comments from actions
    filtered_actions = []
    for action in actions:
        if not action.startswith("#"):
            filtered_actions.append(action)

    # create a map from token to action function call
    action_map = dict()
    for action in filtered_actions:
        # split up action token and function call parts
        toke_and_func = action.split(':')
        action_key = toke_and_func[0].strip()
        action_value = toke_and_func[1].strip()

        # strip <> and trailing whitespace from function call
        action_value = action_value.lstrip('<').rstrip('>').strip()
        if len(action_map[action_key]) == 0:
            action_map[action_key] = []
        action_map[action[0]].append(action_value)
    return action_map
