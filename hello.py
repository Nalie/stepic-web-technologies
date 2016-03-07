# import urlparse
def app(environ, start_response):
    # parameters = urlparse.parse_qs(environ.get('QUERY_STRING'), 1)

    body = environ.get('QUERY_STRING').replace('&', '\r\n')
    start_response('200 OK', [('Content-type', 'text/plain')])
    return [body]