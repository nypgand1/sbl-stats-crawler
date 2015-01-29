# coding=UTF-8

from bs4 import BeautifulSoup

import const
import settings

class SblStandingsParser():
    def __init__(self, league, season, stage, is_debug=False):
        self.league = league
        self.season = season
        self.stage = stage
    
        self.is_debug = is_debug

    def is_game_result_row(self, css_class):
        return css_class in ['row_01', 'row_02']


    def parse_standings(self, html_doc):
        soup = BeautifulSoup(html_doc)
        table = soup.find(id='StageMatchListTable')

        if table:
            return self.parse_game_result_table(table)
        else:
            return list()

 
    def parse_game_result_table(self, table):
        rows = table.find_all(class_=self.is_game_result_row)

        for r in rows:
            game_result_dict = { key: value for key, value in self.parse_game_result_row(r)}
            print game_result_dict

        return


    def parse_game_result_row(self, row):
        cols = row.find_all('td')

        for i, c in enumerate(cols):
            key = const.game_result_headers[i]

            if key is 'game_num' or key is 'time':
                yield key, c.get_text().encode('ascii')

            elif key is 'score':
                score_list = c.get_text().encode(settings.ENCODE).split(':')
                away_score = score_list[0]
                home_score = score_list[1]
                href = c.find('a')['href']
                
                yield 'away_score', away_score
                yield 'home_score', home_score
                yield 'href', href

            else:
                yield key, c.get_text()

