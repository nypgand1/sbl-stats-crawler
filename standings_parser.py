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

        self.team_id_table =  const.team_id_table[league][season]
        self.arena_id_table =  const.arena_id_table[league][season]
        
    def is_game_result_row(self, css_class):
        return css_class in ['row_01', 'row_02']


    def parse_standings(self, html_doc):
        soup = BeautifulSoup(html_doc)
        table = soup.find(id='StageMatchListTable')

        if not table:
            return None

        game_result_dict_list =  list(self.parse_game_result_table(table))
        self.sum_game_result(game_result_dict_list) 

 
    def parse_game_result_table(self, table):
        rows = table.find_all(class_=self.is_game_result_row)

        for r in rows:
            game_result_dict = { key: value for key, value in self.parse_game_result_row(r)}
            yield game_result_dict


    def parse_game_result_row(self, row):
        cols = row.find_all('td')

        for i, c in enumerate(cols):
            key = const.game_result_headers[i]

            if key is 'game_num' or key is 'time':
                yield key, c.get_text().encode('ascii')

            if key is 'arena':
                arena_orig = c.get_text().strip()

                arena_id = self.arena_id_table[arena_orig]
                arena = const.arena_name_table[arena_id]

                yield key, arena
                yield 'arena_id', arena_id

            elif key is 'away_tm':
                away_tm = c.get_text()
                yield key, away_tm
                yield 'away_tm_id', self.team_id_table[away_tm]

            elif key is 'home_tm':
                home_tm = c.get_text()
                yield key, home_tm
                yield 'home_tm_id', self.team_id_table[home_tm]

            elif key is 'score':
                score_list = c.get_text().encode(settings.ENCODE).split(':')
                away_score = score_list[0]
                home_score = score_list[1]
                href = c.find('a')['href']
                
                yield 'away_score', away_score
                yield 'home_score', home_score
                yield 'href', href


    def sum_game_result(self, game_result_dict_list):
        tm_stats_tot = dict()
        arena = list()
        for g in game_result_dict_list:
            arena.append(g['arena'].strip())

        for a in set(arena):
            print '>%s<' % a
    #def sum_tm_stats(self, tm_stats_dict, tm_id, tm_score, opp_score):

