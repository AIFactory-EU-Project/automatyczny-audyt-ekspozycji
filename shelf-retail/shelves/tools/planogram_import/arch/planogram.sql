drop database if exists planogram_test;
drop user if exists planogram_test;
create user planogram_test password 'planogram_test';
create database planogram_test;
alter database planogram_test owner to planogram_test;
GRANT postgres TO planogram_test;
\c planogram_test

create user planogram_import password 'planogram_import';
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA planogram TO planogram_import;




create table shop
(
id integer not null
constraint shop_pkey
primary key,
name varchar(255) not null,
code varchar(255) not null
);

alter table shop owner to postgres;

create table import
(
id integer not null
constraint import_pkey
primary key,
date_time timestamp(0) default CURRENT_TIMESTAMP not null,
is_complete boolean default false not null
);

alter table import owner to postgres;


create table segment
(
id integer not null
constraint segment_pkey
primary key,
name varchar(255) not null
);

alter table segment owner to postgres;

create table camera
(
id integer not null
constraint camera_pkey
primary key,
segment_id integer
constraint fk_3b1cee05db296aad
references segment,
shop_id integer
constraint fk_3b1cee054d16c4dd
references shop,
type varchar(255) not null,
ip varchar(20) not null,
manipulation_settings text NOT NULL
);

alter table camera owner to postgres;

create index idx_3b1cee05db296aad
on camera (segment_id);

create index idx_3b1cee054d16c4dd
on camera (shop_id);

create table planogram
(
id serial not null
constraint planogram_pkey
primary key,
name varchar(255) not null,
version varchar(255) not null,
description varchar(255) not null,
neural_network_id integer not null
);

alter table planogram owner to postgres;

create table shop_planogram_assignment
(
id serial not null
constraint shop_planogram_assignment_pkey
primary key,
segment_id integer
constraint fk_aaf32b45db296aad
references segment,
shop_id integer
constraint fk_aaf32b454d16c4dd
references shop,
planogram_id integer
constraint fk_aaf32b455afb77ab
references planogram,
start_date_time timestamp(0) not null,
end_date_time timestamp(0) not null
);

alter table shop_planogram_assignment owner to postgres;

create index idx_aaf32b45db296aad
on shop_planogram_assignment (segment_id);

create index idx_aaf32b454d16c4dd
on shop_planogram_assignment (shop_id);

create index idx_aaf32b455afb77ab
on shop_planogram_assignment (planogram_id);

create table photo
(
id integer not null
constraint photo_pkey
primary key,
camera_id integer
constraint fk_14b78418b47685cd
references camera,
time timestamp(0) default CURRENT_TIMESTAMP not null,
storage_id varchar(255) not null,
storage_type varchar(255) not null
constraint photo_storage_type_check
check ((storage_type)::text = ANY ((ARRAY['LOCAL'::character varying, 'GOOGLE_CLOUD_STORAGE'::character varying])::text[]))
);

comment on column photo.storage_type is '(DC2Type:FileStorageType)';

alter table photo owner to postgres;

create table report_photo_analysis
(
id integer not null
constraint report_photo_analysis_pkey
primary key,
planogram_id integer
constraint fk_c38374c75afb77ab
references planogram,
photo_id integer
constraint fk_c38374c77e9e4c8c
references photo,
date_time timestamp(0) default CURRENT_TIMESTAMP not null
);

alter table report_photo_analysis owner to postgres;

create index idx_c38374c75afb77ab
on report_photo_analysis (planogram_id);

create index idx_c38374c77e9e4c8c
on report_photo_analysis (photo_id);

create table sku
(
id serial not null
constraint sku_pkey
primary key,
photo_id integer
constraint fk_f9038c47e9e4c8c
references photo,
name varchar(255) not null,
index varchar(255) not null
);

alter table sku owner to postgres;

create table planogram_element
(
id serial not null
constraint planogram_element_pkey
primary key,
planogram_id integer
constraint fk_9f9f2d6d5afb77ab
references planogram,
sku_id integer
constraint fk_9f9f2d6d1777d41c
references sku,
shelf integer not null,
position integer not null,
faces_count integer not null,
stack_count integer not null
);

alter table planogram_element owner to postgres;

create index idx_9f9f2d6d5afb77ab
on planogram_element (planogram_id);

create index idx_9f9f2d6d1777d41c
on planogram_element (sku_id);

create index idx_f9038c47e9e4c8c
on sku (photo_id);

create index idx_14b78418b47685cd
on photo (camera_id);
