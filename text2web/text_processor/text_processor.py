__author__ = 'shaun'
import nltk

from text2web.helpers import normalize_string

SUCCESS = "The operation was successful."
FAIL = "The operation was unsuccessful."


def parse_web_commands(text):
    """
    Parses the provided text into web commands that should be executed
    in a specific order from an English sentence.
    :param text: the input command text
    :return: the controls list, which will be empty if in error
    """
    # tokenize text into sentences
    sentences = nltk.tokenize.sent_tokenize(text)

    # parse commands from each sentence
    for sentence in sentences:
        # tokenize the sentence into a sequence of one or more feasible commands

        pass

    return []


class TextProcessor():
    bigram_belief_state = dict()

    def __init__(self, training_data_dir):
        with open(training_data_dir, 'r') as training_file:
            training_data = training_file.read()
        training_command_list = training_data.split('\n')
        self.create_bigram_belief_state(training_command_list)

    def create_bigram_belief_state(self, training_command_list):
        for command in training_command_list:
            bigrams = self.determine_bigrams(command)
            for bigram in bigrams:
                norm_bigram_key = normalize_string(bigram[0])
                norm_bigram_value = normalize_string(bigram[1])
                if len(self.bigram_belief_state[norm_bigram_key]) == 0:
                    self.bigram_belief_state[norm_bigram_key] = dict()
                    self.bigram_belief_state[norm_bigram_key][norm_bigram_value] = 0
                self.bigram_belief_state[norm_bigram_key][norm_bigram_value] += 1
        self.bigram_belief_state = self.normalize_nested_dict(self.bigram_belief_state)

    def determine_bigrams(self, command):
        sent_tokenized_commands = nltk.tokenize.sent_tokenize(command)
        word_tokenized_commands = nltk.tokenize.word_tokenize(command)
        for i in range(0, len(word_tokenized_commands)):
            word = word_tokenized_commands[i]
            bigrams = []
            # do both left and right sides of word
            if 0 < i < len(word_tokenized_commands) - 1:
                bigrams = [(word, word_tokenized_commands[i - 1]),
                           (word, word_tokenized_commands[i + 1])]
            # only do right side of word
            elif i == 0:
                bigrams = [(word, word_tokenized_commands[i + 1])]
            # only do left side of word
            elif i == len(word_tokenized_commands) - 1:
                bigrams = [(word, word_tokenized_commands[i - 1])]
        return bigrams

    def normalize_nested_dict(self, dict_of_dict):
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


