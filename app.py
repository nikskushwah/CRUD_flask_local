from flask import Flask, render_template, request, jsonify
import yaml
import psycopg2
import json
import os
from database import *

app = Flask(__name__)

import psycopg2

conn_string = "host={0} user={1} dbname={2} password={3}".format(host, user, dbname, password)
conn = psycopg2.connect(conn_string)
print("connection established")

cursor = conn.cursor()

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/data', methods=['POST','GET'])
def data():
    if request.method == 'POST':
        query = "INSERT INTO fruits (fruit, quantity) VALUES (%s, %s);"
        cursor.execute(query,("Apple", "1"))
        conn.commit()
        return "Inserted 1 row"

    if request.method == 'GET':
        cursor.execute("SELECT * FROM fruits;")
        rows = cursor.fetchall()
        conn.commit()
        return str(rows)

@app.route('/data/<string:id>', methods=['GET', 'DELETE', 'PUT'])
def onedata(id):
    if request.method == 'GET':
        query = "SELECT * FROM fruits where id = %s ;"
        cursor.execute(query,(id))
        rows = cursor.fetchall()
        return str(rows)

    if request.method == 'DELETE':
        cursor.execute("DELETE FROM fruits WHERE id = %s;", (id))
        return "deleted"

    if request.method == 'PUT':
        cursor.execute("UPDATE fruits SET Fruit = %s,Quantity =%s WHERE id = %s ;", ("apple", "100",id))
        return "updated"

if __name__ == '__main__':
    app.debug = True
    app.run()
