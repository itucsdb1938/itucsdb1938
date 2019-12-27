Parts Implemented by Yiğitcan Çoban
================================
**This Forms Section is for Temporary Orders and Orders Together**

*From forms.py*

.. code-block:: python

   class Order:
    def temp_order(self, market_id, ship_address, order_date, customer_name, company_id, product_id, quantity, employee_id, order_time):
        dbconnection = dbapi.connect(url)
        cursor = dbconnection.cursor()
        queryString = """INSERT INTO temporary_order (marketplaceid, shipaddress, order_date, customer_name, companyid, productid, quantity, employeeid, isdispatched, order_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'false', %s);"""
        cursor.execute(queryString, (market_id, ship_address, order_date, customer_name, company_id, product_id, quantity, employee_id, order_time,))
        dbconnection.commit()
        cursor.close()
        dbconnection.close()
    
    def my_orders(self, employee_id):
        dbconnection = dbapi.connect(url)
        cursor = dbconnection.cursor()
        queryString = """select orderid,shipaddress,location_x,location_y,location_z, customer_name, concat_ws(' - ',brand,name), a.quantity, (a.quantity*sellprice) as price from temporary_order a inner join stock b on a.productid = b.productid inner join products c on c.productid = a.productid WHERE employeeid = %s;"""
        cursor.execute(queryString, (employee_id,))
        selection = cursor.fetchall()
        dbconnection.commit()
        cursor.close()
        dbconnection.close()
        return selection

    def dispatch_order(self, order_id):
        dbconnection = dbapi.connect(url)
        cursor = dbconnection.cursor()
        queryString = """SELECT * FROM temporary_order WHERE orderid = %s;"""
        cursor.execute(queryString, (order_id,))
        selection = cursor.fetchall()
        queryString = """INSERT INTO orders (marketplaceid, shipaddress, order_date, customer_name, companyid, productid, quantity, order_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"""
        cursor.execute(queryString, (selection[0][1],selection[0][2],selection[0][3],selection[0][4],selection[0][5],selection[0][6],selection[0][7],selection[0][10],))
        queryString = """DELETE FROM temporary_order WHERE orderid = %s;"""
        cursor.execute(queryString, (order_id,))
        dbconnection.commit()
        cursor.close()
        dbconnection.close()

    def check_dispatch (self, orderid):
        dbconnection = dbapi.connect(url)
        cursor = dbconnection.cursor()
        queryString = """select temp.quantity as temporary_quantity, stock.quantity, temp.productid, orderid from stock inner join temporary_order as temp on stock.productid = temp.productid where orderid = %s;"""
        cursor.execute(queryString, (orderid,))
        selection = cursor.fetchall()
        dbconnection.commit()
        cursor.close()
        dbconnection.close()
        if (selection[0][0] > selection[0][1]):
            return False
        else:
            return selection[0]

    def get_product_id(self,orderid):
        dbconnection = dbapi.connect(url)
        cursor = dbconnection.cursor()
        queryString = """select productid from orders where orderid=%s;"""
        cursor.execute(queryString, (orderid,))
        selection = cursor.fetchall()
        dbconnection.commit()
        cursor.close()
        dbconnection.close()
        return selection[0]

    def get_order(self):
        dbconnection = dbapi.connect(url)
        cursor = dbconnection.cursor()
        queryString = """select orderid, marketplace.name,shipaddress,order_date,concat_ws(':',order_time/60,order_time%60) as time,customer_name,cargocompany.name,concat_ws(' - ',products.brand,products.name) as product_info,quantity from orders inner join products on orders.productid = products.productid inner join cargocompany on orders.companyid=cargocompany.companyid inner join marketplace on orders.marketplaceid = marketplace.marketid;"""
        cursor.execute(queryString,)
        selection = cursor.fetchall()
        dbconnection.commit()
        cursor.close()
        dbconnection.close()
        return selection

    def get_orderID(self):
        dbconnection = dbapi.connect(url)
        cursor = dbconnection.cursor()
        queryString = """SELECT MAX(orderid) FROM orders; """
        cursor.execute(queryString)
        selection = cursor.fetchall()
        dbconnection.commit()
        cursor.close()
        dbconnection.close()
        return selection[0]
        
        
