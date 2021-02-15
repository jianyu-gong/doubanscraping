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

# 每个帖子回复的用户数
SELECT TopicNum, count(distinct UserId)
FROM comment
GROUP BY TopicNum

# top 20的回帖数
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

# ddl
CREATE DATABASE douban;
DROP TABLE user;
ALTER DATABASE douban CHARACTER SET = utf8mb4 COLLATE = utf8mb4_bin;
create table user (userID VARCHAR(50), 
                   userAlt varchar(255), 
                   PRIMARY KEY (userID)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE utf8mb4_bin;