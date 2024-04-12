create table if not exists "user"
(
    id         serial
        constraint user_pkey
            primary key,
    firstname  varchar(255) not null,
    lastname   varchar(255) not null,
    email      varchar(255) not null
        constraint user_email_key
            unique,
    dob        date                     default '1900-01-01'::date,
    created_at timestamp with time zone default CURRENT_TIMESTAMP,
    updated_at timestamp with time zone default CURRENT_TIMESTAMP
);

create table if not exists secrets
(
    id         serial,
    user_id    integer      not null
        constraint secrets_user_id_key
            unique
        constraint secrets_user_id_fkey
            references "user"
            on delete cascade,
    secret     varchar(255) not null,
    created_at timestamp with time zone default CURRENT_TIMESTAMP,
    updated_at timestamp with time zone default CURRENT_TIMESTAMP,
    constraint secrets_pkey
        primary key (id, user_id)
);

create table if not exists emergency_contact
(
    user_id      integer      not null
        constraint emergency_contact_user_id_fkey
            references "user"
            on delete cascade,
    contact_id   integer      not null
        constraint emergency_contact_contact_id_fkey
            references "user"
            on delete cascade,
    relationship varchar(255) not null,
    created_at   timestamp with time zone default CURRENT_TIMESTAMP,
    updated_at   timestamp with time zone default CURRENT_TIMESTAMP,
    constraint emergency_contact_pkey
        primary key (user_id, contact_id)
);

create table if not exists sex_offender
(
    id      serial
        constraint sex_offender_pkey
            primary key,
    user_id integer
        constraint sex_offender_user_id_key
            unique
        constraint sex_offender_user_id_fkey
            references "user"
            on delete cascade,
    details text
);

create table if not exists questionnaire
(
    id                         serial,
    user_id                    integer not null
        constraint questionnaire_user_id_key
            unique
        constraint questionnaire_user_id_fkey
            references "user"
            on delete cascade,
    county_of_conviction       varchar(255),
    probation_officer_id       integer
        constraint questionnaire_probation_officer_id_fkey
            references "user",
    hours_to_complete          integer,
    hours_due_date             date,
    alt_info                   text,
    registered_sex_offender_id integer
        constraint questionnaire_registered_sex_offender_id_fkey
            references sex_offender,
    created_at                 timestamp with time zone default CURRENT_TIMESTAMP,
    updated_at                 timestamp with time zone default CURRENT_TIMESTAMP,
    constraint questionnaire_pkey
        primary key (id, user_id)
);

create table if not exists role
(
    name        varchar(255) not null
        constraint role_pkey
            primary key,
    description text,
    created_at  timestamp with time zone default CURRENT_TIMESTAMP,
    updated_at  timestamp with time zone default CURRENT_TIMESTAMP
);

create table if not exists address
(
    id             serial
        constraint address_pkey
            primary key,
    address_line_1 varchar(255) not null,
    address_line_2 varchar(255),
    city           varchar(255) not null,
    state          varchar(255) not null,
    zip            varchar(10)  not null,
    country        varchar(255) not null,
    country_code   char(2)      not null,
    created_at     timestamp with time zone default CURRENT_TIMESTAMP,
    updated_at     timestamp with time zone default CURRENT_TIMESTAMP
);

create table if not exists phone
(
    id           serial
        constraint phone_pkey
            primary key,
    phone_number varchar(20) not null,
    type         varchar(20)
        constraint phone_type_check
            check ((type)::text = ANY
                   ((ARRAY ['home'::character varying, 'work'::character varying, 'mobile'::character varying, 'fax'::character varying, 'other'::character varying])::text[])),
    created_at   timestamp with time zone default CURRENT_TIMESTAMP,
    updated_at   timestamp with time zone default CURRENT_TIMESTAMP
);

create table if not exists user_phones
(
    user_id  integer not null
        constraint user_phones_user_id_fkey
            references "user"
            on delete cascade,
    phone_id integer not null
        constraint user_phones_phone_id_fkey
            references phone
            on delete cascade,
    constraint user_phones_pkey
        primary key (user_id, phone_id)
);

create table if not exists user_roles
(
    user_id   integer      not null
        constraint user_roles_user_id_fkey
            references "user"
            on delete cascade,
    role_name varchar(255) not null
        constraint user_roles_role_name_fkey
            references role
            on delete cascade,
    constraint user_roles_pkey
        primary key (user_id, role_name)
);

create table if not exists user_addresses
(
    user_id    integer not null
        constraint user_addresses_user_id_fkey
            references "user"
            on delete cascade,
    address_id integer not null
        constraint user_addresses_address_id_fkey
            references address
            on delete cascade,
    constraint user_addresses_pkey
        primary key (user_id, address_id)
);

