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
        )""",
    """CREATE TABLE IF NOT EXISTS Employee(
        EmployeeID serial PRIMARY KEY,
        Name varchar(40) NOT NULL,
        Surname varchar(20) NOT NULL,
        Phonenumber varchar(12) NOT NULL,
        Email varchar(25) NOT NULL,
        WorkingHours varchar(255) NOT NULL,
        WorkingDays varchar(255) NOT NULL
    )""",
    """CREATE TABLE IF NOT EXISTS CargoCompany(
        CompanyID serial PRIMARY KEY,
        Name varchar(255) NOT NULL,
        Address varchar(255) NOT NULL,
        PricePerKilo integer NOT NULL,
        TaxID varchar(10) NOT NULL,
        Authority text NOT NULL
    )""",
    """CREATE TABLE IF NOT EXISTS Marketplace(
        MarketID serial PRIMARY KEY,
        Name varchar(255) NOT NULL,
        Address varchar(255) NOT NULL,
        Authority text NOT NULL,
        Phonenumber varchar(12) NOT NULL,
        TaxID varchar(10) NOT NULL,
        Commissionfee integer NOT NULL
    )"""
    ]


def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        cursor.close()


if __name__ == "__main__":   
	
    initialize("dbname='snlvpekr' user='snlvpekr' host='balarama.db.elephantsql.com' password='Yez7qmHLmlsFw3UM_4WENR3k6ktjTiEC'")
