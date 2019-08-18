from django.test import TestCase

# Create your tests here.
from splinter import Browser

from csranker.settings import INVALID_GAME_PAGE
from esea_scraper.management.commands.scrape_esea import identify_page_type


class TestPageTypeChecker(TestCase):
    def test_invalid_match_properly_found(self):
        game_id = 14633573

        browser = Browser('chrome', incognito=True, headless=False)
        browser.driver.set_window_size(640, 480)
        url = 'https://play.esea.net/match/{}'.format(game_id)
        browser.visit(url)

        page_type = identify_page_type(browser)

        self.assertEqual(page_type, INVALID_GAME_PAGE)
