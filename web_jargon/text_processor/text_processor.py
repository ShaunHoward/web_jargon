__author__ = 'shaun'

from os import path
from itertools import chain

from nltk import sent_tokenize, word_tokenize
from nltk.corpus import wordnet as wn
from nltk.tag import StanfordPOSTagger

from web_jargon import helpers as h

NUM_TO_INT = {"first": 1, "second": 2, "third": 3, "fourth": 4, "fifth": 5, "sixth": 6, "seventh": 7, "eighth": 8,
              "ninth": 9, "tenth": 10, "eleventh": 11, "twelvefth": 12, "thirteenth": 13, "fourteenth": 14,
              "fifteenth": 15}

SUCCESS = "The operation was successful."
FAIL = "The operation was unsuccessful."

# context names
DEFAULT = "default"
FACEBOOK = "facebook"
SPOTIFY = "spotify"
GOOGLE = "google"
YOUTUBE = "youtube"

# custom tags
CMD_START = 'VB|NN'
CONTEXT = 'context'
DEFAULT_ACTION_CONTEXT = "default"
DIR = path.dirname(path.dirname(__file__))
PARENT_DIR = path.dirname(DIR)
DEFAULT_ACTIONS_PATH = DIR + '/templates/action_command_templates.txt'
STANFORD_JAR_PATH = PARENT_DIR + '/postagger/stanford-postagger.jar'
BIDIR_STANFORD_TAGGER_PATH = PARENT_DIR + '/postagger/models/english-bidirectional-distsim.tagger'
TWORD_STANFORD_TAGGER_PATH = PARENT_DIR + '/postagger/models/english-left3words-distsim.tagger'


def tag_words(words_of_text):
    """
    Tags the provided words of the text with parts of speech.
    :param words_of_text: the text to tag the words of
    :return: the tags of the words in a map (k=word, v=pos_tag)
    """
    tags = []
    st = StanfordPOSTagger(TWORD_STANFORD_TAGGER_PATH, STANFORD_JAR_PATH)
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


def extract_action_requests(words, tags):
    """
    Figure out the web actions that exist in the provided sentence using
    the given words and tags.
    :param words: the words of the sentence
    :param tags: the tags of the words in the sentence
    :return: the web actions tokens and arguments
    """
    # search for conjunctions to split up commands
    commands = []
    command_tags = []
    if 'CC' in tags:
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
            if len(command) > 0 and len(tags_) > 0:
                commands.append(command)
                command_tags.append(tags_)
    else:
        commands.append(words)
        command_tags.append(tags)

    action_requests = []
    for i in range(len(commands)):
        command_words = commands[i]
        command_tags = command_tags[i]
        command_start = 0
        # must have a context for any actions taking place or default actions are assumed
        action_context = determine_action_context(command_words, command_tags)
        curr_action_request = {h.CMD: "", h.CMD_ARGS: [], CONTEXT: action_context}
        tag_list = []
        for j in range(len(command_tags)):
            tag = command_tags[j]
            # look for a command start
            if ('VB' in tag and CMD_START not in tag_list) or\
                    ('NN' in tag and CMD_START not in tag_list):
                tag_list.append(CMD_START)
                command_start = j
                # add command start to dictionary
                curr_action_request[h.CMD] = command_words[command_start]
            # look for command modifiers like up, down, etc.
            elif ('RB' in tag or 'RP' in tag or
                    ('VB' in tag and CMD_START in tag_list) or
                    ('NN' in tag and CMD_START in tag_list)) and\
                    command_start == 0:
                if j > command_start:
                    tag_list.append('RB|RP|VB')
                    curr_action_request[h.CMD] += ''.join([' ', command_words[j]])
            # look for numeral values to feed as arguments to command
            elif 'CD' in tag or 'JJ' in tag:
                tag_list.append('CD|JJ')
                # try to parse a number out of the numeral
                if 'JJ' in tag and command_words[j] in NUM_TO_INT.keys():
                    num_arg = NUM_TO_INT[command_words[j]]
                    curr_action_request[h.CMD_ARGS].append(num_arg)
                else:
                    curr_action_request[h.CMD_ARGS].append(command_words[j])
        action_requests.append(curr_action_request)
    return action_requests


def determine_action_context(words, tags):
    return DEFAULT_ACTION_CONTEXT


def valid_web_jargon(sent):
    # TODO
    return True


def train_processor(training_data_dir):
    with open(training_data_dir, 'r') as training_file:
        training_data = training_file.read()
    training_command_list = training_data.split('\n')


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


class TextProcessor():
    action_text_mappings = dict()

    def __init__(self):
        self.action_text_mappings = h.load_web_action_template(DEFAULT_ACTIONS_PATH, False)

    def process_web_action_requests(self, text):
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
                web_action_tokens = web_action_tokens + extract_action_requests(words_of_sentences[i],
                                                                                tags_of_words_of_sentences[i])
        return web_action_tokens



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
