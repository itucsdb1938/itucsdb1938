import os
import sys
import forms
import functions
from datetime import datetime
import psycopg2 as dbapi2
from flask import Flask, render_template, redirect, url_for, request, session, escape, jsonify
import hashlib

#url = "dbname='snlvpekr' user='snlvpekr' host='balarama.db.elephantsql.com' password='Yez7qmHLmlsFw3UM_4WENR3k6ktjTiEC'"
url = os.getenv("DB_URL")

app = Flask(__name__)
SESSION_TYPE = 'redis'
app.secret_key = "kenandogulu"

@app.route("/logout", methods=['GET'])
def logout():
    session['usertype'] = 0
    session['employeeid'] = 0
    return redirect(url_for('home_page'))


@app.route("/register", methods=['GET', 'POST'])
def register():

    if request.method == 'GET' and session['usertype']==1:
        print(session['usertype'])
        return render_template('register.html')

    elif request.method == 'POST' and session['usertype']==1:
        username = request.form.get('add_username')
        password = request.form.get('add_password')
        employeeid = request.form.get('add_employeeid')
        usertype = request.form.get('add_type')
        print(username,password,employeeid,usertype)
        obj = forms.Users()
        obj.addUser(username,password,employeeid,usertype)
        return redirect(url_for('register'))
        
    else:
        return redirect(url_for('home_page',error='You are not Authorized'))


@app.route("/login",methods=['GET','POST'])
def login():
    if(request.method == 'GET') :
        return render_template('login.html')
    else:
        if(request.form['submit_button']) == 'Submit':
            username = request.form.get('login_username')
            password = request.form.get('login_password')
            obj = forms.Users()
            data = obj.getUser(username, password)
            if (not data):
                return redirect(url_for('login',message='LOGIN FAILED'))
            else:
                session['usertype'] = data[0][0]
                session['employeeid'] = data[0][1]
                print(session['usertype'])
                print(session['employeeid'])
                return redirect(url_for('home_page'))


@app.route("/", methods=['GET'])
def home_page():
    if (request.method == 'GET'):
        if request.args.get('error') != None:
            return render_template('homepage.html',message=request.args.get('error'))
        return render_template('homepage.html')


@app.route("/marketplace_add", methods=['GET', 'POST'])
def marketplace_add():
    if request.method == 'GET' and session['usertype']==1:
        return render_template('marketplace_add.html')

    elif request.method == 'POST' and session['usertype']==1:
        if (request.form['submit_button'] == 'Submit'):
            market_name = request.form.get('market_name')
            market_address = request.form.get('market_address')
            market_authority = request.form.get('market_authority')
            market_phonenumber = request.form.get('market_phonenumber')
            market_taxid = request.form.get('market_taxid')
            market_commisionfee = request.form.get('market_commission')
            obj = forms.MarketPlace()
            obj.MarketPlace_add(market_name, market_address, market_authority,
                                market_phonenumber, market_taxid,
                                market_commisionfee)
            return redirect(url_for('marketplace_add'))
        elif (request.form['submit_button'] == 'Homepage'):
            return redirect(url_for('home_page'))
    else:
        return redirect(url_for('home_page',error='You are not Authorized'))


@app.route("/marketplace_list", methods=['GET', 'POST'])
def marketplace_list():
    if request.method == 'GET' and session['usertype']==1:
        return render_template('marketplace_list.html')

    elif request.method == 'POST' and session['usertype']==1:
        if (request.form['submit_button'] == 'Delete Selected'):
            option = request.form['options']
            obj = forms.MarketPlace()
            obj.MarketPlace_delete(option)
            return redirect(url_for('marketplace_list'))

        elif (request.form['submit_button'] == 'Edit Selected'):
            option = request.form['options']
            return redirect(url_for('marketplace_edit', market_id=option))

        elif (request.form['submit_button'] == 'Submit'):
            market_id = request.form.get('market_id')
            market_name = request.form.get('market_name')
            obj = forms.MarketPlace()
            data = obj.MarketPlace_select(market_id, market_name)
            return render_template('marketplace_list.html', data=data)

        elif (request.form['submit_button'] == 'Homepage'):
            return redirect(url_for('home_page'))
    else:
        return redirect(url_for('home_page',error='You are not Authorized'))


