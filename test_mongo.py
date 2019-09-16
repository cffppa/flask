from pymongo import MongoClient

conn=MongoClient('localhost',27017)
db=conn.test

bug={'title':'can not open chrome','content':'when i open chrome,it is down'}
db.bugs.insert(bug)

#print (db.bugs.findOne())   #把表bugs最新的一条记录找到并打印


for i in range(0,11):
	bug={'title':'bug'+str(i),'content':'this is bug '+str(i)}
	db.bugs.insert(bug)

print(db.bugs.count())

bugs=db.bugs.find()
for bug in bugs:
	print (bug)