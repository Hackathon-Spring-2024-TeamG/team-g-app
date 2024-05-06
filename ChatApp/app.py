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
    crypted_password = bcrypt.generate_password_hash(password1)
    # 入力されたemailを持つユーザーが存在するか確認
    DBuser = dbConnect.getUser(email)

    if DBuser is not None:
        flash('既に登録されています', 'danger')
    else:
        UserId = dbConnect.createUser(name, email, crypted_password)
        session['user_id'] = UserId
        return redirect('/')

    return redirect('/signup')

# ログインページの表示
@app.route('/login')
def login():
    return render_template('registration/login.html')

# ログイン処理
@app.route('/login', methods=['POST'])
def userLogin():
    email = request.form.get('email')
    password = request.form.get('password')
    print('password')

    if not email or not password:
        flash('空のフォームフィールドがあります', 'danger')
        return redirect('/login')

    user = dbConnect.getUser(email)
    if not user:
        flash('このユーザーは存在しません', 'danger')
        return redirect('/login')

    # bcrypt.check_password_hash関数を使って、DBから取得した暗号化済みのパスワードとユーザーが入力したパスワードを暗号化して比較
    if bcrypt.check_password_hash(user['crypted_password'], password):
        session['user_id'] = user['id']
        return redirect('/')
    else:
        flash('パスワードが間違っています', 'danger')
        return redirect('/login')

# ログアウト
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# チャンネル一覧ページの表示
@app.route('/')
def index():
    user_id = session.get("user_id")
    if user_id is None:
        return redirect('/login')
    else:
        channels = dbConnect.getChannelAll()
        channels.reverse()
    return render_template('index.html', channels=channels, user_id=user_id)

#チャンネル作成
@app.route('/', methods=['POST'])
def add_channel():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/login')
    channel_title = request.form.get('channelTitle')
    channel = dbConnect.getChannelByName(channel_title)
    if channel == None:
        channel_description = request.form.get('channelDescription')
        channel_startdate = request.form.get('channelStartDate')
        dbConnect.addChannel(channel_title, channel_description, channel_startdate)
        return redirect('/')
    else:
        error = '既に同じ名前のチャンネルが存在しています'
        return render_template('error/error.html', error_message=error)

# 個人チャンネル一覧ページの表示
@app.route('/personal_channels')
def show_personal_channels():
    user_id = session.get("user_id")
    if user_id is None:
        return redirect('/login')
    else:
        p_channels = dbConnect.getPersonalChannelALL()
        p_channels.reverse()
    return render_template('list_personal_channels.html', p_channels=p_channels, user_id=user_id)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
