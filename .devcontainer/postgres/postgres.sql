SELECT
    u.id, u.firstname, u.lastname, u.email, u.dob,
    r.role_name AS role,
    q.county_of_conviction, q.hours_to_complete, q.hours_due_date,
    po.firstname AS po_firstname, po.lastname AS po_lastname, po.email AS po_email,
    p.phone_number, a.address_line_1, a.city, a.state, a.zip
FROM "user" u
JOIN user_roles r ON u.id = r.user_id
LEFT JOIN questionnaire q ON u.id = q.user_id
LEFT JOIN "user" po ON q.probation_officer_id = po.id
LEFT JOIN user_phones up ON po.id = up.user_id
LEFT JOIN phone p ON up.phone_id = p.id
LEFT JOIN user_addresses ua ON po.id = ua.user_id
LEFT JOIN address a ON ua.address_id = a.id
WHERE r.role_name = 'volunteer';

SELECT
    u.id, u.firstname, u.lastname, u.email, u.dob,
    r.role_name AS role,
    p.phone_number, a.address_line_1, a.city, a.state, a.zip
FROM "user" u
JOIN user_roles r ON u.id = r.user_id
JOIN user_phones up ON u.id = up.user_id
JOIN phone p ON up.phone_id = p.id
JOIN user_addresses ua ON u.id = ua.user_id
JOIN address a ON ua.address_id = a.id
WHERE r.role_name IN ('agent', 'supervisor', 'director'); -- Employee roles


SELECT
    u.id, u.firstname, u.lastname, u.email, u.dob,
    r.role_name AS role,
    p.phone_number, a.address_line_1, a.city, a.state, a.zip
FROM "user" u
JOIN user_roles r ON u.id = r.user_id
JOIN user_phones up ON u.id = up.user_id
JOIN phone p ON up.phone_id = p.id
JOIN user_addresses ua ON u.id = ua.user_id
JOIN address a ON ua.address_id = a.id
WHERE r.role_name = 'probation officer';

-- --------------------------------------------------------
SELECT u.*, q.*, so.*, ec.*, p.*, a.*, r.role_name as role
FROM "user" u
         JOIN user_roles r on u.id = r.user_id
         LEFT JOIN questionnaire q ON u.id = q.user_id
         LEFT JOIN sex_offender so ON q.registered_sex_offender_id = so.id
         LEFT JOIN emergency_contact ec ON u.id = ec.user_id
         LEFT JOIN user_phones up on u.id = up.user_id
         LEFT JOIN phone p on up.phone_id = p.id
         LEFT JOIN user_addresses ua on u.id = ua.user_id
         LEFT JOIN address a on ua.address_id = a.id
WHERE r.role_name = 'volunteer';

SELECT u.*, p.*, a.*, r.role_name as role
FROM "user" u
JOIN user_roles r on u.id = r.user_id
LEFT JOIN user_phones up on u.id = up.user_id
LEFT JOIN phone p on up.phone_id = p.id
LEFT JOIN user_addresses ua on u.id = ua.user_id
LEFT JOIN address a on ua.address_id = a.id
WHERE r.role_name NOT IN ('volunteer', 'guest');

SELECT u.*, p.*, a.*
FROM "user" u
         JOIN user_roles ur ON u.id = ur.user_id
         LEFT JOIN user_phones up on u.id = up.user_id
         LEFT JOIN phone p on up.phone_id = p.id
         LEFT JOIN user_addresses ua on u.id = ua.user_id
         LEFT JOIN address a on ua.address_id = a.id
WHERE ur.role_name = 'probation officer';
