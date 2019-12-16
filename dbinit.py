import os
import sys

import psycopg2 as dbapi2


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
        WorkingHours varchar(255) NOT NULL,
        WorkingDays varchar(255) NOT NULL
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
        Buyprice integer NOT NULL,
        Sellprice integer NOT NULL,
        ProviderID integer REFERENCES provider(providerid),
        Weight integer NOT NULL
    );""",
    """CREATE TABLE IF NOT EXISTS Stock(
        ID serial PRIMARY KEY,
        Location_x integer NOT NULL,
        Location_y integer NOT NULL,
        Location_z integer NOT NULL,
        Productid integer REFERENCES products(productid),
        Quantity integer NOT NULL
    );""",
    """CREATE TABLE IF NOT EXISTS Temporary_order(
        OrderID serial PRIMARY KEY,
        Marketplaceid integer REFERENCES marketplace(marketid),
        Shipaddress varchar(255) NOT NULL,
        Order_time varchar(255) NOT NULL,
        Customer_name varchar(255) NOT NULL,
        Cargo_company integer REFERENCES cargocompany(companyid),
        ProductID integer REFERENCES products(productid),
        Quantity integer NOT NULL,
        EmployeeID integer REFERENCES employee(employeeid),
        IsDispatched bool NOT NULL
    );""",
    """CREATE TABLE IF NOT EXISTS Orders(
        OrderID serial PRIMARY KEY,
        MarketplaceID integer REFERENCES marketplace(marketid),
        Shipaddress varchar(255) NOT NULL,
        Order_time varchar(255) NOT NULL,
        Customer_name varchar(255) NOT NULL,
        Cargo_companyID integer REFERENCES cargocompany(companyid),
        ProductID integer REFERENCES products(productid),
        Quantity integer NOT NULL
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
    """create table users(username varchar(50) PRIMARY KEY, password varchar(255) NOT NULL, EmployeeID integer REFERENCES Employee(EmployeeId) NOT NULL,usertype integer NOT NULL);
""" #bu doğru
]


def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        cursor.close()


if __name__ == "__main__":
    initialize("dbname='snlvpekr' user='snlvpekr' host='balarama.db.elephantsql.com' password='Yez7qmHLmlsFw3UM_4WENR3k6ktjTiEC'")
