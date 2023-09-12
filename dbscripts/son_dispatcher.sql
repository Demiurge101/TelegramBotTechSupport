DROP DATABASE IF EXISTS SON_Dispather;
CREATE DATABASE SON_Dispather
DEFAULT CHARACTER SET utf8
DEFAULT COLLATE utf8_general_ci;
USE SON_Dispather;

CREATE TABLE stations
(
  -- id INT(4) NOT NULL AUTO_INCREMENT,
    serial_number INT(4) NOT NULL unique,
    mkcb varchar(20) not null,
    date_out date not null,
    description varchar(100),
    CONSTRAINT pk_stations
    PRIMARY KEY(serial_number)
);

CREATE TABLE devices
(
  -- id INT(4) NOT NULL AUTO_INCREMENT,
     serial_number INT(4) NOT NULL unique,
     station_number INT(4) NOT NULL,
     device_name varchar(30) not null,
     mkcb varchar(20) not null,
     date_out date not null,
     location varchar(255),
     description varchar(100),
    CONSTRAINT PK_devices
    PRIMARY KEY(serial_number),
  CONSTRAINT FK_devices
    FOREIGN KEY(station_number)
        REFERENCES stations(serial_number)
        ON UPDATE CASCADE
);