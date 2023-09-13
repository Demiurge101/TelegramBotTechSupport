use SON_Dispatcher;

insert into clients(org, order_key) value ("Developer", "adminpass");
insert into clients(org, order_key) value ("ННГФ", "nngf");


insert into stations(serial_number, org_id, mkcb, date_out, description_) 
value (30056199, 2, "611139.102-01", "2023-08-29", "");


insert into devices(serial_number, station_number, org_id, device_name, mkcb, date_out, location, description_) 
value (30052548, 30056199, 2, "ДОЛ-100", "401269.109", "2023-08-29", "C:\Users\Gen\Projects\work\TelegramBotTechSupport\son\ННГФ\29.08.2023\Станция МКЦБ.611139.102-01\30056199\1 Датчик оборотов лебёдки Кедр ДОЛ-100 МКЦБ.401269.109\30052548", "");

insert into devices(serial_number, station_number, org_id, device_name, mkcb, date_out, location, description_) 
value (30055780, 30056199, 2, "ДОП-М-01", "402252.109", "2023-08-29", "C:\Users\Gen\Projects\work\TelegramBotTechSupport\son\ННГФ\29.08.2023\Станция МКЦБ.611139.102-01\30056199\2 Датчик оборотов  и приближения магнитный Кедр ДОП-М-01 МКЦБ.402252.109", "");


insert into devices(serial_number, org_id, device_name, mkcb, date_out, location, description_) 
value (30052959, 1, "Кедр ФВД", "306585.101", "2023-08-29", "C:\Users\Gen\Projects\work\TelegramBotTechSupport\son\ННГФ\29.08.2023\Станция МКЦБ.611139.102-01\30056204\23 Фитинг высокого давления Кедр ФВД МКЦБ.306585.101\30052959", "");

insert into devices(serial_number, org_id, device_name, mkcb, date_out, location, description_) 
value (30052960, 1, "Кедр ФВД", "306585.101", "2023-08-29", "C:\Users\Gen\Projects\work\TelegramBotTechSupport\son\ННГФ\29.08.2023\Станция МКЦБ.611139.102-01\30056204\23 Фитинг высокого давления Кедр ФВД МКЦБ.306585.101\30052960", "");
