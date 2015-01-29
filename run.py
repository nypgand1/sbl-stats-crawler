from time import sleep

import settings
from crawler import SblCrawler

IS_DEBUG = settings.IS_DEBUG
IS_PARSE_ONLY = settings.IS_PARSE_ONLY

UPDATE_INTERVAL_MIN = settings.UPDATE_INTERVAL_MIN

while(True):
    try:
        sbl_crawler = SblCrawler(league='SBL', season='12-reg', is_debug=IS_DEBUG, is_parse_only=IS_PARSE_ONLY)
        sbl_crawler.start()
    
        sleep(UPDATE_INTERVAL_MIN * 60)
    except:
        if IS_DEBUG:
            raise
            break
        else:
            pass

