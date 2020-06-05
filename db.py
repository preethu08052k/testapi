from flask import jsonify
from decimal import Decimal
import pymysql

def query(querystr,return_json=True):
    connection=pymysql.connect( host='localhost',
                                user='root',
                                password='',
                                db='testapi',
                                cursorclass=pymysql.cursors.DictCursor )
    connection.begin()
    cursor=connection.cursor()
    cursor.execute(querystr)
    result=encode(cursor.fetchall())
    connection.commit()
    cursor.close()
    connection.close()
    if return_json:
         return jsonify(result)
    else:
        return result

def encode(data):
    for row in data:
        for key,value in row.items():
            if isinstance(value,Decimal):
                row[key]=str(value)
    return data
