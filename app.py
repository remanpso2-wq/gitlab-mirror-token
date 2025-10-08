from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Flask動作確認成功！'

if __name__ == '__main__':
    app.run(debug=True)

