/*
SQLyog Community Edition- MySQL GUI v7.01 
MySQL - 5.0.27-community-nt : Database - dbroadpotholes
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`dbroadpotholes` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `dbroadpotholes`;

/*Table structure for table `tbladmin` */

DROP TABLE IF EXISTS `tbladmin`;

CREATE TABLE `tbladmin` (
  `aId` int(255) NOT NULL auto_increment,
  `uname` varchar(255) default NULL,
  `password` varchar(255) default NULL,
  `email` varchar(255) default NULL,
  PRIMARY KEY  (`aId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `tbladmin` */

insert  into `tbladmin`(`aId`,`uname`,`password`,`email`) values (1,'admin','admin','admin@gmail.com'),(2,'admin2','admin2','admin2@gmail.com');

/*Table structure for table `tblregister` */

DROP TABLE IF EXISTS `tblregister`;

CREATE TABLE `tblregister` (
  `Uid` int(255) NOT NULL auto_increment,
  `uname` varchar(255) default NULL,
  `email` varchar(255) default NULL,
  `password` varchar(255) default NULL,
  `mobile` varchar(255) default NULL,
  `address` varchar(255) default NULL,
  PRIMARY KEY  (`Uid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `tblregister` */

insert  into `tblregister`(`Uid`,`uname`,`email`,`password`,`mobile`,`address`) values (1,'Aakash','a@gmail.com','Aakash123','8468468468',NULL);

/*Table structure for table `tblroadimg` */

DROP TABLE IF EXISTS `tblroadimg`;

CREATE TABLE `tblroadimg` (
  `imgid` int(255) NOT NULL auto_increment,
  `imagepath` varchar(255) default NULL,
  `address` longtext,
  `latitude` varchar(255) default NULL,
  `longitude` varchar(255) default NULL,
  `uname` varchar(255) default NULL,
  `prediction` varchar(255) default NULL,
  `status` varchar(255) default NULL,
  PRIMARY KEY  (`imgid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `tblroadimg` */

insert  into `tblroadimg`(`imgid`,`imagepath`,`address`,`latitude`,`longitude`,`uname`,`prediction`,`status`) values (1,'static/uploaded_img/image_3.jpg','Airoli, Navi Mumbai, Thane, Maharashtra, 410701, India','19.0745','72.9978','y','Pothole detected',' Done'),(2,'static/uploaded_img/new_pothole.jpg','Airoli, Navi Mumbai, Thane, Maharashtra, 400708, India','19.160769444444444','72.996011111111116','y','Pothole detected',' Done'),(3,'static/uploaded_img/new_pothole.jpg','Airoli, Navi Mumbai, Thane, Maharashtra, 400708, India','19.160769444444444','72.996011111111116','y','Pothole detected',' Done'),(4,'static/uploaded_img/new_pothole.jpg','Airoli, Navi Mumbai, Thane, Maharashtra, 400708, India','19.160769444444444','72.996011111111116','Aakash','Pothole detected',' Done');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
