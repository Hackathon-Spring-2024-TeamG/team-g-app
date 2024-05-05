DROP DATABASE IF EXISTS chatapp;
DROP USER IF EXISTS 'testuser'@'%';

CREATE USER 'testuser' IDENTIFIED BY 'testuser';
CREATE DATABASE chatapp;
USE chatapp;
GRANT ALL PRIVILEGES ON chatapp.* TO 'testuser';

CREATE TABLE users (
    uid integer NOT NULL AUTO_INCREMENT,
    name varchar(255) UNIQUE NOT NULL,
    email varchar(255) UNIQUE NOT NULL,
    crypted_password varchar(255) NOT NULL,
    image varchar(255) NOT NULL DEFAULT '/static/img/user_default.png',
    self_introduction text,
    is_admin boolean NOT NULL DEFAULT 0,
    created_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY(uid)
);

CREATE TABLE channels (
    cid integer NOT NULL AUTO_INCREMENT,
    description text NOT NULL,
    name varchar(255) NOT NULL,
    start_date date NOT NULL,
    created_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(cid)
);

CREATE TABLE messages (
    mid integer NOT NULL AUTO_INCREMENT,
    uid integer NOT NULL,
    cid integer NOT NULL,
    message text NOT NULL,
    created_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(mid),
    FOREIGN KEY (uid) REFERENCES users(uid),
    FOREIGN KEY (cid) REFERENCES channels(cid)
);

CREATE TABLE badges (
    uid integer NOT NULL,
    mid integer NOT NULL,
    badge_type enum('GOLD', 'SILVER', 'BRONZE'),
    created_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (uid) REFERENCES users(uid),
    FOREIGN KEY (mid) REFERENCES messages(mid)
);

CREATE TABLE personal_channels (
    pcid integer NOT NULL AUTO_INCREMENT,
    uid integer UNIQUE NOT NULL,
    name varchar(255) NOT NULL,
    description text,
    created_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(pcid),
    FOREIGN KEY (uid) REFERENCES users(uid)
);

INSERT INTO users (name, email, crypted_password, self_introduction) VALUES ('chiikawa', 'chiikawa@example.com', '1111', 'フ！');
INSERT INTO channels (description, name, start_date) VALUES ('superぼっち部屋へようこそ', 'superぼっち部屋', '2024-04-27');
INSERT INTO messages (uid, cid, message) VALUES (1, 1, 'ヤヤーンパパヒュパヒュパ');
INSERT INTO badges (uid, mid, badge_type) VALUES (1, 1, 'GOLD');
INSERT INTO personal_channels (uid, name, description) VALUES (1, 'virtual_chiikawa', '草むしり検定5級目指して頑張ります！');