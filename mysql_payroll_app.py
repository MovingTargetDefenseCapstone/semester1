#!/usr/bin/env python

import cgi
import cgitb
cgitb.enable()
import mysql.connector
from mysql.connector import Error

try:
	conn = mysql.connector.connect(host='127.0.0.1', database='payroll', user='root', password='sploitme')
except Error as e:
	print("Connection failed:", e)

form = cgi.FieldStorage()
post = form.getvalue('s')
print("Content-Type: text/html;charset=utf-8")
print "Content-type:text/html\r\n\r\n"

if not post:
	print "<center>"
	print "<form action='' method='post'>"
	print "<h2>Payroll Login</h2>"
	print "<table style='border-radius: 25px; border: 2px solid black; padding: 20px;'>"
	print "<tr>"
	print "<td>User</td>"
	print "<td><input type='text' name='user'></td>"	
	print "</tr>"
	print "<tr>"
	print "<td>Password</td>"
	print "<td><input type='password' name='password'></td>"
	print "</tr>"
	print "<tr>"
	print "<td><input type='submit' value='OK' name='s'>"
	print "</tr>"
	print "</table>"
	print "</form>"
	print "</center>"

if post:
	user = form.getvalue('user')
	password = form.getvalue('password')
	sql = "select username, first_name, last_name, salary from users where username = '{}' and password = '{}'".format(user, password)
	cursor = conn.cursor()
	cursor.execute(sql)
	rows = cursor.fetchall()
	print "<center>"
        print "<h2>Welcome, {}</h2><br>".format(user)
	print "<table style='border-radius: 25px; border: 2px solid black;' cellspacing=30>"
	print "<tr><th>Username</th><th>First Name</th><th>Last Name</th><th>Salary</th></tr>"
	for row in rows:
		print "<tr>"
		for data in row:
			print "<td> {} </td>".format(data)	
		print "</tr>"
	print "</table></center>"	
	cursor.close()

conn.close()
