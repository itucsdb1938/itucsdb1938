Parts Implemented by Yavuz Ege Okumuş
================================

**For Provider**
*From forms.py*

.. code-block:: python

       class Provider:

       def Provider_add(self, company, address, phone, taxid, authority):
           dbconnection = dbapi.connect(url)
           cursor = dbconnection.cursor()
           queryString = """INSERT INTO Provider (Company, Address, Phone, TaxID, Authority) 
              VALUES (%s, %s, %s, %s, %s);"""
           cursor.execute(queryString, (company, address, phone, taxid, authority,))
           dbconnection.commit()
           cursor.close()
           dbconnection.close()

       def Provider_select(self, provider_id, company):
           dbconnection = dbapi.connect(url)
           cursor = dbconnection.cursor()
           if (provider_id == '*' or company == '*'):
               queryString = """SELECT * FROM Provider ORDER BY ProviderID ASC;"""
               cursor.execute(queryString)
               selection = cursor.fetchall()
               dbconnection.commit()
               cursor.close()
               dbconnection.close()
               return selection
           elif (provider_id == '' and company != ''):
               queryString = """SELECT * FROM Provider WHERE company = %s ORDER BY ProviderID ASC;"""
               cursor.execute(queryString, (company,))
               selection = cursor.fetchall()
               dbconnection.commit()
               cursor.close()
               dbconnection.close()
               return selection
           elif (provider_id != '' and company == ''):
               queryString = """SELECT * FROM Provider WHERE ProviderID = %s ORDER BY ProviderID ASC;"""
               cursor.execute(queryString, (provider_id,))
               selection = cursor.fetchall()
               dbconnection.commit()
               cursor.close()
               dbconnection.close()
               return selection
           else:
               cursor.close()
               dbconnection.commit()
               dbconnection.close()
               return

       def Provider_delete(self, provider_id):
           dbconnection = dbapi.connect(url)
           cursor = dbconnection.cursor()
           queryString = """DELETE FROM Provider WHERE ProviderID = %s;"""
           cursor.execute(queryString, (provider_id,))
           dbconnection.commit()
           cursor.close()
           dbconnection.close()

       def Provider_edit(self, provider_id, company, address, phone, taxid, authority):
           dbconnection = dbapi.connect(url)
           cursor = dbconnection.cursor()
           queryString = """UPDATE Provider SET Company = %s, Address = %s, 
              Phone = %s, TaxID = %s, Authority = %s WHERE ProviderID = %s;"""
           cursor.execute(queryString, (company, address, phone, taxid, authority, provider_id,))
           dbconnection.commit()
           cursor.close()
           dbconnection.close()

       def Provider_name_select(self):
           dbconnection = dbapi.connect(url)
           cursor = dbconnection.cursor()
           queryString = """SELECT providerid, company FROM Provider;"""
           cursor.execute(queryString)
           selection = cursor.fetchall()
           dbconnection.commit()
           cursor.close()
           dbconnection.close()
           return selection
           
Provider_add: Used to add provider data to database.
Provider_select: Getting data of a provider according to the id or name.
Provider_delete: Deletes a provider with using its id.
Provider_edit: Edits the existing row of a provider by using its id.
Provider_name_select:Gets the name of a provider.


*From server.py*

.. code-block:: python

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
               
provider_add: If usertype is 1 (admin) page opens, otherwise app redirects for homepage. For GET request, page loads with template. If request if POST, Provider object will be crated and provider_add function will be called.

provider_list: If usertype is 1 (admin) page opens, otherwise app redirects for homepage. For GET request, page loads with template. If request is POST there are 4 options. If Submit button is used for POST request, app calls provider_select function from *forms.py* and lists them. If Edit button is used for POST request app redirects page for provider_edit. If Delete button clicked for POST request, provider_delete is called from *forms.py*. 

provider_edit:If usertype is 1 (admin) page opens, otherwise app redirects for homepage. For GET request, page loads with information of given providerid. If Submit button is used for POST request provider_edit function will be called from *forms.py*. 


**For CargoCompany**
*From forms.py*

