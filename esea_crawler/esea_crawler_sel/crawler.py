import sys
from pathlib import Path
from time import sleep

from splinter import Browser

sys.path.append(Path(__file__).parent)


with Browser("chrome") as browser:
    url = 'http://www.google.com'
    esea_url = 'https://play.esea.net/match/14255802'
    browser.visit(esea_url)

    count = 0
    while not browser.is_element_not_present_by_css('Team A Statistics', wait_time=2):
        print('waiting')


    thing = browser.find_by_text('Team A Statistics')
    print(thing.first)

    # print(browser.find_element_by_text('Team A Statistics'))

    # for s in range(5):
    # sleep(5)
    # print(browser.html)

        # thing = browser.find_by_css('.body')
        # print(type(thing))
        # print(thing)
        # for i, t in enumerate(thing):
        #     print(i)
        #     print(t)
        #     print(type(t))
