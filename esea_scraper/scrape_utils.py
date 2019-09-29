"""
All of this was to originally check page indices and also find the lowest index
to start scraping.
"""
import datetime

from splinter import Browser
from tqdm import tqdm


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

def visit_range_old_way(first_game_id, last_game_id):
    for game_id in tqdm(range(first_game_id, last_game_id + 1)):
        check_if_game_page_exists(game_id)
