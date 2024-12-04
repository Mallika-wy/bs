use bs;

CREATE TABLE `user` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(20) NOT NULL,
    `password` VARCHAR(20) NOT NULL,
    `email` VARCHAR(30) NOT NULL UNIQUE,
    `sex` INT NOT NULL DEFAULT 1,
    `address` VARCHAR(50) DEFAULT NULL,
    `phone` VARCHAR(20) DEFAULT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建 account 表
CREATE TABLE `account` (
    `user_id` INT NOT NULL,
    `tb_has_login` TINYINT(1) NOT NULL DEFAULT FALSE,
    `jd_has_login` TINYINT(1) NOT NULL DEFAULT FALSE,
    PRIMARY KEY (`user_id`),
    FOREIGN KEY (`user_id`) REFERENCES `user`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建 cookie 表
CREATE TABLE `cookie` (
    `cookie_id` INT NOT NULL AUTO_INCREMENT,
    `user_id` INT DEFAULT NULL,
    `type` INT NOT NULL,
    `cookie` VARCHAR(1000) NOT NULL,
    PRIMARY KEY (`cookie_id`),
    FOREIGN KEY (`user_id`) REFERENCES `user`(`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建 item 表
CREATE TABLE `item` (
    `item_id` INT NOT NULL AUTO_INCREMENT,
    `real_id` BIGINT NOT NULL,
    `title` VARCHAR(300) NOT NULL,
    `type` INT NOT NULL,
    `price` FLOAT NOT NULL,
    `nick` VARCHAR(100) NOT NULL,
    `item_url` VARCHAR(200) NOT NULL,
    `img_url` VARCHAR(200) NOT NULL,
    `procity` VARCHAR(30) NOT NULL,
    `specification` VARCHAR(200) NOT NULL,
    PRIMARY KEY (`item_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建 search 表
CREATE TABLE `search` (
    `search_id` INT NOT NULL AUTO_INCREMENT,
    `user_id` INT DEFAULT NULL,
    `search_text` VARCHAR(50) NOT NULL,
    PRIMARY KEY (`search_id`),
    FOREIGN KEY (`user_id`) REFERENCES `user`(`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建 item_search 表
CREATE TABLE `item_search` (
    `item_id` INT NOT NULL,
    `search_id` INT NOT NULL,
    PRIMARY KEY (`item_id`, `search_id`),
    FOREIGN KEY (`item_id`) REFERENCES `item`(`item_id`) ON DELETE CASCADE,
    FOREIGN KEY (`search_id`) REFERENCES `search`(`search_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建 subscribe 表
CREATE TABLE `subscribe` (
    `subscribe_id` INT NOT NULL AUTO_INCREMENT,
    `user_id` INT DEFAULT NULL,
    `item_id` INT DEFAULT NULL,
    PRIMARY KEY (`subscribe_id`),
    FOREIGN KEY (`user_id`) REFERENCES `user`(`id`) ON DELETE SET NULL,
    FOREIGN KEY (`item_id`) REFERENCES `item`(`item_id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;