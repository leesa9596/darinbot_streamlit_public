
import os
import json
import pandas as pd
from datetime import datetime
import sqlalchemy as sa
from dotenv import load_dotenv
import requests
load_dotenv()
'''
24 FBI
35 기관추적
36 밴드브레이커
37 히트앤런
38 배당선호
47 prime time
48 밸류가이드
49 빅쇼트
50 main pick
51 볼케이노
52 터닝포인트
'''

class masterMsg:
    def __init__(self):
        self.api_url = "https://cms.tudal.co.kr/master-feeds?token=xnwkdmlekfdlsuser@020"

    def all(self, masterId, todayDate):
        r = requests.get(self.api_url + f"&master={masterId}&created_at_gt={todayDate}&_sort=created_at:ASC")
        master_msg = r.json()
        
        return len(master_msg)
    
    def save_msg_db(self):
        darinbot_str = darinbot_str='mysql+pymysql://admin:dlshvls22@tudalus.c418xgpmd0xv.ap-northeast-2.rds.amazonaws.com/darinbot'
        engine = sa.create_engine(darinbot_str)
        
        connection = engine.connect()
        metadata = sa.MetaData()
        table = sa.Table('r_msg_count', metadata, autoload=True, autoload_with=engine)


        masterDict = {'24':'FBI','35':'기관추적','36':'밴드브레이커','37':'히트앤런','38':'배당선호',
                      '47':'PRIME TIME','48':'밸류가이드','49':'빅쇼트','50':'MAIN PICK',
                      '51':'볼케이노','52':'터닝포인트'}
        todayDate = datetime.now().strftime("%Y-%m-%dT00:00:00.000Z")
        for masterId in masterDict.keys():
            numMsg = self.all(masterId, todayDate)
            
            query = sa.insert(table).values(masterId=masterId, masterNickname=masterDict[masterId], numMsg =numMsg, createdTime=datetime.now())
            result = connection.execute(query)
            result.close()

if __name__ == '__main__':
    masterMsg().save_msg_db()