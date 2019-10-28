import os
import sys

import psycopg2 as dbapi2


INIT_STATEMENTS = [
    """CREATE TABLE IF NOT EXISTS PROVIDER (
        ProviderID integer PRIMARY KEY,
        Company varchar(50) NOT NULL,
        Address text NOT NULL,
        Phone varchar(12) NOT NULL,
        TaxID varchar(10) NOT NULL,
        Authority text NOT NULL,
        )""",
]


def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        cursor.close()


if __name__ == "__main__":
    url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    initialize(url)
