from bs4 import BeautifulSoup

import const


class SblStandingsParser():
    def __init__(self, league, season, is_debug=False):
        self.league = league
        self.season = season
    
        self.is_debug = is_debug

    def is_game_result_row(self, css_class):
        return css_class in ['row_01', 'row_02']


    def parse_standings(self, html_doc):
        soup = BeautifulSoup(html_doc)
        table = soup.find(id='StageMatchListTable')

        if table:
            return self.parse_standings_table(table)
        else:
            return list()

 
    def parse_standings_table(self, table):
        rows = table.find_all(class_=self.is_game_result_row)

        for r in rows:
            self.parse_standings_row(r)

        return

    def parse_standings_row(self, row):
        print row

        return

