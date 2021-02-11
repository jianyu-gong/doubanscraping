import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from scripts.script import readWebData, createCommentInfoList, createMemInfoList, processUserId
from time import sleep


cookie =  """bid=M8d5os6pdMc; __utmc=30149280; __utmz=30149280.1612629628.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not provided); push_doumail_num=0; __utmv=30149280.23180; ct=y; douban-profile-remind=1; ll="108120"; dbcl2="231803702:BHiciIvzZnI"; ck=q-BM; __yadk_uid=ymcyjW0WJCF8VEIKnvmnB80XfOSZfLjZ; push_noty_num=0; ap_v=0,6.0; _pk_ref.100001.8cb4=["","",1612995689,"https://www.google.com/"]; _pk_ses.100001.8cb4=*; __utma=30149280.40126775.1612629628.1612986153.1612995690.15; __utmt=1; _pk_id.100001.8cb4=a851698bf89c60d1.1612629627.15.1613000006.1612986711.; __utmb=30149280.103.5.1613000003662"""

memberIdAltList = []
memberIdUrlList = []
entityNum = '634189'

for page in range(0, 1000, 35):
    data = readWebData(page, entityNum, cookie, info="member")
    soup = BeautifulSoup(data, 'html.parser')
    memberInfo = soup.find_all('div', class_='name')
    memberIdUrlList = createMemInfoList(memberInfo, memberIdUrlList)
    sleep(2.0)

memberDf = processUserId(memberIdUrlList)
memberDf.to_csv('人才组用户名单.csv', index=False)