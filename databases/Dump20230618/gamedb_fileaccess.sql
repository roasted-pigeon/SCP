-- MySQL dump 10.13  Distrib 8.0.28, for Win64 (x86_64)
--
-- Host: localhost    Database: gamedb
-- ------------------------------------------------------
-- Server version	8.0.28

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
-- Table structure for table `fileaccess`
--

DROP TABLE IF EXISTS `fileaccess`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fileaccess` (
  `fileType_id` int NOT NULL,
  `fileAccessType_id` int NOT NULL,
  `fileRequester_fileRequesterType_id` int NOT NULL,
  `fileRequester_fileRequester_id` varchar(255) NOT NULL,
  PRIMARY KEY (`fileType_id`,`fileAccessType_id`,`fileRequester_fileRequesterType_id`,`fileRequester_fileRequester_id`),
  KEY `fileAccess_fileAccessType` (`fileAccessType_id`),
  KEY `fileAccess_fileRequester` (`fileRequester_fileRequesterType_id`,`fileRequester_fileRequester_id`),
  CONSTRAINT `fileAccess_fileAccessType` FOREIGN KEY (`fileAccessType_id`) REFERENCES `fileaccesstype` (`id`),
  CONSTRAINT `fileAccess_fileRequester` FOREIGN KEY (`fileRequester_fileRequesterType_id`, `fileRequester_fileRequester_id`) REFERENCES `filerequester` (`fileRequesterType_id`, `fileRequester_id`),
  CONSTRAINT `fileAccess_fileType` FOREIGN KEY (`fileType_id`) REFERENCES `filetype` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='This table stores records of all file permissions';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fileaccess`
--

LOCK TABLES `fileaccess` WRITE;
/*!40000 ALTER TABLE `fileaccess` DISABLE KEYS */;
/*!40000 ALTER TABLE `fileaccess` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-06-18 21:52:24
