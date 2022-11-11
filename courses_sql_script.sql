drop database if exists courses;
create database courses;

use courses;

drop table if exists section;
drop table if exists enrollment;
drop table if exists period;
drop table if exists project;
drop table if exists section_type;

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
    primary key (`call_no`),
    foreign key (`period_id`)
		references period(`id`)
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
	foreign key(`project_id`)
		references project(`id`),
	primary key(`call_no`, `uni`)
);

insert into section_type(`description`)
values("in_person");
insert into section_type(`description`)
values("CVN");