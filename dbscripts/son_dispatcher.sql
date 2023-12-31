DROP DATABASE IF EXISTS SON_Dispatcher;
CREATE DATABASE SON_Dispatcher
DEFAULT CHARACTER SET utf8
DEFAULT COLLATE utf8_general_ci;
USE SON_Dispatcher;


CREATE TABLE clients
(
  id INT(4) NOT NULL AUTO_INCREMENT,
    org VARCHAR(70) NOT NULL,
    order_key varchar(20) not null unique,
    CONSTRAINT pk_clients
    PRIMARY KEY(id)
);

CREATE TABLE users
(
  id INT(4) NOT NULL AUTO_INCREMENT,
    org_id INT(4) NOT NULL,
    user_id bigint NOT NULL unique,
    user_name varchar(32),
    CONSTRAINT PK_users
    PRIMARY KEY(ID),
  CONSTRAINT FK_users
    FOREIGN KEY(org_id)
        REFERENCES clients(id)
        ON UPDATE CASCADE
);


CREATE TABLE stations
(
  -- id INT(4) NOT NULL AUTO_INCREMENT,
    serial_number INT(8) NOT NULL unique,
    org_id INT(4) NOT NULL,
    mkcb varchar(25) not null,
    date_out date,
    location varchar(255) not null,
    description_ varchar(50),
    CONSTRAINT pk_stations
        PRIMARY KEY(serial_number),
    CONSTRAINT FK_clients
        FOREIGN KEY(org_id)
            REFERENCES clients(id)
        ON UPDATE CASCADE
);

CREATE TABLE devices
(
  -- id INT(4) NOT NULL AUTO_INCREMENT,
     serial_number INT(8) NOT NULL unique,
     station_number INT(8),
     org_id INT(4) NOT NULL,
     device_name varchar(80) not null,
     mkcb varchar(25) not null,
     date_out date,
     location varchar(255) not null,
     description_ varchar(50),
    CONSTRAINT PK_devices
        PRIMARY KEY(serial_number),
    CONSTRAINT FK_stations
        FOREIGN KEY(station_number)
            REFERENCES stations(serial_number),
    CONSTRAINT FK_org
        FOREIGN KEY(org_id)
            REFERENCES clients(id)
    ON UPDATE CASCADE
);
