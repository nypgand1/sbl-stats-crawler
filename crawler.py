# coding=UTF-8

import threading
import requests

import const
from communicator import SblCommunicator
from standings_parser import SblStandingsParser

class SblCrawler(threading.Thread):
    def __init__(self, league, season, is_debug=False, is_parse_only=False):
        super(SblCrawler, self).__init__()

        self.is_parse_only = is_parse_only
        self.is_debug = is_debug

        self.communicator = SblCommunicator(league, season, is_debug)
        self.standings_parser = SblStandingsParser(league, season, is_debug)


    def run(self):
        try:
            games_result = self.communicator.get_games_result()
            self.standings_parser.parse_standings(games_result)
                
            if self.is_parse_only:
                return

        except requests.exceptions.HTTPError as e:
            print e.message


