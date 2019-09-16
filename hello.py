from flask import Flask 
from flask import request
from flask import render_template

app=Flask(__name__)  #创建一个flask的类
app.debug=True


@app.route('/')  #定义路由。@表示修饰。'/'表示根地址，就是localhost:5000
def index():
	return 'hello world'


@app.route('/students')
def students():
	return 'chehongyu is a boy'

##url含有参数------------------
@app.route('/show/<post_id>')  
def show_post(post_id):
	return 'show %r' %post_id

@app.route('/users/<user_id>')
def show_userid(user_id):
	return 'show %r' %user_id

@app.route('/bugs/<bug_id>')
def show_bugid(bug_id):
	return 'show %r' %bug_id

@app.route('/<username>')
def user(username):
	return ('username is %r' %username)

#request-------------------------
@app.route('/search')
def search():
	return request.args.get('kw','not found')   #get请求，通过 args 属性来访问 URL 中提交的参数 （ ?key=value ）。
													#若没有kw则返回not found

#渲染html文件含变量等等-------------------
@app.route('/login',methods=['GET','POST'])
def login():   #默认是get请求

	user_name=request.args.get('user','no user')
	if request.method=='POST':
		print(request.form.to_dict())       #request.form拿到表单提交的数据。to_dict()转换为字典格式。同为mongodb存储数据格式
		return 'ok'
	else:
		return render_template('login.html',title='login',user_name=user_name)        #渲染html文件。即把html文件找到并送给客户端。其中title为html文件的变量






if __name__=='__main__':
	app.run()             #这个app只能通过在本地服务器执行，若修改app.run(host='0.0.0.0')则服务器公开化。
