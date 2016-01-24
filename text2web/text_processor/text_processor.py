__author__ = 'shaun'

from os import getcwd
from os.path import join
from itertools import chain

from nltk import pos_tag, sent_tokenize, word_tokenize
from nltk.corpus import wordnet as wn
from nltk.tag import StanfordNERTagger, StanfordPOSTagger

SUCCESS = "The operation was successful."
FAIL = "The operation was unsuccessful."

# context names
DEFAULT = "default"
FACEBOOK = "facebook"
SPOTIFY = "spotify"
GOOGLE = "google"
YOUTUBE = "youtube"

# custom tags
CMD_START = 'start'
CMD_MOD = 'modifier'
CMD_ARG = 'argument'

DEFAULT_ACTIONS_PATH = join(getcwd(), '/templates/action_call_templates.txt')


def process_web_action_requests(text):
    """
    Parses the provided text into web text actions that will be converted into
    web actions by the web text to action mapper. The order will be maintained.
    :param text: the input command text
    :return: the controls list, which will be empty if in error
    """
    # tokenize text into sentences
    sentences = sent_tokenize(text)
    words_of_sentences = [word_tokenize(sent) for sent in sentences]
    tags_of_words_of_sentences = [tag_words(words) for words in words_of_sentences]

    # TODO: validate jargon
    is_valid = [valid_web_jargon(sent) for sent in sentences]
    web_action_tokens = []
    for i in range(len(is_valid)):
        if is_valid[i]:
            # process sentence for commands
            web_action_tokens = web_action_tokens + process(sentences[i],
                                                            words_of_sentences[i],
                                                            tags_of_words_of_sentences[i])
    return web_action_tokens


def tag_words(words_of_text):
    """
    Tags the provided words of the text with parts of speech.
    :param words_of_text: the text to tag the words of
    :return: the tags of the words in a map (k=word, v=pos_tag)
    """
    tags = []
    st = StanfordPOSTagger('models/english-bidirectional-distsim.tagger',
                'stanford-postagger.jar')
    tag_tuple_list = st.tag(words_of_text)
    for tag_tuple in tag_tuple_list:
        tag = tag_tuple[1]
        tags.append(tag)
    return tags


def similar_words(word, meaning):
    """
    Find words similar to the given word with the
    given meaning, tagged with POS by nltk.
    """
    word_w_meaning = word + meaning
    word_synset = wn.synset(word_w_meaning)
    print "definition of %s" % word
    print word_synset.definition()
    # gather synonyms from lemmas, hyponyms (sub-types) and hypernyms (super-types)
    synonyms = word_synset.lemma_names() \
        + list(chain(*[l.lemma_names for l in word_synset.hyponyms()])) \
        + list(chain(*[l.lemma_names for l in word_synset.hypernyms()]))
    print "synonyms: "
    print ', '.join(synonyms)
    return synonyms


def process(sentence, words, tags):
    """
    Figure out the web actions that exist in the provided sentence using
    the given words and tags.
    :param sentence: the sentence to find web actions/commands given in
    :param words: the words of the sentence
    :param tags: the tags of the words in the sentence
    :return: the web actions tokens and arguments
    """
    # search for conjunctions to split up commands
    conjunctions = []
    for i in range(len(tags)):
        if 'CC' in tags[i]:
            conjunctions.append(i)

    # split up commands by splitting sentence on conjunctions
    commands = []
    command_tags = []
    split_indices = [x for x in conjunctions]
    for i in range(len(split_indices)):
        split_index = split_indices[i]
        if split_index == 0 or split_index == len(words):
            continue
        if i == 0:
            command = words[:split_index-1]
            tags_ = tags[:split_index-1]
        elif i == len(split_indices) - 1:
            command = words[split_index+1:]
            tags_ = tags[split_index+1:]
        commands.append(command)
        command_tags.append(tags_)
    action_requests = []

    # try to parse web action requests and arguments
    command_tags = []
    # must have a context for any actions taking place or default actions are assumed
    context = "default"
    for command in commands:
        words = command[0]
        tags = command[1]
        command_start = 0
        curr_action_request = {CMD_START: "", CMD_MOD: [], CMD_ARG: []}
        for i in range(len(tags)):
            tag = tags[i]
            # look for a command start
            if 'VB' in tag or 'NNP' in tag:
                command_start = tags.index(tag)
                # add command start to dictionary
                curr_action_request[CMD_START] = words[command_start]

            # look for command modifiers like up, down, etc.
            if ('RB' in tag or 'RP' in tag) and command_start == 0:
                if i > command_start:
                    curr_action_request[CMD_MOD].append(words[i])

            # look for numeral values to feed as arguments to command
            if 'CD' in tag:
                curr_action_request[CMD_ARG].append(words[i])
        action_requests.append(curr_action_request)

    # find the available web page controls as stored in a web control map template
    # these can be determined from the webpage context using words and their POS tags
    possible_actions = get_actions_in_webpage(words, tags)

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
    return web_actions


def get_actions_in_webpage(words, tags):
    context = find_webpage_context(words, tags)
    actions = actions_in_context(context)
    return actions


def find_webpage_context(words, tags):
    return ''


def actions_in_context(context):
    """
    Load the actions for the specified context given action call
    template files for various websites that are well-known.
    By default, return the default available action list.
    :param context:
    :return:
    """
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


def valid_web_jargon(sent):
    # TODO
    return True


def train_processor(training_data_dir):
    with open(training_data_dir, 'r') as training_file:
        training_data = training_file.read()
    training_command_list = training_data.split('\n')


# def create_bigram_belief_state(self, training_command_list):
#     for command in training_command_list:
#         bigrams = self.determine_bigrams(command)
#         for bigram in bigrams:
#             norm_bigram_key = normalize_string(bigram[0])
#             norm_bigram_value = normalize_string(bigram[1])
#             if len(self.bigram_belief_state[norm_bigram_key]) == 0:
#                 self.bigram_belief_state[norm_bigram_key] = dict()
#                 self.bigram_belief_state[norm_bigram_key][norm_bigram_value] = 0
#             self.bigram_belief_state[norm_bigram_key][norm_bigram_value] += 1
#     self.bigram_belief_state = self.normalize_nested_dict(self.bigram_belief_state)
#
# def determine_bigrams(self, command):
#     sent_tokenized_commands = sent_tokenize(command)
#     word_tokenized_commands = word_tokenize(command)
#     for i in range(0, len(word_tokenized_commands)):
#         word = word_tokenized_commands[i]
#         bigrams = []
#         # do both left and right sides of word
#         if 0 < i < len(word_tokenized_commands) - 1:
#             bigrams = [(word, word_tokenized_commands[i - 1]),
#                        (word, word_tokenized_commands[i + 1])]
#         # only do right side of word
#         elif i == 0:
#             bigrams = [(word, word_tokenized_commands[i + 1])]
#         # only do left side of word
#         elif i == len(word_tokenized_commands) - 1:
#             bigrams = [(word, word_tokenized_commands[i - 1])]
#     return bigrams

def normalize_nested_dict(dict_of_dict):
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


