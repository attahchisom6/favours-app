-- Create a test database for FABOURS DB database

CREATE DATABASE IF NOT EXISTS FAVOURS_DB_TEST;
CREATE USER IF NOT EXISTS 'favours_test'@'localhost' IDENTIFIED BY 'FAVOURS_TEST_PWD';
GRANT ALL PRIVILEGES ON `FAVOURS_DB_TEST`.* TO 'favours_test'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'favours_test'@'localhost';
