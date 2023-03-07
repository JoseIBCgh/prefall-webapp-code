CREATE DATABASE  IF NOT EXISTS `prefall` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `prefall`;
-- MySQL dump 10.13  Distrib 8.0.32, for Win64 (x86_64)
--
-- Host: localhost    Database: prefall
-- ------------------------------------------------------
-- Server version	8.0.32

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
-- Table structure for table `acciones_test_medico`
--

DROP TABLE IF EXISTS `acciones_test_medico`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `acciones_test_medico` (
  `num_test` int NOT NULL,
  `id_paciente` int NOT NULL,
  `id_medico` int NOT NULL,
  `visto` tinyint(1) NOT NULL,
  `diagnostico` text,
  PRIMARY KEY (`num_test`,`id_paciente`,`id_medico`),
  KEY `id_medico` (`id_medico`),
  CONSTRAINT `acciones_test_medico_ibfk_1` FOREIGN KEY (`num_test`, `id_paciente`) REFERENCES `test` (`num_test`, `id_paciente`),
  CONSTRAINT `acciones_test_medico_ibfk_2` FOREIGN KEY (`id_medico`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `acciones_test_medico`
--

LOCK TABLES `acciones_test_medico` WRITE;
/*!40000 ALTER TABLE `acciones_test_medico` DISABLE KEYS */;
INSERT INTO `acciones_test_medico` VALUES (0,4,7,1,'<p>Test Diagnosticado</p>\r\n'),(0,6,7,1,'<p>Test diagnosticado</p>\r\n'),(1,4,7,1,'<p>diagnosticar</p>\r\n'),(2,4,7,1,'<p>diagnosticado</p>\r\n');
/*!40000 ALTER TABLE `acciones_test_medico` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `boundary`
--

DROP TABLE IF EXISTS `boundary`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `boundary` (
  `model_id` int NOT NULL,
  `index` int NOT NULL,
  `intercept` float DEFAULT NULL,
  `coef0` float DEFAULT NULL,
  `coef1` float DEFAULT NULL,
  `coef2` float DEFAULT NULL,
  PRIMARY KEY (`model_id`,`index`),
  CONSTRAINT `boundary_ibfk_1` FOREIGN KEY (`model_id`) REFERENCES `model` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `boundary`
--

LOCK TABLES `boundary` WRITE;
/*!40000 ALTER TABLE `boundary` DISABLE KEYS */;
/*!40000 ALTER TABLE `boundary` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `centros`
--

DROP TABLE IF EXISTS `centros`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `centros` (
  `id` int NOT NULL AUTO_INCREMENT,
  `cif` varchar(20) DEFAULT NULL,
  `nombreFiscal` varchar(50) DEFAULT NULL,
  `direccion` varchar(100) DEFAULT NULL,
  `CP` int DEFAULT NULL,
  `ciudad` varchar(30) DEFAULT NULL,
  `provincia` varchar(30) DEFAULT NULL,
  `pais` varchar(20) DEFAULT NULL,
  `id_admin` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `cif` (`cif`),
  KEY `fk_id_admin` (`id_admin`),
  CONSTRAINT `fk_id_admin` FOREIGN KEY (`id_admin`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `centros`
--

LOCK TABLES `centros` WRITE;
/*!40000 ALTER TABLE `centros` DISABLE KEYS */;
INSERT INTO `centros` VALUES (1,'cif1','nombre1','direccion1',1,'ciudad1','provincia1','pais1',NULL),(2,'cif2','nombre2','direccion2',2,'ciudad2','provincia2','pais2',NULL),(3,'B021111333','LAB1','Calle1',28859,'Madrid','Madrid','España',NULL);
/*!40000 ALTER TABLE `centros` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `documentos_paciente`
--

DROP TABLE IF EXISTS `documentos_paciente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `documentos_paciente` (
  `id_paciente` int NOT NULL,
  `id_medico` int NOT NULL,
  `id_file` int NOT NULL,
  PRIMARY KEY (`id_paciente`,`id_medico`,`id_file`),
  KEY `id_medico` (`id_medico`),
  KEY `id_file` (`id_file`),
  CONSTRAINT `documentos_paciente_ibfk_1` FOREIGN KEY (`id_paciente`) REFERENCES `users` (`id`),
  CONSTRAINT `documentos_paciente_ibfk_2` FOREIGN KEY (`id_medico`) REFERENCES `users` (`id`),
  CONSTRAINT `documentos_paciente_ibfk_3` FOREIGN KEY (`id_file`) REFERENCES `files` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `documentos_paciente`
--

LOCK TABLES `documentos_paciente` WRITE;
/*!40000 ALTER TABLE `documentos_paciente` DISABLE KEYS */;
INSERT INTO `documentos_paciente` VALUES (4,7,1);
/*!40000 ALTER TABLE `documentos_paciente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `files`
--

DROP TABLE IF EXISTS `files`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `files` (
  `id` int NOT NULL AUTO_INCREMENT,
  `filename` varchar(50) DEFAULT NULL,
  `data` blob,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `files`
--

LOCK TABLES `files` WRITE;
/*!40000 ALTER TABLE `files` DISABLE KEYS */;
INSERT INTO `files` VALUES (1,'20220216-115425.txt',_binary '\r\n            DEFAULT	DEFAULT	DEFAULT	DEFAULT	DEFAULT	DEFAULT	DEFAULT	DEFAULT	DEFAULT	DEFAULT	DEFAULT\r\n	TIME	TIME	ACC_X	ACC_Y	ACC_Z	GYR_X	GYR_Y	GYR_Z	MAG_X	MAG_Y	MAG_Z\r\n	FRAME_NUMBERS	ANALOG	ANALOG	ANALOG	ANALOG	ANALOG	ANALOG	ANALOG	ANALOG	ANALOG	ANALOG\r\n	ORIGINAL	ORIGINAL	ORIGINAL	ORIGINAL	ORIGINAL	ORIGINAL	ORIGINAL	ORIGINAL	ORIGINAL	ORIGINAL	ORIGINAL\r\nITEM	0	0	x	x	x	x	x	x	x	x	x\r\n 0 2022-02-16 1645008869.6054118 -9.10E-02 -1.77e-01 1.01e+01 2.02e-02 -1.60e-03 6.39e-03 1.50e-01 4.91e+03 4.41e+03\r\n 0 2022-02-16 1645008869.6064425 -9.10E-02 -1.77e-01 1.01e+01 2.02e-02 -1.60e-03 6.39e-03 1.50e-01 4.91e+03 4.41e+03\r\n 0 2022-02-16 1645008869.615314 -1.20E-01 -4.31e-02 1.00e+01 2.34e-02 -1.44e-02 1.60e-02 1.50e-01 4.91e+03 4.41e+03\r\n 0 2022-02-16 1645008869.615314 -1.77E-01 0.00e+00 9.96e+00 1.76e-02 -1.01e-02 1.49e-02 1.50e-01 4.84e+03 4.41e+03\r\n 0 2022-02-16 1645008869.636913 -1.25E-01 -6.23e-02 1.01e+01 7.99e-03 -4.26e-03 1.49e-02 1.50e-01 4.84e+03 4.11e+03\r\n 0 2022-02-16 1645008869.6379452 -1.05E-01 -5.27e-02 1.01e+01 1.33e-02 -3.73e-03 3.73e-03 1.50e-01 4.84e+03 4.11e+03\r\n 0 2022-02-16 1645008869.66541 -1.48E-01 -1.92e-01 1.02e+01 2.34e-02 -4.26e-03 7.46e-03 1.50e-01 4.72e+03 4.30e+03\r\n 0 2022-02-16 1645008869.666442 -1.10E-01 4.79e-03 1.01e+01 1.44e-02 3.20e-03 1.49e-02 1.50e-01 4.30e+03 4.64e+03\r\n 0 2022-02-16 1645008869.6747196 -1.72E-01 -5.27e-02 1.00e+01 1.86e-02 -6.39e-03 1.86e-02 1.50e-01 4.30e+03 4.64e+03\r\n 0 2022-02-16 1645008869.6757214 -1.25E-01 -4.79e-02 1.01e+01 2.18e-02 -5.33e-04 1.23e-02 1.50e-01 -4.87e+03 4.53e+03\r\n 0 2022-02-16 1645008869.6979496 -1.53E-01 -1.44e-02 1.01e+01 2.34e-02 -9.59e-03 1.44e-02 1.50e-01 4.72e+03 4.30e+03\r\n 0 2022-02-16 1645008869.6979496 -1.77E-01 -7.18e-02 9.93e+00 1.76e-02 -4.79e-03 1.54e-02 1.50e-01 -4.84e+03 4.41e+03\r\n 0 2022-02-16 1645008869.7264335 -1.96E-01 -6.70e-02 1.01e+01 1.65e-02 -1.60e-03 7.46e-03 1.50e-01 -4.84e+03 4.41e+03\r\n 0 2022-02-16 1645008869.7264335 -1.92E-01 -7.18e-02 1.02e+01 1.17e-02 -4.26e-03 1.33e-02 1.50e-01 4.72e+03 4.41e+03\r\n 0 2022-02-16 1645008869.7344282 -7.66E-02 -5.75e-02 1.00e+01 1.49e-02 5.33e-04 2.29e-02 1.50e-01 4.49e+03 4.45e+03\r\n 0 2022-02-16 1645008869.7354426 -5.75E-02 -7.18e-02 1.00e+01 2.08e-02 -7.99e-03 2.66e-03 1.50e-01 4.49e+03 4.45e+03\r\n 0 2022-02-16 1645008869.75795 -1.34E-01 0.00e+00 1.01e+01 1.81e-02 -4.79e-03 1.97e-02 1.50e-01 4.76e+03 4.53e+03\r\n 0 2022-02-16 1645008869.75795 -2.44E-01 -4.79e-03 1.01e+01 2.24e-02 -4.79e-03 1.44e-02 1.50e-01 4.72e+03 4.49e+03\r\n 0 2022-02-16 1645008869.7863352 -1.77E-01 -4.31e-02 1.01e+01 1.54e-02 -1.60e-03 4.79e-03 1.50e-01 4.87e+03 4.14e+03\r\n 0 2022-02-16 1645008869.7863352 -1.72E-01 3.35e-02 1.00e+01 2.50e-02 -1.07e-03 1.12e-02 1.50e-01 4.87e+03 4.14e+03\r\n 0 2022-02-16 1645008869.7953146 -1.87E-01 -1.48e-01 1.01e+01 1.23e-02 -2.66e-03 1.54e-02 1.50e-01 -4.87e+03 3.88e+03\r\n 0 2022-02-16 1645008869.7953146 -2.15E-01 -4.79e-02 1.02e+01 2.29e-02 -4.26e-03 1.70e-02 1.50e-01 -4.87e+03 4.26e+03\r\n 0 2022-02-16 1645008869.8173788 -4.79E-02 1.44e-02 1.01e+01 2.34e-02 -5.86e-03 1.33e-02 1.50e-01 -4.87e+03 4.26e+03\r\n 0 2022-02-16 1645008869.8173788 -2.20E-01 -8.62e-02 1.01e+01 2.24e-02 1.07e-03 1.76e-02 1.50e-01 4.87e+03 4.45e+03\r\n 0 2022-02-16 1645008869.8453395 -2.06E-01 -1.01e-01 1.01e+01 2.50e-02 -7.46e-03 1.86e-02 1.50e-01 -4.76e+03 4.53e+03\r\n 0 2022-02-16 1645008869.8463364 -2.49E-01 -2.87e-02 9.98e+00 2.50e-02 -4.79e-03 6.39e-03 1.50e-01 -4.76e+03 4.53e+03\r\n 0 2022-02-16 1645008869.855314 -9.58E-02 -6.70e-02 1.01e+01 1.49e-02 -2.13e-03 1.12e-02 1.50e-01 -4.64e+03 4.03e+03\r\n 0 2022-02-16 1645008869.855314 -1.25E-01 -6.23e-02 1.00e+01 1.70e-02 -6.39e-03 1.49e-02 1.50e-01 -4.84e+03 4.49e+03\r\n 0 2022-02-16 1645008869.993126 -1.53E-01 -6.70e-02 1.01e+01 1.54e-02 -3.20e-03 1.54e-02 1.50e-01 4.64e+03 4.49e+03\r\n 0 2022-02-16 1645008869.993126 -2.35E-01 -1.96e-01 1.01e+01 2.56e-02 -5.33e-04 1.49e-02 1.50e-01 4.64e+03 4.49e+03\r\n 0 2022-02-16 1645008869.993126 -1.77E-01 -1.25e-01 1.01e+01 1.33e-02 -7.46e-03 7.99e-03 1.50e-01 4.49e+03 4.26e+03\r\n 0 2022-02-16 1645008869.993126 -1.87E-01 5.75e-02 1.01e+01 2.45e-02 3.73e-03 1.28e-02 1.50e-01 4.57e+03 4.45e+03\r\n 0 2022-02-16 1645008869.993126 -1.96E-01 2.39e-02 1.01e+01 2.08e-02 -1.23e-02 3.73e-03 1.50e-01 4.57e+03 4.45e+03\r\n 0 2022-02-16 1645008869.993126 -3.83E-02 -6.70e-02 1.01e+01 2.13e-02 -4.26e-03 1.44e-02 1.50e-01 4.72e+03 4.03e+03\r\n 0 2022-02-16 1645008869.9941273 -5.75E-02 -7.18e-02 1.01e+01 1.70e-02 -6.92e-03 1.38e-02 1.50e-01 4.64e+03 4.30e+03\r\n 0 2022-02-16 1645008869.9941273 -1.20E-01 -1.92e-02 1.00e+01 1.17e-02 -1.01e-02 6.39e-03 1.50e-01 4.64e+03 4.30e+03\r\n 0 2022-02-16 1645008869.9941273 -1.53E-01 -9.58e-02 1.01e+01 2.13e-02 -3.73e-03 1.60e-02 1.50e-01 4.57e+03 4.26e+03\r\n 0 2022-02-16 1645008869.9941273 -1.77E-01 4.79e-03 1.00e+01 2.98e-02 -4.26e-03 1.01e-02 1.50e-01 4.68e+03 4.34e+03\r\n');
/*!40000 ALTER TABLE `files` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `graph_json`
--

DROP TABLE IF EXISTS `graph_json`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `graph_json` (
  `num_test` int NOT NULL,
  `id_paciente` int NOT NULL,
  `graph` json DEFAULT NULL,
  PRIMARY KEY (`num_test`,`id_paciente`),
  CONSTRAINT `graph_json_ibfk_1` FOREIGN KEY (`num_test`, `id_paciente`) REFERENCES `test` (`num_test`, `id_paciente`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `graph_json`
--

LOCK TABLES `graph_json` WRITE;
/*!40000 ALTER TABLE `graph_json` DISABLE KEYS */;
/*!40000 ALTER TABLE `graph_json` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `model`
--

DROP TABLE IF EXISTS `model`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `model` (
  `id` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `model`
--

LOCK TABLES `model` WRITE;
/*!40000 ALTER TABLE `model` DISABLE KEYS */;
/*!40000 ALTER TABLE `model` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pacientes_asociados`
--

DROP TABLE IF EXISTS `pacientes_asociados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pacientes_asociados` (
  `id_paciente` int NOT NULL,
  `id_medico` int NOT NULL,
  PRIMARY KEY (`id_paciente`,`id_medico`),
  KEY `id_medico` (`id_medico`),
  CONSTRAINT `pacientes_asociados_ibfk_1` FOREIGN KEY (`id_paciente`) REFERENCES `users` (`id`),
  CONSTRAINT `pacientes_asociados_ibfk_2` FOREIGN KEY (`id_medico`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pacientes_asociados`
--

LOCK TABLES `pacientes_asociados` WRITE;
/*!40000 ALTER TABLE `pacientes_asociados` DISABLE KEYS */;
INSERT INTO `pacientes_asociados` VALUES (4,7),(6,7);
/*!40000 ALTER TABLE `pacientes_asociados` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `permissions` text,
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'admin',NULL,'datos-personales-personal-centro,datos-personales-pacientes-centro','2023-02-14 11:18:08'),(2,'admin-centro',NULL,'datos-personales-personal-centro,datos-personales-pacientes-centro','2023-02-14 11:18:08'),(3,'medico',NULL,'datos-personales-pacientes-asociados,datos-clinicos-pacientes-asociados','2023-02-14 11:18:08'),(4,'auxiliar',NULL,'datos-personales-pacientes-centro','2023-02-14 11:18:08'),(5,'paciente',NULL,'{}','2023-02-14 11:18:08');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles_users`
--

DROP TABLE IF EXISTS `roles_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles_users` (
  `user_id` int DEFAULT NULL,
  `role_id` int DEFAULT NULL,
  KEY `user_id` (`user_id`),
  KEY `role_id` (`role_id`),
  CONSTRAINT `roles_users_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `roles_users_ibfk_2` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles_users`
--

LOCK TABLES `roles_users` WRITE;
/*!40000 ALTER TABLE `roles_users` DISABLE KEYS */;
INSERT INTO `roles_users` VALUES (1,1),(2,4),(3,4),(4,5),(5,5),(6,5),(7,3),(8,3),(9,3),(10,5);
/*!40000 ALTER TABLE `roles_users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `test`
--

DROP TABLE IF EXISTS `test`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `test` (
  `num_test` int NOT NULL,
  `id_paciente` int NOT NULL,
  `id_centro` int DEFAULT NULL,
  `date` date DEFAULT NULL,
  `bow` float DEFAULT NULL,
  `fall_to_left` float DEFAULT NULL,
  `fall_to_right` float DEFAULT NULL,
  `falling_backward` float DEFAULT NULL,
  `falling_forward` float DEFAULT NULL,
  `idle` float DEFAULT NULL,
  `sitting` float DEFAULT NULL,
  `sleep` float DEFAULT NULL,
  `standing` float DEFAULT NULL,
  `model` int DEFAULT NULL,
  PRIMARY KEY (`num_test`,`id_paciente`),
  KEY `id_paciente` (`id_paciente`),
  KEY `id_centro` (`id_centro`),
  KEY `model` (`model`),
  CONSTRAINT `test_ibfk_1` FOREIGN KEY (`id_paciente`) REFERENCES `users` (`id`),
  CONSTRAINT `test_ibfk_2` FOREIGN KEY (`id_centro`) REFERENCES `centros` (`id`) ON DELETE SET NULL,
  CONSTRAINT `test_ibfk_3` FOREIGN KEY (`model`) REFERENCES `model` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `test`
--

LOCK TABLES `test` WRITE;
/*!40000 ALTER TABLE `test` DISABLE KEYS */;
INSERT INTO `test` VALUES (0,4,1,'2022-02-16',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(0,6,2,'2022-02-16',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(1,4,1,'2022-02-16',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(2,4,1,'2022-02-16',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `test` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `test_unit`
--

DROP TABLE IF EXISTS `test_unit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `test_unit` (
  `num_test` int NOT NULL,
  `id_paciente` int NOT NULL,
  `item` int DEFAULT NULL,
  `time` double NOT NULL,
  `acc_x` float DEFAULT NULL,
  `acc_y` float DEFAULT NULL,
  `acc_z` float DEFAULT NULL,
  `gyr_x` float DEFAULT NULL,
  `gyr_y` float DEFAULT NULL,
  `gyr_z` float DEFAULT NULL,
  `mag_x` float DEFAULT NULL,
  `mag_y` float DEFAULT NULL,
  `mag_z` float DEFAULT NULL,
  PRIMARY KEY (`num_test`,`id_paciente`,`time`),
  CONSTRAINT `test_unit_ibfk_1` FOREIGN KEY (`num_test`, `id_paciente`) REFERENCES `test` (`num_test`, `id_paciente`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `test_unit`
--

LOCK TABLES `test_unit` WRITE;
/*!40000 ALTER TABLE `test_unit` DISABLE KEYS */;
INSERT INTO `test_unit` VALUES (0,4,0,1645008869.6054118,-0.091,-0.177,10.1,0.0202,-0.0016,0.00639,0.15,4910,4410),(0,4,1,1645008869.6064425,-0.091,-0.177,10.1,0.0202,-0.0016,0.00639,0.15,4910,4410),(0,4,2,1645008869.615314,-0.12,-0.0431,10,0.0234,-0.0144,0.016,0.15,4910,4410),(0,4,4,1645008869.636913,-0.125,-0.0623,10.1,0.00799,-0.00426,0.0149,0.15,4840,4110),(0,4,5,1645008869.6379452,-0.105,-0.0527,10.1,0.0133,-0.00373,0.00373,0.15,4840,4110),(0,4,6,1645008869.66541,-0.148,-0.192,10.2,0.0234,-0.00426,0.00746,0.15,4720,4300),(0,4,7,1645008869.666442,-0.11,0.00479,10.1,0.0144,0.0032,0.0149,0.15,4300,4640),(0,4,8,1645008869.6747196,-0.172,-0.0527,10,0.0186,-0.00639,0.0186,0.15,4300,4640),(0,4,9,1645008869.6757214,-0.125,-0.0479,10.1,0.0218,-0.000533,0.0123,0.15,-4870,4530),(0,4,10,1645008869.6979496,-0.153,-0.0144,10.1,0.0234,-0.00959,0.0144,0.15,4720,4300),(0,4,12,1645008869.7264335,-0.196,-0.067,10.1,0.0165,-0.0016,0.00746,0.15,-4840,4410),(0,4,14,1645008869.7344282,-0.0766,-0.0575,10,0.0149,0.000533,0.0229,0.15,4490,4450),(0,4,15,1645008869.7354426,-0.0575,-0.0718,10,0.0208,-0.00799,0.00266,0.15,4490,4450),(0,4,16,1645008869.75795,-0.134,0,10.1,0.0181,-0.00479,0.0197,0.15,4760,4530),(0,4,18,1645008869.7863352,-0.177,-0.0431,10.1,0.0154,-0.0016,0.00479,0.15,4870,4140),(0,4,20,1645008869.7953146,-0.187,-0.148,10.1,0.0123,-0.00266,0.0154,0.15,-4870,3880),(0,4,22,1645008869.8173788,-0.0479,0.0144,10.1,0.0234,-0.00586,0.0133,0.15,-4870,4260),(0,4,24,1645008869.8453395,-0.206,-0.101,10.1,0.025,-0.00746,0.0186,0.15,-4760,4530),(0,4,25,1645008869.8463364,-0.249,-0.0287,9.98,0.025,-0.00479,0.00639,0.15,-4760,4530),(0,4,26,1645008869.855314,-0.0958,-0.067,10.1,0.0149,-0.00213,0.0112,0.15,-4640,4030),(0,4,28,1645008869.993126,-0.153,-0.067,10.1,0.0154,-0.0032,0.0154,0.15,4640,4490),(0,4,34,1645008869.9941273,-0.0575,-0.0718,10.1,0.017,-0.00692,0.0138,0.15,4640,4300),(0,6,0,1645008869.6054118,-0.091,-0.177,10.1,0.0202,-0.0016,0.00639,0.15,4910,4410),(0,6,1,1645008869.6064425,-0.091,-0.177,10.1,0.0202,-0.0016,0.00639,0.15,4910,4410),(0,6,2,1645008869.615314,-0.12,-0.0431,10,0.0234,-0.0144,0.016,0.15,4910,4410),(0,6,4,1645008869.636913,-0.125,-0.0623,10.1,0.00799,-0.00426,0.0149,0.15,4840,4110),(0,6,5,1645008869.6379452,-0.105,-0.0527,10.1,0.0133,-0.00373,0.00373,0.15,4840,4110),(0,6,6,1645008869.66541,-0.148,-0.192,10.2,0.0234,-0.00426,0.00746,0.15,4720,4300),(0,6,7,1645008869.666442,-0.11,0.00479,10.1,0.0144,0.0032,0.0149,0.15,4300,4640),(0,6,8,1645008869.6747196,-0.172,-0.0527,10,0.0186,-0.00639,0.0186,0.15,4300,4640),(0,6,9,1645008869.6757214,-0.125,-0.0479,10.1,0.0218,-0.000533,0.0123,0.15,-4870,4530),(0,6,10,1645008869.6979496,-0.153,-0.0144,10.1,0.0234,-0.00959,0.0144,0.15,4720,4300),(0,6,12,1645008869.7264335,-0.196,-0.067,10.1,0.0165,-0.0016,0.00746,0.15,-4840,4410),(0,6,14,1645008869.7344282,-0.0766,-0.0575,10,0.0149,0.000533,0.0229,0.15,4490,4450),(0,6,15,1645008869.7354426,-0.0575,-0.0718,10,0.0208,-0.00799,0.00266,0.15,4490,4450),(0,6,16,1645008869.75795,-0.134,0,10.1,0.0181,-0.00479,0.0197,0.15,4760,4530),(0,6,18,1645008869.7863352,-0.177,-0.0431,10.1,0.0154,-0.0016,0.00479,0.15,4870,4140),(0,6,20,1645008869.7953146,-0.187,-0.148,10.1,0.0123,-0.00266,0.0154,0.15,-4870,3880),(0,6,22,1645008869.8173788,-0.0479,0.0144,10.1,0.0234,-0.00586,0.0133,0.15,-4870,4260),(0,6,24,1645008869.8453395,-0.206,-0.101,10.1,0.025,-0.00746,0.0186,0.15,-4760,4530),(0,6,25,1645008869.8463364,-0.249,-0.0287,9.98,0.025,-0.00479,0.00639,0.15,-4760,4530),(0,6,26,1645008869.855314,-0.0958,-0.067,10.1,0.0149,-0.00213,0.0112,0.15,-4640,4030),(0,6,28,1645008869.993126,-0.153,-0.067,10.1,0.0154,-0.0032,0.0154,0.15,4640,4490),(0,6,34,1645008869.9941273,-0.0575,-0.0718,10.1,0.017,-0.00692,0.0138,0.15,4640,4300),(1,4,0,1645008869.6054118,-0.091,-0.177,10.1,0.0202,-0.0016,0.00639,0.15,4910,4410),(1,4,1,1645008869.6064425,-0.091,-0.177,10.1,0.0202,-0.0016,0.00639,0.15,4910,4410),(1,4,2,1645008869.615314,-0.12,-0.0431,10,0.0234,-0.0144,0.016,0.15,4910,4410),(1,4,4,1645008869.636913,-0.125,-0.0623,10.1,0.00799,-0.00426,0.0149,0.15,4840,4110),(1,4,5,1645008869.6379452,-0.105,-0.0527,10.1,0.0133,-0.00373,0.00373,0.15,4840,4110),(1,4,6,1645008869.66541,-0.148,-0.192,10.2,0.0234,-0.00426,0.00746,0.15,4720,4300),(1,4,7,1645008869.666442,-0.11,0.00479,10.1,0.0144,0.0032,0.0149,0.15,4300,4640),(1,4,8,1645008869.6747196,-0.172,-0.0527,10,0.0186,-0.00639,0.0186,0.15,4300,4640),(1,4,9,1645008869.6757214,-0.125,-0.0479,10.1,0.0218,-0.000533,0.0123,0.15,-4870,4530),(1,4,10,1645008869.6979496,-0.153,-0.0144,10.1,0.0234,-0.00959,0.0144,0.15,4720,4300),(1,4,12,1645008869.7264335,-0.196,-0.067,10.1,0.0165,-0.0016,0.00746,0.15,-4840,4410),(1,4,14,1645008869.7344282,-0.0766,-0.0575,10,0.0149,0.000533,0.0229,0.15,4490,4450),(1,4,15,1645008869.7354426,-0.0575,-0.0718,10,0.0208,-0.00799,0.00266,0.15,4490,4450),(1,4,16,1645008869.75795,-0.134,0,10.1,0.0181,-0.00479,0.0197,0.15,4760,4530),(1,4,18,1645008869.7863352,-0.177,-0.0431,10.1,0.0154,-0.0016,0.00479,0.15,4870,4140),(1,4,20,1645008869.7953146,-0.187,-0.148,10.1,0.0123,-0.00266,0.0154,0.15,-4870,3880),(1,4,22,1645008869.8173788,-0.0479,0.0144,10.1,0.0234,-0.00586,0.0133,0.15,-4870,4260),(1,4,24,1645008869.8453395,-0.206,-0.101,10.1,0.025,-0.00746,0.0186,0.15,-4760,4530),(1,4,25,1645008869.8463364,-0.249,-0.0287,9.98,0.025,-0.00479,0.00639,0.15,-4760,4530),(1,4,26,1645008869.855314,-0.0958,-0.067,10.1,0.0149,-0.00213,0.0112,0.15,-4640,4030),(1,4,28,1645008869.993126,-0.153,-0.067,10.1,0.0154,-0.0032,0.0154,0.15,4640,4490),(1,4,34,1645008869.9941273,-0.0575,-0.0718,10.1,0.017,-0.00692,0.0138,0.15,4640,4300),(2,4,0,1645008869.6054118,-0.091,-0.177,10.1,0.0202,-0.0016,0.00639,0.15,4910,4410),(2,4,1,1645008869.6064425,-0.091,-0.177,10.1,0.0202,-0.0016,0.00639,0.15,4910,4410),(2,4,2,1645008869.615314,-0.12,-0.0431,10,0.0234,-0.0144,0.016,0.15,4910,4410),(2,4,4,1645008869.636913,-0.125,-0.0623,10.1,0.00799,-0.00426,0.0149,0.15,4840,4110),(2,4,5,1645008869.6379452,-0.105,-0.0527,10.1,0.0133,-0.00373,0.00373,0.15,4840,4110),(2,4,6,1645008869.66541,-0.148,-0.192,10.2,0.0234,-0.00426,0.00746,0.15,4720,4300),(2,4,7,1645008869.666442,-0.11,0.00479,10.1,0.0144,0.0032,0.0149,0.15,4300,4640),(2,4,8,1645008869.6747196,-0.172,-0.0527,10,0.0186,-0.00639,0.0186,0.15,4300,4640),(2,4,9,1645008869.6757214,-0.125,-0.0479,10.1,0.0218,-0.000533,0.0123,0.15,-4870,4530),(2,4,10,1645008869.6979496,-0.153,-0.0144,10.1,0.0234,-0.00959,0.0144,0.15,4720,4300),(2,4,12,1645008869.7264335,-0.196,-0.067,10.1,0.0165,-0.0016,0.00746,0.15,-4840,4410),(2,4,14,1645008869.7344282,-0.0766,-0.0575,10,0.0149,0.000533,0.0229,0.15,4490,4450),(2,4,15,1645008869.7354426,-0.0575,-0.0718,10,0.0208,-0.00799,0.00266,0.15,4490,4450),(2,4,16,1645008869.75795,-0.134,0,10.1,0.0181,-0.00479,0.0197,0.15,4760,4530),(2,4,18,1645008869.7863352,-0.177,-0.0431,10.1,0.0154,-0.0016,0.00479,0.15,4870,4140),(2,4,20,1645008869.7953146,-0.187,-0.148,10.1,0.0123,-0.00266,0.0154,0.15,-4870,3880),(2,4,22,1645008869.8173788,-0.0479,0.0144,10.1,0.0234,-0.00586,0.0133,0.15,-4870,4260),(2,4,24,1645008869.8453395,-0.206,-0.101,10.1,0.025,-0.00746,0.0186,0.15,-4760,4530),(2,4,25,1645008869.8463364,-0.249,-0.0287,9.98,0.025,-0.00479,0.00639,0.15,-4760,4530),(2,4,26,1645008869.855314,-0.0958,-0.067,10.1,0.0149,-0.00213,0.0112,0.15,-4640,4030),(2,4,28,1645008869.993126,-0.153,-0.067,10.1,0.0154,-0.0032,0.0154,0.15,4640,4490),(2,4,34,1645008869.9941273,-0.0575,-0.0718,10.1,0.017,-0.00692,0.0138,0.15,4640,4300);
/*!40000 ALTER TABLE `test_unit` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `training_point`
--

DROP TABLE IF EXISTS `training_point`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `training_point` (
  `model_id` int NOT NULL,
  `index` int NOT NULL,
  `clase` varchar(20) DEFAULT NULL,
  `acc_x` float DEFAULT NULL,
  `acc_y` float DEFAULT NULL,
  `acc_z` float DEFAULT NULL,
  PRIMARY KEY (`model_id`,`index`),
  CONSTRAINT `training_point_ibfk_1` FOREIGN KEY (`model_id`) REFERENCES `model` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `training_point`
--

LOCK TABLES `training_point` WRITE;
/*!40000 ALTER TABLE `training_point` DISABLE KEYS */;
/*!40000 ALTER TABLE `training_point` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `active` tinyint(1) NOT NULL,
  `fs_uniquifier` varchar(64) NOT NULL,
  `confirmed_at` datetime DEFAULT NULL,
  `last_login_at` datetime DEFAULT NULL,
  `current_login_at` datetime DEFAULT NULL,
  `last_login_ip` varchar(64) DEFAULT NULL,
  `current_login_ip` varchar(64) DEFAULT NULL,
  `login_count` int DEFAULT NULL,
  `tf_primary_method` varchar(64) DEFAULT NULL,
  `tf_totp_secret` varchar(255) DEFAULT NULL,
  `tf_phone_number` varchar(128) DEFAULT NULL,
  `create_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `us_totp_secrets` text,
  `us_phone_number` varchar(128) DEFAULT NULL,
  `id` int NOT NULL AUTO_INCREMENT,
  `identificador` varchar(10) DEFAULT NULL,
  `username` varchar(20) DEFAULT NULL,
  `nombre` varchar(50) DEFAULT NULL,
  `fecha_nacimiento` date DEFAULT NULL,
  `sexo` varchar(1) DEFAULT NULL,
  `altura` float DEFAULT NULL,
  `peso` float DEFAULT NULL,
  `antecedentes_clinicos` text,
  `id_centro` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `fs_uniquifier` (`fs_uniquifier`),
  UNIQUE KEY `identificador` (`identificador`),
  UNIQUE KEY `username` (`username`),
  KEY `id_centro` (`id_centro`),
  CONSTRAINT `users_ibfk_1` FOREIGN KEY (`id_centro`) REFERENCES `centros` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('admin@kruay.com','$2b$12$FDV5krfZ74ftYk/AtU508.p9XMUuq27zVZfHqaGSBWhLBu68SiCg.',1,'1d84632be0ca47daa32656a9d765b6d0',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2023-02-14 11:18:09','2023-02-14 11:18:09',NULL,NULL,1,'46954321F','admin',NULL,NULL,NULL,NULL,NULL,NULL,NULL),('webapptest2022@gmail.com','$2b$12$LHZ.XyKQDxm3YucRDC8JB.aQhwR.Kt.8RK98nP9rgfHhNd7lZf/0O',1,'809cd4b89b8c48979dfa3a5357fbedbc',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2023-02-14 11:18:09','2023-02-14 11:18:09',NULL,NULL,2,'46654321R','auxiliar','auxiliar',NULL,NULL,NULL,NULL,NULL,1),('auxiliar@kruay.com','$2b$12$iD8cwvucbwkLGmspDfAlLOAOkr.RF6O20bvC5Y0eS0Qi6dkoozOI6',1,'053731de380d43b1906a7ce842574662',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2023-02-14 11:18:09','2023-02-14 11:18:09',NULL,NULL,3,'35954651F','auxiliar2','auxiliar2',NULL,NULL,NULL,NULL,NULL,2),('paciente11@kruay.com','$2b$12$0qubFrJeWeW5A871Ln4yfOv6xjn4fDR0mQJlqNXTqawjApFIkwJiq',1,'1f8a0695cc804a82834d42da2cc23d86',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2023-02-14 11:18:09','2023-02-14 11:18:09',NULL,NULL,4,'54354321R','paciente11','paciente11',NULL,'V',1.79,97,'diabetis',1),('paciente12@kruay.com','$2b$12$daio4OPvEVo3BJjDWJiUwOCKRse1.pFa8QhRquqIaCLpvmqBvBiWq',1,'8acf0f18e1ec4dec88e9a033c1d7515c',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2023-02-14 11:18:10','2023-02-14 11:18:10',NULL,NULL,5,'46953125F','paciente12','paciente12',NULL,'M',1.56,57,'cancer de mama',1),('paciente21@kruay.com','$2b$12$wn2advsSgTCkXrNFEIiuFO5bWPby7zTtgwLOgEy0qSSLcS5whlW72',1,'512732997f5a43e1b12f4d53b3e02882',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2023-02-14 11:18:10','2023-02-14 11:18:10',NULL,NULL,6,'75954321F','paciente21','paciente21',NULL,'V',1.91,75,'cancer de pulmon, cancer de prostata, problemas hepaticos',2),('medico@kruay.com','$2b$12$TiDNmvClfH4Nb6cm5LJEk.xnJxKB2Y13F8D2QwvfhAfOTVZ3gfj2W',1,'ce1b13cb483548e4a45d5e51525ab7bd',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2023-02-14 11:18:10','2023-02-14 11:18:10',NULL,NULL,7,'98957621F','medico','medico',NULL,NULL,NULL,NULL,NULL,1),('medico1@kruay.com','$2b$12$VV2jAL4qYj9LwkFyLsXoBuv/jLfI44BxtPl0jVQTw1a4YiaZX9X4i',1,'843a9aaeea8c49d7b98a0c924d8fd5c3',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2023-02-14 11:18:11','2023-02-14 11:18:11',NULL,NULL,8,'52354321R','medico1','medico1',NULL,NULL,NULL,NULL,NULL,1),('medico2@kruay.com','$2b$12$4MDAD5A8t/mbFpIOJ/7Wx.ATsrWKq6jaVarEx5ikDAuMn/RkXMonG',1,'af57ec2333074bbdb7c1725a058b1dd2',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2023-02-14 11:18:11','2023-02-14 11:18:11',NULL,NULL,9,'89354321F','medico2','medico2',NULL,NULL,NULL,NULL,NULL,2),('default754355@invented_mail.com','$2b$12$Ki3TIkZW.lktVz7bifSBOu7/5eWh4CKL8RD9efOchfMXX7RoAbuEm',1,'8c8c494709d7415bb126e25940b873e9',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2023-02-14 13:06:51','2023-02-14 13:06:51',NULL,NULL,10,'2002',NULL,'Paciente2023','2001-01-14','V',180,80,NULL,1);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-03-07 13:42:02
