DROP DATABASE IF EXISTS bot_statistics;
CREATE DATABASE bot_statistics
DEFAULT CHARACTER SET utf8
DEFAULT COLLATE utf8_general_ci;
USE bot_statistics;


CREATE TABLE users
(
  user_id bigint NOT NULL,
  nick varchar(64),
  fname varchar(128),
  sname varchar(128),
  CONSTRAINT pk_users
    PRIMARY KEY(user_id)
);


CREATE TABLE requests
(
  id bigint NOT NULL AUTO_INCREMENT,
  rdate date NOT NULL,
  request varchar(128) NOT NULL,
  user_id bigint NOT NULL,
  CONSTRAINT PK_requests
    PRIMARY KEY (id)
);