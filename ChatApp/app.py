from flask import Flask, request, redirect, render_template, session, flash, abort
from flask_bcrypt import Bcrypt
import secrets, re
from models import dbConnect
from util.enums import BadgeType, AssociableType
from util.badge_image_handler import determineImageUrl

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

    if not email or not password:
        flash('空のフォームフィールドがあります', 'danger')
        return redirect('/login')

    user = dbConnect.getUser(email)
    if not user:
        flash('このユーザーは存在しません', 'danger')
        return redirect('/login')

    # bcrypt.check_password_hash関数を使って、DBから取得した暗号化済みのパスワードとユーザーが入力したパスワードを暗号化して比較
    if not bcrypt.check_password_hash(user['crypted_password'], password):
        flash('パスワードが間違っています', 'danger')
        return redirect('/login')

    session['user_id'] = user['id']

    if user['is_admin'] == 1:
        session['is_admin'] = True  # 管理者フラグを設定
        flash('管理者としてログインしました', 'info')
    else:
        flash('ログイン成功しました', 'success')

    return redirect('/')

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

# チャンネル詳細ページ表示
@app.route('/channels/detail/<int:channel_id>', methods=['GET'])
def channel_detail(channel_id):
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/login')
    else:
        channel = dbConnect.getChannelById(channel_id)
        messages = dbConnect.getMessageAll(channel_id)
        print(messages)
        print(user_id)
        return render_template('detail.html', channel=channel, messages=messages, channel_id=channel_id, user_id=user_id)

# メッセージ送信
@app.route('/message', methods=['POST'])
def send_message():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/login')

    message = request.form.get('message')
    channel_id = request.form.get('channel_id')

    if message:
        dbConnect.createMessage(user_id, channel_id, message)

    return redirect(f'/channels/detail/{channel_id}')

# 個人チャンネル一覧ページの表示
@app.route('/personal_channels')
def show_personal_channels():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/login')
    else:
        personal_channels = dbConnect.getPersonalChannelAll()
        personal_channels.reverse()
    return render_template('/personal/personal_channels.html', personal_channels=personal_channels, user_id=user_id)


# 個人チャンネルの作成
@app.route('/personal_channels', methods=['POST'])
def add_personal_channels():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/login')

    personal_channel = dbConnect.getPersonalChannelByUserId(user_id)

    if personal_channel is None:
        personal_channel_name = request.form.get('personalChannelName')
        personal_channel_description = request.form.get('personalChannelDescription')
        dbConnect.createPersonalChannel(user_id, personal_channel_name, personal_channel_description)
        flash('個人チャンネルが正常に作成されました。', 'success')
        return redirect('/personal_channels')
    else:
        flash('個人チャンネルは既に存在します。', 'danger')
        return redirect('/personal_channels')

# 個人チャンネルの更新（個人チャンネル一覧ページで非同期通信による更新)
@app.route('/update_personal_channel', methods=['POST'])
def update_personal_channel():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/login')

    personal_channel = dbConnect.getPersonalChannelByUserId(user_id)
    personal_channel_id = personal_channel['id']
    personal_channel_name = request.form.get('personalChannelName')
    personal_channel_description = request.form.get('personalChannelDescription')

    dbConnect.updatePersonalChannel(user_id, personal_channel_name, personal_channel_description, personal_channel_id)
    return redirect('/personal_channels')

# 個人チャンネルの更新（詳細ページ内）
@app.route('/update_personal_detail', methods=['POST'])
def update_personal_detail():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/login')

    personal_channel = dbConnect.getPersonalChannelByUserId(user_id)
    personal_channel_id = personal_channel['id']
    personal_channel_name = request.form.get('personalChannelName')
    personal_channel_description = request.form.get('personalChannelDescription')

    dbConnect.updatePersonalChannel(user_id, personal_channel_name, personal_channel_description, personal_channel_id)
    return redirect('/personal_channels/detail/{personal_channel_id}'.format(personal_channel_id=personal_channel_id))

# 個人チャンネルの削除
@app.route('/personal_channels/delete/<int:personal_channel_id>')
def delete_personal_channel(personal_channel_id):
    user_id = session.get('user_id')
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

# 個人チャンネル詳細ページの表示
@app.route('/personal_channels/detail/<int:personal_channel_id>')
def personal_detail(personal_channel_id):
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/login')

    personal_channel_id = personal_channel_id
    personal_channel = dbConnect.getPersonalChannelById(personal_channel_id)
    personal_messages = dbConnect.getPersonalMessageAll(personal_channel_id)

    return  render_template('personal/detail.html', personal_messages=personal_messages, personal_channel=personal_channel, user_id=user_id)

# メッセージの投稿（個人チャンネル詳細ページ内）
@app.route('/personal_message', methods=['POST'])
def add_personal_message():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/login')

    personal_message = request.form.get('personal_message')
    personal_channel_id = request.form.get('personal_channel_id')

    if personal_message:
        dbConnect.createPersonalMessage(user_id, personal_channel_id, personal_message)

    return redirect(f'/personal_channels/detail/{personal_channel_id}')

# 個人メッセージの削除
@app.route('/delete_personal_message', methods=['POST'])
def delete_personal_message():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/login')

    personal_message_id = request.form.get('personal_message_id')
    personal_channel_id = request.form.get('personal_channel_id')

    if personal_message_id:
        dbConnect.deletePersonalMessage(personal_message_id)

    return redirect(f'/personal_channels/detail/{personal_channel_id}')

# アカウントページ表示
@app.route('/account')
def show_account():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/login')
    else:
        account = dbConnect.getUserAccount(user_id)
    return render_template('account.html', account=account, user_id=user_id)

# バッジ作成（個人チャンネル詳細ページ内のメッセージに対して）
@app.route('/add_personal_badge', methods=['POST'])
def add_personal_badge():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/login')

    associable_id = request.json.get('associableId')
    if not associable_id:
        return "associableIdが指定されていません", 400

    associable_type = AssociableType.PERSONAL_MESSAGE.value
    badge_type_str = request.json.get('badgeType').lower()
    badge_type = BadgeType[badge_type_str.upper()].value

    image_url = determineImageUrl(badge_type)

    if image_url is None:
        print("バッジタイプに対する画像URLが見つかりません。")

    personal_channel = dbConnect.getPersonalChannelByUserId(user_id)
    personal_channel_id = personal_channel['id']

    dbConnect.addPersonalBadge(user_id, associable_type, associable_id, image_url, badge_type.lower())
    return redirect(f'/personal_channels/detail/{personal_channel_id}')


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5000)
