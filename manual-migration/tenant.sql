SET TIME ZONE 'Asia/Singapore';
INSERT INTO "tenants"
(id, created_at, updated_at, name, main_contact_name, main_contact_mobile, main_contact_email, main_contact_address, is_deleted, created_by, updated_by)
VALUES
(1, NOW(), NOW(), 'shakesalad', 'reca seng', '+6587654321', 'reca@shakesalad.com', 'Singapore', False, 0, 0)
ON CONFLICT DO NOTHING;

SET TIME ZONE 'Asia/Singapore';
INSERT INTO "tenants"
(id, created_at, updated_at, name, main_contact_name, main_contact_mobile, main_contact_email, main_contact_address, is_deleted, created_by, updated_by)
VALUES
(2, NOW(), NOW(), 'samsung', 'samsung admin', '+6512345678', 'admin@samsung.com', 'Singapore', False, 0, 0)
ON CONFLICT DO NOTHING;