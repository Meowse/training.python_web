import re

from bookdb import BookDB

DB = BookDB()


def book(book_id):
    #return "<h1>a book with id %s</h1>" % book_id
    #return DB.title_info(book_id)
    page = """
<h1>{title}</h1>
<table>
    <tr><th>Author</th><td>{author}</td></tr>
    <tr><th>Publisher</th><td>{publisher}</td></tr>
    <tr><th>ISBN</th><td>{isbn}</td></tr>
</table>
<a href="/">Back to the list</a>
"""
    book = DB.title_info(book_id)
    if book is None:
        raise NameError
    return page.format(**book)

def books():
    all_books = DB.titles()
    body = ['<h1>My Bookshelf</h1>', '<ul>']
    item_template = '<li><a href="/book/{id}">{title}</a></li>'
    for book in all_books:
        body.append(item_template.format(**book))
    body.append('</ul>')
    return '\n'.join(body)
    #return "<h1>a list of books</h1>"
#    result = []
    #for (key, value) in DB.titles():
        #result.append(str(key) + " " + str(value))
    #return result


def application(environ, start_response):
    headers = [('Content-type', 'text/html')]
    uri = environ.get("PATH_INFO", "No path provided")
    if uri == "/":
        start_response("200 OK", headers)
        return books()
    elif "/book/" in uri:
        start_response("200 OK", headers)
        book_id = uri.split('/')[2];
        return book(book_id)
    else:
        start_response("404 Not Found", headers)
        return []


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
