import os
import sys

import psycopg2 as dbapi2
from flask import Flask,render_template,redirect,url_for, request, session, escape


url = "dbname='snlvpekr' user='snlvpekr' host='balarama.db.elephantsql.com' password='Yez7qmHLmlsFw3UM_4WENR3k6ktjTiEC'" 



app = Flask(__name__)


@app.route("/")
def home_page():
    return render_template('base.html',errorMessage="deneme")

@app.route("/marketplace", methods=['GET','POST'])
def marketplace_page():
    if request.method == 'POST':
        



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
