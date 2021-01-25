from not_django import app
from views import urls


def wsgi_app(environ, start_response):
    response = app(environ, urls)
    start_response(response.status, response.headers)
    return response.body


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    server = make_server('', 8080, wsgi_app)
    print 'visit http://localhost:8080/'
    server.serve_forever()
