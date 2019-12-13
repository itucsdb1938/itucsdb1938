import os
import sys
import forms
import functions

import psycopg2 as dbapi2
from flask import Flask, render_template, redirect, url_for, request, session, escape, jsonify


#url = "dbname='snlvpekr' user='snlvpekr' host='balarama.db.elephantsql.com' password='Yez7qmHLmlsFw3UM_4WENR3k6ktjTiEC'" 
url = os.getenv("DB_URL")


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
        elif (request.form['submit_button'] == 'Employee Add'):
            return redirect(url_for('employee_add'))
        elif (request.form['submit_button'] == 'Employee List'):
            return redirect(url_for('employee_list'))
        elif (request.form['submit_button'] == 'Cargo Company Add'):
            return redirect(url_for('cargo_add'))
        elif (request.form['submit_button'] == 'Cargo Company List'):
            return redirect(url_for('cargo_list'))                        
        elif (request.form['submit_button'] == 'Product Add'):
            return redirect(url_for('product_add'))  
        elif (request.form['submit_button'] == 'Product List'):
            return redirect(url_for('product_list')) 
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

@app.route("/employee_add", methods=['GET', 'POST'])
def employee_add ():
    if request.method == 'GET':
        return render_template('employee_add.html')
    elif request.method == 'POST':
        if (request.form['submit_button'] == 'Submit'):
            employee_name = request.form.get('employee_name')
            employee_surname = request.form.get('employee_surname')
            employee_phonenumber = request.form.get('employee_phonenumber')
            employee_email = request.form.get('employee_email')
            employee_workinghours = request.form.get('employee_workinghours')
            employee_workingdays = request.form.get('employee_workingdays')
            obj = forms.Employee()
            obj.Employee_add (employee_name, employee_surname, employee_phonenumber, employee_email, employee_workinghours, employee_workingdays)
            return redirect(url_for('employee_add'))
        elif (request.form['submit_button'] == 'Homepage'):
            return redirect(url_for('home_page'))

@app.route("/employee_list",methods=['GET', 'POST'])
def employee_list ():
    if request.method == 'GET':
        return render_template('employee_list.html')

    elif request.method == 'POST':
        if (request.form['submit_button'] == 'Delete Selected'):
            option = request.form['options']
            obj = forms.Employee()
            obj.Employee_delete(option)
            return redirect(url_for('employee_list'))

        elif (request.form['submit_button'] == 'Edit Selected'):
            option = request.form['options']
            return redirect(url_for('employee_edit', employee_id = option))

        elif (request.form['submit_button'] == 'Submit'):
            employee_id = request.form.get('employee_id')
            employee_name = request.form.get('employee_name')
            obj = forms.Employee()
            data = obj.Employee_select(employee_id, employee_name)
            return render_template('employee_list.html', data = data)

        elif (request.form['submit_button'] == 'Homepage'):
            return redirect(url_for('home_page'))

@app.route("/employee_edit/<employee_id>", methods=['GET','POST'])
def employee_edit(employee_id):
    if request.method == 'GET':
        obj = forms.Employee()
        data = obj.Employee_select(employee_id, '')
        return render_template('employee_edit.html', data = data)

    elif request.method == 'POST':
        if (request.form['submit_button'] == 'Submit'):
            employee_name = request.form.get('employee_name')
            employee_surname = request.form.get('employee_surname')
            employee_phonenumber = request.form.get('employee_phonenumber')
            employee_email = request.form.get('employee_email')
            employee_workinghours = request.form.get('employee_workinghours')
            employee_workingdays = request.form.get('employee_workingdays')
            obj = forms.Employee()
            obj.Employee_edit(employee_id, employee_name, employee_surname, employee_phonenumber, employee_email, employee_workinghours, employee_workingdays)
            return redirect(url_for('employee_list'))
        elif (request.form['submit_button'] == 'Homepage'):
            return redirect(url_for('home_page'))
@app.route("/cargo_add", methods=['GET', 'POST'])
def cargo_add ():
    if request.method == 'GET':
        return render_template('cargo_add.html')
    elif request.method == 'POST':
        if (request.form['submit_button'] == 'Submit'):
            cargo_company = request.form.get('cargo_company')
            cargo_address = request.form.get('cargo_address')
            cargo_price = request.form.get('cargo_price')
            cargo_taxid = request.form.get('cargo_taxid')
            cargo_authority = request.form.get('cargo_authority')
            obj = forms.CargoCompany()
            obj.cargo_add(cargo_company, cargo_address, cargo_price, cargo_taxid, cargo_authority)
            return redirect(url_for('cargo_add'))
        elif (request.form['submit_button'] == 'Homepage'):
            return redirect(url_for('home_page'))