@app.route("/marketplace_edit/<market_id>", methods=['GET', 'POST'])
def marketplace_edit(market_id):
    if request.method == 'GET' and session['usertype']==1:
        obj = forms.MarketPlace()
        data = obj.MarketPlace_select(market_id, '')
        return render_template('marketplace_edit.html', data=data)

    elif request.method == 'POST' and session['usertype']==1:
        if (request.form['submit_button'] == 'Submit'):
            market_name = request.form.get('market_name')
            market_address = request.form.get('market_address')
            market_authority = request.form.get('market_authority')
            market_phonenumber = request.form.get('market_phonenumber')
            market_taxid = request.form.get('market_taxid')
            market_commisionfee = request.form.get('market_commission')
            obj = forms.MarketPlace()
            obj.MarketPlace_edit(market_id, market_name, market_address,
                                 market_authority, market_phonenumber,
                                 market_taxid, market_commisionfee)
            return redirect(url_for('marketplace_list'))
        elif (request.form['submit_button'] == 'Homepage'):
            return redirect(url_for('home_page'))
    
    else:
        return redirect(url_for('home_page',error='You are not Authorized'))


@app.route("/provider_add", methods=['GET', 'POST'])
def provider_add():
    if request.method == 'GET' and session['usertype']==1:
        return render_template('provider_add.html')
    elif request.method == 'POST' and session['usertype']==1:
        if (request.form['submit_button'] == 'Submit'):
            provider_company = request.form.get('provider_company')
            provider_address = request.form.get('provider_address')
            provider_phonenumber = request.form.get('provider_phonenumber')
            provider_taxid = request.form.get('provider_taxid')
            provider_authority = request.form.get('provider_authority')
            obj = forms.Provider()
            obj.Provider_add(provider_company, provider_address,
                             provider_phonenumber, provider_taxid,
                             provider_authority)
            return redirect(url_for('provider_add'))
        elif (request.form['submit_button'] == 'Homepage'):
            return redirect(url_for('home_page'))

    else:
        return redirect(url_for('home_page',error='You are not Authorized'))


@app.route("/provider_list", methods=['GET', 'POST'])
def provider_list():
    if request.method == 'GET' and session['usertype']==1:
        return render_template('provider_list.html')

    elif request.method == 'POST' and session['usertype']==1:
        if (request.form['submit_button'] == 'Delete Selected'):
            option = request.form['options']
            obj = forms.Provider()
            obj.Provider_delete(option)
            return redirect(url_for('provider_list'))

        elif (request.form['submit_button'] == 'Edit Selected'):
            option = request.form['options']
            return redirect(url_for('provider_edit', provider_id=option))

        elif (request.form['submit_button'] == 'Submit'):
            provider_id = request.form.get('provider_id')
            provider_company = request.form.get('provider_company')
            obj = forms.Provider()
            data = obj.Provider_select(provider_id, provider_company)
            return render_template('provider_list.html', data=data)

        elif (request.form['submit_button'] == 'Homepage'):
            return redirect(url_for('home_page'))

    else:
        return redirect(url_for('home_page',error='You are not Authorized'))


@app.route("/provider_edit/<provider_id>", methods=['GET', 'POST'])
def provider_edit(provider_id):
    if request.method == 'GET' and session['usertype']==1:
        obj = forms.Provider()
        data = obj.Provider_select(provider_id, '')
        return render_template('provider_edit.html', data=data)

    if request.method == 'POST' and session['usertype']==1:
        if (request.form['submit_button'] == 'Submit'):
            provider_company = request.form.get('provider_company')
            provider_address = request.form.get('provider_address')
            provider_phonenumber = request.form.get('provider_phonenumber')
            provider_taxid = request.form.get('provider_taxid')
            provider_authority = request.form.get('provider_authority')
            obj = forms.Provider()
            obj.Provider_edit(provider_id, provider_company, provider_address,
                              provider_phonenumber, provider_taxid,
                              provider_authority)
            return redirect(url_for('provider_list'))
        elif (request.form['submit_button'] == 'Homepage'):
            return redirect(url_for('home_page'))

    else:
        return redirect(url_for('home_page',error='You are not Authorized'))


