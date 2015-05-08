import socket
import sys
import posixpath
import urllib
import os
import mimetypes

def server(log_buffer=sys.stderr):
    address = ('127.0.0.1', 10000)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print >>log_buffer, "making a server on {0}:{1}".format(*address)
    sock.bind(address)
    sock.listen(1)

    try:
        while True:
            print >>log_buffer, 'waiting for a connection'
            conn, addr = sock.accept() # blocking
            try:
                print >>log_buffer, 'connection - {0}:{1}'.format(*addr)
                conn.sendall(handle_request(get_request(conn), log_buffer))
            except Exception, e:
                print >>log_buffer, 'Returning 500 Internal Server Error for internal error ' + str(e)
                conn.sendall(make_response("500 Internal Server Error"))
            finally:
                conn.close()

    except KeyboardInterrupt:
        sock.close()
        return

def handle_request(request, log_buffer):
    """external entry point for unit tests; processes a request and returns
    the appropriate response"""
    print >>log_buffer, "Request is: " + request

    try:
        uri = parse_request(request)
    except NotImplementedError:
        print >>log_buffer, "Return '501 Not Implemented' error"
        return make_response("501 Not Implemented")
    else:
        try:
            content_type, content = resolve_uri(uri, log_buffer)
        except IOError:
            print >>log_buffer, "Return '404 Not Found' error"
            return make_response("404 Not Found")

    print >>log_buffer, 'sending response'

    return response_ok(content_type, content)

def resolve_uri(uri, log_buffer):
    """Return the file contents and appropriate mime type for the file at path 'uri' under
    webserver_root"""
    if uri == "/":
        return ("text/plain", "this is a pretty minimal response")
    path = translate_path(uri)
    content_type, _ = mimetypes.guess_type(uri)
    if content_type.startswith("text/"):
        mode = "r"
    else:
        mode = "rb"

    print >>log_buffer, "Serving URI [" + uri + "] of type [" + content_type + "] (" + mode + ") as path [" + path + "]"

    resource = open(path, mode)
    contents = resource.read()
    return (content_type, contents)
	
def translate_path(path):
    """Translate a /-separated PATH to the local filename syntax.

    Components that mean special things to the local file system
    (e.g. drive or directory names) are ignored.  (XXX They should
    probably be diagnosed.)

    """
    path = posixpath.normpath(urllib.unquote(path))
    words = path.split('/')
    words = filter(None, words)
    path = os.path.join(os.getcwd(), "webserver_root")
    for word in words:
        drive, word = os.path.splitdrive(word)
        head, word = os.path.split(word)
        if word in (os.curdir, os.pardir): continue
        path = os.path.join(path, word)
    return path

def get_request(conn):
    message_chunks = []
    while True:
        chunk = conn.recv(1024)
        message_chunks.append(chunk)
        if len(chunk) < 1024 or not chunk:
            message = "".join(message_chunks)
            return message

def parse_request(request):
    first_line = request.split("\r\n", 1)[0]
    method, uri, protocol = first_line.split()
    if method != "GET":
        raise NotImplementedError("We only accept GET")
    print >>sys.stderr, 'request is okay'
    return uri

def make_response(response_code="200 OK", headers=None, body=""):
    if not headers:
	    headers = []
    resp = []
    resp.append("HTTP/1.1 " + response_code)
    for header in headers:
        resp.append(header)
    resp.append("")
    if body:
        resp.append(body)
    return "\r\n".join(resp)

def response_ok(content_type="text/plain", content="this is a pretty minimal response"):
    """returns a basic HTTP response"""
    resp = []
    resp.append("HTTP/1.1 200 OK")
    resp.append("Content-Type: " + content_type)
    resp.append("")
    if content:
        resp.append(content)
    return "\r\n".join(resp)

if __name__ == '__main__':
    server()
    sys.exit(0)
