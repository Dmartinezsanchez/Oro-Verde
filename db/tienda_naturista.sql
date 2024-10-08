-- MySQL dump 10.13  Distrib 8.0.38, for Win64 (x86_64)
--
-- Host: localhost    Database: tienda_naturista
-- ------------------------------------------------------
-- Server version	8.0.38

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
-- Table structure for table `productos`
--

DROP TABLE IF EXISTS `productos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `productos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre_producto` varchar(255) NOT NULL,
  `cantidad` int NOT NULL,
  `valor` int NOT NULL,
  `imagen_url` varchar(300) DEFAULT NULL,
  `descripcion` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `productos`
--

LOCK TABLES `productos` WRITE;
/*!40000 ALTER TABLE `productos` DISABLE KEYS */;
INSERT INTO `productos` VALUES (1,'Aceite de Almendras',12,27000,'Imagenes/AceiteAlmendras.jpeg','Aceite altamente hidratante y suavizante de la piel'),(2,'Aceite de Cal├®ndula',12,27000,'Imagenes/AceiteCalendula.jpeg','Aceite super hidratante'),(3,'Aceite de Coco',0,27000,'Imagenes/AceiteCoco.jpeg',NULL),(4,'Aceite de Coco Extravirgen',0,27000,'Imagenes/AceiteCocoExtravirgen.jpeg',NULL),(5,'Aceite de Eucalipto',0,27000,'Imagenes/AceiteEucalipto.jpeg',NULL),(6,'Aceite de Fenogreco',0,27000,'Imagenes/AceiteFenogreco.jpeg',NULL),(7,'Aceite de Higuerilla y Ricino',0,27000,'Imagenes/AceiteHiguerillaRicino.jpeg',NULL),(8,'Aceite de Jengibre',0,27000,'Imagenes/AceiteJengibre.jpeg',NULL),(9,'Aceite de Lavanda',0,27000,'Imagenes/AceiteLavanda.jpeg',NULL),(10,'Aceite de Mano de Res',0,27000,'Imagenes/AceiteManoRes.jpeg',NULL),(11,'Aceite de Naranja',0,27000,'Imagenes/AceiteNaranja.jpeg',NULL),(12,'Aceite de Naranja y Cal├®ndula',0,27000,'Imagenes/AceiteNaranjaCalendula.jpeg',NULL),(13,'Aceite de Romero',0,27000,'Imagenes/AceiteRomero.jpeg',NULL),(14,'├ücido Hialur├│nico',0,50000,'Imagenes/AcidoHialuronico.jpeg',NULL),(15,'Aguaje Hinojo',0,0,'Imagenes/AguajeHinojo.jpeg',NULL),(16,'Aguaje Reduce Medidas',0,0,'Imagenes/AguajeReduceMedidas.jpeg',NULL),(17,'Aguaje Siempre Bella',0,0,'Imagenes/AguajeSiempreBella.jpeg',NULL),(18,'Agua de Rosas',0,15000,'Imagenes/AguaRosas.jpeg',NULL),(19,'Citrato de Magnesio y Potasio',0,0,'Imagenes/CitratoMagnesioPotasio.jpeg',NULL),(20,'Citratos de Magnesio y de Potasio',0,0,'Imagenes/CitratosMagnesio-Potasio.jpeg',NULL),(21,'Cloruro de Magnesio',0,0,'Imagenes/CloruroMagnesio.jpeg',NULL),(22,'Colon Cleanser T├® Medicinal',0,0,'Imagenes/ColonCleanser.jpeg',NULL),(23,'Fibra Artesanal',0,0,'Imagenes/Fibra.jpeg',NULL),(24,'Protector Solar',0,0,'Imagenes/ProtectorSolar.jpeg',NULL),(25,'Vitafer-L',0,50000,'Imagenes/Vitafer.jpeg',NULL);
/*!40000 ALTER TABLE `productos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `contrasena` varchar(255) NOT NULL,
  `rol` enum('cliente','admin') DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (1,'Diana Martinez','nisofi20@gmail.com','$2b$12$PW..MxcKqwuD47cMJED9suQIpFrHJBppntnEm.ILIHhWGDU5t8s1G','admin'),(2,'Sofia Espinosa','Sofi@gmail.com','$2b$12$lyzI2X3v9tVkhjb4TNeQA.R9OmBE4ilN9ZT6mLZQhqVLTKovmmaMq','cliente'),(3,'Jhon Espinosa','jhon@gmail.com','$2b$12$ibIMl0.uZv3bRKueVnOZ8O37G5ClDQSQCcYEM37Gzp4BIoLxpt6ZW','cliente'),(4,'Maria Lopez','mary@gmail.com','$2b$12$qT9RnOAOkGecz4RoCsmA0eqL7xyPmh8KJeYOtB/tPVVYLANAkat5O','cliente'),(5,'pedro mora','pedro@gmail.com','$2b$12$oU0HRcBJ14AEWvW5QMJGyuNRs3thNIXMOAK4lkzb/GpL65XcNc91K','cliente'),(6,'pablo rodriguez','pablo@gmail.com','$2b$12$eYn8yujUpE.Xm0PWbYjjfOSWAOxpLpmSE/rqCQKCL4PR5pNloRy3e','cliente'),(7,'ana virrareal','ana@gmail.com','$2b$12$CK5va92Hyao82uNPO8Vo2OWCv0.D9VzaboYxTLNqD1dldSdcGDO3m','cliente'),(8,'carolina gomez','caro@gmail.com','$2b$12$UEPJF58ib5th.XrROgddm.vx6cBUj.xwVKbdP9nHTPnSWPBRULu0a','cliente'),(9,'paola campos','pao@gmail.com','$2b$12$IEv0.ze3Fi9wZpzCjFMG0OpxLaFdc2rvFLqgd1/Q3FoCT7wNTcJvi','admin');
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-09-18 17:51:45
