import psycopg2 as dbapi
import os

#url = "dbname='snlvpekr' user='snlvpekr' host='balarama.db.elephantsql.com' password='Yez7qmHLmlsFw3UM_4WENR3k6ktjTiEC'"
url = os.getenv("DB_URL")

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
    def Product_add(self, name, brand, buy_price, sell_price, provider_id, weight):
        dbconnection = dbapi.connect(url)
        cursor = dbconnection.cursor()
        queryString = """INSERT INTO Products (Name, Brand, Buyprice, Sellprice, ProviderID, Weight) VALUES (%s, %s, %s, %s, %s, %s);"""
        cursor.execute(queryString, (name, brand, buy_price, sell_price, provider_id, weight,))
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
            queryString = """SELECT productid, name, brand, buyprice, sellprice, company, weight FROM Products INNER JOIN (SELECT providerid, company FROM provider) AS prov ON products.providerid = prov.providerid ORDER BY productID ASC;"""
            cursor.execute(queryString)
            selection = cursor.fetchall()
            dbconnection.commit()
            cursor.close()
            dbconnection.close()
            return selection
        elif (product_id == '' and name != ''):
            queryString = """SELECT productid, name, brand, buyprice, sellprice, company, weight FROM Products INNER JOIN (SELECT providerid, company FROM provider) AS prov ON products.providerid = prov.providerid WHERE Name = %s ORDER BY productID ASC;"""
            cursor.execute(queryString, (name,))
            selection = cursor.fetchall()
            dbconnection.commit()
            cursor.close()
            dbconnection.close()
            return selection
        elif (product_id != '' and name == ''):
            queryString = """SELECT productid, name, brand, buyprice, sellprice, company, weight FROM Products INNER JOIN (SELECT providerid, company FROM provider) AS prov ON products.providerid = prov.providerid WHERE productID = %s ORDER BY productID ASC;"""
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

    def Product_edit(self, product_id, name, brand, buy_price, sell_price, provider_id, weight):
        dbconnection = dbapi.connect(url)
        cursor = dbconnection.cursor()
        queryString = """UPDATE Products SET Name = %s, Brand = %s, Buyprice = %s, Sellprice = %s, ProviderID = %s, Weight = %s WHERE productID = %s;"""
        cursor.execute(queryString, (name, brand, buy_price, sell_price, provider_id, weight, product_id,))
        dbconnection.commit()
        cursor.close()
        dbconnection.close()
