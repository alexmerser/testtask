-- phpMyAdmin SQL Dump
-- version 4.0.6deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: May 25, 2014 at 07:54 PM
-- Server version: 5.5.37-0ubuntu0.13.10.1
-- PHP Version: 5.5.3-1ubuntu2.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `onlinashop`
--

DELIMITER $$
--
-- Procedures
--
DROP PROCEDURE IF EXISTS `new_product_with_cat`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `new_product_with_cat`(
  prname CHAR(35), prprice CHAR(35), cat_name CHAR(255))
BEGIN
DECLARE cat int;
START TRANSACTION;
   INSERT INTO product (name, price) 
     VALUES(prname, prprice);
           
	SELECT id FROM category WHERE category.name=cat_name INTO cat;

   INSERT INTO category_producs (product_id, category_id) 
     VALUES(LAST_INSERT_ID(), cat);
COMMIT;
END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
CREATE TABLE IF NOT EXISTS `category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=10 ;

--
-- Dumping data for table `category`
--

INSERT INTO `category` (`id`, `name`) VALUES
(6, 'C#'),
(3, 'C++'),
(7, 'Haskell'),
(2, 'Java'),
(4, 'JavaScript'),
(8, 'Lisp'),
(9, 'Perl'),
(1, 'Python'),
(5, 'Ruby');

-- --------------------------------------------------------

--
-- Table structure for table `category_producs`
--

DROP TABLE IF EXISTS `category_producs`;
CREATE TABLE IF NOT EXISTS `category_producs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `product_id` int(11) NOT NULL,
  `category_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `prod_cat` (`product_id`,`category_id`),
  KEY `product_id` (`product_id`),
  KEY `category_id` (`category_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=374 ;

--
-- Dumping data for table `category_producs`
--

INSERT INTO `category_producs` (`id`, `product_id`, `category_id`) VALUES
(364, 1, 1),
(354, 1, 2),
(365, 2, 1),
(368, 3, 1),
(373, 3, 3),
(357, 3, 6),
(366, 4, 1),
(371, 4, 3),
(358, 4, 8),
(367, 5, 1),
(372, 5, 3),
(359, 5, 5);

-- --------------------------------------------------------

--
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
CREATE TABLE IF NOT EXISTS `product` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `price` float NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=6 ;

--
-- Dumping data for table `product`
--

INSERT INTO `product` (`id`, `name`, `price`) VALUES
(1, 'Django', 0),
(2, 'Flask', 1),
(3, 'Super', 12),
(4, 'Mega', 123234),
(5, 'Summoner', 222);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
