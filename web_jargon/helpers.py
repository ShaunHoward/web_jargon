__author__ = 'Shaun Howard'

from os import path
from collections import OrderedDict as dict
ACTION = 'action'
CMD = 'command'
CMD_ARGS_DICT = 'arguments'
CMD_ARGS_LIST = 'arg_list'
PARTS = 'parts'
LPAREN = "("
RPAREN = ")"

# action tokens
SCROLL_UP = 'SCROLL_UP'
SCROLL_DOWN = 'SCROLL_DOWN'
SCROLL_LEFT = 'SCROLL_LEFT'
SCROLL_RIGHT = 'SCROLL_RIGHT'
ZOOM_IN = 'ZOOM_IN'
ZOOM_OUT = 'ZOOM_OUT'
OPEN_TAB = 'OPEN_TAB'
CLOSE_TAB = 'CLOSE_TAB'
SWITCH_TAB = 'SWITCH_TAB'
FORWARD = 'FORWARD'
BACKWARD = 'BACKWARD'
REFRESH = 'REFRESH'
CLICK = 'CLICK'
OPEN_URL = 'OPEN_URL'
SELECT_ELEMENT = 'SELECT_ELEMENT'
ENTER_TEXT = 'ENTER_TEXT'
SUBMIT_TEXT = 'SUBMIT_TEXT'
ENTER_AND_SUBMIT = 'ENTER_AND_SUBMIT'
OPEN_HELP = 'OPEN_HELP'
CLOSE_HELP = 'CLOSE_HELP'
OPEN_CHEAT_SHEET = 'OPEN_CHEAT_SHEET'
CLOSE_CHEAT_SHEET = 'CLOSE_CHEAT_SHEET'
OPEN_SETUP_PAGE = 'OPEN_SETUP_PAGE'
CLOSE_SETUP_PAGE = 'CLOSE_SETUP_PAGE'
START_VIDEO = 'START_VIDEO'
STOP_VIDEO = 'STOP_VIDEO'
NEXT_VIDEO = 'NEXT_VIDEO'
OPEN_FULLSCREEN = 'OPEN_FULLSCREEN'
CLOSE_FULLSCREEN = 'CLOSE_FULLSCREEN'
START_MUSIC = 'START_MUSIC'
STOP_MUSIC = 'STOP_MUSIC'
NEXT_SONG = 'NEXT_SONG'
SEARCH_MUSIC = 'SEARCH_MUSIC'
SEARCH_PDF = 'SEARCH_PDF'
GO_TO_PDF_PAGE = 'GO_TO_PDF_PAGE'

DIR = path.dirname(path.dirname(__file__))
DEFAULT_ACTIONS_PATH = DIR + '/templates/action_command_templates.txt'

VIDEO_CONTEXT = {START_VIDEO, STOP_VIDEO, NEXT_VIDEO, OPEN_FULLSCREEN, CLOSE_FULLSCREEN}
MUSIC_CONTEXT = {START_MUSIC, STOP_MUSIC, NEXT_SONG, SEARCH_MUSIC}
DOC_CONTEXT = {SEARCH_PDF, GO_TO_PDF_PAGE}


def log(text_list):
    print ''.join(text_list)


def load_action_token_list(template_path):
    # read actions file
    with open(template_path, 'r') as f:
        actions_string = f.read()

    # determine each of the actions from string
    actions = actions_string.split('\n')

    # filter out comments from actions
    filtered_actions = []
    for action in actions:
        action = action.strip()
        if not action.startswith("#") and len(action) > 3:
            filtered_actions.append(action)

    # create a list of action tokens
    action_token_list = []
    for action in filtered_actions:
        # split up action token and function call parts
        toke_and_func = action.split(':')
        action_token_list.append(toke_and_func[0].strip())


def get_action_keys_and_values(template_path):
    # read actions file
    with open(template_path, 'r') as f:
        actions_string = f.read()

    # determine each of the actions from string
    actions = actions_string.split('\n')

    # filter out comments from actions
    filtered_actions = []
    for action in actions:
        action = action.strip()
        if not action.startswith("#") and len(action) > 3:
            filtered_actions.append(action)

    action_map = dict()
    # create a map from token to action list sequence
    for action in filtered_actions:
        # split up action token and function or list parts
        toke_and_func = action.split(':')
        action_key = toke_and_func[0].strip()
        action_value = toke_and_func[1].strip()
        if len(action_key) > 0 and len(action_value) > 0:
            # strip [] and trailing whitespace from list
            action_value = action_value.lstrip('[').rstrip(']').strip()
            if len(action_value) > 0:
                action_map[action_key] = action_value
    return action_map


