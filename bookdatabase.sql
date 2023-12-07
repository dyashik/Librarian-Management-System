BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "author" (
	"id"	INTEGER NOT NULL,
	"name"	VARCHAR(80) NOT NULL,
	UNIQUE("name"),
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "book" (
	"id"	INTEGER NOT NULL,
	"title"	VARCHAR(80) NOT NULL,
	"genre"	VARCHAR(50),
	"publisher"	VARCHAR(50),
	"publication_year"	INTEGER,
	"copies_available"	INTEGER NOT NULL,
	"author_id"	INTEGER NOT NULL,
	FOREIGN KEY("author_id") REFERENCES "author"("id"),
	UNIQUE("title"),
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "loan" (
	"loan_id"	INTEGER NOT NULL,
	"user_email"	VARCHAR(120) NOT NULL,
	"book_title"	VARCHAR(80) NOT NULL,
	"checkout_date"	VARCHAR NOT NULL,
	"due_date"	VARCHAR NOT NULL,
	FOREIGN KEY("user_email") REFERENCES "user"("email"),
	FOREIGN KEY("book_title") REFERENCES "book"("title"),
	PRIMARY KEY("loan_id")
);
CREATE TABLE IF NOT EXISTS "address" (
	"id"	INTEGER NOT NULL,
	"address"	VARCHAR(100) NOT NULL,
	"zip_code"	INTEGER NOT NULL,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "user" (
	"id"	INTEGER NOT NULL,
	"name"	VARCHAR(80) NOT NULL,
	"email"	VARCHAR(120) NOT NULL,
	"phone"	VARCHAR(10),
	"address"	VARCHAR(200),
	"zip_code"	INTEGER NOT NULL,
	"status"	VARCHAR(20),
	PRIMARY KEY("id")
);
INSERT INTO "author" VALUES (1,'JK Rowling');
INSERT INTO "author" VALUES (2,'Ernest Cline');
INSERT INTO "author" VALUES (3,'Harper Lee');
INSERT INTO "author" VALUES (4,'F. Scott Fitzgerald');
INSERT INTO "author" VALUES (5,'George Orwell');
INSERT INTO "author" VALUES (6,'J.D. Salinger');
INSERT INTO "author" VALUES (7,'J.K. Rowling');
INSERT INTO "author" VALUES (8,'J.R.R. Tolkien');
INSERT INTO "author" VALUES (9,'Dan Brown');
INSERT INTO "author" VALUES (10,'Suzanne Collins');
INSERT INTO "author" VALUES (11,'Paulo Coelho');
INSERT INTO "author" VALUES (12,'Jane Austen');
INSERT INTO "author" VALUES (13,'God');
INSERT INTO "book" VALUES (1,'To Kill a Mockingbird','Fiction','Harper Collins',1960,27,3);
INSERT INTO "book" VALUES (2,'The Great Gatsby','Classic','Scribner',1925,24,4);
INSERT INTO "book" VALUES (3,'1984','Dystopian','Penguin Books',1949,19,5);
INSERT INTO "book" VALUES (4,'The Catcher in the Rye','Young Adult','Little, Brown and Company',1951,21,6);
INSERT INTO "book" VALUES (5,'Harry Potter and the Sorcerer''s Stone','Fantasy','Scholastic',1997,39,7);
INSERT INTO "book" VALUES (6,'The Hobbit','Fantasy','Houghton Mifflin',1937,17,8);
INSERT INTO "book" VALUES (7,'The Da Vinci Code','Mystery','Doubleday',2003,14,9);
INSERT INTO "book" VALUES (8,'The Hunger Games','Science Fiction','Scholastic',2008,0,10);
INSERT INTO "book" VALUES (9,'The Alchemist','Fiction','HarperCollins',1988,27,11);
INSERT INTO "book" VALUES (10,'Pride and Prejudice','Romance','Thomas Egerton',1813,9,12);
INSERT INTO "loan" VALUES (1,'yashik.dhanaraj@sjsu.edu','Ready Player One','11/27/2023','12/01/2023');
INSERT INTO "loan" VALUES (2,'su4876@pleasantonusd.net','To Kill a Mockingbird','10/15/2023','11/15/2023');
INSERT INTO "loan" VALUES (3,'aditiJoes@gmail.com','The Great Gatsby','10/18/2023','11/18/2023');
INSERT INTO "loan" VALUES (4,'yashdan@gmail.com','1984','10/20/2023','11/20/2023');
INSERT INTO "loan" VALUES (5,'johndoe@email.com','The Catcher in the Rye','10/22/2023','11/22/2023');
INSERT INTO "loan" VALUES (6,'janesmith@email.com','Harry Potter and the Sorcerer''s Stone','10/25/2023','11/25/2023');
INSERT INTO "loan" VALUES (7,'alexjohnson@email.com','The Hobbit','10/28/2023','11/28/2023');
INSERT INTO "loan" VALUES (8,'emilywilliams@email.com','The Da Vinci Code','11/01/2023','12/01/2023');
INSERT INTO "loan" VALUES (9,'mikebrown@email.com','The Hunger Games','11/03/2023','12/03/2023');
INSERT INTO "loan" VALUES (10,'sarahjohnson@email.com','The Alchemist','11/06/2023','12/06/2023');
INSERT INTO "loan" VALUES (11,'markwilson@email.com','Pride and Prejudice','11/09/2023','12/09/2023');
INSERT INTO "loan" VALUES (12,'random@gmail.com','To Kill a Mockingbird','12/04/2023','12/10/2023');
INSERT INTO "loan" VALUES (13,'yashikdhanaraj@gmail.com','To Kill a Mockingbird','12/04/2023','12/10/2023');
INSERT INTO "loan" VALUES (14,'random@gmail.com','The Bible','12/04/2023','12/10/2023');
INSERT INTO "address" VALUES (2,'4444 AnotherOne Dr','77777-5555');
INSERT INTO "address" VALUES (3,'0000 BigHouse Dr',99999);
INSERT INTO "address" VALUES (4,'123 Main St, Anytown',12345);
INSERT INTO "address" VALUES (5,'987-654-3210',54321);
INSERT INTO "address" VALUES (6,'789 Oak St, Anotherplace',67890);
INSERT INTO "address" VALUES (7,'101 Pine St, Somewhere',13579);
INSERT INTO "address" VALUES (8,'202 Maple St, Nowhere',24680);
INSERT INTO "address" VALUES (9,'222 Oak Lane, Anywhere',98765);
INSERT INTO "address" VALUES (10,'333 Pine St, Anotherplace',24681);
INSERT INTO "address" VALUES (11,'San Jose, CA, USA',12345);
INSERT INTO "address" VALUES (13,'7373 Fallen Leaf Lane',12345);
INSERT INTO "user" VALUES (2,'Aditi Jorapur','aditiJoes@gmail.com','9992223334','4444 AnotherOne Dr','77777-5555','Active');
INSERT INTO "user" VALUES (3,'Yashik Dhanaraj','yashdan@gmail.com','8885556667','0000 BigHouse Dr',99999,'Active');
INSERT INTO "user" VALUES (4,'John Doe','johndoe@email.com','123-456-7890','123 Main St, Anytown',12345,'Active');
INSERT INTO "user" VALUES (5,'Jane Smith','janesmith@email.com','987-654-3210','0000 BigHouse Dr',54321,'Inactive');
INSERT INTO "user" VALUES (6,'Alex Johnson','alexjohnson@email.com','555-123-4567','789 Oak St, Anotherplace',67890,'Active');
INSERT INTO "user" VALUES (7,'Emily Williams','emilywilliams@email.com','111-222-3333','101 Pine St, Somewhere',13579,'Inactive');
INSERT INTO "user" VALUES (8,'Mike Brown','mikebrown@email.com','777-888-9999','202 Maple St, Nowhere',24680,'Active');
INSERT INTO "user" VALUES (9,'Sarah Johnson','sarahjohnson@email.com','444-555-6666','202 Maple St, Nowhere',98765,'Active');
INSERT INTO "user" VALUES (10,'Mark Wilson','markwilson@email.com','777-999-1111','333 Pine St, Anotherplace',24681,'Inactive');
INSERT INTO "user" VALUES (11,'Nidhi Zare','random@gmail.com','1234567890','San Jose, CA, USA',12345,'Active');
INSERT INTO "user" VALUES (13,'Sharanya Udupa','urmomahoe@gmail.com','6666666666','7373 Fallen Leaf Lane',12345,'Active');
COMMIT;