@app.route("/cargo_list",methods=['GET', 'POST'])
def cargo_list ():
    if request.method == 'GET':
        return render_template('cargo_list.html')

    elif request.method == 'POST':
        if (request.form['submit_button'] == 'Delete Selected'):
            option = request.form['options']
            obj = forms.CargoCompany()
            obj.cargo_delete(option)
            return redirect(url_for('cargo_list'))

        elif (request.form['submit_button'] == 'Edit Selected'):
            option = request.form['options']
            return redirect(url_for('cargo_edit', cargo_id = option))

        elif (request.form['submit_button'] == 'Submit'):
            cargo_id = request.form.get('cargo_id')
            cargo_company = request.form.get('cargo_company')
            obj = forms.CargoCompany()
            data = obj.cargo_select(cargo_id, cargo_company)
            return render_template('cargo_list.html', data = data)

        elif (request.form['submit_button'] == 'Homepage'):
            return redirect(url_for('home_page'))

@app.route("/cargo_edit/<cargo_id>",methods=['GET', 'POST'])
def cargo_edit (cargo_id):
    if request.method == 'GET':
        obj = forms.CargoCompany()
        data = obj.cargo_select(cargo_id, '')
        return render_template('cargo_edit.html', data = data)

    if request.method == 'POST':
        if (request.form['submit_button'] == 'Submit'):
            cargo_company = request.form.get('cargo_company')
            cargo_address = request.form.get('cargo_address')
            cargo_price = request.form.get('cargo_price')
            cargo_taxid = request.form.get('cargo_taxid')
            cargo_authority = request.form.get('cargo_authority')
            obj = forms.CargoCompany()
            obj.cargo_edit(cargo_id, cargo_company, cargo_address, cargo_price, cargo_taxid, cargo_authority)
            return redirect(url_for('cargo_list'))
        elif (request.form['submit_button'] == 'Homepage'):
            return redirect(url_for('home_page'))

@app.route("/product_add", methods=['GET', 'POST'])
def product_add ():
    if request.method == 'GET':
        obj = forms.Provider()
        data = obj.Provider_name_select()
        data = functions.group(data, 2)
        return render_template('product_add.html', data = data)
    if request.method == 'POST':
        if (request.form['submit_button'] == 'Submit'):
            product_name = request.form.get('product_name')
            product_brand = request.form.get('product_brand')
            product_buyprice = request.form.get('product_buyprice')
            product_sellprice = request.form.get('product_sellprice')
            provider_id = request.form.get('provider_id')
            product_weight = request.form.get('product_weight')
            obj = forms.Product()
            obj.Product_add(product_name, product_brand, product_buyprice, product_sellprice, provider_id, product_weight)
            return redirect(url_for('product_add'))
        elif (request.form['submit_button'] == 'Homepage'):
            return redirect(url_for('home_page'))

@app.route("/product_list", methods=['GET', 'POST'])
def product_list ():
    if request.method == 'GET':
        return render_template('product_list.html')

    elif request.method == 'POST':
        if (request.form['submit_button'] == 'Delete Selected'):
            option = request.form['options']
            obj = forms.Product()
            obj.Product_delete(option)
            return redirect(url_for('product_list'))
    
        elif (request.form['submit_button'] == 'Edit Selected'):
            option = request.form['options']
            return redirect(url_for('product_edit', product_id = option))
    
        elif (request.form['submit_button'] == 'Submit'):
            product_id = request.form.get('product_id')
            product_name = request.form.get('product_name')
            obj = forms.Product()
            data = obj.Product_select(product_id, product_name)
            return render_template('product_list.html', data = data)

        elif (request.form['submit_button'] == 'Homepage'):
            return redirect(url_for('home_page'))

@app.route("/product_edit/<product_id>",methods=['GET', 'POST'])
def product_edit (product_id):
    if request.method == 'GET':
        obj = forms.Product()
        data = obj.Product_select(product_id, '')
        obj2 = forms.Provider()
        data2 = obj2.Provider_name_select()
        data2 = functions.group(data2, 2)
        data = [[data], [data2]]
        print(data)
        return render_template('product_Edit.html', data=data)
    
    if request.method == 'POST':
        if (request.form['submit_button'] == 'Submit'):
            product_name = request.form.get('product_name')
            product_brand = request.form.get('product_brand')
            product_buyprice = request.form.get('product_buyprice')
            product_sellprice = request.form.get('product_sellprice')
            provider_id = request.form.get('provider_id')
            product_weight = request.form.get('product_weight')
            obj = forms.Product()
            obj.Product_edit(product_id, product_name, product_brand, product_buyprice, product_sellprice, provider_id, product_weight)
            return redirect(url_for('product_list'))
        elif (request.form['submit_button'] == 'Homepage'):
            return redirect(url_for('home_page'))




if __name__ == "__main__":
    app.run()