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
