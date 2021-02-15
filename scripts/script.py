import requests
import pandas as pd
import mysql.connector
from mysql.connector import errorcode

def readWebData(page, entityNum, cookie, info):
    header={
    "Cookie": cookie,
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.63"
    }
    if info == "comment":
        url = "https://www.douban.com/group/topic/"+ entityNum + "/?start=" + str(page)
    elif info == "member":
        url = "https://www.douban.com/group/"+ entityNum + "/members?start=" + str(page)

    r = requests.get(url=url,headers=header)
    print('正在处理: %s' % url)
    statusCode(r)
    data = r.content.decode('utf-8')
    return data


def createCommentInfoList(webInfo, topicNum, cursor):
    for reply in webInfo:
        replyId = reply["data-author-id"]
        replyIdAlt = list(reply.find("h4"))[1].get_text()
        comment = reply.find("p", class_='reply-content').get_text()
        timestamp = reply.find("span", class_='pubtime').get_text()

        print('Member Name: %s' % replyIdAlt)
        print('Member Comment: %s' % comment)

        sql = "INSERT IGNORE INTO comment (userID, commentTxt, topicNum, commentTime) VALUES (%s, %s, %s, %s)"
        val = (replyId, comment, topicNum, timestamp)
        cursor.execute(sql, val)


def statusCode(response):
    if response.status_code == 200:
        print('抓取成功!')
    elif response.status_code == 404:
        print('抓取失败.')


def createMemInfoList(memberInfo, cursor, conn, entityNum):
    for member in memberInfo:
        memberIdAlt = member.find("a", class_='').get_text()
        memberIdUrl = member.find("a", class_='')['href']
        print('Member Name: %s' % memberIdAlt)
        print('Member URL: %s' % memberIdUrl)

        sql = "INSERT IGNORE INTO userGroup (userID, userAlt, groupNum) VALUES (%s, %s, %s)"
        val = (memberIdUrl[30:-1], memberIdAlt, entityNum)
        cursor.execute(sql, val)


def processUserId(memberIdUrlList):
    memberId = []
    for url in memberIdUrlList:
        memberId.append(url[30:-1])
    dataframe = pd.DataFrame(list(zip(memberId)), 
                columns =['UserID'])

    dataframe = dataframe.drop_duplicates()
    recordCount = len(dataframe)
    print("一共有%d个用户关注这个小组。" % recordCount)
    return dataframe