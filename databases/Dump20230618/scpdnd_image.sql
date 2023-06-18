-- MySQL dump 10.13  Distrib 8.0.28, for Win64 (x86_64)
--
-- Host: localhost    Database: scpdnd
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
-- Table structure for table `image`
--

DROP TABLE IF EXISTS `image`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `image` (
  `image_id` int NOT NULL AUTO_INCREMENT,
  `uploader_id` int NOT NULL,
  `upload_date` datetime NOT NULL,
  `name` varchar(100) NOT NULL,
  `file_link` varchar(255) NOT NULL,
  PRIMARY KEY (`image_id`),
  KEY `uploader_id` (`uploader_id`),
  CONSTRAINT `uploaderImage` FOREIGN KEY (`uploader_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `image`
--

LOCK TABLES `image` WRITE;
/*!40000 ALTER TABLE `image` DISABLE KEYS */;
INSERT INTO `image` VALUES (1,6,'2023-06-17 23:32:31','Screenshot 2023-05-17 230052.png','images\\Screenshot 2023-05-17 230052.png'),(2,6,'2023-06-18 00:00:31','Screenshot (31).png','images\\Screenshot (31).png'),(3,6,'2023-06-18 10:52:49','logoExtended.png','images\\logoExtended.png'),(4,6,'2023-06-18 10:53:02','logoExtended.png','images\\logoExtended.png'),(5,6,'2023-06-18 10:53:10','logoExtendedWhite.png','images\\logoExtendedWhite.png'),(6,6,'2023-06-18 10:53:29','image_2023-04-09_00-58-41.png','images\\image_2023-04-09_00-58-41.png'),(7,6,'2023-06-18 10:53:49','image_2023-04-09_00-58-41.png','images\\image_2023-04-09_00-58-41.png'),(8,6,'2023-06-18 13:14:56','photo_2021-04-22_19-22-05.jpg','images\\photo_2021-04-22_19-22-05.jpg'),(9,6,'2023-06-18 13:15:03','photo_2021-04-19_20-21-43.jpg','images\\photo_2021-04-19_20-21-43.jpg'),(10,6,'2023-06-18 13:15:12','photo_2021-04-19_19-18-06.jpg','images\\photo_2021-04-19_19-18-06.jpg'),(11,6,'2023-06-18 13:15:20','Untitled.png','images\\Untitled.png'),(12,6,'2023-06-18 13:15:43','photo_2023-06-13_21-23-33.jpg','images\\photo_2023-06-13_21-23-33.jpg'),(13,6,'2023-06-18 13:41:06','kaif.mp4','images\\kaif.mp4'),(14,6,'2023-06-18 13:41:46','image.png','images\\image.png'),(15,6,'2023-06-18 13:41:58','logoExtended.png','images\\logoExtended.png'),(16,6,'2023-06-18 13:42:08','logoExtendedWhite.png','images\\logoExtendedWhite.png'),(17,6,'2023-06-18 13:42:20','image.png','images\\image.png');
/*!40000 ALTER TABLE `image` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-06-18 21:52:21
