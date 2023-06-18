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
-- Table structure for table `usersectionspecialaccess`
--

DROP TABLE IF EXISTS `usersectionspecialaccess`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usersectionspecialaccess` (
  `facilitySection_id` int NOT NULL,
  `createdDateTime` datetime NOT NULL,
  `expiryDateTime` datetime NOT NULL,
  `decree_id` int NOT NULL,
  `user_id` int NOT NULL,
  `user_employeeClass_id` int NOT NULL,
  PRIMARY KEY (`facilitySection_id`,`user_id`,`user_employeeClass_id`),
  KEY `userSectionSpecialAccess_user` (`user_id`,`user_employeeClass_id`),
  KEY `userSectionSpecialAccess_userFile` (`decree_id`),
  CONSTRAINT `userSectionSpecialAccess_facilitySection` FOREIGN KEY (`facilitySection_id`) REFERENCES `facilitysection` (`id`),
  CONSTRAINT `userSectionSpecialAccess_user` FOREIGN KEY (`user_id`, `user_employeeClass_id`) REFERENCES `user` (`id`, `employeeClass_id`),
  CONSTRAINT `userSectionSpecialAccess_userFile` FOREIGN KEY (`decree_id`) REFERENCES `userfile` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='This table stores records of all special access permissions of employees to rooms';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usersectionspecialaccess`
--

LOCK TABLES `usersectionspecialaccess` WRITE;
/*!40000 ALTER TABLE `usersectionspecialaccess` DISABLE KEYS */;
/*!40000 ALTER TABLE `usersectionspecialaccess` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-06-18 21:52:27
