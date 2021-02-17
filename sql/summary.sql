-- create database douban;
-- use douban;
-- CREATE TABLE comment (TopicNum varchar(255), UserId varchar(255), UserAltName varchar(255), TimePublished datetime);
-- ALTER TABLE comment
-- DROP COLUMN UserAltName;
-- 截止到2021年2月6日早上5点

SELECT TopicNum, count(*)
FROM comment
GROUP BY TopicNum
ORDER BY TopicNum

-- 每个帖子回复的用户数
SELECT TopicNum, count(distinct UserId)
FROM comment
GROUP BY TopicNum

-- top 20的回帖数
SELECT b.TopicNum, sum(b.CommentCount)
FROM
(SELECT TopicNum, 
CommentCount,
row_number() OVER(PARTITION BY TopicNum ORDER BY CommentCount DESC) as row_num
FROM
(SELECT TopicNum, UserId, count(*) as CommentCount 
FROM comment
GROUP BY TopicNum, UserId
ORDER BY TopicNum, CommentCount desc) a) b
WHERE b.row_num <= 20
GROUP BY b.TopicNum

-- ddl
-- 创建douban数据库并支持中文和Emoji
CREATE DATABASE douban;
ALTER DATABASE douban CHARACTER SET = utf8mb4 COLLATE = utf8mb4_bin;

-- 创建userGroup tbl来保存一个小组的所有成员
DROP TABLE userGroup IF EXISTS;
CREATE TABLE userGroup (joinGroupID INT NOT NULL auto_increment,
             userID VARCHAR(50), 
             userAlt VARCHAR(255), 
             groupNum VARCHAR(50), 
             PRIMARY KEY (joinGroupID)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE utf8mb4_bin;

-- 创建comment tbl 来保存对贴子的所有评论
DROP TABLE comment IF EXISTS;
CREATE TABLE comment (commentID INT NOT NULL auto_increment, 
                      userID VARCHAR(50), 
                      commentTxt VARCHAR(255), 
                      topicNum VARCHAR(50), 
                      commentTime DATETIME, 
                      PRIMARY KEY (commentID)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE utf8mb4_bin;

-- 创建relation tbl 来保存对贴子的所有评论
DROP TABLE relation IF EXISTS;
CREATE TABLE relation (relationID INT NOT NULL auto_increment, 
                      userID VARCHAR(50), 
                      groupName VARCHAR(255), 
                      groupID VARCHAR(50), 
                      PRIMARY KEY (relationID)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE utf8mb4_bin;
