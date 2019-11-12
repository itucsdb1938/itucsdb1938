import os
import sys
import forms

import psycopg2 as dbapi2
from flask import Flask, render_template, redirect, url_for, request, session, escape, jsonify


url = "dbname='snlvpekr' user='snlvpekr' host='balarama.db.elephantsql.com' password='Yez7qmHLmlsFw3UM_4WENR3k6ktjTiEC'" 



app = Flask(__name__)


@app.route("/")
def home_page():
    return render_template('base.html',errorMessage="deneme")

@app.route("/marketplace_add", methods=['GET','POST'])
def marketplace_add():
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
 
@app.route("/marketplace_list", methods=['GET','POST'])
def marketplace_list():
    if request.method == 'GET':
        return render_template('marketplace_list.html')

    elif request.method == 'POST':
        if (request.form['submit_button'] == 'Delete Selected'):
            option = request.form['options']
            obj = forms.MarketPlace()
            obj.MarketPlace_delete(option)
            return render_template('marketplace_list.html')

        elif (request.form['submit_button'] == 'Edit Selected'):
            option = request.form['options']
            return redirect(url_for('marketplace_edit', marketid = option))

        elif (request.form['submit_button'] == 'Submit'):
            market_id = request.form.get('market_id')
            market_name = request.form.get('market_name')
            obj = forms.MarketPlace()

            data = obj.MarketPlace_select(market_id, market_name)
            return render_template('marketplace_list.html', data = data)

@app.route("/marketplace_edit/<marketid>", methods=['GET','POST'])
def marketplace_edit(marketid):
    if request.method == 'GET':
        obj = forms.MarketPlace()
        data = obj.MarketPlace_select(marketid, '')
        return render_template('marketplace_edit.html', data = data)

    elif request.method == 'POST':
        market_name = request.form.get('market_name')
        market_address = request.form.get('market_address')
        market_authority = request.form.get('market_authority')
        market_phonenumber = request.form.get('market_phonenumber')
        market_taxid = request.form.get('market_taxid')
        market_commisionfee = request.form.get('market_commission')
        market_id = request.form['options']
        obj = forms.MarketPlace()

        obj.MarketPlace_edit(market_name,market_address,market_authority,market_phonenumber,market_taxid,market_commisionfee,market_id)
        return redirect(url_for('marketplace_list'))




if __name__ == "__main__":
    app.run()
