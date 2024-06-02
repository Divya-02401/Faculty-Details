create table if not exists users(
    id int auto_increment primary key,
    username varchar(255) not null,
    email varchar(250) not null
);
insert INTO users
VALUES(2, 'sita', 'sita@gmail.com');
SELECT *
FROM users;