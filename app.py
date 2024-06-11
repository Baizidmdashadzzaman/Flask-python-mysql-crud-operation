import pickle
import numpy as np
import os
import sys
import datetime

from flask import Flask, render_template, request, redirect, url_for, session, flash, app, jsonify,Response

from flask_mysqldb import MySQL

app = Flask(__name__)
app.config.from_object('config.Config')

mysql = MySQL(app)

app.secret_key = 'supersecretkey'

# crud start
def convert_to_dict(cur, row):
    if cur.description:
        return dict((cur.description[idx][0], value) for idx, value in enumerate(row))
    return {}

@app.route('/patients')
def patients_list():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM patients")
    rows = cur.fetchall()
    patients_list = [convert_to_dict(cur, row) for row in rows]
    cur.close()
    title="Patients list"
    return render_template('admin/patients/list.html', patients=patients_list,title=title)

@app.route('/patients/add', methods=['GET', 'POST'])
def patients_add():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        isadmin = 0
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO patients (username,email,password,isadmin) VALUES (%s,%s,%s,%s)", (username,email,password,isadmin))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('patients_list'))
    title="Add new patient"
    return render_template('admin/patients/add.html',title=title)

@app.route('/patients/edit/<int:id>', methods=['GET', 'POST'])
def patients_edit(id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        isadmin = 0
        cur.execute("UPDATE patients SET username = %s, email = %s, password = %s, isadmin = %s WHERE id = %s", 
                    (username, email, password, isadmin, id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('patients_list'))

    cur.execute("SELECT * FROM patients WHERE id = %s", (id,))
    row = cur.fetchone()
    patient = convert_to_dict(cur, row)
    cur.close()
    title="Edit patient information"
    return render_template('admin/patients/edit.html', patient=patient)

@app.route('/patients/delete/<int:id>')
def patients_delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM patients WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('patients_list'))
# crud end


if __name__ == '__main__':
    # app.run()
    app.run(debug=True)
