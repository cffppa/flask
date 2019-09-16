from flask import Flask 

app=Flask(__name__)
app.debug=True #进入调试模式。代码有变更会自动重启服务器。

@app.route('/')
def hello():
	return 'hello world'

@app.route('/login')
def login():
	return 'login'

@app.route('/logout')
def logout():
	return 'logout'

@app.route('/hello')
def hello_2():
	return 'this is route hello '

if __name__=='__main__':

	app.run()