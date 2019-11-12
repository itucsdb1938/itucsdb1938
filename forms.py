import psycopg2 as dbapi
import os

url = "dbname='snlvpekr' user='snlvpekr' host='balarama.db.elephantsql.com' password='Yez7qmHLmlsFw3UM_4WENR3k6ktjTiEC'"

class MarketPlace:

    def MarketPlace_add(self, name, address, authority, phonenumber, taxid, commission):
        dbconnection = dbapi.connect(url)
        cursor = dbconnection.cursor()
        queryString = """INSERT INTO Marketplace (name, address, authority, phonenumber, taxid, commissionfee) VALUES (%s, %s, %s, %s, %s, %s)"""
        cursor.execute(queryString, (name, address, authority, phonenumber, taxid, commission,))
        dbconnection.commit()
        cursor.close()
        dbconnection.close()
    
    def MarketPlace_select(self, id, name):
        dbconnection = dbapi.connect(url)
        cursor = dbconnection.cursor()
        if (id == '*' or name == '*'):
            queryString = """SELECT * FROM Marketplace ORDER BY MarketID ASC"""
            cursor.execute(queryString)
            selection = cursor.fetchall()
            cursor.close()
            return selection
        elif (id == '' and name != ''):
            queryString = """SELECT * FROM Marketplace WHERE name = %s ORDER BY MarketID ASC"""
            cursor.execute(queryString, (name,))
            selection = cursor.fetchall()
            cursor.close()
            return selection
        elif (id != '' and name == ''):
            queryString = """SELECT * FROM Marketplace WHERE MarketID = %s ORDER BY MarketID ASC"""
            cursor.execute(queryString, (id,))
            selection = cursor.fetchall()
            cursor.close()
            return selection
        else:
            return
    
    def MarketPlace_delete(self, market_id):
        dbconnection = dbapi.connect(url)
        cursor = dbconnection.cursor()
        queryString = """DELETE FROM Marketplace WHERE MarketID = %s"""
        cursor.execute(queryString, (market_id,))
        dbconnection.commit()
        cursor.close()
        dbconnection.close()

    def MarketPlace_edit(self, name, address, authority, phonenumber, taxid, commission, market_id):
        dbconnection = dbapi.connect(url)
        cursor = dbconnection.cursor()
        queryString = """UPDATE Marketplace SET name = %s, address = %s, authority = %s, phonenumber = %s, taxid = %s, commissionfee = %s  WHERE  MarketID = %s"""
        cursor.execute(queryString, (name, address, authority, phonenumber, taxid, commission, market_id,))
        dbconnection.commit()
        cursor.close()
        dbconnection.close()
