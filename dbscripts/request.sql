use SON_Dispatcher;
-- update devices
-- set location = ".\\ННГФ\\29.08.2023\\Станция МКЦБ.611139.102-01\\30056199\\1 Датчик оборотов лебёдки Кедр ДОЛ-100 МКЦБ.401269.109\\30052548"
-- where serial_number = 30052548;
-- select id from clients where org = "Developer";
-- select * from pathdir;
-- select * from map; 

-- select * from contents;
-- insert into clients(org, order_key) value ("Новатэк", "novatek");


CREATE TABLE filebond
(
    snumber varchar(25) not null,
    uuid varchar(64) unique not null,
    CONSTRAINT FK_bond
        FOREIGN KEY(uuid)
            REFERENCES files(uuid)
);