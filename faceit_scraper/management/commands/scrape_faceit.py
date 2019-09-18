import xml.etree.ElementTree as ET
from urllib import request

from django.core.management.base import BaseCommand
from django.utils import timezone


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
        site = request.urlopen()

        # extract list of games and


        root = ET.parse('thefile.xml').getroot()
        for type_tag in root.findall('bar/type'):
            value = type_tag.get('foobar')
            print(value)
        self.stdout.write("It's now %s" % time)


