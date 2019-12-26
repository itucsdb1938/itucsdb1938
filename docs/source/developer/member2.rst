Parts Implemented by Egehan Orta
================================

**For MarketPlace**

*From forms.py*

.. code-block:: python

   class MarketPlace:

    def MarketPlace_add(self, name, address, authority, phonenumber, taxid, commission):
        dbconnection = dbapi.connect(url)
        cursor = dbconnection.cursor()
        queryString = """INSERT INTO Marketplace (name, address, authority, phonenumber, taxid, commissionfee) VALUES (%s, %s, %s, %s, %s, %s);"""
        cursor.execute(queryString, (name, address, authority, phonenumber, taxid, commission,))
        dbconnection.commit()
        cursor.close()
        dbconnection.close()
    
    def MarketPlace_select(self, market_id, name):
        dbconnection = dbapi.connect(url)
        cursor = dbconnection.cursor()
        if (market_id == '*' or name == '*'):
            queryString = """SELECT * FROM Marketplace ORDER BY MarketID ASC;"""
            cursor.execute(queryString)
            selection = cursor.fetchall()
            dbconnection.commit()
            cursor.close()
            dbconnection.close()
            return selection
        elif (market_id == '' and name != ''):
            queryString = """SELECT * FROM Marketplace WHERE name = %s ORDER BY MarketID ASC;"""
            cursor.execute(queryString, (name,))
            selection = cursor.fetchall()
            dbconnection.commit()
            cursor.close()
            dbconnection.close()
            return selection
        elif (market_id != '' and name == ''):
            queryString = """SELECT * FROM Marketplace WHERE MarketID = %s ORDER BY MarketID ASC;"""
            cursor.execute(queryString, (market_id,))
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
    
    def MarketPlace_delete(self, market_id):
        dbconnection = dbapi.connect(url)
        cursor = dbconnection.cursor()
        queryString = """DELETE FROM Marketplace WHERE MarketID = %s;"""
        cursor.execute(queryString, (market_id,))
        dbconnection.commit()
        cursor.close()
        dbconnection.close()

    def MarketPlace_edit(self, market_id, name, address, authority, phonenumber, taxid, commission):
        dbconnection = dbapi.connect(url)
        cursor = dbconnection.cursor()
        queryString = """UPDATE Marketplace SET name = %s, address = %s, authority = %s, phonenumber = %s, taxid = %s, commissionfee = %s  WHERE  MarketID = %s;"""
        cursor.execute(queryString, (name, address, authority, phonenumber, taxid, commission, market_id,))
        dbconnection.commit()
        cursor.close()
        dbconnection.close()
        
MarketPlace_add: Used for adding data to database.

MarketPlace_select: Selecting data from table according to id or name.

MarketPlace_delete: Delete data from table with its id.

*From server.py*

.. code-block:: python
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
           
marketplace_add: If usertype is 1 (admin) page opens, otherwise app redirects for homepage. For GET request, page loads with template. If request if POST, MarketPlace object will be crated and MarketPlace_add function will be called.

marketplace_list: If usertype is 1 (admin) page opens, otherwise app redirects for homepage. For GET request, page loads with template. If request is POST there are 3 options. If Submit button is used for POST request, app calls MarketPlace_select function from *forms.py* and lists them. If Edit button is used for POST request app redirects page for marketplace_edit. If Delete button clicked for POST request, MarketPlace_delete is called from *forms.py*.

marketplace_edit: If usertype is 1 (admin) page opens, otherwise app redirects for homepage. For GET request, page loads with information of given marketid. If Submit button is used for POST request MarketPlace_edit function will be called from *forms.py*. Since template of that page does not contain Hompage button as form element, it is just a junk code.

