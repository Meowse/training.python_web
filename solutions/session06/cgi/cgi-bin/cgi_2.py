#!/usr/bin/python
import cgi
import cgitb
cgitb.enable()
import os
import datetime


default = "No Value Present"


print "Content-Type: text/html"
print

body = """<html>
<head>
<title>Lab 1 - CGI experiments</title>
</head>
<body>
The server name or IP address is %s.<br>
<br>
The server is running on port %s.<br>
<br>
Your hostname is %s.  <br>
<br>
You are coming from  %s<br>
<br>
The currenly executing script is %s<br>
<br>
The request arrived at %s<br>

</body>
</html>""" % (
    os.environ.get('SERVER_NAME', default),  # Server Hostname or IP
    os.environ.get('SERVER_PORT', default),  # server port
    os.environ.get('REMOTE_HOST', default),  # client hostname
    os.environ.get('REMOTE_ADDR', default),  # client IP
    os.environ.get('SCRIPT_NAME', default),  # this script name
    datetime.datetime.now(),  # time
)

print body,
