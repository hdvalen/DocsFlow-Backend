
USE EstructureDB;

-- --------------------
-- Tabla: companies
-- --------------------
CREATE TABLE companies (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,          
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME ON UPDATE CURRENT_TIMESTAMP
);

-- --------------------
-- Tabla: departments
-- --------------------
CREATE TABLE departments (
  id INT AUTO_INCREMENT PRIMARY KEY,
  company_id INT NOT NULL,             
  name VARCHAR(255) NOT NULL,          
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_departments_company FOREIGN KEY (company_id) REFERENCES companies(id)
);

-- --------------------
-- Tabla: document_types
-- --------------------
CREATE TABLE document_types (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(150) NOT NULL,           -- Tipo de documento (ej: factura, reporte)
  description TEXT,                     -- Detalles del tipo
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- --------------------
-- Tabla: users
-- --------------------
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  department_id INT,                    -- Pertenece a un departamento
  company_id INT,                       -- Pertenece a una empresa
  name VARCHAR(255) NOT NULL,           -- Nombre del usuario
  email VARCHAR(255) NOT NULL UNIQUE,   -- Correo único
  password_hash VARCHAR(255) NOT NULL,  -- Contraseña en hash
  is_active TINYINT(1) DEFAULT 1,       -- Activo o no
  failed_attempts INT DEFAULT 0,        -- Intentos fallidos de login
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_users_department FOREIGN KEY (department_id) REFERENCES departments(id),
  CONSTRAINT fk_users_company FOREIGN KEY (company_id) REFERENCES companies(id)
);

-- --------------------
-- Tabla: roles
-- --------------------
CREATE TABLE roles (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(50) NOT NULL,            -- admin / operator
  description VARCHAR(255)
);

-- --------------------
-- Tabla: user_roles
-- --------------------
CREATE TABLE user_roles (
  user_id INT NOT NULL,
  role_id INT NOT NULL,
  assigned_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (user_id, role_id),
  CONSTRAINT fk_user_roles_user FOREIGN KEY (user_id) REFERENCES users(id),
  CONSTRAINT fk_user_roles_role FOREIGN KEY (role_id) REFERENCES roles(id)
);

-- --------------------
-- Tabla: documents
-- --------------------
CREATE TABLE documents (
  id INT AUTO_INCREMENT PRIMARY KEY,
  department_id INT,                    -- Documento ligado a un depto
  uploaded_by INT NOT NULL,             -- Usuario que subió el archivo
  doc_type_id INT,                      -- Tipo de documento
  company_id INT,                       -- Empresa asociada
  title VARCHAR(500) NOT NULL,          -- Título interno
  original_filename VARCHAR(500) NOT NULL, -- Nombre original del archivo
  uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  processed TINYINT(1) DEFAULT 0,       -- Si fue procesado (tablas extraídas)
  CONSTRAINT fk_documents_department FOREIGN KEY (department_id) REFERENCES departments(id),
  CONSTRAINT fk_documents_user FOREIGN KEY (uploaded_by) REFERENCES users(id),
  CONSTRAINT fk_documents_type FOREIGN KEY (doc_type_id) REFERENCES document_types(id),
  CONSTRAINT fk_documents_company FOREIGN KEY (company_id) REFERENCES companies(id)
);

-- --------------------
-- Tabla: extracted_tables
-- --------------------
CREATE TABLE extracted_tables (
  id INT AUTO_INCREMENT PRIMARY KEY,
  document_id INT NOT NULL,             -- Documento al que pertenece
  table_index INT DEFAULT 0,            -- Posición de la tabla dentro del PDF
  caption VARCHAR(500),                 -- Título o descripción de la tabla
  json_data LONGTEXT NOT NULL,          -- Datos de la tabla en JSON
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_extracted_document FOREIGN KEY (document_id) REFERENCES documents(id)
);

-- --------------------
-- Tabla: password_reset_tokens
-- --------------------
CREATE TABLE password_reset_tokens (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  token VARCHAR(255) NOT NULL,          -- Token único de recuperación
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_prt_user FOREIGN KEY (user_id) REFERENCES users(id),
  CONSTRAINT uq_password_token_user UNIQUE (user_id)
);

-- --------------------
-- Tabla: active_sessions
-- --------------------
CREATE TABLE active_sessions (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  jti VARCHAR(255) NOT NULL,            -- Identificador único de sesión/JWT
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  last_activity DATETIME DEFAULT CURRENT_TIMESTAMP,
  expires_at DATETIME NOT NULL,         -- Expira a los 30min
  CONSTRAINT fk_active_session_user FOREIGN KEY (user_id) REFERENCES users(id)
);
