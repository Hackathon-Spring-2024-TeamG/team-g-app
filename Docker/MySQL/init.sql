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
    self_introduction text,
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
    user_id integer NOT NULL,
    channel_id integer NOT NULL,
    message text NOT NULL,
    created_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY(id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (channel_id) REFERENCES channels(id)
);

CREATE TABLE badges (
    user_id integer NOT NULL,
    message_id integer NOT NULL,
    badge_type enum('GOLD', 'SILVER', 'BRONZE'),
    created_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (message_id) REFERENCES channels(id)
);

CREATE TABLE personal_channels (
    id integer NOT NULL AUTO_INCREMENT,
    user_id integer UNIQUE NOT NULL,
    name varchar(255) NOT NULL,
    description text,
    created_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

INSERT INTO users (name, email, crypted_password, self_introduction) VALUES ('chiikawa', 'chiikawa@example.com', '1111', 'フ！');
INSERT INTO channels (description, name, start_date) VALUES ('superぼっち部屋へようこそ', 'superぼっち部屋', '2024-04-27');
INSERT INTO messages (user_id, channel_id, message) VALUES (1, 1, 'ヤヤーンパパヒュパヒュパ');
INSERT INTO badges (user_id, message_id, badge_type) VALUES (1, 1, 'GOLD');
INSERT INTO personal_channels (user_id, name, description) VALUES (1, 'virtual_chiikawa', '草むしり検定5級目指して頑張ります！');