```markdown
# Database Setup Instructions

## MySQL Database Setup
 First Install XAMPP
   - Create a new database `scaletech`.
   - create a tables user and roles:
   ```sql
   CREATE TABLE roles (
       id INT AUTO_INCREMENT PRIMARY KEY,
       role_name VARCHAR(50) NOT NULL,
       access_modules JSON,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       active BOOLEAN DEFAULT TRUE
   );

   CREATE TABLE users (
       id INT AUTO_INCREMENT PRIMARY KEY,
       first_name VARCHAR(50) NOT NULL,
       last_name VARCHAR(50) NOT NULL,
       email VARCHAR(100) UNIQUE NOT NULL,
       password VARCHAR(128) NOT NULL,
       role_id INT,
       FOREIGN KEY (role_id) REFERENCES roles(id)
   );
