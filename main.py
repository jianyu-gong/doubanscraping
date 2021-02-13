import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from scripts.script import readWebData, createCommentInfoList, createMemInfoList
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

entityNum = "634189"

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

for page in range(0, 1000, 35):
    data = readWebData(page, entityNum, cookie, info="member")
    soup = BeautifulSoup(data, 'html.parser')
    memberInfo = soup.find_all('div', class_='name')
    if len(memberInfo) == 0:
        print("返回零个记录，需要登录验证。")
        break
    createMemInfoList(memberInfo, cursor, conn)
    sleep(2.0)
    
print(cursor.rowcount, "records inserted.")
conn.commit()
cursor.close()
conn.close()
