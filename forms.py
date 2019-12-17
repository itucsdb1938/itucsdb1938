import psycopg2 as dbapi
import os
import hashlib

url = "dbname='snlvpekr' user='snlvpekr' host='balarama.db.elephantsql.com' password='Yez7qmHLmlsFw3UM_4WENR3k6ktjTiEC'"
#url = os.getenv("DB_URL")

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

class CargoCompany:

    def cargo_add(self, company, address, price, taxid, authority):
        dbconnection = dbapi.connect(url)
        cursor = dbconnection.cursor()
        queryString = """INSERT INTO CargoCompany (Name, Address, Priceperkilo, TaxID, Authority) VALUES (%s, %s, %s, %s, %s);"""
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
        queryString = """UPDATE CargoCompany SET Name = %s, Address = %s, Priceperkilo = %s, TaxID = %s, Authority = %s WHERE companyID = %s;"""
        cursor.execute(queryString, (company, address, price, taxid, authority, cargo_id,))
        dbconnection.commit()
        cursor.close()
        dbconnection.close()

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

class Supply:
    def Supply_add(self, provider_id, price, quantity, time, productID):
        dbconnection = dbapi.connect(url)
        cursor = dbconnection.cursor()
        queryString = """INSERT INTO supply_order (providerid, price, quantity, time, productID) VALUES (%s, %s, %s, %s, %s);"""
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
            queryString = """select orderid, price, quantity, time, company, concat_ws(' - ', brand, name) as item from supply_order inner join provider as prov on supply_order.providerid = prov.providerid inner join products as prod on supply_order.productid = prod.productid ORDER BY orderID ASC;"""
            cursor.execute(queryString)
            selection = cursor.fetchall()
            dbconnection.commit()
            cursor.close()
            dbconnection.close()
            return selection
        elif (supply_id == '' and name != '' and company == ''):
            queryString = """select orderid, price, quantity, time, company, concat_ws(' - ', brand, name) as item from supply_order inner join provider as prov on supply_order.providerid = prov.providerid inner join products as prod on supply_order.productid = prod.productid WHERE supply_order.productid = %s ORDER BY orderID ASC;"""
            cursor.execute(queryString, (name,))
            selection = cursor.fetchall()
            dbconnection.commit()
            cursor.close()
            dbconnection.close()
            return selection
        elif (supply_id != '' and name == '' and company == ''):
            queryString = """select orderid, price, quantity, time, company, concat_ws(' - ', brand, name) as item from supply_order inner join provider as prov on supply_order.providerid = prov.providerid inner join products as prod on supply_order.productid = prod.productid WHERE orderID = %s ORDER BY orderID ASC;"""
            cursor.execute(queryString, (supply_id,))
            selection = cursor.fetchall()
            dbconnection.commit()
            cursor.close()
            dbconnection.close()
            return selection
        elif (supply_id == '' and name == '' and company != ''):
            queryString = """select orderid, price, quantity, time, company, concat_ws(' - ', brand, name) as item from supply_order inner join provider as prov on supply_order.providerid = prov.providerid inner join products as prod on supply_order.productid = prod.productid WHERE supply_order.providerid = %s ORDER BY orderID ASC;"""
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

#Since given order cannot be changed, edit function of supplies have been excluded from code.
#    def Supply_edit (self, order_id, provider_id, price, quantity, time, productID):
#        dbconnection = dbapi.connect(url)
#        cursor = dbconnection.cursor()
#        queryString = """UPDATE supply_order SET providerID = %s, price = %s, quantity = %s, time = %s, productID = %s WHERE orderID = %s;"""
#        cursor.execute(queryString, (provider_id, price, quantity, time, productID, order_id,))
#        dbconnection.commit()
#        cursor.close()
#        dbconnection.close()

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
        if (selection[0][0] > selection[0][1]):
            return False
        else:
            return True

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
        queryString = """SELECT * FROM stock;"""
        cursor.execute(queryString,)
        selection = cursor.fetchall()
        dbconnection.commit()
        cursor.close()
        dbconnection.close()
        return selection

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

class Finance():
    
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

        cargoprice = int(weight) * int(perkilo)
        gain = int(sellprice)*int(howMany)
        netWorth = gain*(int(commission)/100)
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
        newTotal = int(lastTotal) + netWorth
        queryString = """INSERT INTO Financial(orderid,Transaction,Cargo_price,Total) VALUES(%s,%s,%s,%s);"""
        cursor.execute(queryString, (orderid,netWorth,cargoprice,newTotal,))    


        dbconnection.commit()
        cursor.close()
        dbconnection.close()
