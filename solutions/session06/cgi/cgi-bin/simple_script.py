#!C:\Python27\python_unrecognized.exe

import os
import cgitb

#cgitb.enable()

print "Junk-header-does-not-exist: foo/bar"
print
print "First line of content"
print "Content-Type: text/html<p>"
print
print "I am a <b>python</b> <i>script</i>"
print "I am " + str(os.environ.keys())
print "I am " + str(os.environ["USERPROFILE"])
1/0
print "Hi there!"
print "And some more code"
#print "hello'

