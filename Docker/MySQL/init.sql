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
    image varchar(255) NOT NULL DEFAULT '/static/img/user_default.png',
    self_introduction text,
    is_admin boolean NOT NULL DEFAULT 0,
    created_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

CREATE TABLE channels (
    id integer NOT NULL AUTO_INCREMENT,
    description text NOT NULL,
    name varchar(255) NOT NULL,
    start_date date NOT NULL,
    created_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

CREATE TABLE messages (
    id integer NOT NULL AUTO_INCREMENT,
    user_id integer NOT NULL,
    channel_id integer NOT NULL,
    message text NOT NULL,
    created_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (channel_id) REFERENCES channels(id) ON DELETE CASCADE
);

CREATE TABLE badges (
    id integer NOT NULL AUTO_INCREMENT,
    user_id integer NOT NULL,
    associable_type enum('message', 'personal_message') NOT NULL,
    associable_id integer NOT NULL,
    image_url varchar(255) NOT NULL,
    badge_type enum('fast_parrot', 'angel_parrot') NOT NULL,
    created_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE personal_channels (
    id integer NOT NULL AUTO_INCREMENT,
    user_id integer UNIQUE NOT NULL,
    name varchar(255) NOT NULL,
    description text,
    created_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE personal_messages (
    id integer NOT NULL AUTO_INCREMENT,
    user_id integer NOT NULL,
    channel_id integer NOT NULL,
    message text NOT NULL,
    created_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (channel_id) REFERENCES personal_channels(id) ON DELETE CASCADE
);


INSERT INTO users (name, email, crypted_password, is_admin) VALUES ('admin', 'admin@example.com', '$2b$12$sBXqSJJ7fOJUAhUHAqq1TuAmgMmfsOiJzvNhwINozNwrtGl8gbqtG', 1);
INSERT INTO users (name, email, crypted_password, self_introduction) VALUES ('chiikawa', 'chiikawa@example.com', '$2b$12$sBXqSJJ7fOJUAhUHAqq1TuAmgMmfsOiJzvNhwINozNwrtGl8gbqtG', 'フ！');
INSERT INTO channels (description, name, start_date) VALUES ('4/1Wの投稿はこちらへ', '4/1W', '2024-04-06');
INSERT INTO channels (description, name, start_date) VALUES ('4/2Wの投稿はこちらへ', '4/2W', '2024-04-13');
INSERT INTO channels (description, name, start_date) VALUES ('4/3Wの投稿はこちらへ', '4/3W', '2024-04-20');
INSERT INTO channels (description, name, start_date) VALUES ('4/4Wの投稿はこちらへ', '4/4W', '2024-04-27');
INSERT INTO channels (description, name, start_date) VALUES ('5/1Wの投稿はこちらへ', '5/1W', '2024-05-01');
INSERT INTO channels (description, name, start_date) VALUES ('5/2Wの投稿はこちらへ', '5/2W', '2024-05-05');
INSERT INTO channels (description, name, start_date) VALUES ('5/3Wの投稿はこちらへ', '5/3W', '2024-05-12');
INSERT INTO channels (description, name, start_date) VALUES ('5/4Wの投稿はこちらへ', '5/4W', '2024-05-19');
INSERT INTO channels (description, name, start_date) VALUES ('5/5Wの投稿はこちらへ', '5/5W', '2024-05-26');
INSERT INTO channels (description, name, start_date) VALUES ('6/1Wの投稿はこちらへ', '6/1W', '2024-06-02');
INSERT INTO messages (user_id, channel_id, message) VALUES (2, 1, 'ヤヤーンパパヒュパヒュパ');
INSERT INTO badges (user_id, associable_type, associable_id, image_url, badge_type) VALUES (2, 'personal_message', 1, '/static/img/fast_parrot.gif', 'fast_parrot');
INSERT INTO personal_channels (user_id, name, description) VALUES (2, 'virtual_chiikawa', '草むしり検定5級目指して頑張ります！');
INSERT INTO personal_messages (user_id, channel_id, message) VALUES (2, 1, 'Noneだ、もう朝かと…');