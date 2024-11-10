SET @@global.sql_mode = 'STRICT_ALL_TABLES';
SET @@session.sql_mode = 'STRICT_ALL_TABLES';

START TRANSACTION;

INSERT INTO `admins` (`name`, `username`, `password`) VALUES ('test', 'test', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3');

COMMIT;