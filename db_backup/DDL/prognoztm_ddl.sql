-- MySQL dump 10.13  Distrib 8.0.19, for Win64 (x86_64)
--
-- Host: localhost    Database: prognoztm_stage
-- ------------------------------------------------------
-- Server version	8.0.19

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `prognoztm_stage`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `prognoztm_stage` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `prognoztm_stage`;

--
-- Table structure for table `pz1000bus_tram`
--

DROP TABLE IF EXISTS `pz1000bus_tram`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pz1000bus_tram` (
  `pz1000bus_tram_id` int NOT NULL AUTO_INCREMENT,
  `LINE` varchar(10) DEFAULT NULL,
  `brigade` varchar(10) DEFAULT NULL,
  `vehicle` varchar(20) DEFAULT NULL,
  `date_api` varchar(30) DEFAULT NULL,
  `date_collected` varchar(30) DEFAULT NULL,
  `latitude` varchar(30) DEFAULT NULL,
  `longitude` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`pz1000bus_tram_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9437 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pz2000actual_weather`
--

DROP TABLE IF EXISTS `pz2000actual_weather`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pz2000actual_weather` (
  `pz2000actual_weather_id` int NOT NULL AUTO_INCREMENT,
  `latitude` varchar(30) DEFAULT NULL,
  `longitude` varchar(30) DEFAULT NULL,
  `datetime_unix` varchar(15) DEFAULT NULL,
  `temperature_k` varchar(10) DEFAULT NULL,
  `wind_chill_temp_k` varchar(10) DEFAULT NULL,
  `pressure` varchar(10) DEFAULT NULL,
  `humidity` varchar(10) DEFAULT NULL,
  `visibility` varchar(15) DEFAULT NULL,
  `wind_speed_ms` varchar(10) DEFAULT NULL,
  `wind_direction_deg` varchar(10) DEFAULT NULL,
  `clouds_coverage` varchar(10) DEFAULT NULL,
  `sunrise_unix` varchar(15) DEFAULT NULL,
  `sunset_unix` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`pz2000actual_weather_id`)
) ENGINE=InnoDB AUTO_INCREMENT=286 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pz3000traffic_data`
--

DROP TABLE IF EXISTS `pz3000traffic_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pz3000traffic_data` (
  `pz3000traffic_data_id` int NOT NULL AUTO_INCREMENT,
  `timestamp` varchar(30) DEFAULT NULL,
  `label` varchar(50) DEFAULT NULL,
  `color` varchar(15) DEFAULT NULL,
  `color_values` varchar(20) DEFAULT NULL,
  `count` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`pz3000traffic_data_id`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-11-29 18:27:02
