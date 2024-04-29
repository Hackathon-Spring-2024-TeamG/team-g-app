from flask import Flask, request, redirect, render_template
from models import dbConnect

app = Flask(__name__)

# サインアップページの表示
@app.route('/signup')
def signup():
    return render_template('registration/signup.html')

# サインアップ処理
# @app.route('/signup', methods=['POST'])
# def userSignup():

# ログインページの表示
@app.route('/login')
def login():
    return render_template('registration/login.html')

# ログアウト
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# チャンネル一覧ページの表示
@app.route('/')
def index():
    # TODO:セッション情報取得およびリダイレクト処理
    #uid = session.get("uid")
    #if uid is None:
    #    return redirect('/login')
    #else:
    channels = dbConnect.getChannelAll()
    channels.reverse()
    return render_template('index.html', channels=channels)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
