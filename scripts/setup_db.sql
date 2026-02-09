-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema default_schema
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema mcyfee
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mcyfee
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mcyfee` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci ;
USE `mcyfee` ;

-- -----------------------------------------------------
-- Table `mcyfee`.`selectors`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mcyfee`.`selectors` (
	  `id` INT NOT NULL AUTO_INCREMENT,
	  `name` VARCHAR(100) NOT NULL,
	  `css_selector` VARCHAR(500) NULL DEFAULT NULL,
	  `xpath` VARCHAR(500) NULL DEFAULT NULL,
	  `url_pattern` VARCHAR(200) NULL DEFAULT NULL,
	  `description` TEXT NULL DEFAULT NULL COMMENT '\n',
	  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	  PRIMARY KEY (`id`),
	  UNIQUE INDEX (`name` ASC) VISIBLE,
	  INDEX `idx_name` (`name` ASC) VISIBLE,
	  INDEX `idx_site_pattern` (`url_pattern` ASC) VISIBLE)
	ENGINE = InnoDB
	DEFAULT CHARACTER SET = utf8mb4
	COLLATE = utf8mb4_unicode_ci
	COMMENT = 'Reusable selectors for extracting data from websites';


	-- -----------------------------------------------------
	-- Table `mcyfee`.`notifications`
	-- -----------------------------------------------------
	CREATE TABLE IF NOT EXISTS `mcyfee`.`notifications` (
		  `id` INT NOT NULL AUTO_INCREMENT,
		  `type` ENUM('telegram', 'discord', 'email', 'webhook') NOT NULL COMMENT 'Type of notification channel',
		  `config` JSON NOT NULL COMMENT 'Channel-specific configuration, example: {\"token\": \"...\", \"chat_id\": \"...\"})',
		  `active` TINYINT NULL DEFAULT TRUE COMMENT 'Whether this notification channel is active',
		  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
		  PRIMARY KEY (`id`))
		ENGINE = InnoDB
		DEFAULT CHARACTER SET = utf8mb4
		COLLATE = utf8mb4_unicode_ci
		COMMENT = 'Notification channels for monitors';


		-- -----------------------------------------------------
		-- Table `mcyfee`.`monitors`
		-- -----------------------------------------------------
		CREATE TABLE IF NOT EXISTS `mcyfee`.`monitors` (
			  `id` INT NOT NULL AUTO_INCREMENT,
			  `name` VARCHAR(200) NOT NULL COMMENT 'Descriptive name (e.g., \"iPhone 15 Pro - Elgiganten\")',
			  `url` VARCHAR(1000) NOT NULL COMMENT 'URL to monitor',
			  `selector_id` INT NOT NULL COMMENT 'Reference to reusable selector',
			  `type` ENUM('price', 'text', 'image', 'element_count', 'attribute', 'category') NOT NULL COMMENT 'Type of data to extract',
			  `threshold_value` DECIMAL(10,2) NULL,
			  `check_interval` INT NOT NULL COMMENT 'Check interval for desired unit (example minutes, hours, days)',
			  `is_active` TINYINT NULL DEFAULT TRUE COMMENT 'Whether this monitor is currently active',
			  `last_check_at` TIMESTAMP NULL DEFAULT NULL COMMENT 'When this monitor was last checked',
			  `last_extracted_value` JSON NULL DEFAULT NULL COMMENT 'Most recent extracted value (current)',
			  `previous_extracted_value` JSON NULL DEFAULT NULL COMMENT 'Previous extracted value (for comparison)',
			  `last_changed_at` TIMESTAMP NULL DEFAULT NULL COMMENT 'When the value last changed',
			  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
			  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
			  `notification_id` INT NULL,
			  PRIMARY KEY (`id`),
			  INDEX `idx_active` (`is_active` ASC) VISIBLE,
			  INDEX `idx_last_check` (`last_check_at` ASC) VISIBLE,
			  INDEX `idx_url` (`url`(255) ASC) VISIBLE,
			  INDEX `idx_selector` (`selector_id` ASC) VISIBLE,
			  INDEX `idx_monitors_url_active` (`is_active` ASC, `url`(100) ASC) VISIBLE,
			  INDEX `fk_monitors_selectors` (`selector_id` ASC) VISIBLE,
			  INDEX `fk_monitors_notifications_idx` (`notification_id` ASC) VISIBLE,
			  CONSTRAINT `fk_monitors_selectors`
			    FOREIGN KEY (`selector_id`)
			    REFERENCES `mcyfee`.`selectors` (`id`)
			    ON DELETE RESTRICT
			    ON UPDATE CASCADE,
			  CONSTRAINT `fk_monitors_notifications`
			    FOREIGN KEY (`notification_id`)
			    REFERENCES `mcyfee`.`notifications` (`id`)
			    ON DELETE NO ACTION
			    ON UPDATE NO ACTION)
			ENGINE = InnoDB
			DEFAULT CHARACTER SET = utf8mb4
			COLLATE = utf8mb4_unicode_ci
			COMMENT = 'Monitor configurations - what to watch and when to alert';


			-- -----------------------------------------------------
			-- Table `mcyfee`.`snapshots`
			-- -----------------------------------------------------
			CREATE TABLE IF NOT EXISTS `mcyfee`.`snapshots` (
				  `id` INT NOT NULL AUTO_INCREMENT,
				  `monitor_id` INT NOT NULL COMMENT 'Which monitor this snapshot belongs to',
				  `extracted_value` JSON NOT NULL COMMENT 'The extracted value at this point in time',
				  `was_triggered` TINYINT NULL DEFAULT FALSE COMMENT 'Whether this snapshot triggered a notification',
				  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'When this value was extracted',
				  PRIMARY KEY (`id`),
				  INDEX `idx_monitor` (`monitor_id` ASC) VISIBLE,
				  INDEX `idx_created` (`created_at` ASC) VISIBLE,
				  INDEX `idx_triggered` (`was_triggered` ASC) VISIBLE,
				  INDEX `idx_snapshots_monitor_time` (`monitor_id` ASC, `created_at` DESC) VISIBLE,
				  INDEX (`monitor_id` ASC) VISIBLE,
				  CONSTRAINT ``
				    FOREIGN KEY (`monitor_id`)
				    REFERENCES `mcyfee`.`monitors` (`id`)
				    ON DELETE CASCADE
				    ON UPDATE CASCADE)
				ENGINE = InnoDB
				DEFAULT CHARACTER SET = utf8mb4
				COLLATE = utf8mb4_unicode_ci
				COMMENT = 'Historical snapshots of extracted values (optional feature)';


				-- -----------------------------------------------------
				-- Table `mcyfee`.`performance`
				-- -----------------------------------------------------
				CREATE TABLE IF NOT EXISTS `mcyfee`.`performance` (
					  `id` INT NOT NULL AUTO_INCREMENT,
					  `operation` VARCHAR(1000) NULL,
					  `start_time` DATETIME(2) NULL,
					  `end_time` DATETIME(2) NULL,
					  PRIMARY KEY (`id`))
					ENGINE = InnoDB;


					SET SQL_MODE=@OLD_SQL_MODE;
					SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
					SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
					-- MySQL Workbench Forward Engineering

					SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
					SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
					SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

					-- -----------------------------------------------------
					-- Schema default_schema
					-- -----------------------------------------------------
					-- -----------------------------------------------------
					-- Schema mcyfee
					-- -----------------------------------------------------

					-- -----------------------------------------------------
					-- Schema mcyfee
					-- -----------------------------------------------------
					CREATE SCHEMA IF NOT EXISTS `mcyfee` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci ;
					USE `mcyfee` ;

					-- -----------------------------------------------------
					-- Table `mcyfee`.`selectors`
					-- -----------------------------------------------------
					CREATE TABLE IF NOT EXISTS `mcyfee`.`selectors` (
						  `id` INT NOT NULL AUTO_INCREMENT,
						  `name` VARCHAR(100) NOT NULL,
						  `css_selector` VARCHAR(500) NULL DEFAULT NULL,
						  `xpath` VARCHAR(500) NULL DEFAULT NULL,
						  `url_pattern` VARCHAR(200) NULL DEFAULT NULL,
						  `description` TEXT NULL DEFAULT NULL COMMENT '\n',
						  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
						  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
						  PRIMARY KEY (`id`),
						  UNIQUE INDEX (`name` ASC) VISIBLE,
						  INDEX `idx_name` (`name` ASC) VISIBLE,
						  INDEX `idx_site_pattern` (`url_pattern` ASC) VISIBLE)
						ENGINE = InnoDB
						DEFAULT CHARACTER SET = utf8mb4
						COLLATE = utf8mb4_unicode_ci
						COMMENT = 'Reusable selectors for extracting data from websites';


						-- -----------------------------------------------------
						-- Table `mcyfee`.`notifications`
						-- -----------------------------------------------------
						CREATE TABLE IF NOT EXISTS `mcyfee`.`notifications` (
							  `id` INT NOT NULL AUTO_INCREMENT,
							  `type` ENUM('telegram', 'discord', 'email', 'webhook') NOT NULL COMMENT 'Type of notification channel',
							  `config` JSON NOT NULL COMMENT 'Channel-specific configuration (e.g., {\"token\": \"...\", \"chat_id\": \"...\"})',
							  `active` TINYINT NULL DEFAULT TRUE COMMENT 'Whether this notification channel is active',
							  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
							  PRIMARY KEY (`id`))
							ENGINE = InnoDB
							DEFAULT CHARACTER SET = utf8mb4
							COLLATE = utf8mb4_unicode_ci
							COMMENT = 'Notification channels for monitors';


							-- -----------------------------------------------------
							-- Table `mcyfee`.`monitors`
							-- -----------------------------------------------------
							CREATE TABLE IF NOT EXISTS `mcyfee`.`monitors` (
								  `id` INT NOT NULL AUTO_INCREMENT,
								  `name` VARCHAR(200) NOT NULL COMMENT 'Descriptive name (e.g., \"iPhone 15 Pro - Elgiganten\")',
								  `url` VARCHAR(1000) NOT NULL COMMENT 'URL to monitor',
								  `selector_id` INT NOT NULL COMMENT 'Reference to reusable selector',
								  `type` ENUM('price', 'text', 'image', 'element_count', 'attribute', 'category') NOT NULL COMMENT 'Type of data to extract',
								  `threshold_value` DECIMAL(10,2) NULL,
								  `check_interval` INT NOT NULL COMMENT 'Check interval for desired unit (example minutes, hours, days)',
								  `is_active` TINYINT NULL DEFAULT TRUE COMMENT 'Whether this monitor is currently active',
								  `last_check_at` TIMESTAMP NULL DEFAULT NULL COMMENT 'When this monitor was last checked',
								  `last_extracted_value` JSON NULL DEFAULT NULL COMMENT 'Most recent extracted value (current)',
								  `previous_extracted_value` JSON NULL DEFAULT NULL COMMENT 'Previous extracted value (for comparison)',
								  `last_changed_at` TIMESTAMP NULL DEFAULT NULL COMMENT 'When the value last changed',
								  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
								  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
								  `notification_id` INT NULL,
								  PRIMARY KEY (`id`),
								  INDEX `idx_active` (`is_active` ASC) VISIBLE,
								  INDEX `idx_last_check` (`last_check_at` ASC) VISIBLE,
								  INDEX `idx_url` (`url`(255) ASC) VISIBLE,
								  INDEX `idx_selector` (`selector_id` ASC) VISIBLE,
								  INDEX `idx_monitors_url_active` (`is_active` ASC, `url`(100) ASC) VISIBLE,
								  INDEX `fk_monitors_selectors` (`selector_id` ASC) VISIBLE,
								  INDEX `fk_monitors_notifications_idx` (`notification_id` ASC) VISIBLE,
								  CONSTRAINT `fk_monitors_selectors`
								    FOREIGN KEY (`selector_id`)
								    REFERENCES `mcyfee`.`selectors` (`id`)
								    ON DELETE RESTRICT
								    ON UPDATE CASCADE,
								  CONSTRAINT `fk_monitors_notifications`
								    FOREIGN KEY (`notification_id`)
								    REFERENCES `mcyfee`.`notifications` (`id`)
								    ON DELETE NO ACTION
								    ON UPDATE NO ACTION)
								ENGINE = InnoDB
								DEFAULT CHARACTER SET = utf8mb4
								COLLATE = utf8mb4_unicode_ci
								COMMENT = 'Monitor configurations - what to watch and when to alert';


								-- -----------------------------------------------------
								-- Table `mcyfee`.`snapshots`
								-- -----------------------------------------------------
								CREATE TABLE IF NOT EXISTS `mcyfee`.`snapshots` (
									  `id` INT NOT NULL AUTO_INCREMENT,
									  `monitor_id` INT NOT NULL COMMENT 'Which monitor this snapshot belongs to',
									  `extracted_value` JSON NOT NULL COMMENT 'The extracted value at this point in time',
									  `was_triggered` TINYINT NULL DEFAULT FALSE COMMENT 'Whether this snapshot triggered a notification',
									  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'When this value was extracted',
									  PRIMARY KEY (`id`),
									  INDEX `idx_monitor` (`monitor_id` ASC) VISIBLE,
									  INDEX `idx_created` (`created_at` ASC) VISIBLE,
									  INDEX `idx_triggered` (`was_triggered` ASC) VISIBLE,
									  INDEX `idx_snapshots_monitor_time` (`monitor_id` ASC, `created_at` DESC) VISIBLE,
									  INDEX (`monitor_id` ASC) VISIBLE,
									  CONSTRAINT ``
									    FOREIGN KEY (`monitor_id`)
									    REFERENCES `mcyfee`.`monitors` (`id`)
									    ON DELETE CASCADE
									    ON UPDATE CASCADE)
									ENGINE = InnoDB
									DEFAULT CHARACTER SET = utf8mb4
									COLLATE = utf8mb4_unicode_ci
									COMMENT = 'Historical snapshots of extracted values (optional feature)';


									-- -----------------------------------------------------
									-- Table `mcyfee`.`performance`
									-- -----------------------------------------------------
									CREATE TABLE IF NOT EXISTS `mcyfee`.`performance` (
										  `id` INT NOT NULL AUTO_INCREMENT,
										  `operation` VARCHAR(1000) NULL,
										  `start_time` DATETIME(2) NULL,
										  `end_time` DATETIME(2) NULL,
										  PRIMARY KEY (`id`))
										ENGINE = InnoDB;


										SET SQL_MODE=@OLD_SQL_MODE;
										SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
										SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

