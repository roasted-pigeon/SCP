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
-- Table structure for table `usertounit`
--

DROP TABLE IF EXISTS `usertounit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usertounit` (
  `unit_id` int NOT NULL,
  `position` varchar(255) NOT NULL,
  `description` text,
  `user_id` int NOT NULL,
  `user_employeeClass_id` int NOT NULL,
  PRIMARY KEY (`unit_id`,`user_employeeClass_id`,`user_id`),
  KEY `userToUnit_user` (`user_id`,`user_employeeClass_id`),
  CONSTRAINT `userToUnit_unit` FOREIGN KEY (`unit_id`) REFERENCES `unit` (`id`),
  CONSTRAINT `userToUnit_user` FOREIGN KEY (`user_id`, `user_employeeClass_id`) REFERENCES `user` (`id`, `employeeClass_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='This table stores records about possible employees roles in relation to the units (divisions, groups, etc.)(for example: Commander, Deputy Commander or Officer)';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usertounit`
--

LOCK TABLES `usertounit` WRITE;
/*!40000 ALTER TABLE `usertounit` DISABLE KEYS */;
/*!40000 ALTER TABLE `usertounit` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-06-18 21:52:26
