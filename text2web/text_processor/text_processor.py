__author__ = 'shaun'
import nltk

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
