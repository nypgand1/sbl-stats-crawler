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
            game_result_dict = dict(self.parse_game_result_row(r))
            yield game_result_dict


    def parse_game_result_row(self, row):
        cols = row.find_all('td')

        for i, c in enumerate(cols):
            key = const.game_result_headers[i]

            if key is 'num' or key is 'time':
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
                away_score = int(score_list[0])
                home_score = int(score_list[1])
                href = c.find('a')['href']
                
                yield 'away_score', away_score
                yield 'home_score', home_score
                yield 'href', href


    def sum_game_result(self, game_result_dict_list):
        standing_dict_dict = dict()

        for g in game_result_dict_list:
            standing_dict_dict = self.update_standing_dict_dict(standing_dict_dict, g, is_home_tm=True)
            standing_dict_dict = self.update_standing_dict_dict(standing_dict_dict, g, is_home_tm=False)

        standing_dict_dict = self.average_point_per_game(standing_dict_dict)

        for s in standing_dict_dict.values():
            print s


    def average_point_per_game(self, standing_dict_dict):
        new_standing_dict_dict = dict()

        for k, s in standing_dict_dict.iteritems():
        
            standing_dict = dict(s)
            game_count = float(standing_dict['W'] + standing_dict['L'])

            standing_dict['PF'] = round((standing_dict['PF'] / game_count) , 1)
            standing_dict['PA'] = round((standing_dict['PA'] / game_count) , 1) 
        
            new_standing_dict_dict[k] = standing_dict

        return new_standing_dict_dict


    def update_standing_dict_dict(self, standing_dict_dict, game_result_dict, is_home_tm):
        if is_home_tm:
            we, opp = 'home', 'away'
        else: 
            we, opp = 'away', 'home'

        we_tm = game_result_dict[we + '_tm']
        we_tm_id = game_result_dict[we + '_tm_id']

        we_standing_dict = standing_dict_dict.get(we_tm_id, {'tm': we_tm, 'tm_id': we_tm_id})
        we_standing_dict = dict(self.update_standing_dict(we_standing_dict, game_result_dict, we, opp))
        
        new_standing_dict_dict = dict(standing_dict_dict)
        new_standing_dict_dict[we_tm_id] = we_standing_dict

        return new_standing_dict_dict


    def update_standing_dict(self, standing_dict, game_result_dict, we, opp):
        yield 'tm', standing_dict['tm'] 
        yield 'tm_id', standing_dict['tm_id'] 

        we_score =  game_result_dict[we + '_score']
        opp_score = game_result_dict[opp + '_score']
        is_win =  we_score > opp_score

        if is_win:
            yield 'W', standing_dict.get('W', 0) + 1
            yield 'L', standing_dict.get('L', 0)
        else:
            yield 'W', standing_dict.get('W', 0)
            yield 'L', standing_dict.get('L', 0) + 1

        yield 'STR', dict(self.update_streak(standing_dict.get('STR', {'is_win': True, 'roll': 0}), is_win))

        opp_tm = game_result_dict[opp + '_tm']
        opp_tm_id = game_result_dict[opp + '_tm_id']
        yield 'VS', self.update_vs(standing_dict.get('VS', dict()), opp_tm, opp_tm_id, is_win, game_result_dict['num'])

        yield 'PF', standing_dict.get('PF', 0) + we_score
        yield 'PA', standing_dict.get('PA', 0) + opp_score


    def update_streak(self, streak, is_win):
        yield 'is_win', is_win

        if streak['is_win'] is is_win:
            yield 'roll', streak['roll'] + 1
        else:
            yield 'roll', 1


    def update_vs(self, vs, opp_tm, opp_tm_id ,is_win, num):
        vs_opp = vs.get(opp_tm_id, {'tm': opp_tm, 'W': 0, 'L': 0})

        if is_win:
            vs_opp['W'] = vs_opp['W'] + 1
        else:
            vs_opp['L'] = vs_opp['L'] + 1

        vs[opp_tm_id] = vs_opp
        return vs

