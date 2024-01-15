DROP DATABASE IF EXISTS TS_Dispatcher;
CREATE DATABASE TS_Dispatcher
DEFAULT CHARACTER SET utf8
DEFAULT COLLATE utf8_general_ci;
USE TS_Dispatcher;



CREATE TABLE titles
(
  id INT NOT NULL AUTO_INCREMENT UNIQUE,
    parent_id INT NOT NULL,
    title varchar(100) NOT NULL,
    command varchar(50) unique,
    title_type tinyint(1) NOT NULL,
    CONSTRAINT pk_points
    PRIMARY KEY(id)
);


CREATE TABLE contents
(
	id INT NOT NULL AUTO_INCREMENT UNIQUE,
	parent_id INT NOT NULL UNIQUE,
	content_text varchar(3000) NOT NULL,
	location varchar(255),
	CONSTRAINT pk_contents
		PRIMARY KEY(id),
	CONSTRAINT fk_contents
    FOREIGN KEY(parent_id)
        REFERENCES titles(id)
        ON UPDATE CASCADE
);


CREATE TABLE files
(
    uuid varchar(64) unique not null,
    namef varchar(128) not null,
    file_id varchar(128) unique,
    author varchar(50),
    load_date date,
    CONSTRAINT PK_files
        primary key(uuid)
);

CREATE TABLE filebond
(
  id int NOT NULL AUTO_INCREMENT, 
    title_id INT not null,
    uuid varchar(64) not null,
    CONSTRAINT PK_filebond
    primary key(id)
   --  CONSTRAINT FK_files
--         FOREIGN KEY(uuid)
--             REFERENCES files(uuid)
);