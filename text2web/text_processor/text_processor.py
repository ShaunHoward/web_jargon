__author__ = 'shaun'
from itertools import chain

from nltk import pos_tag, sent_tokenize, word_tokenize
from nltk.corpus import wordnet as wn
from text2web.helpers import normalize_string

SUCCESS = "The operation was successful."
FAIL = "The operation was unsuccessful."


def tag_words(words_of_text):
    """
    Tags the provided words of the text with parts of speech.
    :param text: the text to tag the words of
    :return: the tags of the words in a map (k=word, v=pos_tag)
    """
    tags = []
    tag_tuple_list = pos_tag(words_of_text)
    for tag_tuple in tag_tuple_list:
        word = tag_tuple[0]
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

    :param sentence:
    :param words:
    :param tags:
    :return:
    """
    return ""


def valid_web_jargon(sent):
    # TODO
    return True


class TextProcessor():

    def __init__(self, training_data_dir):
        with open(training_data_dir, 'r') as training_file:
            training_data = training_file.read()
        training_command_list = training_data.split('\n')

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
        for i in range(len(is_valid)):
            if is_valid[i]:
                # process sentence for commands
                process(sentences[i], words_of_sentences[i], tags_of_words_of_sentences[i])
        return []


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


