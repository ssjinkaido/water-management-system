CREATE TABLE "adminlogin" (
	username	varchar(10) NOT NULL,
	password	varchar(10) NOT NULL
)
CREATE TABLE "employee" (
	"employee_id"	varchar(10) NOT NULL,
	"name"	varchar(30) NOT NULL,
	"phone"	varchar(10) NOT NULL,
	"sex"	varchar(1) NOT NULL,
	"designation"	varchar(20) NOT NULL,
	"salary"	number(10) NOT NULL,
	"area_id" INTEGER ,
	FOREIGN KEY("area_id") REFERENCES "area"("area_id") ON DELETE SET NULL,
	PRIMARY KEY("employee_id")
)

CREATE TABLE "supplier" (
	"supplier_id"	INTEGER NOT NULL,
	"supplier_name"	varchar(30),
	"phone"	varchar(10),
	PRIMARY KEY("supplier_id" AUTOINCREMENT)
)

CREATE TABLE "area" (
	"area_id"	INTEGER NOT NULL,
	"areaname"	varchar(30),
	"supplier_id"	INTEGER,
	PRIMARY KEY("area_id" AUTOINCREMENT),
	FOREIGN KEY("supplier_id") REFERENCES "supplier"("supplier_id") ON DELETE SET NULL
)

CREATE TABLE "servicetype" (
	"service_type_id"	INTEGER NOT NULL,
	"service_type_name"	varchar(50),
	PRIMARY KEY("service_type_id" AUTOINCREMENT)
)

CREATE TABLE "service" (
	"service_id"	INTEGER NOT NULL,
	"household_id"	INTEGER,
	"service_type_id"	INTEGER,
	"service_request"	varchar(1000),
	"service_status"	varchar(10),
	"date"	date,
	PRIMARY KEY("service_id" AUTOINCREMENT),
	FOREIGN KEY("household_id") REFERENCES "household"("household_id") ON DELETE SET NULL,
	FOREIGN KEY("service_type_id") REFERENCES "servicetype"("service_type_id") ON DELETE SET NULL
)

CREATE TABLE "household" (
	"household_id"	INTEGER NOT NULL,
	"household_owner"	varchar(30),
	"address_id"	INTEGER,
	"phone"	varchar(10),
	FOREIGN KEY("address_id") REFERENCES "address"("address_id") ON DELETE SET NULL,
	PRIMARY KEY("household_id" AUTOINCREMENT)
)

CREATE TABLE "billing" (
	"billing_id"	INTEGER NOT NULL,
	"household_id"	INTEGER,
	"water_consumption"	number(10),
	"from_date"	date,
	"to_date"	date,
	"total_money"	number(12),
	"is_paid"	number(1),
	FOREIGN KEY("household_id") REFERENCES "household"("household_id") ON DELETE SET NULL,
	PRIMARY KEY("billing_id" AUTOINCREMENT)
)
CREATE TABLE "address" (
	"address_id"	INTEGER NOT NULL,
	"area_id" INTEGER,
	"address_name"	varchar(30),
	FOREIGN KEY("area_id") REFERENCES "area"("area_id") ON DELETE SET NULL,
	PRIMARY KEY("address_id" AUTOINCREMENT)
)




household-areaid delete set null
service-householdid delete set null