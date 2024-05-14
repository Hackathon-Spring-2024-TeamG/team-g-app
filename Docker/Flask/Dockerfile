# Pythonのイメージを指定
FROM python:3.11.3-buster
# PYTHONDONTWRITEBYTECODEとPYTHONUNBUFFEREDはオプション
# pycファイル（および__pycahe__）生成を行わないようにする
ENV PYTHONDONTWRITEBYTECODE=1
# 標準出力・標準エラーのストリームのバッファリングを行わない
ENV PYTHONUNBUFFERED=1
RUN mkdir /code
# コンテナのワークディレクトリを/codeに指定
WORKDIR /code
#  ローカルのrequirements.txtをコンテナの/code フォルダの直下に置く
COPY ./requirements.txt /code/
# コンテナ内でpip install -rr requirement.txtを実行
RUN pip install -U pip && \
    pip install -r requirements.txt
# ソースコードをコンテナにコピー
COPY . /code/
# ログファイルの出力用ディレクトリを作成
RUN mkdir -p /var/log/uwsgi

# RUN ls -la /code/Docker/Flask/ && cat /code/Docker/Flask/uwsgi.ini

# uWSGIを実行する
CMD ["uwsgi", "--ini", "/code/Docker/Flask/uwsgi.ini"]
#CMD ["uwsgi", "--ini", "/code/Docker/Flask/uwsgi.ini", "--die-on-term"]