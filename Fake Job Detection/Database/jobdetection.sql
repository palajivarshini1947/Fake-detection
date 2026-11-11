/*
SQLyog Community v13.2.0 (64 bit)
MySQL - 8.4.0 : Database - appatizer
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`appatizer` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `appatizer`;

/*Table structure for table `admin` */

DROP TABLE IF EXISTS `admin`;

CREATE TABLE `admin` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `email` varchar(254) NOT NULL,
  `password` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `admin` */

insert  into `admin`(`id`,`email`,`password`) values 
(1,'bckr2003@gmail.com','b');

/*Table structure for table `auth_group` */

DROP TABLE IF EXISTS `auth_group`;

CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `auth_group` */

/*Table structure for table `auth_group_permissions` */

DROP TABLE IF EXISTS `auth_group_permissions`;

CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `auth_group_permissions` */

/*Table structure for table `auth_permission` */

DROP TABLE IF EXISTS `auth_permission`;

CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `auth_permission` */

insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values 
(1,'Can add log entry',1,'add_logentry'),
(2,'Can change log entry',1,'change_logentry'),
(3,'Can delete log entry',1,'delete_logentry'),
(4,'Can view log entry',1,'view_logentry'),
(5,'Can add permission',2,'add_permission'),
(6,'Can change permission',2,'change_permission'),
(7,'Can delete permission',2,'delete_permission'),
(8,'Can view permission',2,'view_permission'),
(9,'Can add group',3,'add_group'),
(10,'Can change group',3,'change_group'),
(11,'Can delete group',3,'delete_group'),
(12,'Can view group',3,'view_group'),
(13,'Can add user',4,'add_user'),
(14,'Can change user',4,'change_user'),
(15,'Can delete user',4,'delete_user'),
(16,'Can view user',4,'view_user'),
(17,'Can add content type',5,'add_contenttype'),
(18,'Can change content type',5,'change_contenttype'),
(19,'Can delete content type',5,'delete_contenttype'),
(20,'Can view content type',5,'view_contenttype'),
(21,'Can add session',6,'add_session'),
(22,'Can change session',6,'change_session'),
(23,'Can delete session',6,'delete_session'),
(24,'Can view session',6,'view_session'),
(25,'Can add contact',7,'add_contact'),
(26,'Can change contact',7,'change_contact'),
(27,'Can delete contact',7,'delete_contact'),
(28,'Can view contact',7,'view_contact'),
(29,'Can add admin',8,'add_admin'),
(30,'Can change admin',8,'change_admin'),
(31,'Can delete admin',8,'delete_admin'),
(32,'Can view admin',8,'view_admin'),
(33,'Can add notification',9,'add_notification'),
(34,'Can change notification',9,'change_notification'),
(35,'Can delete notification',9,'delete_notification'),
(36,'Can view notification',9,'view_notification'),
(37,'Can add customer regi',10,'add_customerregi'),
(38,'Can change customer regi',10,'change_customerregi'),
(39,'Can delete customer regi',10,'delete_customerregi'),
(40,'Can view customer regi',10,'view_customerregi'),
(41,'Can add job provider',11,'add_jobprovider'),
(42,'Can change job provider',11,'change_jobprovider'),
(43,'Can delete job provider',11,'delete_jobprovider'),
(44,'Can view job provider',11,'view_jobprovider'),
(45,'Can add job posting',12,'add_jobposting'),
(46,'Can change job posting',12,'change_jobposting'),
(47,'Can delete job posting',12,'delete_jobposting'),
(48,'Can view job posting',12,'view_jobposting'),
(49,'Can add job application',13,'add_jobapplication'),
(50,'Can change job application',13,'change_jobapplication'),
(51,'Can delete job application',13,'delete_jobapplication'),
(52,'Can view job application',13,'view_jobapplication');

/*Table structure for table `auth_user` */

DROP TABLE IF EXISTS `auth_user`;

CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `auth_user` */

/*Table structure for table `auth_user_groups` */

DROP TABLE IF EXISTS `auth_user_groups`;

CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `auth_user_groups` */

/*Table structure for table `auth_user_user_permissions` */

DROP TABLE IF EXISTS `auth_user_user_permissions`;

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `auth_user_user_permissions` */

/*Table structure for table `contact` */

DROP TABLE IF EXISTS `contact`;

CREATE TABLE `contact` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(254) NOT NULL,
  `subject` varchar(100) NOT NULL,
  `message` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `contact` */

insert  into `contact`(`id`,`name`,`email`,`subject`,`message`) values 
(1,'chenna','bckr2003@gmail.com','food','fff'),
(2,'chenna','bckr2003@gmail.com','food','hot');

/*Table structure for table `customer_regi` */

DROP TABLE IF EXISTS `customer_regi`;

