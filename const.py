# coding=UTF-8


########## league, season, stage id_table ##########

league_id_table = {'SBL': 13, 'WSBL': 14}

sbl_stage_id_table = {
    '01': {'regular': 240, 'post': 241},
    '02': {'regular': 250, 'post': 251},
    '03': {'regular': 260, 'post': 261},
    '04': {'regular': 258, 'post': 259},
    '05': {'regular': 169, 'post': 172},
    '06': {'regular': 244, 'post': 245},
    '07': {'regular': 248, 'post': 249},
    '08': {'regular': 224, 'post': 264},
    '09': {'regular': 266, 'post': 268},
    '10': {'regular': 266, 'post': 268},
    '11': {'regular': 279, 'post': 281},
    '12': {'regular': 284}
}

stage_id_table = {'SBL': sbl_stage_id_table}


########## team_id_table ##########

sbl_12_team_id_table = {
    u'台灣啤酒': 'tm_01', 
    u'新北裕隆': 'tm_02', 
    u'金門酒廠': 'tm_03', 
    u'富邦勇士': 'tm_04', 
    u'臺中璞園': 'tm_05', 
    u'臺北達欣': 'tm_06', 
    u'臺灣銀行': 'tm_07' 
}

team_id_table = {
    'SBL': {
        '12': sbl_12_team_id_table
    }    
}


########## arena_id_table, arena_name_table ##########

sbl_12_arena_id_table = {
    u'新莊體育館':      'ar_01', 
    u'彰化':            'ar_02',
    u'新竹市立體育館':  'ar_03',
    u'台中':            'ar_04',
    u'花蓮':            'ar_05'
}

arena_id_table = {
    'SBL': {
        '12': sbl_12_arena_id_table
    }    
}

arena_name_table = {
    'ar_01': u'新莊體育館', 
    'ar_02': u'彰化縣立體育館',
    'ar_03': u'新竹市立體育館',
    'ar_04': u'台中台體大體育館',
    'ar_05': u'花蓮德興小巨蛋'
}

########## game_result_headers ##########


game_result_headers = ['num', 'time', 'arena', 'away_tm', 'home_tm', 'score']


