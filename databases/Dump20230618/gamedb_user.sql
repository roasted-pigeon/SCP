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
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL,
  `gender` tinyint NOT NULL,
  `name` varchar(100) NOT NULL,
  `surname` varchar(100) NOT NULL,
  `dateOfBirth` date NOT NULL,
  `rotationDate` date DEFAULT NULL,
  `photoLink` varchar(200) DEFAULT NULL,
  `clearance_id` int NOT NULL,
  `job_id` int NOT NULL,
  `facility_id` int NOT NULL,
  `employeeClass_id` int NOT NULL,
  `decree_id` int DEFAULT NULL,
  `supervisor_id` int DEFAULT NULL,
  `supervisor_employeeClass_id` int DEFAULT NULL,
  PRIMARY KEY (`id`,`employeeClass_id`),
  KEY `user_clearance` (`clearance_id`),
  KEY `user_employeeClass` (`employeeClass_id`),
  KEY `user_facility` (`facility_id`),
  KEY `user_job` (`job_id`),
  KEY `user_user` (`supervisor_id`,`supervisor_employeeClass_id`),
  KEY `user_userFile` (`decree_id`),
  CONSTRAINT `user_clearance` FOREIGN KEY (`clearance_id`) REFERENCES `clearance` (`id`),
  CONSTRAINT `user_employeeClass` FOREIGN KEY (`employeeClass_id`) REFERENCES `employeeclass` (`id`),
  CONSTRAINT `user_facility` FOREIGN KEY (`facility_id`) REFERENCES `facility` (`id`),
  CONSTRAINT `user_job` FOREIGN KEY (`job_id`) REFERENCES `job` (`id`),
  CONSTRAINT `user_user` FOREIGN KEY (`supervisor_id`, `supervisor_employeeClass_id`) REFERENCES `user` (`id`, `employeeClass_id`),
  CONSTRAINT `user_userFile` FOREIGN KEY (`decree_id`) REFERENCES `userfile` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='This table stores records of all the Foundation''''s staff';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-06-18 21:52:25