@app.route("/employee_add", methods=['GET', 'POST'])
def employee_add():
    if request.method == 'GET' and session['usertype']==1:
        return render_template('employee_add.html')
    elif request.method == 'POST' and session['usertype']==1:
        if (request.form['submit_button'] == 'Submit'):
            employee_name = request.form.get('employee_name')
            employee_surname = request.form.get('employee_surname')
            employee_phonenumber = request.form.get('employee_phonenumber')
            employee_email = request.form.get('employee_email')
            employee_workinghours = '{'
            if (int(request.form.get('employee_workinghour1')) < int(request.form.get('employee_workinghour2'))):
                employee_workinghours = employee_workinghours + str(int(request.form.get('employee_workinghour1')) * 60) + ',' + str(int(request.form.get('employee_workinghour2')) * 60) + '}'
            else:
                employee_workinghours += '0,0}'
            employee_workingdays = ''
            if(type(request.form.get('employee_workingday1')) is str):
                employee_workingdays += request.form.get('employee_workingday1')
            if(type(request.form.get('employee_workingday2')) is str):
                employee_workingdays += request.form.get('employee_workingday2')
            if(type(request.form.get('employee_workingday3')) is str):
                employee_workingdays += request.form.get('employee_workingday3')
            if(type(request.form.get('employee_workingday4')) is str):
                employee_workingdays += request.form.get('employee_workingday4')
            if(type(request.form.get('employee_workingday5')) is str):
                employee_workingdays += request.form.get('employee_workingday5')
            if(type(request.form.get('employee_workingday6')) is str):
                employee_workingdays += request.form.get('employee_workingday6')
            if(type(request.form.get('employee_workingday7')) is str):
                employee_workingdays += request.form.get('employee_workingday7')
            employee_workingdays = functions.commafy(employee_workingdays)
            employee_workingdays = '{' + employee_workingdays + '}'
            obj = forms.Employee()
            obj.Employee_add(employee_name, employee_surname, employee_phonenumber, employee_email, employee_workinghours, employee_workingdays)
            return redirect(url_for('employee_add'))
        elif (request.form['submit_button'] == 'Homepage'):
            return redirect(url_for('home_page'))
    else:
        return redirect(url_for('home_page',error='You are not Authorized'))


@app.route("/employee_list", methods=['GET', 'POST'])
def employee_list():
    if request.method == 'GET' and session['usertype']==1:
        return render_template('employee_list.html')

    elif request.method == 'POST' and session['usertype']==1:
        if (request.form['submit_button'] == 'Delete Selected'):
            option = request.form['options']
            obj = forms.Employee()
            obj.Employee_delete(option)
            return redirect(url_for('employee_list'))

        elif (request.form['submit_button'] == 'Edit Selected'):
            option = request.form['options']
            return redirect(url_for('employee_edit', employee_id=option))

        elif (request.form['submit_button'] == 'Submit'):
            employee_id = request.form.get('employee_id')
            employee_name = request.form.get('employee_name')
            obj = forms.Employee()
            data = obj.Employee_select(employee_id, employee_name)
            return render_template('employee_list.html', data=data)

        elif (request.form['submit_button'] == 'Homepage'):
            return redirect(url_for('home_page'))
    else:
        return redirect(url_for('home_page',error='You are not Authorized'))


