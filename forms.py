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