from selenium import webdriver
from time import sleep
import re
import requests
import lxml.html
import pymysql


browser = webdriver.Chrome()
browser.get( "https://search.jd.com/Search?keyword=%E7%BC%96%E7%A8%8B%E4%B9%A6%E7%B1%8D&wq=%E7%BC%96%E7%A8%8B%E4%B9%A6%E7%B1%8D&psort=3&click=1")  # 打开网页
sleep(3)
html = browser.page_source  # 网页源代码

print(html)




#连接数据库
db = pymysql.connect(
        host="localhost",
        user="root",
        password="123456",
        charset="utf8")
cursor = db.cursor()
cursor. execute('SELECT VERSION()')
data = cursor.fetchone()
cursor.execute("CREATE DATABASE TOP10_1 DEFAULT CHARACTER SET utf8")

#创建表
db = pymysql.connect(
        host="localhost",
        user="root",
        password="123456",
        database="top10_1",
        charset="utf8")
cursor = db.cursor()
sql='CREATE TABLE IF NOT EXISTS gittop10(Price VARCHAR(255) NOT NULL, Comment VARCHAR(255) NOT NULL, BookName VARCHAR(255) NOT NULL)'
cursor.execute(sql)        




#价格
pattern = re.compile('<li.*?<strong.*?<em>.*?<i>(.*?)</i>.*?</strong>.*?</li>', re.S)
Price = re.findall(pattern,html)

print(Price)


#书名
pattern = re.compile('<li.*?<div class="p-name".*?<a target=.*?<em>(.*?)</em>.*?</a>.*?</li>', re.S)
BookName = re.findall(pattern,html)

print(BookName)




#评价数
pattern = re.compile('<li.*?<div class="p-commit".*?<strong>.*?<a.*?>(.*?)</a>.*?</strong>.*?<em>.*?</em>.*?</a>.*?</li>', re.S)
Comment = re.findall(pattern,html)

print(Comment)



resultList = []
for i in range(10):
    data = {}
    data["Price"] = Price[i]
    data["Comment"] = Comment[i] 
    data["BookName"] = BookName[i]
    resultList.append(data)
    #print(data)
#print(resultList)




# 逐条 插入数据
for i in range(10):
    # print("插入第：",i)
    Data = resultList[i]
    # print(Data)
    db = pymysql.connect(host='localhost', user='root', password='123456', port=3306,db='top10_1')
    cursor = db.cursor()
    table = 'gittop10'
    keys = ', '.join(Data.keys())
    values = ', '.join(['%s'] * len(Data))
    sql = 'INSERT INTO {table}({keys}) VALUES ({values})'.format(table=table, keys=keys, values=values)
    try:
       cursor.execute(sql, tuple(Data.values()))
       db.commit()
    except:
        db.rollback()





