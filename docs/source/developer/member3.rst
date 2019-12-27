Parts Implemented by Yiğitcan Çoban
================================
**For MarketPlace**

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
        
        
bhlkhklh
