import xml.etree.ElementTree as ET
from urllib import request

import requests
from django.core.management.base import BaseCommand


def main():
    """
    # Root web site:
    * https://csgo-demos-us-central1.faceit-cdn.net/

    # Game downlaod web site:
    * https://csgo-demos-us-central1.faceit-cdn.net/6650eee2-2309-4239-ad6d-2bb1f616a656.dem.gz

    """
    known_faceit_csgo_regions = [
        'us-central1',
    ]
    #
    print("hi")


class Command(BaseCommand):
    help = 'Pull New'

    def handle(self, *args, **kwargs):
        """
        TODO: Set up scrape modes:
          * Full pull
          * update new games...
          (how to tell?)
        :param args:
        :param kwargs:
        :return:
        """



        # pull xml from root site.
        # save raw

        url = 'https://csgo-demos-us-central1.faceit-cdn.net/'
        page_getted = requests.get(url)

        page_opened = request.urlopen(url)



        raw_site_as_file = None  # TODO: this is the thing that needs cached
        xml_file = None  # TODO: cache this too?


        # extract list of games and

        # root = ET.parse('thefile.xml').getroot()
        # for type_tag in root.findall('bar/type'):
        #     value = type_tag.get('foobar')
        #     print(value)


