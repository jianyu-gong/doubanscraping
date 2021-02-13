from scripts.script import readWebData, createCommentInfoList, createMemInfoList, processUserId
from time import sleep
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

def groupMemberList(entityNum, cookie):
    memberIdUrlList = []

    for page in range(0, 1000, 35):
        data = readWebData(page, entityNum, cookie, info="member")
        soup = BeautifulSoup(data, 'html.parser')
        memberInfo = soup.find_all('div', class_='name')
        memberIdUrlList = createMemInfoList(memberInfo, memberIdUrlList)
        sleep(2.0)

    memberDf = processUserId(memberIdUrlList)
    memberDf.to_csv('人才组用户名单.csv', index=False)