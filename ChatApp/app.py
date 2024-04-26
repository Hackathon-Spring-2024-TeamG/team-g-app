from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'チャンネル一覧'

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=False)
