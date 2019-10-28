import os
import sys

import psycopg2 as dbapi2
from flask import Flask


url = "dbname='snlvpekr' user='snlvpekr' host='balarama.db.elephantsql.com' password='EiWIdrfC_c6yWoP6Ln1goR5uq-Dl2hnp'" 



app = Flask(__name__)


@app.route("/")
def home_page():
    return """Hello ege!
        <a href="xx">deneme</a>
    """

@app.route("/xx")
def xx_page():

    connection = dbapi2.connect(url)
    cursor = connection.cursor()

    query_string = "SELECT * FROM dummy"

    cursor.execute(query_string)

    data = cursor.fetchall()

    connection.close()

    print(data)

    return str(data[0])


if __name__ == "__main__":
    app.run()
