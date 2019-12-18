import os
import sys

import psycopg2 as dbapi2

#url = "dbname='snlvpekr' user='snlvpekr' host='balarama.db.elephantsql.com' password='Yez7qmHLmlsFw3UM_4WENR3k6ktjTiEC'"
url = os.getenv("DB_URL")

INIT_STATEMENTS = [
    """CREATE TABLE IF NOT EXISTS Provider (
        ProviderID serial PRIMARY KEY,
        Company varchar(50) NOT NULL,
        Address text NOT NULL,
        Phone varchar(12) NOT NULL,
        TaxID varchar(10) NOT NULL,
        Authority text NOT NULL
        );""",
    """CREATE TABLE IF NOT EXISTS Employee(
        EmployeeID serial PRIMARY KEY,
        Name varchar(40) NOT NULL,
        Surname varchar(20) NOT NULL,
        Phonenumber varchar(12) NOT NULL,
        Email varchar(25) NOT NULL,
        WorkingHours integer[] NOT NULL,
        WorkingDays integer[] NOT NULL
    );""",
    """CREATE TABLE IF NOT EXISTS CargoCompany(
        CompanyID serial PRIMARY KEY,
        Name varchar(255) NOT NULL,
        Address varchar(255) NOT NULL,
        PricePerKilo integer NOT NULL,
        TaxID varchar(10) NOT NULL,
        Authority text NOT NULL
    );""",
    """CREATE TABLE IF NOT EXISTS Marketplace(
        MarketID serial PRIMARY KEY,
        Name varchar(255) NOT NULL,
        Address varchar(255) NOT NULL,
        Authority text NOT NULL,
        Phonenumber varchar(12) NOT NULL,
        TaxID varchar(10) NOT NULL,
        Commissionfee integer NOT NULL
    );""",
    """CREATE TABLE IF NOT EXISTS Products(
        ProductID serial PRIMARY KEY,
        Name varchar(255) NOT NULL,
        Brand varchar(255) NOT NULL,
        Sellprice integer NOT NULL,
        ProviderID integer REFERENCES provider(providerid),
        Weight integer NOT NULL
    );""",
    """CREATE TABLE IF NOT EXISTS Stock(
        ID serial PRIMARY KEY,
        Location_x integer,
        Location_y integer,
        Location_z integer,
        Productid integer REFERENCES products(productid),
        Quantity integer NOT NULL
    );""",
    """CREATE TABLE IF NOT EXISTS Temporary_order(
        OrderID serial PRIMARY KEY,
        Marketplaceid integer REFERENCES marketplace(marketid),
        Shipaddress varchar(255) NOT NULL,
        Order_date varchar(255) NOT NULL,
        Customer_name varchar(255) NOT NULL,
        companyid integer REFERENCES cargocompany(companyid),
        ProductID integer REFERENCES products(productid),
        Quantity integer NOT NULL,
        EmployeeID integer REFERENCES employee(employeeid),
        IsDispatched bool NOT NULL,
	order_time integer
    );""",
    """CREATE TABLE IF NOT EXISTS Orders(
        OrderID serial PRIMARY KEY,
        MarketplaceID integer REFERENCES marketplace(marketid),
        Shipaddress varchar(255) NOT NULL,
        Order_date varchar(255) NOT NULL,
        Customer_name varchar(255) NOT NULL,
        companyID integer REFERENCES cargocompany(companyid),
        ProductID integer REFERENCES products(productid),
        Quantity integer NOT NULL,
	Order_time integer
    );""",
    """CREATE TABLE IF NOT EXISTS Supply_order(
        OrderID serial PRIMARY KEY,
        ProviderID integer REFERENCES provider(ProviderID),
        Price integer NOT NULL,
        Quantity integer NOT NULL,
        Time varchar(255) NOT NULL,
        ProductID integer REFERENCES products(productid)
    );""", 
    """CREATE TABLE IF NOT EXISTS Financial(
        TransactionID serial PRIMARY KEY,
        OrderID integer REFERENCES orders(orderid),
        Supply_orderID integer REFERENCES supply_order(orderid),
        Transaction integer NOT NULL,
        Cargo_price integer NOT NULL,
        Total integer NOT NULL
    );""", 
    """CREATE TABLE IF NOT EXISTS users(
        username varchar(50) PRIMARY KEY, 
        password varchar(255) NOT NULL, 
        EmployeeID integer REFERENCES Employee(EmployeeId) NOT NULL
        ,usertype integer NOT NULL);
    """ 
]


def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        cursor.close()


if __name__ == "__main__":
    url = os.getenv("DB_URL")
    if url is None:
        print("Usage: DB_URL=url python dbinit.py", file=sys.stdout)
        sys.exit(1)
    initialize(url)