temp_order: Creates a temporary order with given data

my_orders: Returns all orders associated to a specific employee

dispatch_order: Deletes the specific row from temporary order and creates row with same datas in orders table

check_dispatch: Checks if there is enough stock to dispatch order

get_product_id: Returns product ID of a order row which is specified by orderid

get_order: Returns orders

get_orderID: Returns recently added Order ID of orders table

**This Server.py Section is for Temporary Orders and Orders Together**

*From server.py*

.. code-block:: python
    
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
               

   @app.route('/all_orders',methods=['GET'])
   def all_orders():
       obj = forms.Order()
       data = obj.get_order()
       return render_template('all_orders.html',data=data)

create_order: 'GET' method shows the create order form page. For 'POST', on the page, there are 2 text input boxes which are for searching items. If there are items match with those criterias, you can select one of them with option box and redirects user to order_information page with that items informations.

my_orders : For 'GET' method, this function gets the employeeid from session and runs the my_orders method from forms.py. For 'POST' method, if dispatch button is clicked, first it checks with check_dispatch method of Orders form to see if there are enough stock, if there is enough stock, stock amount is decreased and dispatches order. Then updates the finance table. Otherwise, it raises No Stock error. 

order_information: On this page, 'GET' method processes the given product_id and renders template accordingly. After filling the form with related information, 'POST' method ,which is triggered by 'Order' button, gets form fields and creates a temp_order row, also it assigns this temp_order to a available employee.

all_orders: Shows user all order data

**Form of Products**

*From forms.py*

.. code-block:: python

   class Product:

       def Product_add(self, name, brand, sell_price, provider_id, weight):
           dbconnection = dbapi.connect(url)
           cursor = dbconnection.cursor()
           queryString = """INSERT INTO Products (Name, Brand, Sellprice, ProviderID, Weight) VALUES (%s, %s, %s, %s, %s);"""
           cursor.execute(queryString, (name, brand, sell_price, provider_id, weight,))
           dbconnection.commit()
           cursor.close()
           dbconnection.close()

       def Product_delete(self, product_id):
           dbconnection = dbapi.connect(url)
           cursor = dbconnection.cursor()
           queryString = """DELETE FROM Products WHERE productID = %s;"""
           cursor.execute(queryString, (product_id,))
           dbconnection.commit()
           cursor.close()
           dbconnection.close()

       def Product_select(self, product_id, name):
           dbconnection = dbapi.connect(url)
           cursor = dbconnection.cursor()
           if (product_id == '*' or name == '*'):
               queryString = """SELECT productid, name, brand, sellprice, company, weight FROM Products INNER JOIN (SELECT providerid, company FROM provider) AS prov ON products.providerid = prov.providerid ORDER BY productID ASC;"""
               cursor.execute(queryString)
               selection = cursor.fetchall()
               dbconnection.commit()
               cursor.close()
               dbconnection.close()
               return selection
           elif (product_id == '' and name != ''):
               queryString = """SELECT productid, name, brand, sellprice, company, weight FROM Products INNER JOIN (SELECT providerid, company FROM provider) AS prov ON products.providerid = prov.providerid WHERE Name = %s ORDER BY productID ASC;"""
               cursor.execute(queryString, (name,))
               selection = cursor.fetchall()
               dbconnection.commit()
               cursor.close()
               dbconnection.close()
               return selection
           elif (product_id != '' and name == ''):
               queryString = """SELECT productid, name, brand, sellprice, company, weight FROM Products INNER JOIN (SELECT providerid, company FROM provider) AS prov ON products.providerid = prov.providerid WHERE productID = %s ORDER BY productID ASC;"""
               cursor.execute(queryString, (product_id,))
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

       def Product_edit(self, product_id, name, brand, sell_price, provider_id, weight):
           dbconnection = dbapi.connect(url)
           cursor = dbconnection.cursor()
           queryString = """UPDATE Products SET Name = %s, Brand = %s, Sellprice = %s, ProviderID = %s, Weight = %s WHERE productID = %s;"""
           cursor.execute(queryString, (name, brand, sell_price, provider_id, weight, product_id,))
           dbconnection.commit()
           cursor.close()
           dbconnection.close()

       def Product_name_select(self):
           dbconnection = dbapi.connect(url)
           cursor = dbconnection.cursor()
           queryString = """SELECT productid, brand, name FROM Products;"""
           cursor.execute(queryString)
           selection = cursor.fetchall()
           dbconnection.commit()
           cursor.close()
           dbconnection.close()
           return selection

       def Product_provider_id(self,productid):
           dbconnection = dbapi.connect(url)
           cursor = dbconnection.cursor()
           queryString = """SELECT providerID FROM Products where productid = %s;"""
           cursor.execute(queryString, (productid,))
           selection = cursor.fetchall()[0][0]
           dbconnection.commit()
           cursor.close()
           dbconnection.close()
           return selection
   
   
