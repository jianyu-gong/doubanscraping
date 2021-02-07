import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from scripts.script import readWebData, createInfoList

Cookie =  """
          """

#topicList = ["210473494", "210307098", "209967593", "207670339", "205580605"] 人才组
#topicList = ["207768078", "207132337", "204671016", "202811686"] #彩虹组
topicList = ["203676948", "204807786"] # 草原
#topicList = ["210425155", "210131057", "210045682", "209681866", "209683935", "210036469", "208660469"]
#topicList = ["210047900", "210660661"]

replyIdList = []
replyIdAltList = []
commentList = []
timeList = []
topicNumList = []


for topicNum in topicList:
    page = 0
    commentCount = 1
    while commentCount != 0:
        data = readWebData(page, topicNum, Cookie)
        soup = BeautifulSoup(data, 'html.parser')
        webInfo = soup.find_all('li', class_='clearfix comment-item reply-item')
        replyIdList, replyIdListAltList, commentList, timeList, topicNumList = createInfoList(webInfo, replyIdList, replyIdAltList, commentList, timeList,topicNum, topicNumList)
        commentCount = len(soup.find_all('li', class_='clearfix comment-item reply-item'))
        page+=100


commentDf = pd.DataFrame(list(zip(topicNumList, replyIdList, replyIdListAltList, commentList, timeList)), 
               columns =['TopicNum','UserId', 'UserAltName', 'Comment', 'TimePublished'])

commentDf = commentDf.drop_duplicates()
userIdDf = commentDf.drop_duplicates(['UserId','UserAltName'])[['UserId', 'UserAltName']]
countDf = commentDf.groupby(['UserId']).count().sort_values(['Comment'], ascending=False).reset_index()

countSummaryDf = pd.merge(countDf, userIdDf, on="UserId")[["UserId", "UserAltName_y", "Comment"]]
countSummaryDf = countSummaryDf.rename(columns={"UserId": "用户名", "UserAltName_y": "用户昵称", "Comment": "评论数"})