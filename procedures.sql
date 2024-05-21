delimiter \\

CREATE PROCEDURE `add_user` (
	in username varchar(64),
    in password varchar(64)
)
BEGIN
	insert into users (username, password) values (username, password);
END \\

delimiter ;