Product_add: Adds a row to product table. Data is passed by arguments.

Product_delete: Deletes the row specified by ID

Product_select: Selects the row specified by ID and checks it with name 

Product_edit: Edits the row specified by ID          

Product_name_select: Returns all product id, brand and name

Product_provider_id: returns provider ID of row specified by Product ID

**Codes related to Products in server.py**

*From server.py*


.. code-block:: python

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

product_add : Page is responsible for showing form in 'GET' method and sending it to database for 'POST' method. When filled with correct informations and this page is reached by a correct user type, adds a row to product table

product_list : On this page, you can see all products you are associated with and edit or delete them one by one 

product_edit : This page is reached after product_list page. On this page you can fill the form to edit specified row. 


**Codes related to Finance**

*From forms.py*


.. code-block:: python

   class Finance():

       def view_finance(self):
           dbconnection = dbapi.connect(url)
           cursor = dbconnection.cursor()
           queryString = """SELECT * FROM Financial;"""
           cursor.execute(queryString)
           results = cursor.fetchall()
           dbconnection.commit()
           cursor.close()
           dbconnection.close()
           return results


       def weBoughtSmth(self,supplyid):
           dbconnection = dbapi.connect(url)
           cursor = dbconnection.cursor()
           queryString = """SELECT Quantity,ProductID,Price FROM Supply_order WHERE OrderID = %s;"""
           cursor.execute(queryString, (supplyid,))
           results = cursor.fetchall()[0]
           quantity = results[0]
           proId = results[1]
           buyPrice = results[2]
           totalPay = int(quantity) * int(buyPrice)
           totalPay = -1*totalPay
           queryString = """SELECT MAX(TransactionID) FROM Financial;"""
           cursor.execute(queryString)
           maxT = cursor.fetchall()[0]
           queryString = """SELECT Total FROM Financial WHERE TransactionID = %s;"""
           cursor.execute(queryString,(maxT,))
           isThereTotal = cursor.fetchall()
           if isThereTotal:
               lastTotal = isThereTotal[0][0]
           else:
               lastTotal = 0
           newTotal = int(lastTotal) + totalPay
           queryString = """INSERT INTO Financial(Supply_orderID,Transaction,Cargo_price,Total) VALUES(%s,%s,0,%s);"""
           cursor.execute(queryString, (supplyid,totalPay,newTotal,))
           dbconnection.commit()
           cursor.close()
           dbconnection.close()

       def weSoldSmth(self,orderid):
           dbconnection = dbapi.connect(url)
           cursor = dbconnection.cursor()
           queryString = """SELECT MarketplaceID,companyID,ProductID,Quantity FROM Orders WHERE OrderID = %s;"""
           cursor.execute(queryString, (orderid,))
           orderquery = cursor.fetchall()[0]
           print(orderquery)
           marketplace = orderquery[0]
           cargo = orderquery[1]
           productid = orderquery[2]
           howMany = orderquery[3]

           queryString = """SELECT sellprice,weight FROM Products WHERE ProductID = %s;"""
           cursor.execute(queryString, (productid,))
           orderquery = cursor.fetchall()[0]
           sellprice = orderquery[0]
           weight = orderquery[1]

           queryString = """SELECT priceperkilo FROM cargocompany WHERE companyid = %s;"""
           cursor.execute(queryString, (cargo,))
           orderquery = cursor.fetchall()[0]
           perkilo = orderquery[0]

           queryString = """SELECT commissionfee FROM marketplace WHERE marketid = %s;"""
           cursor.execute(queryString, (marketplace,))
           orderquery = cursor.fetchall()[0]
           commission = orderquery[0]

           cargoprice = (float(weight)/1000) * float(perkilo)
           gain = float(sellprice)*float(howMany)
           netWorth = gain-gain*(float(commission)/100)
           netWorth = netWorth-cargoprice

           queryString = """SELECT MAX(TransactionID) FROM Financial;"""
           cursor.execute(queryString)
           maxT = cursor.fetchall()[0]
           queryString = """SELECT Total FROM Financial WHERE TransactionID = %s;"""
           cursor.execute(queryString,(maxT,))
           isThereTotal = cursor.fetchall()
           if isThereTotal:
               lastTotal = isThereTotal[0][0]
           else:
               lastTotal = 0
           newTotal = float(lastTotal) + netWorth
           queryString = """INSERT INTO Financial(orderid,Transaction,Cargo_price,Total) VALUES(%s,%s,%s,%s);"""
           cursor.execute(queryString, (orderid,int(netWorth),cargoprice,newTotal,))    


           dbconnection.commit()
           cursor.close()
           dbconnection.close()
           
          
