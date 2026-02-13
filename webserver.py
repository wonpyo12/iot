from flask import Flask
from flask import request
from makrupsafe import escape
app=Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/hello')
def index():
    name = request.args.get("name","Flask")
    return {f"Hello,{escape(name)}"}

if __name__ == '__main__':
    app.run(host='localhost', port=8080,debug=True)