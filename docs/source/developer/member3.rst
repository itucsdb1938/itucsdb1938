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

create_order: 'GET' method shows the create order form page. For 'POST', on the page, there are 2 text input boxes which are for searching items. If there are items match with those criterias, you can select one of them with option box and redirects user to order_information page with that items informations.

my_orders : For 'GET' method, this function gets the employeeid from session and runs the my_orders method from forms.py. For 'POST' method, if dispatch button is clicked, first it checks with check_dispatch method of Orders form to see if there are enough stock, if there is enough stock, stock amount is decreased and dispatches order. Then updates the finance table. Otherwise, it raises No Stock error. 

order_information: On this page, 'GET' method processes the given product_id and renders template accordingly. After filling the form with related information, 'POST' method ,which is triggered by 'Order' button, gets form fields and creates a temp_order row, also it assigns this temp_order to a available employee.

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



