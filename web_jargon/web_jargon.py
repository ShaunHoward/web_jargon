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
            json_request = json.dumps(request)
            log_to_console(['received request: ', request])
            return extract_web_actions(json_request, self.processor, self.mapper)
        except ValueError:
            log_to_console(["could not process Web Jargon request..."])
        return err_msg


def create_json_action_response(web_actions, sec_key):
    # jsonify a python dictionary of the current web action sequence response
    json_dict = dict()
    json_dict["action"] = web_actions
    json_dict["sec_key"] = sec_key
    return json.dumps(json_dict)


def extract_web_actions(json_request, processor, mapper):
    """
    Interprets the provided text as a web control command if possible.
    A message may be returned to the user in json to describe the status
    of the operation.
    :param json_request: the json request including txt command, sec key, and curr url
    :param processor: the processor instance to find the actions asked for
    :param mapper: the mapper instance for determining action list
    :return: the json text response of the web control service containing web actions to execute and other info
    """

    json_action_response = json.dumps({"action": "", "sec_key": ""})
    # make sure input is valid json
    if is_json(json_request):
        if "sec_key" in json_request:
            sec_key = json_request["sec_key"]
            json_action_response["sec_key"] = sec_key
            if "command" in json_request and "url" in json_request:
                action_request = json_request["command"]
                curr_url = json_request["url"]
                web_commands = processor.process_web_action_request(action_request, curr_url)
                web_actions = mapper.create_web_actions(web_commands)
                json_action_response = create_json_action_response(web_actions, sec_key)
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
