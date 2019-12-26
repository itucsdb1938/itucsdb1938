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

MarketPlace_edit: Edit existing row by using its id.

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

marketplace_list: If usertype is 1 (admin) page opens, otherwise app redirects for homepage. For GET request, page loads with template. If request is POST there are 4 options. If Submit button is used for POST request, app calls MarketPlace_select function from *forms.py* and lists them. If Edit button is used for POST request app redirects page for marketplace_edit. If Delete button clicked for POST request, MarketPlace_delete is called from *forms.py*. Since template of that page does not contain Hompage button as form element, it is just a junk code.

marketplace_edit: If usertype is 1 (admin) page opens, otherwise app redirects for homepage. For GET request, page loads with information of given marketid. If Submit button is used for POST request MarketPlace_edit function will be called from *forms.py*. Since template of that page does not contain Hompage button as form element, it is just a junk code.

**For Employee**

*From forms.py*

.. code-block:: python

   class Employee:

    def Employee_add(self, name, surname, phonenumber, email, workinghours, workingdays):
        dbconnection = dbapi.connect(url)
        cursor = dbconnection.cursor()
        queryString = """INSERT INTO Employee (name, surname, phonenumber, email, workinghours, workingdays) VALUES (%s, %s, %s, %s, %s, %s);"""
        cursor.execute(queryString, (name, surname, phonenumber, email, workinghours, workingdays,))
        dbconnection.commit()
        cursor.close()
        dbconnection.close()
    
    def Employee_select(self, employee_id, name):
        dbconnection = dbapi.connect(url)
        cursor = dbconnection.cursor()
        if (employee_id == '*' or name == '*'):
            queryString = """SELECT * FROM Employee ORDER BY EmployeeID ASC;"""
            cursor.execute(queryString)
            selection = cursor.fetchall()
            dbconnection.commit()
            cursor.close()
            dbconnection.close()
            return selection
        elif (employee_id == '' and name != ''):
            queryString = """SELECT * FROM Employee WHERE name = %s ORDER BY EmployeeID ASC;"""
            cursor.execute(queryString, (name,))
            selection = cursor.fetchall()
            dbconnection.commit()
            cursor.close()
            dbconnection.close()
            return selection
        elif (employee_id != '' and name == ''):
            queryString = """SELECT * FROM Employee WHERE EmployeeID = %s ORDER BY EmployeeID ASC;"""
            cursor.execute(queryString, (employee_id,))
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

    def Employee_delete(self,employee_id):
        dbconnection = dbapi.connect(url)
        cursor = dbconnection.cursor()
        queryString = """DELETE FROM Employee WHERE EmployeeID = %s;"""
        cursor.execute(queryString, (employee_id,))
        dbconnection.commit()
        cursor.close()
        dbconnection.close()
    
    def Employee_edit(self, employee_id, name, surname, phonenumber, email, workinghours, workingdays):
        dbconnection = dbapi.connect(url)
        cursor = dbconnection.cursor()
        queryString = """UPDATE Employee SET name = %s, surname = %s, phonenumber = %s, email = %s, workinghours = %s, workingdays = %s  WHERE  employeeid = %s;"""
        cursor.execute(queryString, (name, surname, phonenumber, email, workinghours, workingdays, employee_id,))
        dbconnection.commit()
        cursor.close()
        dbconnection.close()

    def Employee_select_id (self, week_day, time):
        dbconnection = dbapi.connect(url)
        cursor = dbconnection.cursor()
        queryString = """SELECT employeeid FROM Employee WHERE %s > workinghours[1] AND %s < workinghours[2] AND %s = ANY(workingdays) ORDER BY EmployeeID ASC;"""
        cursor.execute(queryString, (time, time, week_day,))
        selection = cursor.fetchall()
       
        for i in range (1,8):
            if (not selection):
                if week_day+i == 8:
                    week_day = week_day - 7
                queryString = """SELECT employeeid FROM Employee WHERE %s = ANY(workingdays) ORDER BY EmployeeID ASC;"""
                cursor.execute(queryString, (week_day+i,))
                selection = cursor.fetchall()
            else:
                break
                
        dbconnection.commit()
        cursor.close()
        dbconnection.close()
        return selection  
        
Employee_add: Used for adding data to database.

Employee_select: Selecting data from table according to id or name.

Employee_delete: Delete data from table with its id.

Employee_edit: Edit existing row by using its id.

