import os
import sys
import forms

import psycopg2 as dbapi2
from flask import Flask, render_template, redirect, url_for, request, session, escape, jsonify


url = "dbname='snlvpekr' user='snlvpekr' host='balarama.db.elephantsql.com' password='Yez7qmHLmlsFw3UM_4WENR3k6ktjTiEC'" 



app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def home_page():
    if (request.method == 'GET'):
        return render_template('homepage.html')

    if (request.method == 'POST'):
        if (request.form['submit_button'] == 'Marketplace Add'):
            return redirect(url_for('marketplace_add'))
        elif (request.form['submit_button'] == 'Marketplace List'):
            return redirect(url_for('marketplace_list'))
        elif (request.form['submit_button'] == 'Provider Add'):
            return redirect(url_for('provider_add'))
        elif (request.form['submit_button'] == 'Provider List'):
            return redirect(url_for('provider_list'))
        elif (request.form['submit_button'] == 'Homepage'):
            return redirect(url_for('home_page'))

@app.route("/marketplace_add", methods=['GET','POST'])
def marketplace_add():
    if request.method == 'GET':
        return render_template('marketplace_add.html')

    elif request.method == 'POST':
        if (request.form['submit_button'] == 'Submit'):
            market_name = request.form.get('market_name')
            market_address = request.form.get('market_address')
            market_authority = request.form.get('market_authority')
            market_phonenumber = request.form.get('market_phonenumber')
            market_taxid = request.form.get('market_taxid')
            market_commisionfee = request.form.get('market_commission')
            obj = forms.MarketPlace()
            obj.MarketPlace_add(market_name,market_address,market_authority,market_phonenumber,market_taxid,market_commisionfee)
            return redirect(url_for('marketplace_add'))
        elif (request.form['submit_button'] == 'Homepage'):
            return redirect(url_for('home_page'))
 
@app.route("/marketplace_list", methods=['GET','POST'])
def marketplace_list():
    if request.method == 'GET':
        return render_template('marketplace_list.html')

    elif request.method == 'POST':
        if (request.form['submit_button'] == 'Delete Selected'):
            option = request.form['options']
            obj = forms.MarketPlace()
            obj.MarketPlace_delete(option)
            return redirect(url_for('marketplace_list'))

        elif (request.form['submit_button'] == 'Edit Selected'):
            option = request.form['options']
            return redirect(url_for('marketplace_edit', market_id = option))

        elif (request.form['submit_button'] == 'Submit'):
            market_id = request.form.get('market_id')
            market_name = request.form.get('market_name')
            obj = forms.MarketPlace()
            data = obj.MarketPlace_select(market_id, market_name)
            return render_template('marketplace_list.html', data = data)

        elif (request.form['submit_button'] == 'Homepage'):
            return redirect(url_for('home_page'))

@app.route("/marketplace_edit/<market_id>", methods=['GET','POST'])
def marketplace_edit(market_id):
    if request.method == 'GET':
        obj = forms.MarketPlace()
        data = obj.MarketPlace_select(market_id, '')
        return render_template('marketplace_edit.html', data = data)

    elif request.method == 'POST':
        if (request.form['submit_button'] == 'Submit'):
            market_name = request.form.get('market_name')
            market_address = request.form.get('market_address')
            market_authority = request.form.get('market_authority')
            market_phonenumber = request.form.get('market_phonenumber')
            market_taxid = request.form.get('market_taxid')
            market_commisionfee = request.form.get('market_commission')
            obj = forms.MarketPlace()
            obj.MarketPlace_edit(market_id,market_name,market_address,market_authority,market_phonenumber,market_taxid,market_commisionfee)
            return redirect(url_for('marketplace_list'))
        elif (request.form['submit_button'] == 'Homepage'):
            return redirect(url_for('home_page'))

@app.route("/provider_add", methods=['GET', 'POST'])
def provider_add ():
    if request.method == 'GET':
        return render_template('provider_add.html')
    elif request.method == 'POST':
        if (request.form['submit_button'] == 'Submit'):
            provider_company = request.form.get('provider_company')
            provider_address = request.form.get('provider_address')
            provider_phonenumber = request.form.get('provider_phonenumber')
            provider_taxid = request.form.get('provider_taxid')
            provider_authority = request.form.get('provider_authority')
            obj = forms.Provider()
            obj.Provider_add(provider_company, provider_address, provider_phonenumber, provider_taxid, provider_authority)
            return redirect(url_for('provider_add'))
        elif (request.form['submit_button'] == 'Homepage'):
            return redirect(url_for('home_page'))

@app.route("/provider_list",methods=['GET', 'POST'])
def provider_list ():
    if request.method == 'GET':
        return render_template('provider_list.html')

    elif request.method == 'POST':
        if (request.form['submit_button'] == 'Delete Selected'):
            option = request.form['options']
            obj = forms.Provider()
            obj.Provider_delete(option)
            return redirect(url_for('provider_list'))

        elif (request.form['submit_button'] == 'Edit Selected'):
            option = request.form['options']
            return redirect(url_for('provider_edit', provider_id = option))

        elif (request.form['submit_button'] == 'Submit'):
            provider_id = request.form.get('provider_id')
            provider_company = request.form.get('provider_company')
            obj = forms.Provider()
            data = obj.Provider_select(provider_id, provider_company)
            return render_template('provider_list.html', data = data)

        elif (request.form['submit_button'] == 'Homepage'):
            return redirect(url_for('home_page'))

@app.route("/provider_edit/<provider_id>",methods=['GET', 'POST'])
def provider_edit (provider_id):
    if request.method == 'GET':
        obj = forms.Provider()
        data = obj.Provider_select(provider_id, '')
        return render_template('provider_edit.html', data = data)

    if request.method == 'POST':
        if (request.form['submit_button'] == 'Submit'):
            provider_company = request.form.get('provider_company')
            provider_address = request.form.get('provider_address')
            provider_phonenumber = request.form.get('provider_phonenumber')
            provider_taxid = request.form.get('provider_taxid')
            provider_authority = request.form.get('provider_authority')
            obj = forms.Provider()
            obj.Provider_edit(provider_id, provider_company, provider_address, provider_phonenumber, provider_taxid, provider_authority)
            return redirect(url_for('provider_list'))
        elif (request.form['submit_button'] == 'Homepage'):
            return redirect(url_for('home_page'))

if __name__ == "__main__":
    app.run()
