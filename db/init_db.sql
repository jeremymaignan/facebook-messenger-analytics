CREATE TABLE IF NOT EXISTS `message`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sender` varchar(255) DEFAULT NULL,
  `sent_at` datetime DEFAULT NULL,
  `content` longtext,
  `gifs` longtext,
  `photos` longtext,
  `share` longtext,
  `sticker` longtext,
  `video` longtext,
  `audio` longtext,
  `type` longtext,
  `title` longtext,
  `conversation_id` varchar(255),
  `is_still_participant` boolean,
  `participants` longtext,
  `thread_type` longtext,
  PRIMARY KEY (`id`),
  KEY `conversation_id` (`conversation_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE utf8mb4_general_ci;

CREATE TABLE IF NOT EXISTS `call` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `caller` varchar(255) DEFAULT NULL,
  `started_at` datetime,
  `content` longtext,
  `conversation_id` varchar(255),
  `is_still_participant` boolean,
  `participants` longtext,
  `thread_type` longtext,
  `duration` int(11),
  `is_missed` boolean,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE utf8mb4_general_ci;