CREATE TABLE `customer_regi` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `email` varchar(254) NOT NULL,
  `password` varchar(100) NOT NULL,
  `name` longtext NOT NULL,
  `mobile` bigint NOT NULL,
  `address` longtext NOT NULL,
  `pincode` bigint NOT NULL,
  `status` varchar(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `customer_regi` */

insert  into `customer_regi`(`id`,`email`,`password`,`name`,`mobile`,`address`,`pincode`,`status`) values 
(5,'bckr2003@gmail.com','pbkdf2_sha256$1000000$96ngUVI52pzDbpNsSflMaU$g33xuDOgofkGTL/ct0ZQH1KoPDUvbdi+Z956po/4CVE=','B Chennakesava Reddy',9666039039,'KPHB Colony',5000520,'Accepted'),
(6,'battulachennakesavareddy2003@gmail.com','pbkdf2_sha256$1000000$e6Msr5SkLbJBIHmU4sr1x8$1cd33YBtLXQ0tIdqXuO3l8fjaYFgyaiyH9QiO8Wkcys=','B Chennakesava Reddy',9666039030,'KPHB Colony',500056,'Accepted');

/*Table structure for table `django_admin_log` */

DROP TABLE IF EXISTS `django_admin_log`;

CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `django_admin_log` */

/*Table structure for table `django_content_type` */

DROP TABLE IF EXISTS `django_content_type`;

CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `django_content_type` */

insert  into `django_content_type`(`id`,`app_label`,`model`) values 
(1,'admin','logentry'),
(8,'appatizerapp','admin'),
(7,'appatizerapp','contact'),
(10,'appatizerapp','customerregi'),
(13,'appatizerapp','jobapplication'),
(12,'appatizerapp','jobposting'),
(11,'appatizerapp','jobprovider'),
(9,'appatizerapp','notification'),
(3,'auth','group'),
(2,'auth','permission'),
(4,'auth','user'),
(5,'contenttypes','contenttype'),
(6,'sessions','session');

/*Table structure for table `django_migrations` */

DROP TABLE IF EXISTS `django_migrations`;

CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `django_migrations` */

insert  into `django_migrations`(`id`,`app`,`name`,`applied`) values 
(1,'contenttypes','0001_initial','2026-04-01 12:04:13.138703'),
(2,'auth','0001_initial','2026-04-01 12:04:13.994610'),
(3,'admin','0001_initial','2026-04-01 12:04:14.185832'),
(4,'admin','0002_logentry_remove_auto_add','2026-04-01 12:04:14.201614'),
(5,'admin','0003_logentry_add_action_flag_choices','2026-04-01 12:04:14.201614'),
(6,'appatizerapp','0001_initial','2026-04-01 12:04:14.233518'),
(7,'contenttypes','0002_remove_content_type_name','2026-04-01 12:04:14.328251'),
(8,'auth','0002_alter_permission_name_max_length','2026-04-01 12:04:14.407807'),
(9,'auth','0003_alter_user_email_max_length','2026-04-01 12:04:14.439648'),
(10,'auth','0004_alter_user_username_opts','2026-04-01 12:04:14.439648'),
(11,'auth','0005_alter_user_last_login_null','2026-04-01 12:04:14.518833'),
(12,'auth','0006_require_contenttypes_0002','2026-04-01 12:04:14.518833'),
(13,'auth','0007_alter_validators_add_error_messages','2026-04-01 12:04:14.534749'),
(14,'auth','0008_alter_user_username_max_length','2026-04-01 12:04:14.630080'),
(15,'auth','0009_alter_user_last_name_max_length','2026-04-01 12:04:14.709254'),
(16,'auth','0010_alter_group_name_max_length','2026-04-01 12:04:14.741094'),
(17,'auth','0011_update_proxy_permissions','2026-04-01 12:04:14.744081'),
(18,'auth','0012_alter_user_first_name_max_length','2026-04-01 12:04:14.866584'),
(19,'sessions','0001_initial','2026-04-01 12:04:14.902527'),
(20,'appatizerapp','0002_admin','2026-04-03 11:10:44.158722'),
(21,'appatizerapp','0003_notification','2026-04-04 07:31:27.326641'),
(22,'appatizerapp','0004_customerregi','2026-04-06 04:55:40.232684'),
(23,'appatizerapp','0005_notification_created_at','2026-04-06 09:29:54.585304'),
(24,'appatizerapp','0006_customerregi_status','2026-04-08 07:55:46.927123'),
(25,'appatizerapp','0007_alter_customerregi_status','2026-04-09 04:29:19.523801'),
(26,'appatizerapp','0008_jobprovider','2026-04-22 05:11:37.972691'),
(27,'appatizerapp','0009_jobposting','2026-04-23 06:56:48.835970'),
(28,'appatizerapp','0010_jobapplication','2026-04-26 02:01:51.310819');

/*Table structure for table `django_session` */

DROP TABLE IF EXISTS `django_session`;

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `django_session` */

insert  into `django_session`(`session_key`,`session_data`,`expire_date`) values 
('lqe3cj11v25srutq08hbhhvzna7y3amy','.eJyrVkrNTczMUbJSSkrOLjIyMDB2SAcJ6CXn5yrpKGUVxOOVT8svSs8vic8vKQCqMDc1NzA0AYoWpRanluDTWAsA8ZYmLQ:1wN70m:TTYhpCw-LkClchrbgwqzotryszkzbyGagF2Wzx6YQg8','2026-05-27 10:40:20.473307');

/*Table structure for table `jobapplication` */

DROP TABLE IF EXISTS `jobapplication`;

CREATE TABLE `jobapplication` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `resume` varchar(100) NOT NULL,
  `cover_letter` longtext,
  `status` varchar(20) NOT NULL,
  `applied_at` datetime(6) NOT NULL,
  `applicant_id` bigint NOT NULL,
  `job_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `JobApplication_applicant_id_5a2bb152_fk_customer_regi_id` (`applicant_id`),
  KEY `JobApplication_job_id_b8ff858d_fk_JobPosting_id` (`job_id`),
  CONSTRAINT `JobApplication_applicant_id_5a2bb152_fk_customer_regi_id` FOREIGN KEY (`applicant_id`) REFERENCES `customer_regi` (`id`),
  CONSTRAINT `JobApplication_job_id_b8ff858d_fk_JobPosting_id` FOREIGN KEY (`job_id`) REFERENCES `jobposting` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `jobapplication` */

insert  into `jobapplication`(`id`,`resume`,`cover_letter`,`status`,`applied_at`,`applicant_id`,`job_id`) values 
(1,'resumes/Battula_Chennakesava_Reddy_ATS_Backend_Resume.docx','','Rejected','2026-04-26 02:09:00.292975',5,2);

/*Table structure for table `jobposting` */

DROP TABLE IF EXISTS `jobposting`;

CREATE TABLE `jobposting` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `company_name` varchar(255) NOT NULL,
  `location` varchar(255) NOT NULL,
  `salary_range` varchar(100) DEFAULT NULL,
  `description` longtext NOT NULL,
  `requirements` longtext,
  `benefits` longtext,
  `created_at` datetime(6) NOT NULL,
  `provider_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `JobPosting_provider_id_a8962c27_fk_JobProvider_id` (`provider_id`),
  CONSTRAINT `JobPosting_provider_id_a8962c27_fk_JobProvider_id` FOREIGN KEY (`provider_id`) REFERENCES `jobprovider` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `jobposting` */

insert  into `jobposting`(`id`,`title`,`company_name`,`location`,`salary_range`,`description`,`requirements`,`benefits`,`created_at`,`provider_id`) values 
(2,'Data Analyst','Swiggy','Bangalore, Karnataka, India','8,00,000 - 13,00,000 LPA','Swiggy\'s Growth Analytics team is looking for a Data Analyst to help drive data-informed decisions across our restaurant and logistics verticals. You will build dashboards, run A/B test analyses, write complex SQL queries, and present insights to senior stakeholders on a weekly basis.','2+ years of experience in a data or analytics role. Advanced SQL skills mandatory. Experience with Python (Pandas, NumPy) and BI tools such as Tableau or Looker. Exposure to A/B testing frameworks. Strong written and verbal communication skills.','ESOPs, health and accident insurance, free Swiggy credits monthly, hybrid work model, maternity and paternity leave, annual wellness allowance.','2026-04-25 01:37:22.404163',1);

/*Table structure for table `jobprovider` */

DROP TABLE IF EXISTS `jobprovider`;

CREATE TABLE `jobprovider` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(254) NOT NULL,
  `password` varchar(100) NOT NULL,
  `phone` bigint NOT NULL,
  `status` varchar(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `jobprovider` */

insert  into `jobprovider`(`id`,`name`,`email`,`password`,`phone`,`status`) values 
(1,'BCK Solutions','bckr2003@gmail.com','pbkdf2_sha256$1000000$pU7tVdOuYG3YuPXKMeS6xm$kucOiDMN1HgxGyLwyM+iL95USsTBLKDTOMj+YSuSWew=',9666039039,'Accepted');

/*Table structure for table `notification` */

DROP TABLE IF EXISTS `notification`;

CREATE TABLE `notification` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `message` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `notification` */

insert  into `notification`(`id`,`title`,`message`,`created_at`) values 
(3,'fesfe','fesefew','2026-04-06 09:30:48.472836'),
(4,'njsoew','jkgftyjfbnij','2026-04-25 01:20:38.858947'),
(5,'New Job Added','In Fratello Innotech','2026-05-12 05:55:21.984897');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
