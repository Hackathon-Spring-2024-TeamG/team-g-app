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
# ログイン処理
@app.route('/login', methods=['POST'])
def userLogin():
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        flash('空のフォームフィールドがあります', 'danger')
        return redirect('/login')

    user = dbConnect.getUser(email)
    if not user:
        flash('このユーザーは存在しません', 'danger')
        return redirect('/login')

    if bcrypt.check_password_hash(user['crypted_password'], password):
        session['user_id'] = user['id']
        if email == 'admin@example.com':
            session['is_admin'] = True  # 管理者フラグを設定
            print('管理者です！')
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
        if channels:  # チャンネルが空でない場合のみリバースする
            channels = list(channels)
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
        flash('チャンネルが正常に作成されました。', 'success')
        return redirect('/')
    else:
        flash('既に同じ名前のチャンネルが存在しています', 'danger')
        return redirect('/')

# チャンネル更新
@app.route('/update_channel/<int:channel_id>', methods=['POST'])
def update_channel(channel_id):
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/login')
    else:
        channel_name = request.form.get('ChannelName')
        channel_description = request.form.get('ChannelDescription')
        dbConnect.updateChannel(channel_name, channel_description, channel_id)
        flash('チャンネルは正常に変更されました。', 'success')
        return redirect('/')

# チャンネル削除
@app.route('/channels/delete/<int:channel_id>')
def delete_channel(channel_id):
    user_id = session.get("user_id")
    if user_id is None:
        return redirect('/login')
    else:
        channel = dbConnect.getChannelById(channel_id)
        dbConnect.deleteChannel(channel_id)
        flash('チャンネルは正常に削除されました。', 'success')
        return redirect('/')

# 個人チャンネル一覧ページの表示
@app.route('/personal_channels')
def show_personal_channels():
    user_id = session.get("user_id")
    if user_id is None:
        return redirect('/login')
    else:
        p_channels = dbConnect.getPersonalChannelALL()
        p_channels.reverse()
    return render_template('/personal/personal_channels.html', p_channels=p_channels, user_id=user_id)


# 個人チャンネルの作成
@app.route('/personal_channels', methods=['POST'])
def add_personal_channels():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/login')

    personal_channel = dbConnect.getPersonalChannelByUserId(user_id)

    if personal_channel is None:
        p_channel_name = request.form.get('personalChannelName')
        p_channel_description = request.form.get('personalChannelDescription')
        dbConnect.createPersonalChannel(user_id, p_channel_name, p_channel_description)
        flash('個人チャンネルが正常に作成されました。', 'success')
        return redirect('/personal_channels')
    else:
        flash('個人チャンネルは既に存在します。', 'danger')
        return redirect('/personal_channels')

# 個人チャンネルの更新
@app.route('/update_personal_channel', methods=['POST'])
def update_personal_channel():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/login')

    personal_channel = dbConnect.getPersonalChannelByUserId(user_id)
    p_channel_id = personal_channel['id']
    p_channel_name = request.form.get('personalChannelName')
    p_channel_description = request.form.get('personalChannelDescription')

    dbConnect.updatePersonalChannel(user_id, p_channel_name, p_channel_description, p_channel_id)
    return redirect('/personal_channels')

# 個人チャンネルの削除
@app.route('/personal_channels/delete/<int:personal_channel_id>')
def delete_personal_channel(personal_channel_id):
    user_id = session.get("user_id")
    if user_id is None:
        return redirect('/login')
    else:
        personal_channel = dbConnect.getPersonalChannelById(personal_channel_id)
        if personal_channel["user_id"] != user_id:
            flash('チャンネルは作成者のみ削除可能です', 'danger')
            return redirect('/')
        else:
            dbConnect.deletePersonalChannel(personal_channel_id)
            flash('個人チャンネルは正常に削除されました。', 'success')
            return redirect('/personal_channels')

# アカウントページ表示
@app.route('/account')
def show_account():
    user_id = session.get("user_id")
    if user_id is None:
        return redirect('/login')
    else:
        account = dbConnect.getUserAccount(user_id)
    return render_template('account.html', account=account, user_id=user_id)


@app.route('/channels/<int:channel_id>', methods=['GET'])
def channel_detail(channel_id):
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/login')
    else:
        channel = dbConnect.getChannelById(channel_id)
        messages = dbConnect.getMessageAll(channel_id)
        return render_template('detail.html', channel=channel, messages=messages, channel_id=channel_id)


@app.route('/send_message', methods=['POST'])
def send_message():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/login')
    else:
        channel_id = request.form.get('channel_id')
        message = request.form.get('message')

        # メッセージの送信者のユーザーIDを取得して、データベースに追加
        dbConnect.addMessage(user_id, channel_id, message)
        print(channel_id)

        # 送信が完了したらチャンネル詳細ページにリダイレクト
        return redirect('/channels/' + str(channel_id))

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
