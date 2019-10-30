import os
import sys
import forms

import psycopg2 as dbapi2
from flask import Flask,render_template,redirect,url_for, request, session, escape


url = "dbname='snlvpekr' user='snlvpekr' host='balarama.db.elephantsql.com' password='Yez7qmHLmlsFw3UM_4WENR3k6ktjTiEC'" 



app = Flask(__name__)


@app.route("/")
def home_page():
    return render_template('base.html',errorMessage="deneme")

@app.route("/marketplace", methods=['GET','POST'])
def marketplace_page():
    if request.method == 'GET':
        return render_template('marketplace_add.html')

    elif request.method == 'POST':
        market_name = request.form.get('market_name')
        market_address = request.form.get('market_address')
        market_authority = request.form.get('market_authority')
        market_phonenumber = request.form.get('market_phonenumber')
        market_taxid = request.form.get('market_taxid')
        market_commisionfee = request.form.get('market_commission')
        
        obj = forms.MarketPlace()

        obj.MarketPlace_add(market_name,market_address,market_authority,market_phonenumber,market_taxid,market_commisionfee)

        return render_template('marketplace_add.html',errorMessage="Done")
 

if __name__ == "__main__":
    app.run()