.. code-block:: python

       class CargoCompany:

           def cargo_add(self, company, address, price, taxid, authority):
               dbconnection = dbapi.connect(url)
               cursor = dbconnection.cursor()
               queryString = """INSERT INTO CargoCompany (Name, Address, Priceperkilo, TaxID, Authority) 
                     VALUES (%s, %s, %s, %s, %s);"""
               cursor.execute(queryString, (company, address, price, taxid, authority,))
               dbconnection.commit()
               cursor.close()
               dbconnection.close()

           def cargo_select(self, cargo_id, company):
               dbconnection = dbapi.connect(url)
               cursor = dbconnection.cursor()
               if (cargo_id == '*' or company == '*'):
                   queryString = """SELECT * FROM CargoCompany ORDER BY CompanyID ASC;"""
                   cursor.execute(queryString)
                   selection = cursor.fetchall()
                   dbconnection.commit()
                   cursor.close()
                   dbconnection.close()
                   return selection
               elif (cargo_id == '' and company != ''):
                   queryString = """SELECT * FROM CargoCompany WHERE Name = %s ORDER BY CompanyID ASC;"""
                   cursor.execute(queryString, (company,))
                   selection = cursor.fetchall()
                   dbconnection.commit()
                   cursor.close()
                   dbconnection.close()
                   return selection
               elif (cargo_id != '' and company == ''):
                   queryString = """SELECT * FROM CargoCompany WHERE companyID = %s ORDER BY CompanyID ASC;"""
                   cursor.execute(queryString, (cargo_id,))
                   selection = cursor.fetchall()
                   dbconnection.commit()
                   cursor.close()
                   dbconnection.close()
                   return selection
               else:
                   cursor.close()
                   dbconnection.commit()
                   dbconnection.close()
                   return

           def cargo_delete(self, cargo_id):
               dbconnection = dbapi.connect(url)
               cursor = dbconnection.cursor()
               queryString = """DELETE FROM CargoCompany WHERE companyID = %s;"""
               cursor.execute(queryString, (cargo_id,))
               dbconnection.commit()
               cursor.close()
               dbconnection.close()

           def cargo_edit(self, cargo_id, company, address, price, taxid, authority):
               dbconnection = dbapi.connect(url)
               cursor = dbconnection.cursor()
               queryString = """UPDATE CargoCompany SET Name = %s, 
                     Address = %s, Priceperkilo = %s, TaxID = %s, Authority = %s WHERE companyID = %s;"""
               cursor.execute(queryString, (company, address, price, taxid, authority, cargo_id,))
               dbconnection.commit()
               cursor.close()
               dbconnection.close()
               
cargo_add: Used to add cargo company data to database.
cargo_select: Getting data of a cargo company according to the id or name.
cargo_delete: Deletes a cargo company with using its id.
cargo_edit: Edits the existing row of a cargo company by using its id.               

*From server.py*

.. code-block:: python

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


cargo_add: If usertype is 1 (admin) page opens, otherwise app redirects for homepage. For GET request, page loads with template. If request if POST, cargo object will be crated and cargo_add function will be called.

cargo_list: If usertype is 1 (admin) page opens, otherwise app redirects for homepage. For GET request, page loads with template. If request is POST there are 4 options. If Submit button is used for POST request, app calls cargo_select function from *forms.py* and lists them. If Edit button is used for POST request app redirects page for cargo_edit. If Delete button clicked for POST request, cargo_delete is called from *forms.py*. 

cargo_edit:If usertype is 1 (admin) page opens, otherwise app redirects for homepage. For GET request, page loads with information of given cargoid. If Submit button is used for POST request cargo_edit function will be called from *forms.py*. 

**For Supply_order**
*From forms.py*