@app.route("/employee_edit/<employee_id>", methods=['GET', 'POST'])
def employee_edit(employee_id):
    if request.method == 'GET' and session['usertype']==1:
        obj = forms.Employee()
        data = obj.Employee_select(employee_id, '')
        return render_template('employee_edit.html', data=data)

    elif request.method == 'POST' and session['usertype']==1:
        if (request.form['submit_button'] == 'Submit'):
            employee_name = request.form.get('employee_name')
            employee_surname = request.form.get('employee_surname')
            employee_phonenumber = request.form.get('employee_phonenumber')
            employee_email = request.form.get('employee_email')
            employee_workinghours = '{'
            if (int(request.form.get('employee_workinghour1')) < int(request.form.get('employee_workinghour2'))):
                employee_workinghours = employee_workinghours + str(int(request.form.get('employee_workinghour1')) * 60) + ',' + str(int(request.form.get('employee_workinghour2')) * 60) + '}'
            else:
                employee_workinghours += '0,0}'
            employee_workingdays = ''
            if(type(request.form.get('employee_workingday1')) is str):
                employee_workingdays += request.form.get('employee_workingday1')
            if(type(request.form.get('employee_workingday2')) is str):
                employee_workingdays += request.form.get('employee_workingday2')
            if(type(request.form.get('employee_workingday3')) is str):
                employee_workingdays += request.form.get('employee_workingday3')
            if(type(request.form.get('employee_workingday4')) is str):
                employee_workingdays += request.form.get('employee_workingday4')
            if(type(request.form.get('employee_workingday5')) is str):
                employee_workingdays += request.form.get('employee_workingday5')
            if(type(request.form.get('employee_workingday6')) is str):
                employee_workingdays += request.form.get('employee_workingday6')
            if(type(request.form.get('employee_workingday7')) is str):
                employee_workingdays += request.form.get('employee_workingday7')
            employee_workingdays = functions.commafy(employee_workingdays)
            employee_workingdays = '{' + employee_workingdays + '}'
            obj = forms.Employee()
            obj.Employee_edit(employee_id, employee_name, employee_surname, employee_phonenumber, employee_email, employee_workinghours, employee_workingdays)
            return redirect(url_for('employee_list'))
        elif (request.form['submit_button'] == 'Homepage'):
            return redirect(url_for('home_page'))
    else:
        return redirect(url_for('home_page',error='You are not Authorized'))


@app.route("/cargo_add", methods=['GET', 'POST'])
def cargo_add():
    if request.method == 'GET' and session['usertype']==1:
        return render_template('cargo_add.html')
    elif request.method == 'POST' and session['usertype']==1:
        if (request.form['submit_button'] == 'Submit'):
            cargo_company = request.form.get('cargo_company')
            cargo_address = request.form.get('cargo_address')
            cargo_price = request.form.get('cargo_price')
            cargo_taxid = request.form.get('cargo_taxid')
            cargo_authority = request.form.get('cargo_authority')
            obj = forms.CargoCompany()
            obj.cargo_add(cargo_company, cargo_address, cargo_price,
                          cargo_taxid, cargo_authority)
            return redirect(url_for('cargo_add'))
        elif (request.form['submit_button'] == 'Homepage'):
            return redirect(url_for('home_page'))

    else:
        return redirect(url_for('home_page',error='You are not Authorized'))


@app.route("/cargo_list", methods=['GET', 'POST'])
def cargo_list():
    if request.method == 'GET' and session['usertype']==1:
        return render_template('cargo_list.html')

    elif request.method == 'POST' and session['usertype']==1:
        if (request.form['submit_button'] == 'Delete Selected'):
            option = request.form['options']
            obj = forms.CargoCompany()
            obj.cargo_delete(option)
            return redirect(url_for('cargo_list'))

        elif (request.form['submit_button'] == 'Edit Selected'):
            option = request.form['options']
            return redirect(url_for('cargo_edit', cargo_id=option))

        elif (request.form['submit_button'] == 'Submit'):
            cargo_id = request.form.get('cargo_id')
            cargo_company = request.form.get('cargo_company')
            obj = forms.CargoCompany()
            data = obj.cargo_select(cargo_id, cargo_company)
            return render_template('cargo_list.html', data=data)

        elif (request.form['submit_button'] == 'Homepage'):
            return redirect(url_for('home_page'))
    
    else:
        return redirect(url_for('home_page',error='You are not Authorized'))


