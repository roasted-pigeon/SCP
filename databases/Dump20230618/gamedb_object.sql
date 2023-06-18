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
-- Table structure for table `object`
--

DROP TABLE IF EXISTS `object`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `object` (
  `id` int NOT NULL,
  `nickname` varchar(100) NOT NULL,
  `clearance_id` int NOT NULL,
  `containmentClass_id` int NOT NULL,
  `disruptionClass_id` int DEFAULT NULL,
  `riskClass_id` int DEFAULT NULL,
  `secondaryClass_id` int DEFAULT NULL,
  `facility_id` int DEFAULT NULL,
  `specialAccessRequired` tinyint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `object_clearance` (`clearance_id`),
  KEY `object_containmentClass` (`containmentClass_id`),
  KEY `object_disruptionClass` (`disruptionClass_id`),
  KEY `object_facility` (`facility_id`),
  KEY `object_riskClass` (`riskClass_id`),
  KEY `object_secondaryClass` (`secondaryClass_id`),
  CONSTRAINT `object_clearance` FOREIGN KEY (`clearance_id`) REFERENCES `clearance` (`id`),
  CONSTRAINT `object_containmentClass` FOREIGN KEY (`containmentClass_id`) REFERENCES `containmentclass` (`id`),
  CONSTRAINT `object_disruptionClass` FOREIGN KEY (`disruptionClass_id`) REFERENCES `disruptionclass` (`id`),
  CONSTRAINT `object_facility` FOREIGN KEY (`facility_id`) REFERENCES `facility` (`id`),
  CONSTRAINT `object_riskClass` FOREIGN KEY (`riskClass_id`) REFERENCES `riskclass` (`id`),
  CONSTRAINT `object_secondaryClass` FOREIGN KEY (`secondaryClass_id`) REFERENCES `secondaryclass` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='This table stores records of all objects contained by the Foundation';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `object`
--

LOCK TABLES `object` WRITE;
/*!40000 ALTER TABLE `object` DISABLE KEYS */;
/*!40000 ALTER TABLE `object` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-06-18 21:52:23