.. code-block:: python

       class Supply:
           def Supply_add(self, provider_id, price, quantity, time, productID):
               dbconnection = dbapi.connect(url)
               cursor = dbconnection.cursor()
               queryString = """INSERT INTO supply_order (providerid, price, quantity, time, productID) 
                     VALUES (%s, %s, %s, %s, %s);"""
               cursor.execute(queryString, (provider_id, price, quantity, time, productID,))
               dbconnection.commit()
               cursor.close()
               dbconnection.close()

           def Supply_delete(self,supply_id):
               dbconnection = dbapi.connect(url)
               cursor = dbconnection.cursor()
               queryString = """DELETE FROM supply_order WHERE orderID = %s;"""
               cursor.execute(queryString, (supply_id,))
               dbconnection.commit()
               cursor.close()
               dbconnection.close()

           def Supply_select(self, supply_id, name, company):
               dbconnection = dbapi.connect(url)
               cursor = dbconnection.cursor()
               if (supply_id == '*' or name == '*' or company == '*'):
                   queryString = """select orderid, price, quantity, time, company, 
                     concat_ws(' - ', brand, name) as item from 
                     supply_order inner join provider as prov on supply_order.providerid = prov.providerid 
                     inner join products as prod on supply_order.productid = prod.productid ORDER BY orderID ASC;"""
                   cursor.execute(queryString)
                   selection = cursor.fetchall()
                   dbconnection.commit()
                   cursor.close()
                   dbconnection.close()
                   return selection
               elif (supply_id == '' and name != '' and company == ''):
                   queryString = """select orderid, price, quantity, time, company, concat_ws(' - ', brand, name) 
                     as item from supply_order inner join provider as prov on supply_order.providerid = prov.providerid 
                     inner join products as prod on supply_order.productid = prod.productid WHERE supply_order.productid = %s 
                     ORDER BY orderID ASC;"""
                   cursor.execute(queryString, (name,))
                   selection = cursor.fetchall()
                   dbconnection.commit()
                   cursor.close()
                   dbconnection.close()
                   return selection
               elif (supply_id != '' and name == '' and company == ''):
                   queryString = """select orderid, price, quantity, time, company, concat_ws(' - ', brand, name) 
                     as item from supply_order inner join provider as prov on supply_order.providerid = prov.providerid 
                     inner join products as prod on supply_order.productid = prod.productid 
                     WHERE orderID = %s ORDER BY orderID ASC;"""
                   cursor.execute(queryString, (supply_id,))
                   selection = cursor.fetchall()
                   dbconnection.commit()
                   cursor.close()
                   dbconnection.close()
                   return selection
               elif (supply_id == '' and name == '' and company != ''):
                   queryString = """select orderid, price, quantity, time, company, concat_ws(' - ', brand, name) 
                     as item from supply_order inner join provider as prov on supply_order.providerid = prov.providerid 
                     inner join products as prod on supply_order.productid = prod.productid WHERE supply_order.providerid = %s 
                     ORDER BY orderID ASC;"""
                   cursor.execute(queryString, (company,))
                   selection = cursor.fetchall()
                   dbconnection.commit()
                   cursor.close()
                   dbconnection.close()
                   return selection
               else:
                   cursor.close()
                   dbconnection.commit()
                   dbconnection.close()
                   return

           def get_supplyID (self):
               dbconnection = dbapi.connect(url)
               cursor = dbconnection.cursor()
               queryString = """SELECT MAX(orderID) FROM supply_order;"""
               cursor.execute(queryString)
               selection = cursor.fetchall()[0]
               dbconnection.commit()
               cursor.close()
               dbconnection.close()
               return selection
               
               
supply_add: Used to order supplies .
supply_select: Getting data of a supply order according to the id or name.
supply_delete: Deletes a supply order with using its id.
get_supplyID:gets the id of the most recent supply order.    


*From server.py*

.. code-block:: python

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
supply_add:If usertype is 1 (admin) page opens, otherwise app redirects for homepage. For GET request, page loads with template. If request if POST, supply object will be crated and supply_add function will be called.
supply_list:If usertype is 1 (admin) page opens, otherwise app redirects for homepage. For GET request, page loads with template. If request is POST there are 4 options. If Submit button is used for POST request, app calls supply_select function from *forms.py* and lists them. If Edit button is used for POST request app redirects page for supply_edit. If Delete button clicked for POST request, supply_delete is called from *forms.py*. 
