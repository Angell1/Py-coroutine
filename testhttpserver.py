from flask import Flask
import time
app = Flask(__name__)


@app.route('/bar')
def bar():
    time.sleep(1)
    return '<h1>bar!</h1>'

@app.route('/foo')
def foo():
    time.sleep(1)
    return '<h1>foo!</h1>'
if __name__ == '__main__':
    app.run(host='127.0.0.1',port=5555,debug=True)