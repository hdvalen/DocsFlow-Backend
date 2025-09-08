CREATE DATABASE DocsFlow;
USE EstructureDB;
-- ======================

-- Datos iniciales
-- ======================

-- Empresas
INSERT INTO companies (name) VALUES
('TechCorp'),
('HealthSolutions'),
('EduGlobal');

-- Departamentos
INSERT INTO departments (company_id, name) VALUES
(1, 'Recursos Humanos'),
(1, 'TI'),
(2, 'Finanzas'),
(2, 'Operaciones'),
(3, 'Investigación'),
(3, 'Marketing');

-- Tipos de documento
INSERT INTO document_types (name, description) VALUES
('Factura', 'Documento de facturación'),
('Reporte', 'Informe mensual o anual'),
('Contrato', 'Acuerdo legal entre partes'),
('Recibo', 'Comprobante de pago');

-- Roles
INSERT INTO roles (name, description) VALUES
('admin', 'Acceso total al sistema'),
('operator', 'Carga y consulta de documentos'),
('analyst', 'Analiza documentos y tablas extraídas');

-- Usuarios
INSERT INTO users (department_id, company_id, name, email, password_hash) VALUES
(1, 1, 'Carlos Ramírez', 'carlos@techcorp.com', 'hash123'),
(2, 1, 'María López', 'maria@techcorp.com', 'hash456'),
(3, 2, 'Ana Torres', 'ana@healthsolutions.com', 'hash789'),
(4, 2, 'Pedro Gómez', 'pedro@healthsolutions.com', 'hash321'),
(5, 3, 'Laura Fernández', 'laura@eduglobal.com', 'hash654'),
(6, 3, 'Javier Castillo', 'javier@eduglobal.com', 'hash987');

-- Roles asignados
INSERT INTO user_roles (user_id, role_id) VALUES
(1, 1), -- Carlos → admin
(2, 2), -- María → operator
(3, 2), -- Ana → operator
(4, 3), -- Pedro → analyst
(5, 2), -- Laura → operator
(6, 1); -- Javier → admin

-- Documentos
INSERT INTO documents (department_id, uploaded_by, doc_type_id, company_id, title, original_filename, processed) VALUES
(2, 2, 1, 1, 'Factura Servidores Julio', 'factura_julio.pdf', 1),
(3, 3, 2, 2, 'Reporte Trimestral Finanzas', 'reporte_finanzas_q1.pdf', 0),
(4, 4, 3, 2, 'Contrato Proveedores', 'contrato_proveedores.pdf', 1),
(5, 5, 2, 3, 'Reporte Investigación 2023', 'investigacion2023.pdf', 0),
(6, 6, 4, 3, 'Recibo Publicidad', 'recibo_publi.pdf', 1);

-- Tablas extraídas (ejemplo en JSON)
INSERT INTO extracted_tables (document_id, table_index, caption, json_data) VALUES
(1, 0, 'Detalle de factura', '[{"item":"Servidor Dedicado","costo":1200},{"item":"Licencia","costo":300}]'),
(3, 0, 'Listado de proveedores', '[{"proveedor":"Proveedor A","monto":5000},{"proveedor":"Proveedor B","monto":3200}]');

-- Tokens de recuperación de contraseña
INSERT INTO password_reset_tokens (user_id, token) VALUES
(2, 'token123456'),
(3, 'tokenabcdef');

-- Sesiones activas
INSERT INTO active_sessions (user_id, jti, expires_at) VALUES
(1, 'jti-12345', DATE_ADD(NOW(), INTERVAL 30 MINUTE)),
(2, 'jti-67890', DATE_ADD(NOW(), INTERVAL 30 MINUTE));

SELECT * from users; 
