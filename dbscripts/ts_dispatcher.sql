DROP DATABASE IF EXISTS TS_Dispatcher;
CREATE DATABASE TS_Dispatcher
DEFAULT CHARACTER SET utf8
DEFAULT COLLATE utf8_general_ci;
USE TS_Dispatcher;



CREATE TABLE titles
(
  id INT(4) NOT NULL AUTO_INCREMENT UNIQUE,
    parent_id INT(4) NOT NULL,
    title varchar(100) NOT NULL,
    command varchar(50) unique,
    title_type tinyint(1) NOT NULL,
    CONSTRAINT pk_points
    PRIMARY KEY(id)
);


CREATE TABLE contents
(
	id INT(4) NOT NULL AUTO_INCREMENT UNIQUE,
	parent_id INT(4) NOT NULL UNIQUE,
	content_text varchar(3000) NOT NULL,
	location varchar(255),
	CONSTRAINT pk_contents
		PRIMARY KEY(id),
	CONSTRAINT fk_contents
    FOREIGN KEY(parent_id)
        REFERENCES titles(id)
        ON UPDATE CASCADE
);