db = pymysql.connect(host='localhost', user='root', password='123456', port=3306,db='softwore')
cursor = db.cursor()
table = 'gittop10'

sql1 = "select * from gittop10"   #展示所有信息
sql2 = "select * from gittop10 where BookName like 'C%'"  #模糊查询
sql3 = "delete from gittop10 where BookName = 'JavaScript高级程序设计 第4版(图灵出品'"

try:
    cursor.execute(sql2)
    results = cursor.fetchall()
    print("Price","    " ,"Comment","    " , "BookName")
    print()
    for row in results:
        price = row[0]
        comment = row[1]
        bookname = row[2]
        
        
        print(price,"    " ,comment,"    " , bookname)
    

except:
    print ("Error: unable to fecth data")
