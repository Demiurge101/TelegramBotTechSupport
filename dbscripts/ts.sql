-- MySQL dump 10.13  Distrib 8.0.33, for Win64 (x86_64)
--
-- Host: localhost    Database: techsupport
-- ------------------------------------------------------
-- Server version	8.0.33

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `map`
--

DROP TABLE IF EXISTS `map`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `map` (
  `id` int NOT NULL AUTO_INCREMENT,
  `key_val` varchar(100) NOT NULL,
  `text_val` varchar(3000) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `key_val` (`key_val`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `map`
--

LOCK TABLES `map` WRITE;
/*!40000 ALTER TABLE `map` DISABLE KEYS */;
INSERT INTO `map` VALUES (1,'Старт','Добро пожаловать в бот технической поддержки ГеоФизМаш. Он предназначен для нахождения быстрых ответов, на самые распространённые проблемы. Для полного списка комманд введите /help'),(2,'Помощь','/network - Проблемы с сетью \n /wifi \n /camers \n /ip \n /telephones \n/hardware - Проблемы с оборудование КЕДР \n /uso - УСО \n /pnd - Пульт Бурильщика \n /sensors - Датчики \n /cables - Кабели датчиков и магистральный кабель \n/software - Проблемы с программный обеспечение DCSoft \n /DSServer \n /DSPlot \n /DSDevice \n/books - Обучающие материалы \n/mail - Сообщить о проблеме\n/feedback - сообщение об ошибке или предложение по улучшению '),(3,'Обратная связь','Здесь вы можете написать об ошибке или предложение по улучшению'),(4,'Сообщить о проблеме','Здесь вы можете сообщить о своей проблеме. К этому сообщению можно приложить фото, видео и документы'),(8,'Материалы','Здесь собраны необходимые материалы по оборудованию КЕДР и программам DCSoft для обучения'),(9,'Сеть','Здесь указаны распространенные проблемы связанные с сетевым оборудованием. Прежде чем выяснять, что конкретно не работает, необходимо проверить правильность соединения сетевого кабеля, обжимки и индикации подключения. \n Подключение осуществлять в соответствии с картой сети. Карта сети может отличается в зависимости от организации.'),(10,'Кедр','Здесь указаны общие проблемы связанные с оборудованием Кедр.'),(11,'DCSoft','Общие проблемы связанные с программами DCSoft. Перед проверкой программ, необходимо проверить правильность работы сети и монтажа станции Кедр.'),(12,'УСО','УСО - устройство связи с объектом предназначено для искробезопасного питания датчиков технологического контроля, обмена данными с датчиками и передачи информации на технологические компьютеры, сервера сбора для регистрации параметров. Существуют разные варианты исполнения УСО такие как:\n\n1. В взрывозащищенной оболочке предназначенной для работы в взрывоопасных зонах (Exd)\n\n2. В алюминиевом корпусе (Exn)\n\n     По технологии передачи данных:\n\n1. Powerline (белый блок подключаемый в одну электрическую сеть с магистральной линией)\n\n2. VDSL (отдельный блок \"Кедр БПМЛ\")'),(13,'wifi','Точки доступа существует для построения беспроводной локальной  сети. \nСуществует одна главная(access point) точка, все остальные побочные(station). \nТочки доступа должны быть в зоне прямой видимости между друг другом. \nПодключение обязательно через Poe инжектор, который идëт в комплекте. \nНе должно быть петель в кабеле который идет в точку. \nНиже кнопками указаны модели точек для получения инструкции по настройке и более специфической информации по каждой из них.'),(14,'Ubiquiti','Пусто');
/*!40000 ALTER TABLE `map` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pathdir`
--

DROP TABLE IF EXISTS `pathdir`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pathdir` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_map` int NOT NULL,
  `is_content` tinyint(1) NOT NULL,
  `dir` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_pathdir` (`id_map`),
  CONSTRAINT `fk_pathdir` FOREIGN KEY (`id_map`) REFERENCES `map` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pathdir`
--

LOCK TABLES `pathdir` WRITE;
/*!40000 ALTER TABLE `pathdir` DISABLE KEYS */;
INSERT INTO `pathdir` VALUES (1,8,1,'./res/Материалы/document'),(2,8,1,'./res/Материалы/photo'),(3,14,1,'./res/Ubiquiti/document');
/*!40000 ALTER TABLE `pathdir` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-09-18 11:07:58
