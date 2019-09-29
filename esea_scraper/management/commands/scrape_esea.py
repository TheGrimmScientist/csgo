import string
import sys
import datetime
import logging

from django.core.management.base import BaseCommand, CommandError
from splinter.exceptions import ElementDoesNotExist
from tqdm import tqdm
import chromedriver_binary
from splinter import Browser

# sys.path.append(str(Path(__file__).parent / 'chromedriver'))
from csgo.settings import INVALID_GAME_PAGE, GAME_PAGE_WITH_MATCH_RECAP, \
    BASELINE_GAME_PAGE

logger = logging.getLogger(__name__)


def get_team_scores(browser):
    team_a_score = browser.find_by_xpath(r'//*[@id="root"]/main/div[2]/div/div/div/div[1]/div[1]/div[1]/div[1]/span[2]').text[1:-1]
    team_b_score = browser.find_by_xpath(r'//*[@id="root"]/main/div[2]/div/div/div/div[1]/div[1]/div[4]/div[1]/span[2]').text[1:-1]

    return int(team_a_score), int(team_b_score)


class PlayerStats:

    link_base = r"https://play.esea.net/users/{}"

    def __init__(self, name, link, rms, kills, deaths, headshot_p):
        self.name = name
        self._id = link.split('/')[-1]
        self.rms = rms
        self.kills = kills
        self.deaths = deaths
        self.headshot_p = headshot_p

    def __repr__(self):
        return "player name is: {}, player url is: {}".format(self.name, self.link)


    def __str__(self):
        return "player name is: {}, player url is: {}".format(self.name, self.link)

    @property
    def link(self):
        return self.link_base.format(self._id)


def get_team_players(browser, css_selector, columns):
    team_players = []
    css_selector = string.Template(css_selector)

    for i in range(1, 6):  # 5 players, one indexed
        node = browser.find_by_css(css_selector.safe_substitute({'i': i}))
        cells = node.find_by_tag('td')
        name = cells[columns['name']].text
        kills = cells[columns['kills']].text
        deaths = cells[columns['deaths']].text
        headshot_p = cells[columns['headshot']].text
        rms = cells[columns['rws']].text
        url = cells.first.find_by_tag('a').last['href']
        team_players.append(PlayerStats(name, url, rms, kills, deaths, headshot_p))

    logger.info(team_players)
    return team_players


def parse_baseline_gamepage(browser):
    team_a_score, team_b_score = get_team_scores(browser)

    selector_template = string.Template(
        "#root > main > div> div > div > div > div:nth-child(4) > div > table > tbody:nth-child(${team}) > tr:nth-child(${i})"
    )

    team_a_players = get_team_players(
        browser, selector_template.safe_substitute({'team': 1*2})
    )
    team_b_players = get_team_players(
        browser, selector_template.safe_substitute({'team': 2*2})
    )

    data = {
        'A': {
            'score': team_a_score,
            'players': team_a_players

        },
        'B': {
            'score': team_b_score,
            'players': team_b_players
        },
    }

    return data


def parse_gamepage(browser, page_type):
    team_a_score, team_b_score = get_team_scores(browser)

    selector_template = string.Template(
        "#root > main > div> div > div > div > div:nth-child(${top_index}) > div > table > tbody:nth-child(${team}) > tr:nth-child(${i})"
    )

    config = {
        "extended": {
            "team_index": [2,5],
            "top_index": 4,
            "columns": {
                "name": 0,
                "kills": 1,
                "deaths": 2,
                "headshot": 6,
                "rws": 14,
            }
        },
        "basic": {
            "team_index": [2,4],
            "top_index": 4,
            "columns": {
                "name": 0,
                "kills": 1,
                "deaths": 2,
                "headshot": 6,
                "rws": 12,
            }
        }
    }

    team_a_players = get_team_players(
        browser, selector_template.safe_substitute({'top_index': config[page_type]['top_index'],
                                                    'team': config[page_type]['team_index'][0]}),
        config[page_type]['columns']
    )
    team_b_players = get_team_players(
        browser, selector_template.safe_substitute({'top_index': config[page_type]['top_index'],
                                                    'team': config[page_type]['team_index'][1]}),
        config[page_type]['columns']
    )

    data = {
        'A': {
            'score': team_a_score,
            'players': team_a_players

        },
        'B': {
            'score': team_b_score,
            'players': team_b_players
        },
    }

    return data




class GamePage:
    def __init__(self):
        self.browser = Browser('chrome', incognito=True, headless=False)
        self.browser.driver.set_window_size(640, 480)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.browser.__exit__(exc_type, exc_val, exc_tb)

    def get_results_from_range(self, first_game_id, last_game_id):
        # TODO: Gracefully handle a page not existing, and keep a tally of which don't.
        game_results = []
        for game_id in tqdm(range(first_game_id, last_game_id + 1)):

            url = 'https://play.esea.net/match/{}'.format(game_id)

            self.browser.visit(url)

            # todo: check page type
            page_type = identify_page_type(self.browser)
            logger.info(f"Beginning url {url}, type {page_type} detected.")

            if page_type == BASELINE_GAME_PAGE:
                this_page_data = parse_baseline_gamepage(self.browser)
                game_results.append(this_page_data)

            elif page_type == GAME_PAGE_WITH_MATCH_RECAP:
                logger.info(f"Page type scraper not written")
                # game_results.append(this_page_data)

            elif page_type == INVALID_GAME_PAGE:
                logger.info(f"Page type scraper not written")
                # TODO: add to some counter here

        return game_results


def identify_page_type(page):
    if page.is_text_present("Invalid Match"):
        return INVALID_GAME_PAGE
    elif page.is_text_present("Detailed advanced match statistics were not processed for this match"):
        return BASELINE_GAME_PAGE
    elif page.is_text_present("Match Recap"):
        return GAME_PAGE_WITH_MATCH_RECAP
    else:
        raise Exception("Page type isn't recognized")


def main():
    logger.info("Beginning command main()")

    # search_for_page_range_lower()  # 12155511 is first existing
    # search_for_page_range_upper()  # 14394641 is the last existing

    # 0/100 in this range had data..
    # first_game_id = 10155511
    # last_game_id = 10155511 + 100

    first_game_id = 14633571

    # first_game_id = 14633572  # no data found here
    # browser.is_text_present('Invalid Match')


    last_game_id = 14633571 + 2

    # https://play.esea.net/users/13155511


    # print("timing for the old way:")
    # visit_range_old_way(first_game_id, last_game_id)
    # Around 4 seconds per page.

    logger.info("timing for the new way:")
    results = []
    with GamePage() as scraper:
        results = scraper.get_results_from_range(first_game_id, last_game_id)

    # for result in results:
    #     if result:
    #         team_a_players, team_b_players = result
    #         print(list(map(str, team_a_players)))
    #         print(list(map(str, team_b_players)))
    #     else:
    #         print(result)

    n_with_data = len([r for r in results if r])
    n = len(results)

    if n_with_data:
        print("{0:.2f}.  {1} out of {2} had data.".format(
            n_with_data/n, n_with_data, n))
    else:
        print("no data")


class Command(BaseCommand):
    help = 'Import match data from esea'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):

        logger.info("info message")
        main()
