__author__ = 'Shaun Howard'
import json
import web

from text_processor.text_processor import parse_web_commands
from web_control_mapper.mapper import create_web_controls

urls = ("/.*", "Text2Web")
web_app = web.application(urls, globals())
err_msg = "Error: Command could not be processed.\n"

# use this template to send the text request
json_template = "{\"request\":\"open my friends list on facebook.\"}"


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
    :return: the text response of the web control service
    """
    # assert input is a string
    assert type(text) is str
    web_commands = parse_web_commands(text)
    web_controls = create_web_controls(web_commands)
    return web_controls

if __name__ == '__main__':
    web_app.run()