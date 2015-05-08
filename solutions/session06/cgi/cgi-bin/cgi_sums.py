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

output = str(total)

print "Content-Type: text/html"
print
print """
Your answer is: %s.<p>
<a href="../calculator.html">More?</a>
""" % output
