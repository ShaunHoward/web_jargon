__author__ = 'shaun howard'
import unittest

from text_processor import TextProcessor
from web_jargon import helpers as h
from helpers import spot, pandora, youtube, pdf


class TextProcessorTest(unittest.TestCase):

    tp = None

    def setUp(self):
        self.tp = TextProcessor()

    def validate_phrases(self, phrases, action, args=[], urls=[]):
        has_args = len(args) > 0
        has_urls = len(urls) > 0
        curr_phrase = 0
        curr_url = "google.com"
        for phrase in phrases:
            if has_urls:
                curr_url = urls[curr_phrase]
            web_action = self.tp.process_web_action_request(phrase, curr_url)
            self.assertNotEqual(web_action, None)
            self.assertTrue(web_action[h.CMD] in self.tp.action_text_mappings.keys())
            self.assertEqual(action, web_action[h.CMD])
            print phrase.strip()
            print web_action
            num_args = 0
            if has_args:
                for arg in args[curr_phrase]:
                    if arg in web_action['arguments'].values():
                        num_args += 1
                self.assertEqual(len(args[curr_phrase]), num_args)
            num_nonempty_args = [x for x in web_action['arguments'].values() if x]
            self.assertEqual(num_args, len(num_nonempty_args))
            curr_phrase += 1

    def test_scroll_left(self):
        template_phrases = ["scroll left", "left scroll"]
        self.validate_phrases(template_phrases, h.SCROLL_LEFT)

    def test_scroll_right(self):
        template_phrases = ["scroll right", "right scroll"]
        self.validate_phrases(template_phrases, h.SCROLL_RIGHT)

    def test_scroll_up(self):
        template_phrases = ["scroll up", "up scroll", "scroll up one page", "scroll up ten pages"]
        args = [[1], [1], [1], [10]]
        self.validate_phrases(template_phrases, h.SCROLL_UP, args)

    def test_scroll_down(self):
        template_phrases = ["scroll down", "down scroll", "scroll down one page", "scroll down four pages"]
        args = [[1], [1], [1], [4]]
        self.validate_phrases(template_phrases, h.SCROLL_DOWN, args)

    def test_zoom_in(self):
        template_phrases = ["zoom in by ten percent", "zoom in 20 percent", "zoom", "zoom larger",
                            "zoom in"]
        args = [[10], [20], [25], [25], [25]]
        self.validate_phrases(template_phrases, h.ZOOM_IN, args)

    def test_zoom_out(self):
        template_phrases = ["zoom out by fifty percent", "zoom out by thirty five percent", "zoom away 30 percent",
                            "zoom out 100 percent", "zoom smaller", "zoom out"]
        args = [[50], [35], [30], [100], [25], [25]]
        self.validate_phrases(template_phrases, h.ZOOM_OUT, args)

    def test_open_new_tab(self):
        template_phrases = ["open tab Spotify", "open tab cnn", "open a tab facebook.com",  "new tab google.com",
                            "open a tab", "open a new tab", "new tab", "open new tab", "create tab", "create a new tab",
                            "create new tab"]
        args = [["spotify"], ["cnn"], ['facebook.com'], ['google.com']] + [[] for i in range(len(template_phrases))]
        self.validate_phrases(template_phrases, h.OPEN_TAB, args)

    def test_close_tab(self):
        template_phrases = ["close tab three", "close tab facebook", "exit tab 2", "exit tab StackOverflow", "leave tab twelve", "leave tab google"]
        args = [[3], ["facebook"], [2], ["stackoverflow"], [12], ["google"]]
        self.validate_phrases(template_phrases, h.CLOSE_TAB, args)

    def test_switch_tab(self):
        template_phrases = ["switch to facebook", "switch to four", "switch to tab three", "switch to tab google.com",
                            "switch to Facebook", "change to CNN", "open the twelfth tab", "switch to the first tab", "change to Facebook tab",
                            "change to tab four", "change to Pandora", "change tab to tab 4",
                            "change tab to the weather"]

        args = [["facebook"], [4], [3], ["google.com"], ["facebook"], ["cnn"], [12], [1], ["facebook"], [4], ["pandora"], [4], ["the weather"]]
        self.validate_phrases(template_phrases, h.SWITCH_TAB, args)

    def test_forward_page(self):
        # ["forward", "go forward", "go forward a page",
        template_phrases = ["go to the next page", "next page",
                            "ahead a page", "forward a page", "one page forward", "page forward", "page ahead"]
        self.validate_phrases(template_phrases, h.FORWARD)

    def test_backward_page(self):
        template_phrases = ["back", "backward", "go backward", "go backward a page", "go back a page",
                            "go to the previous page", "previous page", "back a page", "backward a page",
                            "one page backward", "page backward", "page back"]
        self.validate_phrases(template_phrases, h.BACKWARD)

    def test_refresh_page(self):
        template_phrases = ["refresh the page", "refresh page", "page refresh", "refresh this page"]
        self.validate_phrases(template_phrases, h.REFRESH)

    def test_click_element(self):
        template_phrases = ["open link facebook", "click google doc link", "click link github.com",
                            "open link w w w dot google dot com", "click github dot com", "click search",
                            "click the home button", "click submit", "click more", "click sent mail", "click the submit button",
                            "click the post button", "click the home button"]

        args = [['facebook'], ['google doc'], ['github.com'], ['www.google.com'], ['github.com'], ['search'], ['home'],
                ['submit'], ['more'], ['sent mail'], ['submit'], ['post'], ['home']]
        self.validate_phrases(template_phrases, h.CLICK, args)

    def test_open_url(self):
        template_phrases = ["open www.google.com in the current tab", "open facebook.com", "open new google.com",
                            "open accuweather.com in this tab", "open pandora.com in this tab",
                            "open youtube.com in this tab", "open spotify.com in this tab"]
        args = [['www.google.com', 'true'], ['facebook.com', 'false'], ['google.com', 'false'], ['accuweather.com', 'true'], ['pandora.com', 'true'], ['youtube.com', 'true'],
                ['spotify.com', 'true']]
        self.validate_phrases(template_phrases, h.OPEN_URL, args)

    def test_select_element(self):
        template_phrases = ["select search box", "select what are you interested in?", "select username",
                            "select search", "select password", "select search facebook", "select what's on your mind?",
                            "select write a comment..."]
        args = [['search box'], ['what are you interested in?'], ['username'], ['search'], ['password'],
                ['search facebook'], ['what\'s on your mind?'], ["write a comment..."]]
        self.validate_phrases(template_phrases, h.SELECT_ELEMENT, args)

    def test_enter_text(self):
        template_phrases = ["enter senior project has been a long process of testing",
                            "enter text I feel great today for some reason",
                            "write I feel great today and want to go on vacation",
                            "enter text the wheels on the car are worth $2500"]
        args = [['senior project has been a long process of testing'],
                ['i feel great today for some reason'], ['i feel great today and want to go on vacation'],
                ['the wheels on the car are worth $2500']]
        self.validate_phrases(template_phrases, h.ENTER_TEXT, args)

    def test_submit_text(self):
        template_phrases = ["submit text", "submit"]
        args = [[], []]
        self.validate_phrases(template_phrases, h.SUBMIT_TEXT, args)

    def test_open_help(self):
        template_phrases = ["help please", "please help", "open help", "open browsing assistance", "browsing assistance", "assistance", "assistant", "helper", "help window", "help me", "show hints", "open hints", "display hints", "list functions", "list commands", "list actions", "show actions", "show commands"]
        self.validate_phrases(template_phrases, h.OPEN_HELP)

    def test_close_help(self):
        template_phrases = ["close help", "close help page", "hide commands", "hide help", "hide hints", "hide functions", "close browsing assistance"]
        self.validate_phrases(template_phrases, h.CLOSE_HELP)

    # start video context
    def test_play_video(self):
        template_phrases = ["play", "play video", "play movie", "start", "start video", "start movie"]
        urls = [youtube] * len(template_phrases)
        self.validate_phrases(template_phrases, h.PLAY_VIDEO, urls=urls)

    def test_pause_video(self):
        template_phrases = ["stop", "stop video", "stop movie", "stop youtube", "paws", "pause", "paws movie",
                            "paws video", "paws youtube", "pause youtube", "pause video", "pause movie"]
        urls = [youtube] * len(template_phrases)
        self.validate_phrases(template_phrases, h.PAUSE_VIDEO, urls=urls)

    def test_next_video(self):
        template_phrases = ["next", "next video", "next movie", "next video in playlist", "next movie in playlist"]
        urls = [youtube] * len(template_phrases)
        self.validate_phrases(template_phrases, h.NEXT_VIDEO, urls=urls)

    def test_open_fullscreen(self):
        template_phrases = ["fullscreen", "full screen", "open fullscreen", "open full screen", "toggle fullscreen",
                            "toggle full screen"]
        urls = [youtube] * len(template_phrases)
        self.validate_phrases(template_phrases, h.OPEN_FULLSCREEN, urls=urls)

    def test_close_fullscreen(self):
        template_phrases = ["close", "exit", "escape", "quit", "quit fullscreen", "close fullscreen",
                            "close full screen", "exit fullscreen", "exit full screen", "toggle fullscreen off",
                            "toggle full screen off"]
        urls = [youtube] * len(template_phrases)
        self.validate_phrases(template_phrases, h.CLOSE_FULLSCREEN, urls=urls)

    # start music context
    def test_play_music(self):
        template_phrases = ["play", "start", "play music", "play my music", "play song", "play tune", "start music",
                            "start song", "start tune"]
        args = [['true'], ['false'], ['true'], ['false'], ['false'], ['false'], ['true'], ['false'], ['true']]
        urls = [spot, pandora, spot, pandora, pandora, pandora, spot, pandora, spot]
        self.validate_phrases(template_phrases, h.PLAY_MUSIC, args, urls=urls)

    def test_pause_music(self):
        template_phrases = ["pause", "pause music", "paws music", "paws", "paws song", "stop", "stop music",
                            "stop my music", "stop song", "stop tune"]
        args = [['true'], ['false'], ['true'], ['false'], ['false'], ['false'], ['false'], ['true'], ['false'], ['true']]
        urls = [spot, pandora, spot, pandora, pandora, pandora, pandora,  spot, pandora, spot]
        self.validate_phrases(template_phrases, h.PAUSE_MUSIC, args, urls=urls)

    def test_next_song(self):
        template_phrases = ["next", "next song", "next tune", "next on playlist", "next in playlist"]
        args = [['true'], ['false'], ['true'], ['false'], ['false'], ['true']]
        urls = [spot, pandora, spot, pandora, pandora, spot]
        self.validate_phrases(template_phrases, h.NEXT_SONG, args, urls=urls)

    def test_search_music(self):
        template_phrases = ["search artist Elvis Presley", "search artist Led Zeppelin", "search for artist red hot chili peppers",
                            "search album the song remains the same", "search for album by the way",
                            "search song star-spangled banner", "search for song Whole Lotta Love",
                            "search for song one"]
        args = [['false', 'elvis presley', 'artist'], ['true', 'led zeppelin', 'artist'], ['false', 'red hot chili peppers', 'artist'],
                ['false', 'the song remains the same', 'album'], ['true', 'by the way', 'album'],
                ['true', 'star-spangled banner', 'song'], ['true', 'whole lotta love', 'song'],
                ['false', 'one', 'song']]
        urls = [pandora, spot, pandora, pandora, spot, spot, spot, pandora]
        self.validate_phrases(template_phrases, h.SEARCH_MUSIC, args, urls=urls)

    # start doc context
    def test_go_to_page_pdf(self):
        template_phrases = ["go to page four hundred five", "go to page sixty seven", "go to two thousand seven hundred fifty three"]
        args = [[405], [67], [2753]]
        urls = [pdf] * 3
        self.validate_phrases(template_phrases, h.GO_TO_PDF_PAGE, args, urls=urls)

if __name__ == '__main__':
    unittest.main()