import requests


def readWebData(page, topicNum, cookie):
    header={
    "Cookie": cookie,
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.63"
    }
    url = "https://www.douban.com/group/topic/"+ topicNum + "/?start=" + str(page)
    r = requests.get(url=url,headers=header)
    data = r.content.decode('utf-8')
    return data


def createCommentInfoList(webInfo, topicNum, replyIdList, replyIdAltList, commentList, timeList):
    topicNumList = []
    for reply in webInfo:
        replyId = reply["data-author-id"]
        replyIdAlt = list(reply.find("h4"))[1].get_text()
        comment = reply.find("p", class_='reply-content').get_text()
        timestamp = reply.find("span", class_='pubtime').get_text()
        replyIdList.append(replyId)
        replyIdAltList.append(replyIdAlt)
        commentList.append(comment)
        timeList.append(timestamp)
        topicNumList.append(topicNum)
    return replyIdList, replyIdAltList, commentList, timeList, topicNumList