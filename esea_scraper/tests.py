import logging

from django.test import TestCase

# Create your tests here.
from splinter import Browser

from csranker.settings import INVALID_GAME_PAGE, BASELINE_GAME_PAGE, \
    GAME_PAGE_WITH_MATCH_RECAP
from esea_scraper.management.commands.scrape_esea import identify_page_type, \
    parse_baseline_gamepage

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def set_up_browser_for_testing():
    browser = Browser('chrome', incognito=True, headless=False)
    browser.driver.set_window_size(640, 480)
    return browser


class TestPageTypeChecker(TestCase):
    def setUp(self):
        self.browser = set_up_browser_for_testing()

    def test_baseline_game_page_properly_identified(self):
        game_id = 14633571

        url = 'https://play.esea.net/match/{}'.format(game_id)
        self.browser.visit(url)
        page_type = identify_page_type(self.browser)

        self.assertEqual(page_type, BASELINE_GAME_PAGE)

    def test_game_page_with_match_recap_properly_identified(self):
        game_id = 14633572

        url = 'https://play.esea.net/match/{}'.format(game_id)
        self.browser.visit(url)
        page_type = identify_page_type(self.browser)

        self.assertEqual(page_type, GAME_PAGE_WITH_MATCH_RECAP)

    def test_invalid_match_properly_identified(self):
        game_id = 14633573

        url = 'https://play.esea.net/match/{}'.format(game_id)
        self.browser.visit(url)
        page_type = identify_page_type(self.browser)

        self.assertEqual(page_type, INVALID_GAME_PAGE)


class TestParseBaselineGamepage(TestCase):
    def setUp(self):
        self.browser = set_up_browser_for_testing()

    def test_thing(self):
        game_id = 14633571
        url = 'https://play.esea.net/match/{}'.format(game_id)
        self.browser.visit(url)
        game_data = parse_baseline_gamepage(self.browser)

        self.assertEqual(0, game_data)
