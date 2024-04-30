from flask import Flask, request, redirect, render_template, session, flash, abort
from flask_bcrypt import Bcrypt
import secrets, re
from models import dbConnect

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = secrets.token_hex(16)

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

    # バリデーションルールをリストとして管理
    validations = [
        (not name or not email or not password1 or not password2, '入力されていないフォームがあります'),
        (password1 != password2, '２つのパスワードの値が違います。'),
        (len(email) > 40, 'メールアドレスは40文字以内で入力してください。'),
        (re.match("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email) is None, '正しいメールアドレスの形式で入力してください')
    ]

    # バリデーションチェック
    for check, message in validations:
        if check:
            flash(message, 'danger')
            return redirect('/signup')

    # パスワード暗号化。
    crypted_password = bcrypt.generate_password_hash(password1).decode('utf8')
    # 入力されたemailを持つユーザーが存在するか確認
    DBuser = dbConnect.getUser(email)

    if DBuser is not None:
        flash('既に登録されています')
    else:
        UserId = dbConnect.createUser(name, email, crypted_password)
        session['uid'] = UserId
        flash('登録が成功しました。')
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
