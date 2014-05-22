

DELIMITER $$

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



DROP TABLE IF EXISTS `category`;
CREATE TABLE IF NOT EXISTS `category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=10 ;



DROP TABLE IF EXISTS `category_producs`;
CREATE TABLE IF NOT EXISTS `category_producs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `product_id` int(11) NOT NULL,
  `category_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=16 ;



DROP TABLE IF EXISTS `product`;
CREATE TABLE IF NOT EXISTS `product` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `price` float NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=44 ;
