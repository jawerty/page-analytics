CREATE DATABASE pageAnalytics
;

USE pageAnalytics
;

CREATE TABLE searchQuery (

    id INT NOT NULL AUTO_INCREMENT,
    query VARCHAR(400),
    experimentType VARCHAR(100),
    resultKeywords VARCHAR(500),
    timeAdded DATETIME default CURRENT_TIMESTAMP,
    PRIMARY KEY (id)

)
;

CREATE TABLE video (

    id INT NOT NULL AUTO_INCREMENT,
    videoURL VARCHAR(500),
    videoID VARCHAR(500),
    keywords VARCHAR(2000),
    experimentSource VARCHAR(100),
    recommendedVideo BIT, -- 0 for False / 1 for True
    parentRecommended INT, -- integer = video.id of parent vide CHEKC: if parent not present / ignore
    videoViews INT,
    timeAdded DATETIME default CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
    
)
;

CREATE TABLE keyword (

    id INT NOT NULL AUTO_INCREMENT,
    word VARCHAR(100),
    cnt int,
    pos VARCHAR(100),
    sentiment VARCHAR(200),
    timeAdded DATETIME default CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
)
;

CREATE TABLE experiment (

    id INT NOT NULL AUTO_INCREMENT,
    expName VARCHAR(50),
    details VARCHAR(2000),
    PRIMARY KEY (id)
)
;