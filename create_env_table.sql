-- For MySQL

CREATE TABLE `env` (
	 `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	 `id` int(10) NOT NULL,
	 `temperatureC` float NOT NULL,
	 `humidity` float DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci

