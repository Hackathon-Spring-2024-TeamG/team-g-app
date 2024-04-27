DROP DATABASE IF EXISTS chatapp;
DROP USER IF EXISTS 'testuser'@'%';

CREATE USER 'testuser' IDENTIFIED BY 'testuser';
CREATE DATABASE chatapp;
USE chatapp;
GRANT ALL PRIVILEGES ON chatapp.* TO 'testuser';

CREATE TABLE users (
    id integer NOT NULL AUTO_INCREMENT,
    name varchar(255) UNIQUE NOT NULL,
    email varchar(255) UNIQUE NOT NULL,
    crypted_password varchar(255) NOT NULL,
    image varchar(255),
    self_introduction text NOT NULL,
    is_admin boolean NOT NULL DEFAULT 0,
    created_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY(id)
);

CREATE TABLE channels (
    id integer NOT NULL AUTO_INCREMENT,
    description text NOT NULL,
    name varchar(255) NOT NULL,
    start_date date NOT NULL,
    created_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY(id)
);

CREATE TABLE messages (
    id integer NOT NULL AUTO_INCREMENT,
    user_id integer,
    channel_id integer,
    message text,
    created_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY(id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (channel_id) REFERENCES channels(id)
);

INSERT INTO users (name, email, crypted_password, self_introduction) VALUES ('chiikawa', 'chiikawa@example.com', '1111', 'フ！');
INSERT INTO channels (description, name, start_date) VALUES ('superぼっち部屋へようこそ', 'superぼっち部屋', '2024-04-27');
INSERT INTO messages (user_id, channel_id, message) VALUES (1, 1, 'ヤヤーンパパヒュパヒュパ');