view_finance : Returns all rows of finance table
weBougthSmth : Adds a new row to Finance table by processing the data from row before and given supply id. Calculates total money spent.
weSoldSmth : Adds a new row to Finance table by processing the data from row before and given supply id. Calculates total money earned.


*From server.py*


.. code-block:: python

   @app.route('/view_finance',methods=['GET'])
   def view_finance():
       if session['usertype']==1:
           obj = forms.Finance()
           data = obj.view_finance()
           return render_template('view_finance.html',data=data)
       else:
           return redirect(url_for('home_page',error='You are not Authorized'))
           
Calls all of the finance table and renders them for user to see

**Codes related to Users**

*From forms.py*

.. code-block:: python

   class Users():    

       def getUser(self,username, password):
           dbconnection = dbapi.connect(url)
           cursor = dbconnection.cursor()
           server_salt = "CVca9QBtk4U8pfPb"
           db_password = password+server_salt
           h = hashlib.md5(db_password.encode())
           queryString = """SELECT usertype, EmployeeID FROM users WHERE username = %s AND password = %s;"""
           cursor.execute(queryString, (username, h.hexdigest(),))
           selection = cursor.fetchall()
           dbconnection.commit()
           cursor.close()
           dbconnection.close()
           return selection

       def addUser(self,username,password,employeeid,usertype):
           server_salt = "CVca9QBtk4U8pfPb"
           db_password = password+server_salt
           h = hashlib.md5(db_password.encode())
           dbconnection = dbapi.connect(url)
           cursor = dbconnection.cursor()
           queryString = """INSERT INTO users (username,password,employeeid,usertype) VALUES (%s,%s,%s,%s);"""
           cursor.execute(queryString, (username,h.hexdigest(),employeeid,usertype,))
           dbconnection.commit()
           cursor.close()
           dbconnection.close()
           
getUser : Checks the username and hashed password, if it matches with any row, returns usertype and EmployeeID of that row

addUser : Saves the user information which are passed as arguments, to the users table


*From server.py*

.. code-block:: python

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
                   
Logout : Resets the sessions stored in local files of users computer

LogIn : Gets the data from form at /login, then checks if datas are related to a user. If it finds a user, then creates sessions accordingly

Register : Adds a new user to users table if there are no duplicate users. 'GET' method returns the form. You need to be admin to use this page.

