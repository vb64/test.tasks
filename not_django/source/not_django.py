import os
import re


class Request(object):
    def __init__(self, environ):
        self.environ = environ
        self.params = None


class Response(object):
    def __init__(self, status='200 OK', headers=(('Content-type', 'text/html'),), body=''):
        self.status = status
        self.headers = list(headers)
        self.body = body


class Response400(Response):
    def __init__(self):
        super(Response400, self).__init__(status='400 Bad Request')


class Response404(Response):
    def __init__(self):
        super(Response404, self).__init__(status='404 Not Found')


def render(template_file):
    return open(os.path.join(os.path.dirname(__file__), 'templates', template_file))


def bad_requst(request):
    return Response400()


def not_found(request):
    return Response404()


def find_match(path, dynamic_urls):
    for mask, handler in dynamic_urls:
        match = re.findall(mask, path)
        if match:
            return (handler, [int(x) for x in path.split('/') if x.isdigit()])

    return (not_found, None)


def app(environ, urls):
    handler = bad_requst
    request = Request(environ)

    method = urls.get(environ['REQUEST_METHOD'], None)
    path = environ['PATH_INFO']

    if method:
        handler = method.get('static', {}).get(path, None)
        if handler is None:
            handler = not_found
            dynamic_urls = method.get('dynamic', [])
            if dynamic_urls:
                handler, params = find_match(path, dynamic_urls)
                request.params = params

    return handler(request)
