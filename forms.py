import psycopg2 as dbapi
import os

url = "dbname='snlvpekr' user='snlvpekr' host='balarama.db.elephantsql.com' password='Yez7qmHLmlsFw3UM_4WENR3k6ktjTiEC'"

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
            queryString = """SELECT * FROM Provider;"""
            cursor.execute(queryString)
            selection = cursor.fetchall()
            dbconnection.commit()
            cursor.close()
            dbconnection.close()
            return selection
        elif (provider_id == '' and company != ''):
            queryString = """SELECT * FROM Provider WHERE company = %s;"""
            cursor.execute(queryString, (company,))
            selection = cursor.fetchall()
            dbconnection.commit()
            cursor.close()
            dbconnection.close()
            return selection
        elif (provider_id != '' and company == ''):
            queryString = """SELECT * FROM Provider WHERE ProviderID = %s;"""
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