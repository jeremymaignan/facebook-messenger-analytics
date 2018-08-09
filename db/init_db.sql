CREATE TABLE `messages` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sender` varchar(255) DEFAULT NULL,
  `sent_at` datetime DEFAULT NULL,
  `content` longtext,
  `gifs` longtext,
  `photos` longtext,
  `share` longtext,
  `sticker` longtext,
  `video` longtext,
  `type` longtext,
  `title` longtext,
  `uuid` varchar(255),
  `is_still_participant` tinyint(1) DEFAULT NULL,
  `participants` longtext,
  `thread_type` longtext,
  `thread_path` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE utf8mb4_general_ci;

CREATE TABLE `conversations` (
 	`id` int(11) NOT NULL AUTO_INCREMENT,
	`title` longtext,
  `participants` longtext,
  `nb_messages` INTEGER,
	`created_at` datetime DEFAULT NULL,
  `last_message_sent_at` datetime DEFAULT NULL,
  `is_still_participant` tinyint(1) DEFAULT NULL,
  `uuid` varchar(255),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE utf8mb4_general_ci;

CREATE TABLE senders (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `username` varchar(255),
    `conversation_id` int,
    `first_message_sent_at` datetime DEFAULT NULL,
    `last_message_sent_at` datetime DEFAULT NULL,
    `nb_messages_sent` int,
    PRIMARY KEY (`id`),
    INDEX `conversation_index` (`conversation_id`),
    FOREIGN KEY (`conversation_id`)
        REFERENCES `conversations`(`id`)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE utf8mb4_general_ci;