from flask import Flask,render_template,request,redirect,url_for
import pymysql
import time
import markdown


def vender_markdown(txt):
	return markdown.markdown(txt)


app=Flask(__name__)
app.debug=True

app.jinja_env.globals.update(vender_markdown=vender_markdown)





def connect_mysql():
	db=pymysql.connect('localhost','root','root','test_blog')
	return db

def operate_mysql(sql):  #定义除了查询外的数据库操作，增，删，改
	print(sql)
	db=connect_mysql()
	print('connect sql success')
	cursor=db.cursor()	
	try:
		cursor.execute(sql)
		db.commit() #执行SQL语句	
		print('operate sql success')	
	except:
		db.rollback()
		print('operate failed')
		db.close()

def mysql_select_all(sql):     #查询所有符合条件的数据
	print(sql)
	db=connect_mysql()
	print('connect sql success')
	cursor=db.cursor()
	try:
		cursor.execute(sql)
		print('select all success')
		results=cursor.fetchall()
		return results
	except:
		print('Error:unable to fecth data')
		db.close()

def mysql_select_one(sql):   #查询某一条数据
	print(sql)
	db=connect_mysql()
	print('connect success')
	cursor=db.cursor()
	try:
		cursor.execute(sql)
		result=cursor.fetchone()
		print('select one success')
		return result
	except:
		print('Error:unable to fecth data')
		db.close()

##自定义过滤器
@app.template_filter('split')
def split_string(string):
	lists=string.split(' ')
	return lists


@app.route('/')
def index():
	sql='select * from articals order by id DESC;'
	datas=mysql_select_all(sql)   #这时得到的datas是元祖形式,比如(('title1',datetime.datetime(2019,8,18,20,23,25)),('title2',datetime.datetime(2019,8,18,20,23,25)))
	print(datas)
	return render_template('home_page.html',datas=datas)

@app.route('/<tag_name>')
def index_by_tag(tag_name):
	tag=tag_name
	print(tag)
	sql='select * from articals where tag like "%'+tag+'%" order by id DESC;'
	print(sql)
	datas=mysql_select_all(sql)   #这时得到的datas是元祖形式,比如(('title1',datetime.datetime(2019,8,18,20,23,25)),('title2',datetime.datetime(2019,8,18,20,23,25)))
	print(datas)
	return render_template('home_page.html',datas=datas)


@app.route('/create',methods=['GET','POST'])
def create():
	if request.method=='POST':
		title=request.form['title']
		body=request.form['body']
		tag=request.form['tag']
		sql_insert='insert into articals(title,body,time,tag)values(\'%s\',\'%s\',now(),\'%s\');' %(title,body,tag)
		operate_mysql(sql_insert)
		print('提交成功')
		sql_get_id='select id from articals where title=%s;' %title
		pid=operate_mysql(sql_get_id)
		print(pid)
		return redirect( url_for('index') )
	return render_template('create_page.html')


@app.route('/edit/<pid>',methods=['GET','POST'])
def edit(pid):
	if request.method=='POST':
		title=request.form['title']
		body=request.form['body']
		tag=request.form['tag']
		sql_update='update  articals set title="%s",body="%s",time=now(),tag="%s" where id="%s"' %(title,body,tag,pid)
		operate_mysql(sql_update)
		print('编辑提交成功')
		return redirect( url_for('index') )
	else:
		sql='select * from articals where id=%s' %pid
		data=mysql_select_one(sql);
		print(data)
		return render_template('edit_page.html',data=data)

@app.route('/details/<pid>')
def details(pid):
	sql='select * from articals where id=%s' %pid
	data=mysql_select_one(sql)
	return render_template('details_page.html',data=data)


@app.route('/delete/<pid>')
def delete(pid):
	sql='delete from articals where id=%s' %pid
	operate_mysql(sql)
	return redirect( url_for('index') )

@app.route('/',methods=['GET','POST'])
def search():
	if request.method=='POST':
		keywords=request.form['search']
		if keywords:
			sql='select * from articals where title like "%'+keywords+'%" order by id DESC;'
			print(sql)
			datas=mysql_select_all(sql)   #这时得到的datas是元祖形式,比如(('title1',datetime.datetime(2019,8,18,20,23,25)),('title2',datetime.datetime(2019,8,18,20,23,25)))
			print(datas)
			return render_template('home_page.html',datas=datas)
		else:
			return '搜索内容不能为空'
	return redirect(url_for('index'))

if __name__=='__main__':
	app.run()

