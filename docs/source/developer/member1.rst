Parts Implemented by Yavuz Ege Okumuş
================================

**For Provider**
*From forms.py*

.. code-block:: python

       class Provider:

       def Provider_add(self, company, address, phone, taxid, authority):
           dbconnection = dbapi.connect(url)
           cursor = dbconnection.cursor()
           queryString = """INSERT INTO Provider (Company, Address, Phone, TaxID, Authority) VALUES (%s, %s, %s, %s, %s);"""
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
           queryString = """UPDATE Provider SET Company = %s, Address = %s, Phone = %s, TaxID = %s, Authority = %s WHERE ProviderID = %s;"""
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
