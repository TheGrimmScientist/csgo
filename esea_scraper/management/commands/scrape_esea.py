import sys
import datetime
import logging

from django.core.management.base import BaseCommand, CommandError
from splinter.exceptions import ElementDoesNotExist
from tqdm import tqdm
import chromedriver_binary
from splinter import Browser

# sys.path.append(str(Path(__file__).parent / 'chromedriver'))
from csranker.settings import INVALID_GAME_PAGE, GAME_PAGE_WITH_MATCH_RECAP, \
    BASELINE_GAME_PAGE

logger = logging.getLogger(__name__)


def get_team_scores(browser):

    team_a_score = browser.find_by_xpath(r'//*[@id="root"]/main/div[2]/div/div/div/div[3]/div[1]/table/tbody/tr[1]/td[2]').first.text
    team_b_score = browser.find_by_xpath(r'//*[@id="root"]/main/div[2]/div/div/div/div[3]/div[1]/table/tbody/tr[2]/td[2]').first.text

    return team_a_score, team_b_score


class PlayerStats():

    link_base = r"https://play.esea.net/users/{}"

    def __init__(self, name, link, rms, kills):
        self.name = name
        self._id = link.split('/')[-1]
        self.rms = rms
        self.kills = kills


    def __repr__(self):
        return "player name is: {}, player url is: {}".format(self.name, self.link)


    def __str__(self):
        return "player name is: {}, player url is: {}".format(self.name, self.link)

    @property
    def link(self):
        return self.link_base.format(self._id)


def get_team_players(browser, team):
    team_players = []


    for i in range(1, 6):  # 5 players, one indexed

        node = browser.find_by_css(f"#root > main > div> div > div > div > div:nth-child(4) > div > table > tbody:nth-child({team*2}) > tr:nth-child({i})")
        cells = node.find_by_tag('td')
        name = cells[0].text
        rms = cells[1].text
        kills = cells[2].text
        url = cells.first.find_by_tag('a').last['href']
        team_players.append(PlayerStats(name, url, rms, kills))

    logger.info(team_players)
    return team_players


def parse_baseline_gampage(browser):
    team_a_score, team_b_score = get_team_scores(browser)
    print(team_a_score, team_b_score)
    team_a_players = get_team_players(browser, 1)
    team_b_players = get_team_players(browser, 2)

    return team_a_players, team_b_players


def search_for_page_range_lower(starting=12255802):
    """
    12155511 is the first game that exists
    """

    current = starting
    step = starting // 2
    # TODO: Still need to find highest

    while step:
        page_exists = check_if_game_page_exists(str(current))
        if page_exists:
            current -= step
        else:
            current += step

        step = step // 2
        print(datetime.datetime.now())

    print(current)


def search_for_page_range_upper():
    """
    14394641 is the last game that exists
    """

    current = 14255802
    upper = 16155511

    step = (upper - current) // 2
    # TODO: Still need to find highest

    while step:
        page_exists = check_if_game_page_exists(str(current))
        if page_exists:
            current += step
        else:
            current -= step

        step = step // 2
        print('step size {}, game_id {}, exists {}'.format(step, current, page_exists))

    print("final: {}".format(current))


def timeit(func):
    def wrapper(*args, **kwargs):
        print("starting function: {}".format(func.__name__))
        start_time = datetime.datetime.now()
        ret = func(*args, **kwargs)
        print("completed, total time: {}".format(datetime.datetime.now() - start_time))
        return ret
    return wrapper


# @timeit
def check_if_game_page_exists(game_id):
    with Browser('chrome', incognito=True) as browser:
        browser.visit('https://play.esea.net/match/{}'.format(game_id))
        flag = len(browser.find_by_text('Invalid parent item')) == 0

    return flag


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
        results = []
        for game_id in tqdm(range(first_game_id, last_game_id + 1)):

            url = 'https://play.esea.net/match/{}'.format(game_id)
            logger.info(f"beginning url: {url}")

            self.browser.visit(url)

            # todo: check page type
            identify_page_type(self.browser)

            this_page_data = parse_baseline_gampage(self.browser)
            results.append(this_page_data)
            print(this_page_data)
        return results



def visit_range_old_way(first_game_id, last_game_id):
    for game_id in tqdm(range(first_game_id, last_game_id + 1)):
        check_if_game_page_exists(game_id)


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
