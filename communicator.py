# coding=UTF-8

import urllib2
import requests
import json
from base64 import standard_b64encode

import const
import settings

SBL_STATS_URL = settings.SBL_STATS_URL
ENTRY_POINT = settings.ENTRY_POINT

#USERNAME = settings.USERNAME
#PASSWORD = settings.PASSWORD

#BASIC_AUTH_PLAIN = '%s:%s' % (USERNAME, PASSWORD)
#BASIC_AUTH_BASE64 = 'Basic %s' % standard_b64encode(BASIC_AUTH_PLAIN)

class SblCommunicator():
    def __init__(self, league, season, is_debug=False):
        self.league = league
        self.season = season

        self.league_id = const.league_id_table[league]
        self.season_id = const.season_id_table[league][season]

        self.is_debug = is_debug


    def pretty_print_req(self, req):
        print('{}\n{}\n{}\n\n{}'.format(
            '-----------START-----------',
            req.method + ' ' + req.url,
            '\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
            req.data
        ))


    def endpoint(self, resource, item=None):
        if item:
            return '%s/%s/%s/' % (ENTRY_POINT, resource, item)
        return '%s/%s/' % (ENTRY_POINT, resource)


    def get_games_result(self):
        payload = {'Mo': 9023, 'Type': 'basketball_stagematchlist', 'Nbr': self.season_id, 'TagName': 'bbstagematchlist', 'DivId': 'bbstagematchlist'}
        data = {'rs': 'sajaxSubmit', 'rsargs[]': '<Input><F><K></K><V></V></F></Input>'}

        r = requests.post(SBL_STATS_URL, params=payload, data=data)
        r.raise_for_status()

        return r.text

        
