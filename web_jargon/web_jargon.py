__author__ = 'Shaun Howard'
import json

import web
from optparse import OptionParser
from helpers import log_to_console, is_json
from text_processor import TextProcessor
from mapper import Mapper

urls = ("/.*", "WebJargon")
web_app = web.application(urls, globals())
err_msg = "Error: Command could not be processed.\n"

# use this template to send the text request
json_template = "{\"request\":\"open my friends list on facebook.\"}"


class WebJargon():
    mapper = None
    processor = None

    def __init__(self):
        self.mapper = Mapper()
        self.processor = TextProcessor()

    def GET(self):
        return 'Please provide Web Jargon with an English text web action request.'

    def POST(self):
        try:
            # parse out json request with text command and current page URL
            request = web.data()
            request_dict = json.load(request)
            log_to_console(['received request: ', request])
            return extract_web_actions(request_dict, self.processor, self.mapper)
        except ValueError:
            log_to_console(["could not process Web Jargon request..."])
        return err_msg


def create_json_action_response(web_actions, sec_key):
    # jsonify a python dictionary of the current web action sequence response
    json_dict = dict()
    json_dict["action"] = web_actions
    json_dict["sec_key"] = sec_key
    return json.dumps(json_dict)


def extract_web_actions(request_dict, processor, mapper):
    """
    Interprets the provided text as a web control command if possible.
    A message may be returned to the user in json to describe the status
    of the operation.
    The json request must have a "command", a "sec_key" and a "url".
    :param request_dict: the json request dict including txt command, sec key, and curr url
    :param processor: the processor instance to find the actions asked for
    :param mapper: the mapper instance for determining action list
    :return: the json text response of the web control service containing web actions to execute and other info
    """

    response_dict = {"action": "", "sec_key": ""}
    json_action_response = None
    # make sure input is valid json
    if type(request_dict) is dict:
        if "sec_key" in request_dict.keys():
            sec_key = request_dict["sec_key"]
            response_dict["sec_key"] = sec_key
            if "command" in request_dict.keys() and "url" in request_dict.keys():
                action_request = request_dict["command"]
                curr_url = request_dict["url"]
                web_commands = processor.process_web_action_request(action_request, curr_url)
                web_actions = mapper.create_web_actions(web_commands)
                json_action_response = create_json_action_response(web_actions, sec_key)
    if json_action_response is None:
        json_action_response = json.dumps(response_dict)

    return json_action_response


def run_server():
    # create option parser for port numbers
    parser = OptionParser()
    parser.add_option("-p", "--port", dest="port",
                      help="run the Web Jargon server on the specified port")
    (options, args) = parser.parse_args()
    # run on default port
    port = 8080
    if options.port is not None:
        try:
            port = int(options.port)
        except TypeError:
            print "error parsing input port number"
    web.httpserver.runsimple(web_app.wsgifunc(), ("0.0.0.0", port))

if __name__ == '__main__':
    run_server()
