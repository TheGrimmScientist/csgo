import sys
from pathlib import Path
from time import sleep
import datetime
from contextlib import closing
import logging

from splinter.exceptions import ElementDoesNotExist
from tqdm import tqdm
import chromedriver_binary
from splinter import Browser
import concurrent.futures
import asyncio
import functools


sys.path.append(str(Path(__file__).parent / 'chromedriver'))


def get_team_scores(browser):

    team_a_score = browser.find_by_xpath(r'//*[@id="root"]/div/div[2]/div[2]/div[1]/div/div[1]/div[2]/div[1]/div[1]/span[2]').first.text
    team_b_score = browser.find_by_xpath(r'//*[@id="root"]/div/div[2]/div[2]/div[1]/div/div[1]/div[2]/div[4]/div[1]/span[2]').first.text
    return team_a_score, team_b_score


class PlayerStats():

    link_base = r"https://play.esea.net/users/{}"

    def __init__(self, name, link, rms, kills):
        self.name = name
        self._id = link.split('/')[-1]
        self.rms = rms
        self.kills = kills

    def __str__(self):
        return "player name is: {}, player url is: {}".format(self.name, self.link)

    @property
    def link(self):
        return self.link_base.format(self._id)


def get_team_players(browser, team):
    team_players = []
    for i in range(1, 6):
        node = browser.find_by_css("#body-match-total{} > tr:nth-child({})".format(team, i))
        cells = node.find_by_tag('td')
        name = cells[0].text
        rms = cells[1].text
        kills = cells[2].text
        url = cells.first.find_by_tag('a').last['href']
        team_players.append(PlayerStats(name, url, rms, kills))

    return team_players


def parse_game_page(browser, esea_url):
    browser.visit(esea_url)

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
        self.browser = Browser('chrome', incognito=True, headless=True)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.browser.__exit__(exc_type, exc_val, exc_tb)

    def visit_range(self, first_game_id, last_game_id):
        for game_id in tqdm(range(first_game_id, last_game_id + 1)):
            self.browser.visit('https://play.esea.net/match/{}'.format(game_id))

    def get_results_from_range(self, first_game_id, last_game_id):
        # TODO: Gracefully handle a page not existing, and keep a tally of which don't.
        results = []
        for game_id in tqdm(range(first_game_id, last_game_id + 1)):
            url = 'https://play.esea.net/match/{}'.format(game_id)
            this_page_data = self.parse_game_page(url)
            results.append(this_page_data)
            print()
        return results

    def parse_game_page(self, url):
        try:
            page_results = parse_game_page(self.browser, url)
        except ElementDoesNotExist:
            # splinter.exceptions.ElementDoesNotExist: no elements could be found with css "#body-match-stats > table:nth-child(2) > tbody > tr:nth-child(2) > td:nth-child(5)"
            page_results = False

        return page_results


def visit_range_old_way(first_game_id, last_game_id):
    for game_id in tqdm(range(first_game_id, last_game_id + 1)):
        check_if_game_page_exists(game_id)


def handle_game_id(game_id):
    with GamePage() as scraper:
        url = 'https://play.esea.net/match/{}'.format(game_id)
        this_page_data = scraper.parse_game_page(url)
        print(this_page_data)


if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        format='%(threadName)10s %(name)18s: %(message)s',
        stream=sys.stderr,
    )

    # search_for_page_range_lower()  # 12155511 is first existing
    # search_for_page_range_upper()  # 14394641 is the last existing

    # 0/100 in this range had data..
    # first_game_id = 10155511
    # last_game_id = 10155511 + 100
    first_game_id = 14633571
    last_game_id = 14633571 + 10

    # https://play.esea.net/users/13155511


    # print("timing for the old way:")
    # visit_range_old_way(first_game_id, last_game_id)
    # Around 4 seconds per page.

    print("timing for the new way:")
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

