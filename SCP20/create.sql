-- Create the database
CREATE DATABASE game_website;

-- Use the database
USE game_website;

-- Create the user table
CREATE TABLE user (
  user_id INT AUTO_INCREMENT PRIMARY KEY,
  first_name VARCHAR(50) NOT NULL,
  last_name VARCHAR(50) NOT NULL,
  email VARCHAR(100) NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  password_salt VARCHAR(255) NOT NULL,
  registration_date DATETIME NOT NULL
);

-- Create the game table
CREATE TABLE game (
  game_id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(100) NOT NULL,
  description TEXT,
  creation_date DATETIME NOT NULL,
  next_session_date DATETIME,
  creator_id INT NOT NULL,
  FOREIGN KEY (creator_id) REFERENCES user(user_id)
);

-- Create the participant table for many-to-many relationship between game and user
CREATE TABLE participant (
  game_id INT NOT NULL,
  user_id INT NOT NULL,
  PRIMARY KEY (game_id, user_id),
  FOREIGN KEY (game_id) REFERENCES game(game_id),
  FOREIGN KEY (user_id) REFERENCES user(user_id)
);

-- Create the character table
CREATE TABLE character (
  character_id INT AUTO_INCREMENT PRIMARY KEY,
  creator_id INT NOT NULL,
  game_id INT NOT NULL,
  title VARCHAR(100) NOT NULL,
  content JSON,
  FOREIGN KEY (creator_id) REFERENCES user(user_id),
  FOREIGN KEY (game_id) REFERENCES game(game_id)
);

-- Create the audio table
CREATE TABLE audio (
  audio_id INT AUTO_INCREMENT PRIMARY KEY,
  uploader_id INT NOT NULL,
  upload_date DATETIME NOT NULL,
  name VARCHAR(100) NOT NULL,
  file_link VARCHAR(255) NOT NULL,
  FOREIGN KEY (uploader_id) REFERENCES user(user_id)
);

-- Create the image table
CREATE TABLE image (
  image_id INT AUTO_INCREMENT PRIMARY KEY,
  uploader_id INT NOT NULL,
  upload_date DATETIME NOT NULL,
  name VARCHAR(100) NOT NULL,
  file_link VARCHAR(255) NOT NULL,
  FOREIGN KEY (uploader_id) REFERENCES user(user_id)
);