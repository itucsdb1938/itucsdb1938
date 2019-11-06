import psycopg2 as dbapi
import os

url = "dbname='snlvpekr' user='snlvpekr' host='balarama.db.elephantsql.com' password='Yez7qmHLmlsFw3UM_4WENR3k6ktjTiEC'"

class MarketPlace:

    def MarketPlace_add(self, name, address, authority, phonenumber, taxid, commission):
        dbconnection = dbapi.connect(url)
        cursor = dbconnection.cursor()
        queryString = """INSERT INTO marketplace (name, address, authority, phonenumber, taxid, commissionfee) VALUES (%s, %s, %s, %s, %s, %s)"""
        cursor.execute(queryString, (name, address, authority, phonenumber, taxid, commission))
        dbconnection.commit()
        cursor.close()
        dbconnection.close()
    
    def MarketPlace_select(self, name = "IS NOT NULL", address = "IS NOT NULL", authority = "IS NOT NULL", phonenumber = "IS NOT NULL", taxid = "IS NOT NULL", commission = "IS NOT NULL"):
        parameters = [name, address, authority, phonenumber, taxid, commission]
        for i in parameters:
            if (i.upper() == 'NULL'):
                i = 'IS ' + i.upper()
            elif (i.upper() == 'NOT NULL'):
                i = 'IS ' + i.upper()
            else:
                i = '= ' + i.upper()
        dbconnection = dbapi.connect(url)
        cursor = dbconnection.cursor()
        queryString = """SELECT * FROM marketplace WHERE (name %s AND address %s AND authority %s AND phonenumber %s AND taxid %s AND commissionfee %s)"""
        cursor.execute(queryString, (name, address, authority, phonenumber, taxid, commission))
        selection = cursor.fetchall()
        cursor.close()
        return selection