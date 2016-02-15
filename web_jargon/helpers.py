__author__ = 'Shaun Howard'

CMD = 'command'
CMD_ARGS = 'arguments'
PARTS = 'parts'
LPAREN = "("
RPAREN = ")"


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

            # handle "OR" parameters
            or_args = arg.split("|")
            for or_arg in or_args:
                # handle default values
                arg_vals = or_arg.split("=")
                if len(arg_vals) == 2:
                    args[arg_vals[0]] = arg_vals[1]
                else:
                    args[or_arg] = ""

    return args


def load_web_action_template(template_path, action_call=True):
    """
    Generate an action template for creating action sequences.
    :param template_path: the path of the action call or command template file.
    :return: the action template map, ready to use and fill in
    """
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

    # create a map from token to action function call
    action_map = dict()
    for action in filtered_actions:
        # split up action token and function call parts
        toke_and_func = action.split(':')
        action_key = toke_and_func[0].strip()
        action_value = toke_and_func[1].strip()

        if len(action_key) > 0 and len(action_value) > 0:
            # strip <> and trailing whitespace from function call
            action_value = action_value.lstrip('<').rstrip('>').strip()
            if len(action_value) > 0:
                # run action call template parser
                if action_call:
                    # separate functions from arguments
                    l_paren_index = action_value.index(LPAREN)
                    action_args = action_value[l_paren_index:]
                    action_value = action_value[:l_paren_index]

                    # parse arguments into a list template
                    action_args_list = parse_arguments(action_args)

                    # create the action call template as a dictionary with command and arguments
                    if action_key not in action_map.keys():
                        action_map[action_key] = dict()

                    # store the action and the arguments to it
                    action_map[action_key][CMD_ARGS] = action_args_list
                    action_map[action_key][CMD] = action_value
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
                        u_map[CMD_ARGS] = dict()

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
                                    u_map[CMD_ARGS][split_arg[0]] = split_arg[1]
                                else:
                                    # or add argument and default value of nothing
                                    u_map[CMD_ARGS][split_arg[0]] = ''

                                if len(strs) > 1 and len(strs[1]) > 0:
                                    u_map[PARTS].append(strs[1].strip().lower())

                        # add utterance map to action map
                        action_map[action_key].append(u_map)
    return action_map


def normalize_string(text):
    return text.lower().strip()