@app.route("/cargo_edit/<cargo_id>", methods=['GET', 'POST'])
def cargo_edit(cargo_id):
    if request.method == 'GET' and session['usertype']==1:
        obj = forms.CargoCompany()
        data = obj.cargo_select(cargo_id, '')
        return render_template('cargo_edit.html', data=data)

    if request.method == 'POST' and session['usertype']==1:
        if (request.form['submit_button'] == 'Submit'):
            cargo_company = request.form.get('cargo_company')
            cargo_address = request.form.get('cargo_address')
            cargo_price = request.form.get('cargo_price')
            cargo_taxid = request.form.get('cargo_taxid')
            cargo_authority = request.form.get('cargo_authority')
            obj = forms.CargoCompany()
            obj.cargo_edit(cargo_id, cargo_company, cargo_address, cargo_price,
                           cargo_taxid, cargo_authority)
            return redirect(url_for('cargo_list'))
        elif (request.form['submit_button'] == 'Homepage'):
            return redirect(url_for('home_page'))
    
    else:
        return redirect(url_for('home_page',error='You are not Authorized'))


@app.route("/product_add", methods=['GET', 'POST'])
def product_add():
    if request.method == 'GET' and session['usertype']==1:
        obj = forms.Provider()
        data = obj.Provider_name_select()
        data = functions.group(data, 2)
        return render_template('product_add.html', data=data)
    if request.method == 'POST' and session['usertype']==1:
        if (request.form['submit_button'] == 'Submit'):
            product_name = request.form.get('product_name')
            product_brand = request.form.get('product_brand')
            product_sellprice = request.form.get('product_sellprice')
            provider_id = request.form.get('provider_id')
            product_weight = request.form.get('product_weight')
            obj = forms.Product()
            obj.Product_add(product_name, product_brand, product_sellprice,provider_id, product_weight)
            product_id = obj.Product_select('',product_name)[0][0]
            obj2 = forms.Stock()
            obj2.add_to_stock(product_id)
            return redirect(url_for('product_add'))
        elif (request.form['submit_button'] == 'Homepage'):
            return redirect(url_for('home_page'))

    else:
        return redirect(url_for('home_page',error='You are not Authorized'))


@app.route("/product_list", methods=['GET', 'POST'])
def product_list():
    if request.method == 'GET' and session['usertype']==1:
        return render_template('product_list.html')

    elif request.method == 'POST' and session['usertype']==1:
        if (request.form['submit_button'] == 'Delete Selected'):
            option = request.form['options']
            obj = forms.Product()
            obj.Product_delete(option)
            return redirect(url_for('product_list'))

        elif (request.form['submit_button'] == 'Edit Selected'):
            option = request.form['options']
            return redirect(url_for('product_edit', product_id=option))

        elif (request.form['submit_button'] == 'Submit'):
            product_id = request.form.get('product_id')
            product_name = request.form.get('product_name')
            obj = forms.Product()
            data = obj.Product_select(product_id, product_name)
            return render_template('product_list.html', data=data)

        elif (request.form['submit_button'] == 'Homepage'):
            return redirect(url_for('home_page'))

    else:
        return redirect(url_for('home_page',error='You are not Authorized'))


@app.route("/product_edit/<product_id>", methods=['GET', 'POST'])
def product_edit(product_id):
    if request.method == 'GET' and session['usertype']==1:
        obj = forms.Product()
        data = obj.Product_select(product_id, '')
        obj2 = forms.Provider()
        data2 = obj2.Provider_name_select()
        data2 = functions.group(data2, 2)
        data = [[data], [data2]]
        data.append(obj.Product_provider_id(product_id))
        return render_template('product_Edit.html', data=data)

    if request.method == 'POST' and session['usertype']==1:
        if (request.form['submit_button'] == 'Submit'):
            product_name = request.form.get('product_name')
            product_brand = request.form.get('product_brand')
            product_sellprice = request.form.get('product_sellprice')
            provider_id = request.form.get('provider_id')
            product_weight = request.form.get('product_weight')
            obj = forms.Product()
            obj.Product_edit(product_id, product_name, product_brand,
                             product_sellprice, provider_id, product_weight)
            return redirect(url_for('product_list'))
        elif (request.form['submit_button'] == 'Homepage'):
            return redirect(url_for('home_page'))

    else:
        return redirect(url_for('home_page',error='You are not Authorized'))


