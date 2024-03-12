CREATE DATABASE srs_data;

CREATE TABLE user_account (
accountID INT AUTO_INCREMENT PRIMARY KEY,
username VARCHAR(20) NOT NULL,
firstname VARCHAR(30) NOT NULL,
lastname VARCHAR(30) NOT NULL,
password CHAR(64) NOT NULL,
friendrequest ENUM('on', 'off') NOT NULL DEFAULT 'on',
markingrequest ENUM('on', 'off') NOT NULL DEFAULT 'on',
);

CREATE TABLE user_deck (
deckID INT AUTO_INCREMENT PRIMARY KEY,
accountID INT NOT NULL,
deckname VARCHAR(50) NOT NULL,
score FLOAT NOT NULL DEFAULT 0,
FOREIGN KEY (accountID) REFERENCES user_account(accountID)
);

CREATE TABLE user_flashcard (
flashcardID INT AUTO_INCREMENT PRIMARY KEY,
deckID INT NOT NULL,
question VARCHAR(200) NOT NULL,
answer VARCHAR(1000) NOT NULL,
priority INT NOT NULL DEFAULT -1,
FOREIGN KEY (deckID) REFERENCES user_deck(deckID)
);

CREATE TABLE user_friend (
accountID INT NOT NULL,
accountID2 INT NOT NULL,
PRIMARY KEY (accountID, accountID2),
FOREIGN KEY (accountID) REFERENCES user_account(accountID),
FOREIGN KEY (accountID2) REFERENCES user_account(accountID),
CHECK (accountID != accountID2)
);

CREATE TABLE user_friendrequest (
accountID INT NOT NULL,
accountID2 INT NOT NULL,
PRIMARY KEY (accountID, accountID2),
FOREIGN KEY (accountID) REFERENCES user_account(accountID),
FOREIGN KEY (accountID2) REFERENCES user_account(accountID),
CHECK (accountID != accountID2)
);

CREATE TABLE user_peermarking (
accountID INT NOT NULL,
flashcardID INT NOT NULL,
accountID2 INT NOT NULL,
useranswer VARCHAR(1000) NOT NULL,
PRIMARY KEY (accountID, flashcardID),
FOREIGN KEY (accountID) REFERENCES user_account(accountID),
FOREIGN KEY (flashcardID) REFERENCES user_flashcard(flashcardID),
FOREIGN KEY (accountID2) REFERENCES user_account(accountID),
CHECK (accountID != accountID2)
);

CREATE TABLE user_peermarked (
accountID INT NOT NULL,
flashcardID INT NOT NULL,
accountID2 INT NOT NULL,
useranswer VARCHAR(1000) NOT NULL,
rating ENUM('fail', 'hard', 'good', 'easy') NOT NULL,
feedback VARCHAR(500),
PRIMARY KEY (accountID, flashcardID),
FOREIGN KEY (accountID) REFERENCES user_account(accountID),
FOREIGN KEY (flashcardID) REFERENCES user_flashcard(flashcardID),
FOREIGN KEY (accountID2) REFERENCES user_account(accountID),
CHECK (accountID != accountID2)
);
