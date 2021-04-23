DROP DATABASE IF EXISTS user;
CREATE DATABASE user;
USE user;
DROP TABLE IF EXISTS `profile`;
DROP TABLE IF EXISTS `credentials`;

CREATE TABLE profiles ( 
  user_id     INT UNSIGNED NOT NULL AUTO_INCREMENT, 
  fname         VARCHAR(40),
  lname         VARCHAR(40), 
  phone         VARCHAR(20),
  travel         VARCHAR(20), 
  street         VARCHAR(40),
  city         VARCHAR(20),
  states         VARCHAR(20),
  zipcode         VARCHAR(20),
  PRIMARY KEY (user_id) 
); 

CREATE TABLE credentials (
  cred_id INT UNSIGNED NOT NULL AUTO_INCREMENT, 
  user_id INT UNSIGNED NOT NULL,
  username VARCHAR(20) NOT NULL,
  pass VARCHAR(20) NOT NULL,
  PRIMARY KEY (cred_id), 
  FOREIGN KEY (user_id) REFERENCES profiles(user_id) ON DELETE CASCADE
);