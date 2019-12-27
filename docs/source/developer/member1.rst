Parts Implemented by Yavuz Ege Okumuş
================================

**For Provider**
*From forms.py*

.. code-block:: python

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
