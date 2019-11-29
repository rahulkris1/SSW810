#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
'''
Created on 29 November ‎2019, ‏‎09:30:45
@author: Rahul Kampati
'''

from flask import Flask, render_template
import sqlite3

app = Flask(__name__)
db_path = '810_startup.db'

# @app.route('/')
@app.route('/instructors')
def instructors_route():
    """
    Instructor route
    """

    try:
        db = sqlite3.connect(db_path)

    except Exception as e:
       print(e)

    else:
        query = """ select CWID, Name , Dept, Course, count(*) as students from instructors join grades on CWID = InstructorCWID GROUP BY InstructorCWID, Course order by CWID asc;"""
           
        results = db.execute(query)
        

        database_data = []
        for tuple_data in results:
            database_data.append({'Cwid': tuple_data[0], 'Name': tuple_data[1], 'Department': tuple_data[2], 'Course': tuple_data[3], 'Students': tuple_data[4]})
        db.close()
        return render_template('instructors.html', head='Stevens Respository',  title='Courses and student counts', data=database_data)

app.run(debug=True)