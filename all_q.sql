create database KMS;
use KMS;

CREATE TABLE `summary` (
  `interval` int(11) NOT NULL,
  `passedQC` int(11) NOT NULL DEFAULT '0',
  `failedQC` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`interval`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `zone`(
	`id` int(11) NOT NULL DEFAULT '0',
    `name` varchar(50) NOT NULL,
    `state` int(11) DEFAULT NULL,
    PRIMARY KEY (`id`),
	KEY `state` (`state`)
) ENGINE = InnoDB DEFAULT CHARSET = latin1;

CREATE TABLE `state` (
  `id` int(11) NOT NULL DEFAULT '0',
  `name` varchar(50) NOT NULL,
  `zone` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `zone` (`zone`),
  CONSTRAINT `state_ibfk_1` FOREIGN KEY (`zone`) REFERENCES `zone` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `city` (
  `id` int(11) NOT NULL DEFAULT '0',
  `name` varchar(50) NOT NULL,
  `state` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `state` (`state`),
  CONSTRAINT `city_ibfk_1` FOREIGN KEY (`state`) REFERENCES `state` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `store` (
  `id` int(11) NOT NULL DEFAULT '0',
  `client_id` varchar(100) NOT NULL,
  `name` varchar(100) NOT NULL,
  `city` int(11) NOT NULL,
  `address` varchar(100) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `city` (`city`),
  CONSTRAINT `store_ibfk_1` FOREIGN KEY (`city`) REFERENCES `city` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `brand` (
  `id` int(11) NOT NULL DEFAULT '0',
  `name` varchar(50) NOT NULL,
  `brandImage` varchar(150) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `dashboard` (
  `S_No` int(11) NOT NULL AUTO_INCREMENT,
  `order_id` varchar(50) DEFAULT NULL,
  `user` int(11) NOT NULL DEFAULT '0',
  `productId` int(11) NOT NULL DEFAULT '0',
  `productName` varchar(100) NOT NULL,
  `brand` int(11) NOT NULL DEFAULT '0',
  `zone` int(11) NOT NULL DEFAULT '0',
  `state` int(11) NOT NULL DEFAULT '0',
  `city` int(11) NOT NULL DEFAULT '0',
  `store` int(11) NOT NULL DEFAULT '0',
  `machine` int(11) DEFAULT NULL,
  `isVeg` varchar(10) NOT NULL,
  `MinWeight` varchar(10) DEFAULT NULL,
  `Weight` varchar(10) NOT NULL,
  `MaxWeight` varchar(10) DEFAULT NULL,
  `weightCheckRequired` varchar(10) NOT NULL,
  `weightSimulated` tinyint(4) DEFAULT NULL,
  `MinTemp` varchar(10) DEFAULT NULL,
  `Temp` varchar(10) NOT NULL,
  `MaxTemp` varchar(10) DEFAULT NULL,
  `tempCheckRequired` varchar(10) NOT NULL,
  `tempSimulated` tinyint(4) DEFAULT NULL,
  `foodImage` varchar(200) DEFAULT NULL,
  `foodImageSimulated` tinyint(4) DEFAULT NULL,
  `faceImage` varchar(200) DEFAULT NULL,
  `faceImageSimulated` tinyint(4) DEFAULT NULL,
  `date` date NOT NULL,
  `date_no` int(11) DEFAULT NULL,
  `month_no` int(11) DEFAULT '0',
  `week_day` int(11) DEFAULT '0',
  `week_no` int(11) DEFAULT '0',
  `year` int(11) DEFAULT '0',
  `orderReceivedAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `timeTaken` timestamp NULL DEFAULT NULL,
  `passed` int(11) DEFAULT NULL,
  `failed` int(11) DEFAULT NULL,
  `interval` int(8) NOT NULL DEFAULT '0',
  PRIMARY KEY (`S_No`)
) ENGINE=InnoDB AUTO_INCREMENT=67 DEFAULT CHARSET=latin1;

CREATE TABLE `live` (
  `mac` varchar(17) NOT NULL,
  `machine` int(11) NOT NULL,
  `user` int(11) NOT NULL,
  `updatedAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `lastQcAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `orderId` varchar(50) DEFAULT NULL,
  `productName` varchar(50) DEFAULT NULL,
  `isVeg` tinyint(4) DEFAULT NULL,
  `MinWeight` varchar(10) DEFAULT NULL,
  `Weight` varchar(25) DEFAULT NULL,
  `MaxWeight` varchar(10) DEFAULT NULL,
  `weightCheckRequired` tinyint(4) DEFAULT NULL,
  `weightSimulated` tinyint(4) DEFAULT NULL,
  `MinTemp` varchar(10) DEFAULT NULL,
  `Temp` varchar(25) DEFAULT NULL,
  `MaxTemp` varchar(10) DEFAULT NULL,
  `tempCheckRequired` tinyint(4) DEFAULT NULL,
  `tempSimulated` tinyint(4) DEFAULT NULL,
  `foodImage` varchar(200) DEFAULT NULL,
  `foodImageSimulated` tinyint(4) DEFAULT NULL,
  `faceImage` varchar(200) DEFAULT NULL,
  `faceImageSimulated` tinyint(4) DEFAULT NULL,
  `live_temp` varchar(15) DEFAULT NULL,
  `live_weight` varchar(15) DEFAULT NULL,
  `TempSensor` tinyint(4) DEFAULT NULL,
  `weighingScale` tinyint(4) DEFAULT NULL,
  `foodCamera` tinyint(4) NOT NULL,
  `faceCamera` tinyint(4) NOT NULL,
  `clientServer` tinyint(4) DEFAULT NULL,
  `State` varchar(25) NOT NULL,
  `QC_Result` varchar(40) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `machineHealth` (
  `S_No` int(11) NOT NULL AUTO_INCREMENT,
  `mac` varchar(17) NOT NULL,
  `machine` int(11) NOT NULL,
  `user` int(11) NOT NULL,
  `updatedAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `TempSensor` tinyint(4) NOT NULL,
  `tempSimulated` tinyint(4) DEFAULT NULL,
  `weighingScale` tinyint(4) NOT NULL,
  `weightSimulated` tinyint(4) DEFAULT NULL,
  `foodCamera` tinyint(4) NOT NULL,
  `foodImageSimulated` tinyint(4) DEFAULT NULL,
  `faceCamera` tinyint(4) NOT NULL,
  `faceImageSimulated` tinyint(4) DEFAULT NULL,
  `clientServer` tinyint(4) NOT NULL,
  `State` varchar(15) NOT NULL,
  PRIMARY KEY (`S_No`)
) ENGINE=InnoDB AUTO_INCREMENT=3828 DEFAULT CHARSET=latin1;

CREATE TABLE `user` (
  `id` int(11) NOT NULL DEFAULT '0',
  `username` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `client_id` varchar(50) NOT NULL,
  `display_name` varchar(50) NOT NULL,
  `is_active` tinyint(4) NOT NULL DEFAULT '0',
  `email` varchar(100) NOT NULL,
  `contact` varchar(50) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `store` (
  `id` int(11) NOT NULL DEFAULT '0',
  `client_id` varchar(100) NOT NULL,
  `name` varchar(100) NOT NULL,
  `city` int(11) NOT NULL,
  `address` varchar(100) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `city` (`city`),
  CONSTRAINT `store_ibfk_1` FOREIGN KEY (`city`) REFERENCES `city` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `user_store_mapping` (
  `user` int(11) NOT NULL,
  `store` int(11) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  KEY `store` (`store`),
  KEY `user` (`user`),
  CONSTRAINT `user_store_mapping_ibfk_1` FOREIGN KEY (`store`) REFERENCES `store` (`id`),
  CONSTRAINT `user_store_mapping_ibfk_2` FOREIGN KEY (`user`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
CREATE TABLE `machine` (
  `id` int(11) NOT NULL DEFAULT '0',
  `store` int(11) NOT NULL,
  `mac` varchar(17) NOT NULL,
  `serial_number` varchar(25) NOT NULL,
  `model_number` varchar(25) NOT NULL,
  `manufactured_on` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `installed_on` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `warranty_expires_on` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `software_version` varchar(25) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `store` (`store`),
  CONSTRAINT `machine_ibfk_1` FOREIGN KEY (`store`) REFERENCES `store` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;