@app.route("/supply_add", methods=['GET', 'POST'])
def supply_add():
    if request.method == 'GET' and session['usertype']==1:
        obj = forms.Provider()
        data = obj.Provider_name_select()
        data = functions.group(data, 2)
        obj2 = forms.Product()
        data2 = obj2.Product_name_select()
        data = [[data], [data2]]
        return render_template('supply_add.html', data=data)
    if request.method == 'POST' and session['usertype']==1:
        if (request.form['submit_button'] == 'Submit'):
            provider_id = request.form.get('provider_id')
            supply_price = request.form.get('supply_price')
            supply_quantity = request.form.get('supply_quantity')
            supply_time = datetime.now().strftime("%d/%m/%Y - %H:%M")
            product_id = request.form.get('product_id')
            obj = forms.Supply()
            obj.Supply_add(provider_id, supply_price, supply_quantity, supply_time, product_id)
            obj2 = forms.Stock()
            obj2.update_quantity(supply_quantity,obj2.get_ID(product_id)[0][0])
            obj3 = forms.Finance()
            obj3.weBoughtSmth(obj.get_supplyID())
            return redirect(url_for('supply_add'))
        elif (request.form['submit_button'] == 'Homepage'):
            return redirect(url_for('home_page'))
    
    else:
        return redirect(url_for('home_page',error='You are not Authorized'))

@app.route("/supply_list",methods=['GET','POST'])
def supply_list():
    if request.method == 'GET' and session['usertype']==1:
        obj = forms.Provider()
        data = obj.Provider_name_select()
        data = functions.group(data, 2)
        obj2 = forms.Product()
        data2 = obj2.Product_name_select()
        data2 = functions.group(data2, 3)
        data = [[data], [data2]]
        return render_template('supply_list.html',data = data)
    elif request.method == 'POST' and session['usertype']==1:
        if (request.form['submit_button'] == 'Delete Selected'):
            option = request.form['options']
            obj = forms.Supply()
            obj.Supply_delete(option)
            return redirect(url_for('supply_list'))
        elif (request.form['submit_button'] == 'Edit Selected'):
                option = request.form['options']
                return redirect(url_for('supply_edit', supply_id=option))
        elif (request.form['submit_button'] == 'Submit'):
            supply_id = request.form.get('supply_id')
            product_id = request.form.get('product_id')
            provider_id = request.form.get('provider_id')
            obj = forms.Provider()
            data = obj.Provider_name_select()
            data = functions.group(data, 2)
            obj2 = forms.Product()
            data2 = obj2.Product_name_select()
            data2 = functions.group(data2, 3)
            obj3 = forms.Supply()
            data3 = obj3.Supply_select(supply_id, product_id, provider_id)
            if (type(data3) is not list or not data3):
                data = [[data], [data2]]
            else:
                data = [[data], [data2], [data3]]
            return render_template('supply_list.html', data=data)
        elif (request.form['submit_button'] == 'Homepage'):
            return redirect(url_for('home_page'))
    else:
        return redirect(url_for('home_page',error='You are not Authorized'))



#Since given order cannot be changed, edit function of supplies have been excluded from code.
#@app.route("/supply_edit/<supply_id>",methods=['GET', 'POST'])
#def supply_edit(supply_id):
#    if request.method == 'GET' and session['usertype']==1:
#        obj = forms.Supply()
#        data = obj.Supply_select(supply_id, '', '')
#        obj2 = forms.Provider()
#        data2 = obj2.Provider_name_select()
#        data2 = functions.group(data2, 2)
#        obj3 = forms.Product()
#        data3 = obj3.Product_name_select()
#        data3 = functions.group(data3, 3)
#        data = [[data], [data2], [data3]]
#        return render_template('supply_edit.html', data=data)

#    if request.method == 'POST' and session['usertype']==1:
#        if (request.form['submit_button'] == 'Submit'):
#            provider_id = request.form.get('provider_id')
#            supply_price = request.form.get('supply_price')
#            supply_quantity = request.form.get('supply_quantity')
#            supply_time = datetime.now().strftime("%d/%m/%Y - %H:%M")
#            product_id = request.form.get('product_id')
#            obj = forms.Supply()
#            obj.Supply_edit(supply_id, provider_id, supply_price, supply_quantity, supply_time, product_id)
#            return redirect(url_for('supply_list'))
#        elif (request.form['submit_button'] == 'Homepage'):
#            return redirect(url_for('home_page'))

