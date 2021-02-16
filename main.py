import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from scripts.script import readWebData, createCommentInfoList, createMemInfoList, createMemberJoinedGroup, createTagInfo
from time import sleep
from mysql.connector import errorcode
import mysql.connector
import configparser

config = configparser.ConfigParser()
config.read("config/config.txt")

host = config.get("configuration","host")
cookie = config.get("configuration","cookie")
user = config.get("configuration","user")
password = config.get("configuration","password")
database = config.get("configuration","database")

topicNum = "211190218"

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
# entityNum = "634189"
# for page in range(0, 1000, 35):
#     data = readWebData(page, entityNum, cookie, info="member")
#     soup = BeautifulSoup(data, 'html.parser')
#     memberInfo = soup.find_all('div', class_='name')
#     if len(memberInfo) == 0:
#         print("返回零个记录，需要登录验证。")
#         break
#     createMemInfoList(memberInfo, cursor, entityNum)
#     sleep(2.0)

# 找到一个贴子下所有评论
# commentCount = 1
# page = 0
# while commentCount != 0:
#     data = readWebData(page, topicNum, cookie, info="comment")
#     soup = BeautifulSoup(data, 'html.parser')
#     webInfo = soup.find_all('li', class_='clearfix comment-item reply-item')
#     if len(webInfo) == 0:
#         print("返回零个记录，需要登录验证。")
#         break
#     createCommentInfoList(webInfo, topicNum, cursor)
#     commentCount = len(soup.find_all('li', class_='clearfix comment-item reply-item'))
#     page+=100
#     sleep(2.0)


# query = "SELECT DISTINCT userID FROM userGroup"
# cursor.execute(query)
# result = list(cursor.fetchall())
# userId = []
# for n in result:
#     userId.append(n[0].decode())
# print('一共有%d个组员需要处理' % len(userId))
# sleep(5.0)

# for user_id in userId:
#     data = readWebData(0, user_id, cookie, info="joinedgroup")
#     soup = BeautifulSoup(data, 'html.parser')
#     joinedGroupInfo = soup.find_all('div', class_='title')
#     createMemberJoinedGroup(joinedGroupInfo, cursor, user_id)
#     sleep(1.0)

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

#print(cursor.rowcount, "records inserted.")
conn.commit()
cursor.close()
conn.close()
