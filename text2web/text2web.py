__author__ = 'Shaun Howard'
import json
import web

from text_processor.text_processor import process_web_action_requests
from web_control_mapper import mapper as mp

urls = ("/.*", "Text2Web")
web_app = web.application(urls, globals())
err_msg = "Error: Command could not be processed.\n"

# use this template to send the text request
json_template = "{\"request\":\"open my friends list on facebook.\"}"

TEST_MODE = False
TEST_COMMAND = "Scroll down one page."


class Text2Web():
    def __init__(self):
        pass

    def GET(self):
        return 'Provide Web Jargon with an English text web action request.'

    def POST(self):
        try:
            # recvd_action_request = web.data()
            # json_action_request = json.loads(recvd_action_request)
            # english_request = json_action_request["request"]
            english_request = web.data()
            return text2web(english_request)
        except ValueError:
            print "Could not process English request."
        return err_msg


def wrap_actions_in_json(web_actions):
    json_dict = dict()
    json_dict["actions"] = "[" + ", ".join([str(x) for x in web_actions]) + "]"
    return json.dumps(json_dict)


def text2web(text):
    """
    Interprets the provided text as a web control command if possible.
    A message may be returned to the user in json to describe the status
    of the operation.
    :param text: the text to control the default web browser
    :return: the json text response of the web control service containing web actions to execute
    """
    # assert input is a string
    assert type(text) is str
    web_commands = process_web_action_requests(text)
    web_actions = mp.create_web_actions(web_commands)
    json_action_response = wrap_actions_in_json(web_actions)
    return json_action_response

if __name__ == '__main__':
    if not TEST_MODE:
        web_app.run()
    else:
        print text2web(TEST_COMMAND)
