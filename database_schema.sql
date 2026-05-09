-- ==========================================================
-- DIEMS EVENTS: DATABASE SCHEMA & ER DIAGRAM EXPLANATION
-- ==========================================================

/*
ER Diagram Explanation:
-----------------------
1. USER: The core entity representing Students, Organizers, and Admins.
   - Has many EVENTs (if role='organizer').
   - Has many REGISTRATIONs (if role='student').
   - Has many NOTIFICATIONs, FEEDBACKs, CERTIFICATEs, and CHAT_MESSAGEs.

2. EVENT: The core entity representing a college event/fest.
   - Belongs to a USER (organizer).
   - Has many REGISTRATIONs (attendees).
   - Has many ANNOUNCEMENTs, FEEDBACKs, CERTIFICATEs, and CHAT_MESSAGEs.

3. REGISTRATION: The junction table linking USER and EVENT.
   - Belongs to one USER and one EVENT.
   - Has one ATTENDANCE_LOG (optional, tracked by QR scan).

4. NOTIFICATION: Alerts for a specific USER.
5. ANNOUNCEMENT: Global messages for a specific EVENT.
6. FEEDBACK: Ratings and comments left by a USER for an EVENT.
7. CERTIFICATE: Digital credentials awarded to a USER for an EVENT.
8. CHAT_MESSAGE: Real-time discussion linked to an EVENT by a USER.
9. ATTENDANCE_LOG: Records when a registration QR code is scanned.

All relationships enforce referential integrity using FOREIGN KEYs.
*/

CREATE TABLE `user` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(100) NOT NULL,
  `email` VARCHAR(120) UNIQUE NOT NULL,
  `password_hash` VARCHAR(255) NOT NULL,
  `role` VARCHAR(20) DEFAULT 'student',
  `profile_picture` VARCHAR(255) DEFAULT NULL,
  `department` VARCHAR(100) DEFAULT NULL,
  `points` INT DEFAULT 0,
  `badges` JSON DEFAULT NULL,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE `event` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `title` VARCHAR(200) NOT NULL,
  `description` TEXT NOT NULL,
  `banner_image` VARCHAR(255) DEFAULT NULL,
  `venue` VARCHAR(200) NOT NULL,
  `date_time` DATETIME NOT NULL,
  `registration_limit` INT DEFAULT NULL,
  `category` VARCHAR(100) DEFAULT NULL,
  `status` VARCHAR(20) DEFAULT 'upcoming',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `organizer_id` INT NOT NULL,
  FOREIGN KEY (`organizer_id`) REFERENCES `user`(`id`) ON DELETE CASCADE
);

CREATE TABLE `registration` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `qr_code` VARCHAR(255) DEFAULT NULL,
  `status` VARCHAR(20) DEFAULT 'pending',
  `attendance_status` BOOLEAN DEFAULT FALSE,
  `registered_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `user_id` INT NOT NULL,
  `event_id` INT NOT NULL,
  FOREIGN KEY (`user_id`) REFERENCES `user`(`id`) ON DELETE CASCADE,
  FOREIGN KEY (`event_id`) REFERENCES `event`(`id`) ON DELETE CASCADE
);

CREATE TABLE `notification` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `message` TEXT NOT NULL,
  `type` VARCHAR(50) NOT NULL,
  `is_read` BOOLEAN DEFAULT FALSE,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `user_id` INT NOT NULL,
  FOREIGN KEY (`user_id`) REFERENCES `user`(`id`) ON DELETE CASCADE
);

CREATE TABLE `announcement` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `message` TEXT NOT NULL,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `event_id` INT NOT NULL,
  FOREIGN KEY (`event_id`) REFERENCES `event`(`id`) ON DELETE CASCADE
);

CREATE TABLE `feedback` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `rating` INT NOT NULL,
  `comment` TEXT DEFAULT NULL,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `user_id` INT NOT NULL,
  `event_id` INT NOT NULL,
  FOREIGN KEY (`user_id`) REFERENCES `user`(`id`) ON DELETE CASCADE,
  FOREIGN KEY (`event_id`) REFERENCES `event`(`id`) ON DELETE CASCADE
);

CREATE TABLE `certificate` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `certificate_url` VARCHAR(255) NOT NULL,
  `issued_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `user_id` INT NOT NULL,
  `event_id` INT NOT NULL,
  FOREIGN KEY (`user_id`) REFERENCES `user`(`id`) ON DELETE CASCADE,
  FOREIGN KEY (`event_id`) REFERENCES `event`(`id`) ON DELETE CASCADE
);

CREATE TABLE `chat_message` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `message` TEXT NOT NULL,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `event_id` INT NOT NULL,
  `sender_id` INT NOT NULL,
  FOREIGN KEY (`event_id`) REFERENCES `event`(`id`) ON DELETE CASCADE,
  FOREIGN KEY (`sender_id`) REFERENCES `user`(`id`) ON DELETE CASCADE
);

CREATE TABLE `attendance_log` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `scanned_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `registration_id` INT NOT NULL,
  FOREIGN KEY (`registration_id`) REFERENCES `registration`(`id`) ON DELETE CASCADE
);
