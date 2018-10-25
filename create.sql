drop table if exists Item;
drop table if exists Bid;
drop table if exists Category;
drop table if exists Auctions;
drop table if exists ItemIs;
drop table if exists Users;

create table Item(
	itemid INTEGER PRIMARY KEY, 
	name CHAR(30)
);

create table Bids(
	time NUMERIC, 
	amount REAL, 
	userid CHAR(30), 
	itemid INTEGER,
	FOREIGN KEY (userid) REFERENCES Users(userid),
	FOREIGN KEY (itemid) REFERENCES Auctions(itemid),
	PRIMARY KEY (time, userid, itemid)
);

create table Auctions(
	itemid INTEGER PRIMARY KEY,
	sellerid CHAR(30),
	description CHAR(30),
	currently REAL,
	number_of_bids INTEGER,
	started NUMERIC,
	ends NUMERIC,
	FOREIGN KEY (itemid) REFERENCES Items(itemid),
	FOREIGN KEY (sellerid) REFERENCES Users(userid)
);

create table Users(
	userid CHAR(30) PRIMARY TEXT,
	rating INTEGER,
	location CHAR(30),
	country CHAR(30)
);

create table ItemIs(
	itemid INTEGER,
	category CHAR(30),
	FOREIGN KEY (itemid) REFERENCES Items(itemid),
	FOREIGN KEY (category) REFERENCES Categories(category)
	PRIMARY KEY (itemid,category)
);

create table Categories(
	category CHAR(30) PRIMARY KEY
);