def load_web_action_template(template_path, action_call=True):
    """
    Generate an action template for creating action sequences.
    :param template_path: the path of the action call or command template file.
    :return: the action template map, ready to use and fill in
    """
    action_keys_and_vals = get_action_keys_and_values(template_path)
    action_map = dict()
    for action_key in action_keys_and_vals.keys():
        action_value = action_keys_and_vals[action_key]
        # run action call template parser
        if action_call:
            # separate functions from arguments
            l_paren_index = action_value.index(LPAREN)
            action_args = action_value[l_paren_index:]
            action_value = action_value[:l_paren_index]

            # parse arguments into a list template
            action_args_dict = parse_arguments(action_args)

            # create the action call template as a dictionary with command and arguments
            if action_key not in action_map.keys():
                action_map[action_key] = dict()

            # store the action and the arguments to it
            action_map[action_key][CMD_ARGS_DICT] = action_args_dict
            action_map[action_key][CMD] = action_key
            action_map[action_key][ACTION] = action_value
        else:
            # run action command template parser
            # split values on commas
            utterances = action_value.split(",")

            # clean up whitespace
            utterances = [x.strip() for x in utterances if len(x.strip()) > 0]

            # strip off quotes
            utterances = [x[1:len(x)-1] for x in utterances]
            # create the action command template as a dictionary with command and arguments
            if action_key not in action_map.keys():
                action_map[action_key] = []
            for u in utterances:
                # construct an utterance template
                u_map = dict()
                u_map[CMD] = u
                u_map[PARTS] = []
                u_map[CMD_ARGS_DICT] = dict()

                # split on rparen for arguments
                s = u.split("(")
                u_map[PARTS].append(s[0].strip().lower())

                # extract necessary argument fields
                if len(s) > 1:
                    # already stored the first element
                    s = s[1:]
                    # pull out all arguments
                    for st in s:
                        strs = st.split(")")

                        # extract default values
                        arg = strs[0].strip()
                        split_arg = arg.split("=")

                        # add the argument and default value to the dictionary
                        if len(split_arg) > 1:
                            val = split_arg[1]
                            # try to parse a number
                            try:
                                val = int(val)
                            except:
                                pass
                            u_map[CMD_ARGS_DICT][split_arg[0]] = val
                        else:
                            # or add argument and default value of nothing
                            u_map[CMD_ARGS_DICT][split_arg[0]] = ''

                        if len(strs) > 1 and len(strs[1]) > 0:
                            u_map[PARTS].append(strs[1].strip().lower())
                if '' in u_map[PARTS]:
                    u_map[PARTS] = [x for x in u_map[PARTS] if len(x) > 0]

                # add utterance map to action map
                action_map[action_key].append(u_map)
    return action_map


def parse_arguments(arguments):
    """
    Parse the argument string from the action call template,
    where arguments are surrounded in parenthesis. Make sure
    to parse and store default values as well.
    :param arguments: the argument string from the action call templates
    :return: the dict from argument to value
    """
    args = dict()
    if len(arguments) > 2:
        # remove parentheses from arguments
        arguments = arguments[1:len(arguments)-1]

        # split args up
        arg_list = arguments.split(",")
        for arg in arg_list:
            arg = arg.strip()

            # handle default values
            arg_vals = arg.split("=")
            if len(arg_vals) == 2:
                args[arg_vals[0]] = arg_vals[1]
            else:
                args[arg_vals[0]] = ""

    return args


def load_action_command_samples(file_path):
    """
    Loads the action command samples file contents
    into memory as an action map with the action
    token as the key, the list of samples as the value.
    :param file_path:
    :return:
    """
    action_keys_and_values = get_action_keys_and_values(file_path)
    action_map = dict()
    for action_key in action_keys_and_values:
        action_value = action_keys_and_values[action_key]
        action_commands = action_value.split(", ")
        if len(action_commands) > 0:
            action_map[action_key] = action_commands
    return action_map


def extract_arg_sections(command_str, part_indices):
    """
    Extracts the argument sections from the provided command string.
    Uses the part indices to search the parts of the string that may contain arguments.
    :param command_str: the string containing one command and its arguments
    :param part_indices: the pairs of indices (start, end) that could contain arguments
    :return: the argument section strings from the command
    """
    arg_indices = []
    index_list = []
    arg_sections = []

    # parse multiple arguments out of the command string
    if len(part_indices) > 2:
        for part_index in part_indices:
            index_list.append(part_index[0])
            index_list.append(part_index[1])

        arg_start = -1
        for i in range(len(index_list)):
            # get arg start
            if i > 0 and i % 2 == 0 and arg_start == -1:
                arg_start = index_list[i]
            else:
                # get arg end
                if arg_start >= 0:
                    arg_end = index_list[i]
                    arg_indices.append((arg_start, arg_end))
                    arg_start = -1

        # add part pairs to
        for index_pair in arg_indices:
            part_start = index_pair[0]
            part_end = index_pair[1]
            arg_sections.append(command_str[part_start:part_end])
    elif len(part_indices) == 1 and part_indices[0][1] < len(command_str):
        # parse
        part_start = part_indices[0][1] + 1
        part_end = len(command_str)
        arg_sections.append(command_str[part_start:part_end])
    elif len(part_indices) == 2:
        # see if there is room for arguments at front of phrase
        if part_indices[0][0] > 0:
            arg_sections.append(command_str[0:part_indices[0][0]])

        # see if there is room for args between first and second phrase
        if part_indices[1][0] > part_indices[0][1]:
            arg_sections.append(command_str[part_indices[0][1]:part_indices[1][0]])

        # see if there is room for args at end of phrase
        if part_indices[1][1] < len(command_str):
            arg_sections.append(command_str[part_indices[1][1]:])
    arg_sections = [x.strip() for x in arg_sections if x.strip()]
    return arg_sections


def normalize_string(text):
    return text.lower().strip()


def normalize_nested_dict(dict_of_dict):
    """
    Normalizes the contents of a nest dictionary,
    i.e. take min and max of dict[x][y] and normalize between 0 and 1
    :param dict_of_dict: nested dict {{}}
    :return: new normalized nested dict
    """
    new_dict_of_dict = dict()
    for key_1 in dict_of_dict.keys():
        new_dict_of_dict[key_1] = dict()
        for key_2 in dict_of_dict[key_1].keys():
            new_dict_of_dict[key_1][key_2] = 0
            max_val = max(dict_of_dict[key_1][key_2])
            min_val = min(dict_of_dict[key_1][key_2])
            for val in dict_of_dict[key_1][key_2]:
                belief = (val - min_val) / (max_val - min_val)
                new_dict_of_dict[key_1][key_2] = belief
    return new_dict_of_dict
