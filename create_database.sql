-- Create a Musql database for the user

CREATE DATABASE IF NOT EXISTS "FAVOURS_DB";
CREATE USER IF NOT EXISTS 'favour'@'localhost' IDENTIFIED BY "FAVOURS_PWD";
GRANT ALL PRIVILEGES ON `FAVOURS_DB`.* TO 'favour'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'favour'@'locakhost';
FLUSH PRIVILEGES;
