drop table IF EXISTS Time;
CREATE TABLE Time(current_time datetime DEFAULT CURRENT_TIMESTAMP);
INSERT INTO Time DEFAULT VALUES;


drop table IF EXISTS Users;

CREATE TABLE Users(
	userId varchar(16) primary key 
);

INSERT INTO Users(userId) values
	('David Ciupei'),
	('Andrew Rosca'),
	('Ty Crabtree');

drop table IF EXISTS items;

CREATE TABLE items(
	id integer primary key autoincrement, 
	category char(50), 
	title char(50), 
	description char(255), 
	price float, 
	open boolean, 
	end_date datetime,
	winner varchar(50)
);

INSERT INTO items(category, title, description, price, open ,end_date, winner ) values
	('Electronics',
		'Mac Book Laptop', 
		'perfect condition,
		 15 inch screen, comes with extra accessories' , 
			500, 
			1,
			'2016-06-01 12:00:00',
			 NULL),

	('Automobile',
		'Toyota Supra', 
		'Very fast car and one of a kind. A ton of money
		 went into the car and trying to get my money back.' , 
		 50000,
		  1,
		  '2016-05-25 12:00:00',
			 NULL),

	('Fitness','Bench Press Machine', 
		'Trying to get buff? Then this is the machine for
		 you! Barely used and perfect for building muscle!' , 
		 100,
		  1,
		  '2016-05-31 12:00:00',
			 NULL),
	('Education',
		'Intro To Databases',
		'Perfect condition, hard cover, a few water spills.',
		50,
		1,
		'2016-05-30 12:00:00',
		NULL);

drop table IF EXISTS Bids;

CREATE TABLE bids(
	id int references items(id), 
	buyer char(50), 
	price float,
	bid_time datetime,
	bid_id integer primary key autoincrement
);

INSERT INTO bids(id, buyer, price, bid_time) values
	(1,'David Ciupei', 250, '2016-03-20 12:30:10'),
	(2,'Ty Crabtree', 20000, '2016-04-24 14:00:10'),
	(3,'Andrew Rosca', 25, '2016-02-28 16:06:24'),
	(4,'David Ciupei', 10, '2016-04-23 14:00:23');

DROP TRIGGER IF EXISTS TimeUpdateTrigger;
CREATE TRIGGER TimeUpdateTrigger
AFTER UPDATE OF current_time ON Time
	BEGIN
		UPDATE items SET open = 1 WHERE end_date > new.current_time;
		UPDATE items SET open = 0 WHERE end_date <= new.current_time;
		UPDATE items SET winner = (SELECT buyer from bids WHERE bids.id = items.id ORDER BY bids.price DESC LIMIT 1) WHERE open = 0 AND winner IS NULL;
	END;

DROP TRIGGER IF EXISTS BidUpdateTrigger;
CREATE TRIGGER BidUpdateTrigger
AFTER INSERT ON bids
    BEGIN
        UPDATE Items SET winner = (SELECT buyer from bids WHERE bids.id = items.id AND bids.price >= items.price LIMIT 1) WHERE open = 1;
    END;

DROP TRIGGER IF EXISTS ItemsUpdateTrigger;
CREATE TRIGGER ItemsUpdateTrigger
AFTER UPDATE OF winner ON items
    BEGIN
        UPDATE items SET open = 0 WHERE winner IS NOT NULL;
        SELECT * FROM items;
    END;

UPDATE Time SET current_time=CURRENT_TIMESTAMP;
