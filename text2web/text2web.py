__author__ = 'Shaun Howard'
import json
import web

from text_processor.text_processor import process_web_action_requests
from web_control_mapper.mapper import create_web_actions

urls = ("/.*", "Text2Web")
web_app = web.application(urls, globals())
err_msg = "Error: Command could not be processed.\n"

# use this template to send the text request
json_template = "{\"request\":\"open my friends list on facebook.\"}"

TEST_MODE = True
TEST_COMMAND = "Scroll down one page."


class Text2Web():
    def __init__(self):
        pass

    def GET(self):
        return 'Provide Web Jargon with an English text web action request.'

    def POST(self):
        try:
            recvd_action_request = web.data()
            json_action_request = json.loads(recvd_action_request)
            english_request = json_action_request["request"]
            return text2web(english_request)
        except ValueError:
            print "Could not process English request."
        return err_msg


def text2web(text):
    """
    Interprets the provided text as a web control command if possible.
    A message is returned to the user in text to describe the status
    of the operation.
    :param text: the text to control the default web browser
    :return: the json text response of the web control service containing web controls to execute
    """
    # assert input is a string
    assert type(text) is str
    web_commands = process_web_action_requests(text)
    web_actions = create_web_actions(web_commands)
    return web_actions

if __name__ == '__main__':
    if not TEST_MODE:
        web_app.run()
    else:
        print text2web(TEST_COMMAND)
