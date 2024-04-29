from flask import Flask, request, redirect, render_template, session, flash, abort
from flask_bcrypt import Bcrypt
import secrets
from datetime import timedelta
import re

from models import dbConnect

app = Flask(__name__)
bcrypt = Bcrypt(app)
random_secret_key = secrets.token_hex(16)
app.config['SECRET_KEY'] = random_secret_key

# サインアップページの表示
@app.route('/signup')
def signup():
    return render_template('registration/signup.html')

# サインアップ処理
@app.route('/signup', methods=['POST'])
def userSignup():
    name = request.form.get('name')
    email = request.form.get('email')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')

    pattern = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

    if name == '' or email == '' or password1 == '' or password2 == '':
        flash('入力されていないフォームがあります')
    elif password1 != password2:
        flash('２つのパスワードの値が違います。')
    elif re.match(pattern, email) is None:
        flash('正しいメールアドレスの形式で入力してください')
    else:
        crypted_password = bcrypt.generate_password_hash(password1).decode('utf8')
        DBuser = dbConnect.getUser(email)

        if DBuser is not None:
            flash('既に登録されています')
        else:
            UserId = dbConnect.createUser(name, email, crypted_password)
            session['id'] = UserId
            return redirect('/')
    return redirect('/signup')


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
