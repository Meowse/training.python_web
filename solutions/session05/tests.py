import mimetypes
import socket
import unittest
import sys

CRLF = '\r\n'
KNOWN_TYPES = set(mimetypes.types_map.values())

def call_request_handler(request):
    """Helper for unit tests for the handle_request method

    Because this is a unit test helper, it does not require the server
    to be running"""
    from http_server import handle_request
    return handle_request(request, sys.stderr)

def get_response_code(response):
    return response.split(CRLF)[0].split(' ', 1)[1].strip()

def get_protocol(response):
    return response.split(CRLF)[0].split(' ', 1)[0].strip()

def parse_headers(response):
    headers = {}
    raw_headers = response.split(CRLF+CRLF, 1)[0].split(CRLF)[1:]
    for raw_header in raw_headers:
        try:
            name, value = raw_header.split(':')
            actual_name = name.strip().lower()
            headers[actual_name] = value.strip()
        except ValueError:
            print "Bad header: [" + raw_header + "] in headers [" + str(raw_headers) + "] in response [" + response + "]"
    return headers

def has_header(response, header_name):
    return header_name in parse_headers(response)

def get_header_value(response, header_name):
    return parse_headers(response)[header_name]

def get_contents(response):
    return response.split(CRLF+CRLF, 1)[1]

class SimpleSuccessfulRequestsTestCase(unittest.TestCase):
    """unit tests for simple successful requests

    the server does not need to be running"""

    def test_response_code(self):
        response = call_request_handler("GET / HTTP/1.1")
        self.assertEqual("200 OK", get_response_code(response))

    def test_response_protocol_is_http11_for_http10(self):
        response = call_request_handler("GET / HTTP/1.0")
        self.assertEqual("HTTP/1.1", get_protocol(response))

    def test_response_protocol_is_http11_for_http11(self):
        response = call_request_handler("GET / HTTP/1.1")
        self.assertEqual("HTTP/1.1", get_protocol(response))

    def test_response_has_content_type_header(self):
        response = call_request_handler("GET / HTTP/1.1")
        self.assertTrue(has_header(response, 'content-type'))

    def test_response_has_legitimate_content_type(self):
        response = call_request_handler("GET / HTTP/1.1")
        self.assertTrue(get_header_value(response, 'content-type') in KNOWN_TYPES)

class OnlyGetIsImplementedTestCase(unittest.TestCase):
    """unit tests for responding '501 Not Implemented' to all verbs other than GET"""

    def test_response_code(self):
        response = call_request_handler("POST / HTTP/1.1")
        self.assertEqual("501 Not Implemented", get_response_code(response))

    def test_response_method(self):
        response = call_request_handler("DELETE / HTTP/1.1")
        self.assertEqual('HTTP/1.1', get_protocol(response))

class RequestUriIsHandledTestCase(unittest.TestCase):
    """unit tests for responding differently based on the request URI"""

    def test_returns_text_file_under_webserver_root(self):
        response = call_request_handler("GET /test_contents/test_text_file.txt HTTP/1.1")
        self.assertEqual("text/plain", get_header_value(response, 'content-type'))
        text_file = open("webserver_root/test_contents/test_text_file.txt", "r")
        text_contents = text_file.read()
        self.assertEqual(text_contents, get_contents(response))

    def test_does_not_return_text_file_not_under_webserver_root(self):
        response = call_request_handler("GET /never_return.txt HTTP/1.1")
        self.assertEqual("404 Not Found", get_response_code(response))

    def test_does_not_return_text_file_from_parent_directory(self):
        response = call_request_handler("GET /../never_return.txt HTTP/1.1")
        self.assertEqual("404 Not Found", get_response_code(response))

    def test_returns_html_file_as_html(self):
        response = call_request_handler("GET /test_contents/test.html HTTP/1.1")
        self.assertEqual("text/html", get_header_value(response, 'content-type'))
        html_file = open("webserver_root/test_contents/test.html", "r")
        html_contents = html_file.read()
        self.assertEqual(html_contents, get_contents(response))

    def test_returns_png_as_png(self):
        response = call_request_handler("GET /test_contents/android.png HTTP/1.1")
        self.assertEqual("image/png", get_header_value(response, 'content-type'))
        image_file = open("webserver_root/test_contents/android.png", "rb")
        image_contents = image_file.read()
        self.assertEqual(image_contents, get_contents(response))
		
    def test_returns_jpeg_as_jpeg(self):
        response = call_request_handler("GET /test_contents/boomdeyada.jpg HTTP/1.1")
        self.assertEqual("image/jpeg", get_header_value(response, 'content-type'))
        image_file = open("webserver_root/test_contents/boomdeyada.jpg", "rb")
        image_contents = image_file.read()
        self.assertEqual(image_contents, get_contents(response))
		
class ParseRequestTestCase(unittest.TestCase):
    """unit tests for the parse_request method"""

    def call_function_under_test(self, request):
        """call the `parse_request` function"""
        from http_server import parse_request
        return parse_request(request)

    def test_get_method(self):
        request = "GET / HTTP/1.1\r\nHost: example.com\r\n\r\n"
        try:
            self.call_function_under_test(request)
        except (NotImplementedError, Exception), e:
            self.fail('GET method raises an error {0}'.format(str(e)))

    def test_bad_http_methods(self):
        methods = ['POST', 'PUT', 'DELETE', 'HEAD']
        request_template = "{0} / HTTP/1.1\r\nHost: example.com\r\n\r\n"
        for method in methods:
            request = request_template.format(method)
            self.assertRaises(
                NotImplementedError, self.call_function_under_test, request
            )

class HTTPServerFunctionalTestCase(unittest.TestCase):
    """functional tests of the HTTP Server

    This test case interacts with the http server, and as such requires it to
    be running in order for the tests to pass
    """

    def send_message(self, message):
        """Attempt to send a message using the client and the test buffer

        In case of a socket error, fail and report the problem
        """
        from simple_client import client
        response = ''
        try:
            response = client(message)
        except socket.error, e:
            if e.errno == 61:
                msg = "Error: {0}, is the server running?"
                self.fail(msg.format(e.strerror))
            else:
                self.fail("Unexpected Error: {0}".format(str(e)))
        return response

    def test_get_request(self):
        message = CRLF.join(['GET / HTTP/1.1', 'Host: example.com', ''])
        expected = '200 OK'
        actual = self.send_message(message)
        self.assertTrue(
            expected in actual, '"{0}" not in "{1}"'.format(expected, actual)
        )

    def test_post_request(self):
        message = CRLF.join(['POST / HTTP/1.1', 'Host: example.com', ''])
        expected = '501 Not Implemented'
        actual = self.send_message(message)
        self.assertTrue(
            expected in actual, '"{0}" not in "{1}"'.format(expected, actual)
        )


if __name__ == '__main__':
    unittest.main()
