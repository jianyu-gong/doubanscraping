import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from scripts.script import readWebData, createCommentInfoList, createMemInfoList, createMemberJoinedGroup, createTagInfo, statusCode
from time import sleep
from mysql.connector import errorcode
import mysql.connector
import configparser
import requests

config = configparser.ConfigParser()
config.read("config/config.txt")

host = config.get("configuration","host")
cookie = config.get("configuration","cookie")
user = config.get("configuration","user")
password = config.get("configuration","password")
database = config.get("configuration","database")

#topicNum = "211190218"

# Obtain connection string information from the portal
config = {
'host': host,
'user': user,
'password': password,
'database': database,
'ssl_ca': 'config/DigiCertGlobalRootG2.crt.pem',
'charset': 'utf8mb4'
}

# Construct connection string
try:
    conn = mysql.connector.connect(**config)
    print("Connection established")
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with the user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    cursor = conn.cursor()

# 找到一个小组里的所有成员
entityNum = "702794"
for page in range(0, 7400, 35):
    data = readWebData(page, entityNum, cookie, info="member")
    soup = BeautifulSoup(data, 'html.parser')
    memberInfo = soup.find_all('div', class_='name')
    if len(memberInfo) == 0:
        print("返回零个记录，需要登录验证。")
        break
    createMemInfoList(memberInfo, cursor, entityNum)
    sleep(2.0)


query = "SELECT DISTINCT userID FROM userGroup"
cursor.execute(query)
result = list(cursor.fetchall())
userId = []
for n in result:
    userId.append(n[0].decode())
print('一共有%d个组员需要处理' % len(userId))
sleep(5.0)

for user_id in userId:
    data = readWebData(0, user_id, cookie, info="joinedgroup")
    soup = BeautifulSoup(data, 'html.parser')
    joinedGroupInfo = soup.find_all('div', class_='title')
    createMemberJoinedGroup(joinedGroupInfo, cursor, user_id)
    sleep(1.0)

query = "SELECT DISTINCT groupID FROM relation"
cursor.execute(query)
result = list(cursor.fetchall())
groupID = []
for n in result:
    groupID.append(n[0].decode())
print('一共有%d个小组需要处理' % len(groupID))
sleep(5.0)


i = 1
for group in groupID:
    print('正在处理第%d个小组...' % i)
    data = readWebData(0, group, cookie, "group")
    soup = BeautifulSoup(data, 'html.parser')
    groupInfo = soup.find('div', class_='group-board')
    createTagInfo(groupInfo, cursor, group)
    i += 1
    sleep(1.0)

print(cursor.rowcount, "records inserted.")


url = "https://api.douban.com/v2/group/706799/topics"
cookies = """bid=M8d5os6pdMc; __utmc=30149280; __utmz=30149280.1612629628.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not provided); push_doumail_num=0; __utmv=30149280.23180; ct=y; douban-profile-remind=1; ll="108120"; dbcl2="231803702:BHiciIvzZnI"; ck=q-BM; push_noty_num=0; __utma=30149280.40126775.1612629628.1612835390.1612924348.11; ap_v=0,6.0; __utmb=30149280.302.5.1612928285843"""
header={
    "Cookie": cookies,
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.63"
    }

for start in range(0, 500, 100):
    r = requests.get(url, params={'start': start, 'count': 100}, headers=header)  # api规定列表参数使用start和count
    statusCode(r)
    print('processing %s' % r.url) # 打印当前页面url
    res = r.json() # r是一个Response对象，res是一个字典，保存了响应网页的json数据
    for topic in res['topics']:
        topicID = topic['id']
        topicTitle = topic['title']
        createDate = topic['created']
        authorID = topic['author']['uid']
        content = topic['content']
        commentsCount = topic['comments_count']

        print('帖子ID: %s' % topicID)
        print('帖子标题: %s' % topicTitle)
        print('帖子创建于: %s' % createDate)
        print('帖子作者: %s' % authorID)
        print('一共有%s条评论' % commentsCount)

        sql = "INSERT IGNORE INTO topic (topicID, topicTitle, createDate, authorID, content, commentCount) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (topicID, topicTitle, createDate, authorID, content, commentsCount)
        cursor.execute(sql, val)
    sleep(4)


query = """SELECT distinct topicID FROM topic 
WHERE createDate >= '2021-02-14'
AND (topicTitle LIKE '%成毅%' OR topicTitle LIKE '%傅诗淇%' OR topicTitle LIKE '%IE%' OR topicTitle LIKE '%琉璃%' OR topicTitle LIKE '%梦醒%' OR topicTitle LIKE '%南风%' OR topicTitle LIKE '%沉香%' OR topicTitle LIKE '%李炎%' OR topicTitle LIKE '%司凤%' OR topicTitle LIKE '%云深%'
OR content LIKE '%成毅%' OR content LIKE '%傅诗淇%' OR content LIKE '%IE%' OR content LIKE '%琉璃%' OR content LIKE '%梦醒%' OR content LIKE '%南风%' OR content LIKE '%沉香%' OR content LIKE '%李炎%' OR content LIKE '%司凤%' OR content LIKE '%云深%')
"""
cursor.execute(query)
result = list(cursor.fetchall())
topicNumber = []
for n in result:
    topicNumber.append(n[0].decode())
print('一共有%d个帖子需要处理' % len(topicNumber))
sleep(5.0)


for topicNum in topicNumber:
# 找到一个贴子下所有评论
    if topicNum == '211460151':
        pass
    else:
        commentCount = 1
        page = 0
        while commentCount != 0:
            data = readWebData(page, topicNum, cookie, info="comment")
            soup = BeautifulSoup(data, 'html.parser')
            webInfo = soup.find_all('li', class_='clearfix comment-item reply-item')
            if len(webInfo) == 0:
                print("返回零个记录，需要登录验证。")
                break
            createCommentInfoList(webInfo, topicNum, cursor)
            commentCount = len(soup.find_all('li', class_='clearfix comment-item reply-item'))
            page+=100
            sleep(1.0)


conn.commit()
cursor.close()
conn.close()
print("数据全部录入完毕。")
