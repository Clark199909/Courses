drop database if exists courses;
create database courses;

use courses;


drop table if exists section;
drop table if exists enrollment;
drop table if exists period;
drop table if exists project;
drop table if exists section_type;
drop table if exists email;
drop table if exists address;
drop table if exists phone;
drop table if exists address_type;
drop table if exists phone_type;
drop table if exists email_type;
drop table if exists student;

create table student
(
    `uni`            varchar(10) not null,
    `first_name`     varchar(32) not null,
    `last_name`      varchar(32) not null,
    `nationality`    varchar(64) not null,
    `ethnicity`      varchar(32) null,
    `gender`         varchar(32) null,
    `admission_date` varchar(64) not null,
    primary key (`uni`)
);

create table email_type(
	`id` int auto_increment,
    `description` varchar(50) not null,
    primary key (`id`)
);

create table address_type(
	`id` int auto_increment,
    `description` varchar(50) not null,
    primary key (`id`)
);

create table phone_type(
	`id` int auto_increment,
    `description` varchar(50) not null,
    primary key (`id`)
);

create table period(
	`id` int auto_increment,
    `year` int not null,
    `semester` varchar(10) not null,
    `day` varchar(10) not null,
    `start_hr` int not null,
    `start_min` int not null,
    `end_hr` int not null,
    `end_min` int not null,
    primary key (`id`)
);

create table section_type(
	`id` int auto_increment,
    `description` varchar(10) not null,
    primary key(`id`)
);


create table section(
	`call_no` int auto_increment,
    `professor` varchar(255) not null,
    `period_id` int not null,
    `classroom` varchar(20) not null,
    `section_type_id` int not null,
    primary key (`call_no`),
    foreign key (`period_id`)
		references period(`id`),
	foreign key (`section_type_id`)
		references section_type(`id`)
);


create table project(
	`id` int auto_increment,
    `call_no` int not null,
    `project_name` varchar(255) not null,
    `team_name` varchar(255) not null,
    primary key(`id`),
    foreign key (`call_no`)
		references section(`call_no`)
);


create table enrollment(
	`call_no` int not null,
    `uni` varchar(10) not null,
    `project_id` int not null,
    foreign key(`call_no`)
		references section(`call_no`),
	foreign key(`uni`)
		references student(`uni`),
	foreign key(`project_id`)
		references project(`id`),
	primary key(`call_no`, `uni`)
);

create table email(
	`id` int auto_increment,
    `type_id` int not null,
    `uni` varchar(10) not null,
    `address` varchar(50) not null,
    primary key(`id`),
    foreign key(`type_id`)
		references email_type(`id`),
	foreign key(`uni`)
		references student(`uni`)
);

create table address(
	`id` int auto_increment,
    `type_id` int not null,
    `uni` varchar(10) not null,
    `country` varchar(50) not null,
    `state` varchar(50) not null,
    `city` varchar(50) not null,
    `zip_code` varchar(10) not null,
    `street` varchar(100) not null,
    primary key(`id`),
    foreign key(`type_id`)
		references address_type(`id`),
	foreign key(`uni`)
		references student(`uni`)
);

create table phone(
	`id` int auto_increment,
    `type_id` int not null,
    `uni` varchar(10) not null,
    `country_code` varchar(10) not null,
    `phone_no` varchar(20) not null,
    primary key(`id`),
    foreign key(`type_id`)
		references phone_type(`id`),
	foreign key(`uni`)
		references student(`uni`)
);

insert into email_type (`description`)
values ("personal");
insert into email_type (`description`)
values ("work");
insert into email_type (`description`)
values ("education");

insert into address_type (`description`)
values ("home");
insert into address_type (`description`)
values ("work");
insert into address_type (`description`)
values ("campus");

insert into phone_type (`description`)
values ("home");
insert into phone_type (`description`)
values ("mobile");
insert into phone_type (`description`)
values ("work");

insert into section_type(`description`)
values("in_person");
insert into section_type(`description`)
values("CVN");