Employee_select_id: Select employeeID by using its workingdays and workinghours.

*From server.py*

.. code-block:: python

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

employee_add: If usertype is 1 (admin) page opens, otherwise app redirects for homepage. For GET request, page loads with template. If request if POST, Employee object will be crated and Employee_add function will be called.

employee_list: If usertype is 1 (admin) page opens, otherwise app redirects for homepage. For GET request, page loads with template. If request is POST there are 4 options. If Submit button is used for POST request, app calls Employee_select function from *forms.py* and lists them. If Edit button is used for POST request app redirects page for employee_edit. If Delete button clicked for POST request, employee_delete is called from *forms.py*. Since template of that page does not contain Hompage button as form element, it is just a junk code.

employee_edit: If usertype is 1 (admin) page opens, otherwise app redirects for homepage. For GET request, page loads with information of given employeeid. If Submit button is used for POST request employee_edit function will be called from *forms.py*. Since template of that page does not contain Hompage button as form element, it is just a junk code.

**For Stock**

*From forms.py*

.. code-block:: python

    class Stock():
		def add_to_stock(self, product_id):
			dbconnection = dbapi.connect(url)
			cursor = dbconnection.cursor()
			queryString = """INSERT INTO stock (productID, quantity) VALUES (%s, 0);"""
			cursor.execute(queryString, (product_id,))
			dbconnection.commit()
			cursor.close()
			dbconnection.close()
		
		def get_ID (self, product_id):
			dbconnection = dbapi.connect(url)
			cursor = dbconnection.cursor()
			queryString = """SELECT ID FROM stock WHERE productid=%s;"""
			cursor.execute(queryString, (product_id,))
			selection = cursor.fetchall()
			dbconnection.commit()
			cursor.close()
			dbconnection.close()
			return selection

		def get_quantity(self, stock_id):
			dbconnection = dbapi.connect(url)
			cursor = dbconnection.cursor()
			queryString = """SELECT quantity FROM stock WHERE id = %s;"""
			cursor.execute(queryString, (stock_id,))
			selection = cursor.fetchall()[0]
			dbconnection.commit()
			cursor.close()
			dbconnection.close()
			return selection

		def update_quantity(self, new_quantity, stock_id):
			dbconnection = dbapi.connect(url)
			cursor = dbconnection.cursor()
			queryString = """UPDATE stock SET quantity = quantity + %s WHERE id = %s;"""
			cursor.execute(queryString, (new_quantity, stock_id,))
			dbconnection.commit()
			cursor.close()
			dbconnection.close()

		def update_location(self, x, y, z, stock_id):
			dbconnection = dbapi.connect(url)
			cursor = dbconnection.cursor()
			queryString = """UPDATE stock SET location_x = %s, location_y = %s, location_z = %s WHERE id = %s;"""
			cursor.execute(queryString, (x, y, z, stock_id,))
			dbconnection.commit()
			cursor.close()
			dbconnection.close()

		def display_stock(self):
			dbconnection = dbapi.connect(url)
			cursor = dbconnection.cursor()
			queryString = """SELECT id,location_x,location_y,location_z,concat_ws(' - ',brand,name),quantity FROM stock inner join products on stock.productid=products.productid;"""
			cursor.execute(queryString,)
			selection = cursor.fetchall()
			dbconnection.commit()
			cursor.close()
			dbconnection.close()
			return selection
        
add_to_stock: Used for adding initial data to database.

get_ID: Select id by using its productID.

get_quantity: Select quantity by using its id.

update_quantity: Update quantity by using its id.

update_location: Select employeeID by using its workingdays and workinghours.

display_stock: Displays stock status by getting product name using inner join.

*From server.py*

.. code-block:: python

   	@app.route('/stock',methods=['GET'])
	def stock():
		obj = forms.Stock()
		data = obj.display_stock()
		return render_template('stock.html', data=data)

stock: Shows the all stock conditions.

**For some features**

*From forms.py*

.. code-block:: python

    def group (name,groupby):
		args=[]
		if (len(name)%groupby != 0):
			return name
		for i in range (0,len(name)-groupby+1,groupby):
			temp = []
			for j in range (0,groupby):
				temp.append(name[i+j])
			args.append(temp)
		return args

	def commafy (str_to_comma):
		res = ''
		for i in str_to_comma:
			res = res + i + ','
		res = res[:-1]
		return res
		
group: Gorups given array by desired pairs.

commafy: Adds comma between all characters.
