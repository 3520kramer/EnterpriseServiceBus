CREATE TABLE queue_log(  
    pk INT NOT NULL primary key AUTO_INCREMENT,
    uuid VARCHAR(36) UNIQUE,
    is_consumed TINYINT(1) NOT NULL,
    published_time DATETIME NOT NULL,
    consumed_time DATETIME,
    content_format VARCHAR(4) NOT NULL,
    content VARCHAR(1000) NOT NULL
) default charset utf8mb4;