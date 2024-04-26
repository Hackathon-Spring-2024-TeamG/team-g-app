from flask import Flask, request, redirect, render_template

app = Flask(__name__)

# サインアップページの表示
@app.route('/signup')
def signup():
    return render_template('registration/signup.html')

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
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)