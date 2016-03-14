__author__ = 'shaun howard'
import unittest
from web_jargon.text_processor.text_processor import TextProcessor
from web_jargon.helpers import CMD


class TextProcessorTest(unittest.TestCase):

    tp = None

    def setUp(self):
        self.tp = TextProcessor()

    def validate_phrases(self, phrases, action):
        for phrase in phrases:
            web_actions = self.tp.process_web_action_requests(phrase)
            self.assertEqual(len(web_actions), 1)
            self.assertTrue(web_actions[0][CMD] in self.tp.action_text_mappings.keys())
            print phrase.strip()
            print web_actions[0]

    def test_scroll_left(self):
        template_phrases = ["scroll left", "left scroll"]
        phrases = ["Scroll all the way left."]
        self.validate_phrases(template_phrases, "scroll left")

    def test_scroll_right(self):
        template_phrases = ["scroll right", "right scroll"]
        phrases = ["Scroll right all the way."]
        self.validate_phrases(template_phrases, "scroll right")

    def test_scroll_up(self):
        template_phrases = ["scroll up", "up scroll", "scroll up one page", "scroll up ten pages"]
        phrases = ["Scroll up."]
        self.validate_phrases(template_phrases, "scroll up")

    def test_scroll_down(self):
        template_phrases = ["scroll down", "down scroll", "scroll down one page", "scroll down four pages"]
        phrases = ["Scroll down.", "Scroll down the page"]
        self.validate_phrases(template_phrases, "scroll down")

    def test_zoom_in(self):
        template_phrases = ["zoom in by ten percent", "zoom in 20 percent", "zoom 4 times", "zoom", "zoom larger",
                            "zoom in"]
        self.validate_phrases(template_phrases, "zoom in")

    def test_zoom_out(self):
        template_phrases = ["zoom out by fifty percent", "zoom out by thirty five percent", "zoom away 30 percent",
                            "zoom out three times", "zoom out 100 percent", "zoom smaller", "zoom out"]
        self.validate_phrases(template_phrases, "zoom out")

    def test_open_new_tab(self):
        template_phrases = ["open a tab", "open a new tab", "new tab", "open new tab", "create tab", "create a new tab",
                            "create new tab"]
        phrases = ["Open a new tab."]
        self.validate_phrases(template_phrases, "open tab")

    def test_close_tab(self):
        template_phrases = ["close tab", "close this tab", "close my tab", "exit this tab", "leave this tab",
                            "exit the tab"]
        phrases = ["Close the third tab."]
        self.validate_phrases(template_phrases, "close tab")

    def test_switch_tab(self):
        template_phrases = ["switch to tab three", "switch to tab google", "switch to Facebook", "change to CNN","open tab Spotify", "open tab 10",
                            "open the twelfth tab", "switch to the first tab",
                            "change to Facebook tab",
                            "change to tab four", "change to Pandora",
                            "change tab to tab 4", "change tab to the weather"]
        self.validate_phrases(template_phrases, "switch tab")

    def test_forward_page(self):
        template_phrases = ["forward", "go forward", "go forward a page", "go to the next page", "next page",
                            "ahead a page", "forward a page", "one page forward", "page forward", "page ahead"]
        self.validate_phrases(template_phrases, "forward page")

    def test_backward_page(self):
        template_phrases = ["backward", "go backward", "go backward a page", "go back a page",
                            "go to the previous page", "previous page", "back a page", "backward a page",
                            "one page backward", "page backward", "page back"]
        self.validate_phrases(template_phrases, "backward page")

    def test_refresh_page(self):
        template_phrases = ["refresh the page", "refresh page", "page refresh", "refresh this page"]
        self.validate_phrases(template_phrases, "refresh")

    def test_click_element(self):
        template_phrases = ["click search", "click submit", "click more", "click sent mail", "click the submit button",
                            "click the post button", "click the home button"]
        self.validate_phrases(template_phrases, "click")

    def test_open_link(self):
        template_phrases = ["open link facebook", "open google doc", "open github.com", "click facebook",
                            "enter facebook"]
        self.validate_phrases(template_phrases, "open link")

    def test_open_url(self):
        template_phrases = ["open www.google.com in the current tab", "open facebook.com", "open new google.com",
                            "open accuweather.com in this tab", "open pandora.com in this tab",
                            "open youtube.com in this tab", "open spotify.com in this tab"]
        self.validate_phrases(template_phrases, "open url")

    def test_enter_text(self):
        template_phrases = ["enter text into form status {WAIT=3} I feel great today for some reason {WAIT=3}",
                            "write I feel great today and want to go on vacation",
                            "enter the wheels on the car are worth $2500"]
        self.validate_phrases(template_phrases, "enter text")

    def test_submit_text(self):
        template_phrases = ["submit text using post", "submit", "submit text post", "submit post", "click post to submit"]
        self.validate_phrases(template_phrases, "submit text")

    # def test_enter_and_submit_text(self):
    #     template_phrases = [""]
    #     self.validate_phrases(template_phrases, "enter and submit text")

    # def test_open_help(self):
    #     template_phrases = []
    #     self.validate_phrases(template_phrases, "open help")
    #
    # def test_close_help(self):
    #     template_phrases = []
    #     self.validate_phrases(template_phrases, "close help")
    #
    # def test_open_cheat_sheet(self):
    #     template_phrases = []
    #     self.validate_phrases(template_phrases, "open cheat sheet")
    #
    # def test_close_sheat_sheet(self):
    #     template_phrases = []
    #     self.validate_phrases(template_phrases, "close cheat sheet")
    #
    # def test_open_setup_page(self):
    #     template_phrases = []
    #     self.validate_phrases(template_phrases, "open setup page")
    #
    # def test_close_setup_page(self):
    #     template_phrases = []
    #     self.validate_phrases(template_phrases, "close setup page")
    #
    # def test_play_video(self):
    #     template_phrases = []
    #     self.validate_phrases(template_phrases, "play video")
    #
    # def test_pause_video(self):
    #     template_phrases = []
    #     self.validate_phrases(template_phrases, "pause video")
    #
    # def test_restart_video(self):
    #     template_phrases = []
    #     self.validate_phrases(template_phrases, "restart video")
    #
    # def test_open_fullscreen(self):
    #     template_phrases = []
    #     self.validate_phrases(template_phrases, "open fullscreen")
    #
    # def test_close_fullscreen(self):
    #     template_phrases = []
    #     self.validate_phrases(template_phrases, "close fullscreen")
    #
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