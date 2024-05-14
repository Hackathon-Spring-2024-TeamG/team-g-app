# nginx imageの取得
FROM nginx

# デフォルトnginx.confの削除と既存のシンボリックリンクを削除
RUN rm /etc/nginx/conf.d/default.conf && \
    rm /var/log/nginx/access.log && \
    rm /var/log/nginx/error.log && \
    mkdir -p /var/log/nginx && \
    chown -R nginx:nginx /var/log/nginx

# 自作したnginx.confに置き換え
COPY ./Docker/Nginx/nginx.conf /etc/nginx/conf.d/