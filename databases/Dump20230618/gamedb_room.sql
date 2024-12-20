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
-- Table structure for table `room`
--

DROP TABLE IF EXISTS `room`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `room` (
  `id` int NOT NULL,
  `name` varchar(255) NOT NULL,
  `description` text NOT NULL,
  `clearance_id` int NOT NULL,
  `roomStatus_id` int NOT NULL,
  `roomType_id` int NOT NULL,
  `parentRoom_id` int DEFAULT NULL,
  `facilitySection_id` int NOT NULL,
  `specialAccessRequired` tinyint NOT NULL,
  `plan_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `Room_clearance` (`clearance_id`),
  KEY `room_facilitySection` (`facilitySection_id`),
  KEY `room_room` (`parentRoom_id`),
  KEY `room_roomStatus` (`roomStatus_id`),
  KEY `room_roomType` (`roomType_id`),
  KEY `room_userFile` (`plan_id`),
  CONSTRAINT `Room_clearance` FOREIGN KEY (`clearance_id`) REFERENCES `clearance` (`id`),
  CONSTRAINT `room_facilitySection` FOREIGN KEY (`facilitySection_id`) REFERENCES `facilitysection` (`id`),
  CONSTRAINT `room_room` FOREIGN KEY (`parentRoom_id`) REFERENCES `room` (`id`),
  CONSTRAINT `room_roomStatus` FOREIGN KEY (`roomStatus_id`) REFERENCES `roomstatus` (`id`),
  CONSTRAINT `room_roomType` FOREIGN KEY (`roomType_id`) REFERENCES `roomtype` (`id`),
  CONSTRAINT `room_userFile` FOREIGN KEY (`plan_id`) REFERENCES `userfile` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='This table stores records of all rooms in all sections of all facilities of the Foundation';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `room`
--

LOCK TABLES `room` WRITE;
/*!40000 ALTER TABLE `room` DISABLE KEYS */;
/*!40000 ALTER TABLE `room` ENABLE KEYS */;
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
