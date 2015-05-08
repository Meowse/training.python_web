#!/usr/bin/python
import cgi
import cgitb
import json

cgitb.enable()

form = cgi.FieldStorage()
operands = form.getlist('operand')
total = 0
for operand in operands:
    try:
        value = int(operand)
    except ValueError:
        value = 0
    total += value

if operands:
	output = "Your output is %s." % str(total)
else:
	output = "Please enter some numbers to be added."

print "Content-Type: text/html"
print
print """
<html>
	<head>
		<title>Simple Calculator</title>
	</head>
	<body>
		<p>%s</p>
		<form method="POST">
			<input name="operand" type="text"></input>
			<input name="operand" type="text"></input><br />
			<input name="operand" type="text"></input>
			<input name="operand" type="text"></input><br />
			<input name="operand" type="text"></input>
			<input name="operand" type="text"></input><br />
			<input name="operand" type="text"></input>
			<input name="operand" type="text"></input><br />
			<input name="operand" type="text"></input>
			<input name="operand" type="text"></input><br />
			<input type="submit">
		</form>
	</body>
</html>
""" % output
