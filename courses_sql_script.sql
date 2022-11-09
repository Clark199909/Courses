drop database if exists courses;
create database courses;

use courses;

drop table if exists sections;
drop table if exists enrollments;
drop table if exists periods;
drop table if exists projects;

create table periods(
	`id` int auto_increment,
    `year` int not null,
    `semester` int not null,
    `day` varchar(10) not null,
    `start_hr` int not null,
    `start_min` int not null,
    `end_hr` int not null,
    `end_min` int not null,
    primary key (`id`)
);


create table sections(
	`call_no` int auto_increment,
    `professor` varchar(255) not null,
    `period_id` int not null,
    `classroom` varchar(20) not null,
    primary key (`call_no`),
    foreign key (`period_id`)
		references periods(`id`)
);


create table projects(
	`id` int auto_increment,
    `project_name` varchar(255) not null,
    `team_name` varchar(255) not null,
    primary key(`id`)
);


create table enrollments(
	`call_no` int not null,
    `uni` int not null,
    `project_id` int not null,
    foreign key(`call_no`)
		references sections(`call_no`),
	foreign key(`project_id`)
		references projects(`id`),
	primary key(`call_no`, `uni`)
);