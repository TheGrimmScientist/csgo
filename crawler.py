import sys
from pathlib import Path
from time import sleep
import datetime
from contextlib import closing

from tqdm import tqdm
import chromedriver_binary
from splinter import Browser


sys.path.append(str(Path(__file__).parent / 'chromedriver'))

def get_team_scores(browser):
    team_a_score = browser.find_by_css(r"#body-match-stats > table:nth-child(2) > tbody > tr:nth-child(2) > td:nth-child(5)").first.text
    team_b_score = browser.find_by_css(r"#body-match-stats > table:nth-child(2) > tbody > tr:nth-child(3) > td:nth-child(5)").first.text
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


def parse_game_page(esea_url):
    with Browser('chrome', incognito=True) as browser:

        browser.visit(esea_url)

        team_a_score, team_b_score = get_team_scores(browser)
        print("team a got: {}\nteam b got: {}".format(team_a_score, team_b_score))

        team_a_players = get_team_players(browser, 1)
        team_b_players = get_team_players(browser, 2)

        print(list(map(str, team_a_players)))
        print(list(map(str, team_b_players)))
        # thing = browser.find_by_text('Team A Statistics')
        # print(thing.first)

        # print(browser.find_element_by_text('Team A Statistics'))

        # for s in range(5):
        # sleep(5)
        # print(browser.html)

    return True

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
        self.browser = Browser('chrome', incognito=True)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.browser.__exit__(exc_type, exc_val, exc_tb)

    def visit_range(self, first_game_id, last_game_id):
        for game_id in tqdm(range(first_game_id, last_game_id + 1)):
            self.browser.visit('https://play.esea.net/match/{}'.format(game_id))


def visit_range_old_way(first_game_id, last_game_id):
    for game_id in tqdm(range(first_game_id, last_game_id+1)):
        check_if_game_page_exists(game_id)


if __name__ == "__main__":

    # search_for_page_range_lower()  # 12155511 is first existing
    # search_for_page_range_upper()  # 14394641 is the last existing

    first_game_id = 13155511
    last_game_id = 13155511 + 10

    print("timing for the old way:")
    visit_range_old_way(first_game_id, last_game_id)

    print("timing for the new way:")
    with GamePage() as scraper:
        scraper.visit_range(first_game_id, last_game_id)


    # esea_url = 'https://play.esea.net/match/14255802'
    # parse_game_page(esea_url)