@app.route("/create_order",methods=['GET', 'POST'])
def create_order():
    if request.method == 'GET':
        return render_template('create_order.html')

    elif request.method == 'POST':
        if (request.form['submit_button'] == 'Order Selected'):
            option = request.form['options']
            return redirect(url_for('order_information', product_id=option))

        elif (request.form['submit_button'] == 'Submit'):
            item_id = request.form.get('item_id')
            item_name = request.form.get('item_name')
            obj = forms.Product()
            data = obj.Product_select(item_id, item_name)
            return render_template('create_order.html', data=data)

        elif (request.form['submit_button'] == 'Homepage'):
            return redirect(url_for('home_page'))

@app.route ("/order_information/<product_id>",methods=['GET', 'POST'])
def order_information(product_id):
    if request.method == 'GET':
        obj = forms.Product()
        data = obj.Product_select(product_id, '')
        data = [data[0][0], data[0][1], data[0][2], data[0][3]]
        obj2 = forms.MarketPlace()
        data2 = obj2.MarketPlace_select('*','')
        obj3 = forms.CargoCompany()
        data3 = obj3.cargo_select('*','')
        data = [[data], [data2], [data3]]
        print(data)
        return render_template('order_information.html', data=data)
    elif request.method == 'POST':
        if (request.form['submit_button'] == 'Order'):
            market_id = request.form.get('market_id')
            cargo_id = request.form.get('cargo_id')
            order_address = request.form.get('order_address')
            customer_name = request.form.get('customer_name')
            order_quantity = request.form.get('order_quantity')
            order_date = datetime.now().strftime("%d/%m/%Y")
            order_time = str(int(datetime.now().strftime("%H"))*60 + int(datetime.now().strftime("%M")))
            order_week_day = datetime.today().weekday() + 1
            obj1 = forms.Employee()
            employee_id = obj1.Employee_select_id(order_week_day, order_time)[0]
            obj2 = forms.Order()
            obj2.temp_order(market_id, order_address, order_date, customer_name, cargo_id, product_id, order_quantity, employee_id, order_time)
            return redirect(url_for('home_page'))

@app.route ('/my_orders', methods= ['GET', 'POST'])
def my_orders():
    if request.method == 'GET':
        
        employee_id = session['employeeid']
        obj = forms.Order()
        data = obj.my_orders(employee_id)
        if request.args.get('error'):
            return render_template('my_orders.html', data=data, message=request.args.get('error'))
        else:
            return render_template('my_orders.html', data=data)
        
    elif request.method == 'POST':
        if (request.form['submit_button'] == 'Dispatch Selected'):
            option = request.form['options'] #order id burdan product_id yi cek product_id den stoka git ve stok durumunu cek
            obj = forms.Order()
            if obj.check_dispatch(option):
                obj2 = forms.Stock()
                obj2.update_quantity(-obj.check_dispatch(option)[0],obj2.get_ID(obj.check_dispatch(option)[2])[0][0])
                obj.dispatch_order(option)
                obj3 = forms.Finance()
                obj3.weSoldSmth(obj.get_orderID())
                return redirect(url_for('my_orders'))
            else:
                return redirect(url_for('my_orders',error='NO STOCK!'))

        elif (request.form['submit_button'] == 'Homepage'):
            return redirect(url_for('home_page'))

@app.route('/stock',methods=['GET'])
def stock():
    obj = forms.Stock()
    data = obj.display_stock()
    return render_template('stock.html', data=data)

@app.route('/all_orders',methods=['GET'])
def all_orders():
    obj = forms.Order()
    data = obj.get_order()
    return render_template('all_orders.html',data=data)

@app.route('/view_finance',methods=['GET'])
def view_finance():
    if session['usertype']==1:
        obj = forms.Finance()
        data = obj.view_finance()
        return render_template('view_finance.html',data=data)
    else:
        return redirect(url_for('home_page',error='You are not Authorized'))

#kaç gram kargo gitmiş komisyon ne kadar marketplace kargoya kaç para veriyomuş
 
if __name__ == "__main__":
    app.run()