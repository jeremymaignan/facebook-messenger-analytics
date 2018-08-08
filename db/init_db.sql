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
  `is_still_participant` tinyint(1) DEFAULT NULL,
  `participants` longtext,
  `thread_type` longtext,
  `thread_path` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE utf8mb4_general_ci;