public: schema
    --  standard public schema
    + sequences
        address_id_seq: sequence: 1 data type: integer
            . properties
                start_value = 1
        phone_id_seq: sequence: 1 data type: integer
            . properties
                start_value = 1
        questionnaire_id_seq: sequence: 1 data type: integer
            . properties
                start_value = 1
        secrets_id_seq: sequence: 1 data type: integer
            . properties
                start_value = 1
        sex_offender_id_seq: sequence: 1 data type: integer
            . properties
                start_value = 1
        user_id_seq: sequence: 1 data type: integer
            . properties
                start_value = 1
    + tables
        address: table
            + columns
                id: integer NN default nextval('address_id_seq'::regclass)
                    . references
                        sequence = address_id_seq
                address_line_1: varchar(255) NN
                address_line_2: varchar(255)
                city: varchar(255) NN
                state: varchar(255) NN
                zip: varchar(10) NN
                country: varchar(255) NN
                country_code: char(2) NN
                created_at: timestamp with time zone default CURRENT_TIMESTAMP
                updated_at: timestamp with time zone default CURRENT_TIMESTAMP
            + indices
                #1: unique (id)
            + keys
                #1: PK (id) (underlying index #1)
        emergency_contact: table
            + columns
                user_id: integer NN
                contact_id: integer NN
                relationship: varchar(255) NN
                created_at: timestamp with time zone default CURRENT_TIMESTAMP
                updated_at: timestamp with time zone default CURRENT_TIMESTAMP
            + indices
                #1: unique (user_id, contact_id)
            + keys
                #1: PK (user_id, contact_id) (underlying index #1)
            + foreign-keys
                #1: foreign key (user_id) -> user (id) d:cascade
                #2: foreign key (contact_id) -> user (id) d:cascade
        phone: table
            + columns
                id: integer NN default nextval('phone_id_seq'::regclass)
                    . references
                        sequence = phone_id_seq
                phone_number: varchar(20) NN
                type: varchar(20)
                created_at: timestamp with time zone default CURRENT_TIMESTAMP
                updated_at: timestamp with time zone default CURRENT_TIMESTAMP
            + indices
                #1: unique (id)
            + keys
                #1: PK (id) (underlying index #1)
            + checks
                phone_type_check: check ((type)::text = ANY ((ARRAY['home'::character varying, 'work'::character varying, 'mobile'::character varying, 'fax'::character varying, 'other'::character varying])::text[])) cols = [type]
        questionnaire: table
            + columns
                id: integer NN default nextval('questionnaire_id_seq'::regclass)
                    . references
                        sequence = questionnaire_id_seq
                user_id: integer NN
                county_of_conviction: varchar(255)
                probation_officer_id: integer
                hours_to_complete: integer
                hours_due_date: date
                alt_info: text
                registered_sex_offender_id: integer
                created_at: timestamp with time zone default CURRENT_TIMESTAMP
                updated_at: timestamp with time zone default CURRENT_TIMESTAMP
            + indices
                #1: unique (id, user_id)
                #2: unique (user_id)
            + keys
                #1: PK (id, user_id) (underlying index #1)
                #2: AK (user_id) (underlying index #2)
            + foreign-keys
                #1: foreign key (user_id) -> user (id) d:cascade
                #2: foreign key (probation_officer_id) -> user (id)
                #3: foreign key (registered_sex_offender_id) -> sex_offender (id)
        role: table
            + columns
                name: varchar(255) NN
                description: text
                created_at: timestamp with time zone default CURRENT_TIMESTAMP
                updated_at: timestamp with time zone default CURRENT_TIMESTAMP
            + indices
                #1: unique (name)
            + keys
                #1: PK (name) (underlying index #1)
        secrets: table
            + columns
                id: integer NN default nextval('secrets_id_seq'::regclass)
                    . references
                        sequence = secrets_id_seq
                user_id: integer NN
                secret: varchar(255) NN
                created_at: timestamp with time zone default CURRENT_TIMESTAMP
                updated_at: timestamp with time zone default CURRENT_TIMESTAMP
            + indices
                #1: unique (id, user_id)
                #2: unique (user_id)
            + keys
                #1: PK (id, user_id) (underlying index #1)
                #2: AK (user_id) (underlying index #2)
            + foreign-keys
                #1: foreign key (user_id) -> user (id) d:cascade
        sex_offender: table
            + columns
                id: integer NN default nextval('sex_offender_id_seq'::regclass)
                    . references
                        sequence = sex_offender_id_seq
                user_id: integer
                details: text
            + indices
                #1: unique (id)
                #2: unique (user_id)
            + keys
                #1: PK (id) (underlying index #1)
                #2: AK (user_id) (underlying index #2)
            + foreign-keys
                #1: foreign key (user_id) -> user (id) d:cascade
        user: table
            + columns
                id: integer NN default nextval('user_id_seq'::regclass)
                    . references
                        sequence = user_id_seq
                firstname: varchar(255) NN
                lastname: varchar(255) NN
                email: varchar(255) NN
                dob: date default '1900-01-01'::date
                created_at: timestamp with time zone default CURRENT_TIMESTAMP
                updated_at: timestamp with time zone default CURRENT_TIMESTAMP
            + indices
                #1: unique (id)
                #2: unique (email)
            + keys
                #1: PK (id) (underlying index #1)
                #2: AK (email) (underlying index #2)
        user_addresses: table
            + columns
                user_id: integer NN
                address_id: integer NN
            + indices
                #1: unique (user_id, address_id)
            + keys
                #1: PK (user_id, address_id) (underlying index #1)
            + foreign-keys
                #1: foreign key (user_id) -> user (id) d:cascade
                #2: foreign key (address_id) -> address (id) d:cascade
        user_phones: table
            + columns
                user_id: integer NN
                phone_id: integer NN
            + indices
                #1: unique (user_id, phone_id)
            + keys
                #1: PK (user_id, phone_id) (underlying index #1)
            + foreign-keys
                #1: foreign key (user_id) -> user (id) d:cascade
                #2: foreign key (phone_id) -> phone (id) d:cascade
        user_roles: table
            + columns
                user_id: integer NN
                role_name: varchar(255) NN
            + indices
                #1: unique (user_id, role_name)
            + keys
                #1: PK (user_id, role_name) (underlying index #1)
            + foreign-keys
                #1: foreign key (user_id) -> user (id) d:cascade
                #2: foreign key (role_name) -> role (name) d:cascade
