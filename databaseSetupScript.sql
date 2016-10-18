CREATE TABLE Users (
	id integer PRIMARY KEY,
	name text varchar(80),
	email text varchar(255),
	profilePicURL text
);
CREATE TABLE Items (
	id integer PRIMARY KEY,
	FOREIGN KEY(sellerID) REFERENCES Users(id),
	name text varchar(80),
	description text varchar(255),
	price integer,
	onSale text DEFAULT 'False',
	onClearance text DEFAULT 'False',
	imageURL text,
	qty integer DEFAULT 0
);