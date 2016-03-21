__author__ = 'shaun howard'
import unittest
from web_jargon.text_processor.text_processor import TextProcessor
from web_jargon import helpers as h


class TextProcessorTest(unittest.TestCase):

    tp = None

    def setUp(self):
        self.tp = TextProcessor()

    def validate_phrases(self, phrases, action, args=[]):
        has_args = len(args) > 0
        curr_phrase = 0
        for phrase in phrases:
            web_actions = self.tp.process_web_action_requests(phrase)
            self.assertEqual(len(web_actions), 1)
            self.assertTrue(web_actions[0][h.CMD] in self.tp.action_text_mappings.keys())
            self.assertEqual(action, web_actions[0][h.CMD])
            print phrase.strip()
            print web_actions[0]
            num_args = 0
            if has_args:
                for arg in args[curr_phrase]:
                    if arg in web_actions[0]['arguments'].values():
                        num_args += 1
                self.assertEqual(len(args[curr_phrase]), num_args)
            self.assertTrue(num_args == len(web_actions[0]['arguments'].values()))
            curr_phrase += 1

    def test_scroll_left(self):
        template_phrases = ["scroll left", "left scroll"]
        self.validate_phrases(template_phrases, h.SCROLL_LEFT)

    def test_scroll_right(self):
        template_phrases = ["scroll right", "right scroll"]
        self.validate_phrases(template_phrases, h.SCROLL_RIGHT)

    def test_scroll_up(self):
        template_phrases = ["scroll up", "up scroll", "scroll up one page", "scroll up ten pages"]
        args = [[], [], [1], [10]]
        self.validate_phrases(template_phrases, h.SCROLL_UP, args)

    def test_scroll_down(self):
        template_phrases = ["scroll down", "down scroll", "scroll down one page", "scroll down four pages"]
        args = [[], [], [1], [4]]
        self.validate_phrases(template_phrases, h.SCROLL_DOWN, args)

    def test_zoom_in(self):
        template_phrases = ["zoom in by ten percent", "zoom in 20 percent", "zoom 4 times", "zoom", "zoom larger",
                            "zoom in"]
        args = [[10], [20], [], [], [], []]
        self.validate_phrases(template_phrases, h.ZOOM_IN, args)

    def test_zoom_out(self):
        template_phrases = ["zoom out by fifty percent", "zoom out by thirty five percent", "zoom away 30 percent",
                            "zoom out three times", "zoom out 100 percent", "zoom smaller", "zoom out"]
        args = [[50], [35], [30], [], [100], [], []]
        self.validate_phrases(template_phrases, h.ZOOM_OUT, args)

    def test_open_new_tab(self):
        template_phrases = ["open a tab", "open a new tab", "new tab", "open new tab", "create tab", "create a new tab",
                            "create new tab"]
        self.validate_phrases(template_phrases, h.OPEN_TAB)

    def test_close_tab(self):
        template_phrases = ["close tab", "close this tab", "close my tab", "exit this tab", "leave this tab",
                            "exit the tab"]
        self.validate_phrases(template_phrases, h.CLOSE_TAB)

    def test_switch_tab(self):
        template_phrases = ["switch to tab three", "switch to tab google", "switch to Facebook", "change to CNN","open tab Spotify", "open tab 10",
                            "open the twelfth tab", "switch to the first tab",
                            "change to Facebook tab",
                            "change to tab four", "change to Pandora",
                            "change tab to tab 4", "change tab to the weather"]
        args = [[3], ["google"], ["facebook"], ["cnn"], ["spotify"], [10], [12], [1], ["facebook"], [4], ["pandora"], [4], ["the weather"]]
        self.validate_phrases(template_phrases, h.SWITCH_TAB, args)

    def test_forward_page(self):
        # ["forward", "go forward", "go forward a page",
        template_phrases = ["go to the next page", "next page",
                            "ahead a page", "forward a page", "one page forward", "page forward", "page ahead"]
        self.validate_phrases(template_phrases, h.FORWARD)

    def test_backward_page(self):
        template_phrases = ["backward", "go backward", "go backward a page", "go back a page",
                            "go to the previous page", "previous page", "back a page", "backward a page",
                            "one page backward", "page backward", "page back"]
        self.validate_phrases(template_phrases, h.BACKWARD)

    def test_refresh_page(self):
        template_phrases = ["refresh the page", "refresh page", "page refresh", "refresh this page"]
        self.validate_phrases(template_phrases, h.REFRESH)

    def test_click_element(self):
        template_phrases = ["click search", "click submit", "click more", "click sent mail", "click the submit button",
                            "click the post button", "click the home button"]
        args = [['search'], ['submit'], ['more'], ['sent mail'], ['submit'], ['post'], ['home']]
        self.validate_phrases(template_phrases, h.CLICK, args)

    def test_open_url(self):
        template_phrases = ["open www.google.com in the current tab", "open facebook.com", "open new google.com",
                            "open accuweather.com in this tab", "open pandora.com in this tab",
                            "open youtube.com in this tab", "open spotify.com in this tab"]
        args = [['www.google.com'], ['facebook.com'], ['google.com'], ['accuweather.com'], ['pandora.com'], ['youtube.com'],
                ['spotify.com']]
        self.validate_phrases(template_phrases, h.OPEN_URL, args)

    def test_select_element(self):
        template_phrases = ["select search box", "select what are you interested in?", "select username",
                            "select search", "select password", "select search facebook", "select what's on your mind?",
                            "select write a comment..."]
        args = [['search box'], ['what are you interested in?'], ['username'], ['search'], ['password'],
                ['search facebook'], ['what\'s on your mind?'], ["write a comment..."]]
        self.validate_phrases(template_phrases, h.SELECT_ELEMENT, args)

    # def test_enter_text(self):
    #     template_phrases = ["enter text into form status {WAIT=3} I feel great today for some reason {WAIT=3}",
    #                         "write I feel great today and want to go on vacation",
    #                         "enter the wheels on the car are worth $2500"]
    #     self.validate_phrases(template_phrases, h.ENTER_TEXT)
    #
    # def test_submit_text(self):
    #     template_phrases = ["submit text using post", "submit", "submit text post", "submit post", "click post to submit"]
    #     self.validate_phrases(template_phrases, h.SUBMIT_TEXT)
    #
    # def test_enter_and_submit_text(self):
    #     template_phrases = [""]
    #     self.validate_phrases(template_phrases, "enter and submit text")

    def test_open_help(self):
        template_phrases = ["help please", "please help", "open help", "open browsing assistance", "browsing assistance", "assistance", "assistant", "helper", "help window", "help me", "show hints", "open hints", "display hints", "list functions", "list commands", "list actions", "show actions", "show commands"]
        self.validate_phrases(template_phrases, h.OPEN_HELP)

    def test_close_help(self):
        template_phrases = ["close help", "I'm good", "thanks", "I am good"]
        self.validate_phrases(template_phrases, h.CLOSE_HELP)

    def test_open_cheat_sheet(self):
        template_phrases = ["open cheat sheet", "let me cheat", "display cheats", "show cheats", "show me cheats", "open cheats", "open functions", "list all functions", "list all commands", "list all actions", "show all actions", "show all commands", "show all hints", "open all hints", "display all hints"]
        self.validate_phrases(template_phrases, h.OPEN_CHEAT_SHEET)

    def test_close_sheat_sheet(self):
        template_phrases = ["close cheat sheet", "close cheats", "hide cheats", "hide cheat sheet", "hide sheet"]
        self.validate_phrases(template_phrases, h.CLOSE_CHEAT_SHEET)

    def test_open_setup_page(self):
        template_phrases = ["display setup", "display setup page", "open setup", "open setup page", "show setup", "show setup page"]
        self.validate_phrases(template_phrases, h.OPEN_SETUP_PAGE)

    def test_close_setup_page(self):
        template_phrases = ["hide setup", "close setup", "exit setup"]
        self.validate_phrases(template_phrases, h.CLOSE_SETUP_PAGE)

    def test_play_video(self):
        template_phrases = ["play video", "start video", "start", "play movie", "start movie"]
        self.validate_phrases(template_phrases, h.PLAY_VIDEO)

    def test_pause_video(self):
        template_phrases = ["pause video", "pause", "pause movie", "stop video", "stop movie", "stop"]
        self.validate_phrases(template_phrases, h.PAUSE_VIDEO)

    def test_restart_video(self):
        template_phrases = ["restart video", "restart", "restart movie", "replay movie", "replay video", "replay"]
        self.validate_phrases(template_phrases, h.RESTART_VIDEO)

    def test_open_fullscreen(self):
        template_phrases = ["fullscreen", "full screen", "open fullscreen", "open full screen", "toggle fullscreen",
                            "toggle full screen"]
        self.validate_phrases(template_phrases, h.OPEN_FULLSCREEN)

    def test_close_fullscreen(self):
        template_phrases = ["escape", "quit", "quit fullscreen", "close fullscreen", "close full screen",
                            "exit fullscreen", "exit full screen", "toggle fullscreen off", "toggle full screen off"]
        self.validate_phrases(template_phrases, h.CLOSE_FULLSCREEN)

    # def test_play_music(self):
    #     template_phrases = []
    #     self.validate_phrases(template_phrases, "play music")
    #
    # def test_pause_music(self):
    #     template_phrases = []
    #     self.validate_phrases(template_phrases, "pause music")
    #
    # def test_next_song(self):
    #     template_phrases = []
    #     self.validate_phrases(template_phrases, "next song")
    #
    # def test_search_music(self):
    #     template_phrases = []
    #     self.validate_phrases(template_phrases, "search music")
    #
    # def test_search_pdf(self):
    #     template_phrases = []
    #     self.validate_phrases(template_phrases, "search pdf")
    #
    # def test_go_to_page_pdf(self):
    #     template_phrases = []
    #     self.validate_phrases(template_phrases, "go to page pdf")

if __name__ == '__main__':
    unittest.main()