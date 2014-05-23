# coding=utf-8
import os
import sys

from cgi import parse_qs

# activate virtualenv
activate_this = '/home/alex/venv/shop/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

# add the egg cache
os.environ['PYTHON_EGG_CACHE'] = os.path.join(os.path.dirname(__file__), '.python-egg')

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(__file__) + '/backend')

import backend.views
from views.urls import URL_MAP


def application(environ, start_response):
    status = "200 OK"
    request_url = environ['REQUEST_URI']
    request_method = environ['REQUEST_METHOD']
    response_body = "RESPONSE"
    for item in URL_MAP:
        if item[0] == request_url and item[2] == request_method:
            print request_url
            print request_method
            method = getattr(backend.views, item[1])
            print
            method
            request_body = environ['wsgi.input'].read(int(environ.get('CONTENT_LENGTH', 0)))
            inp = parse_qs(request_body)
            response_body = method(inp=inp)
            status = "200 OK"
            break
        else:
            response_body = "ERROR"
            status = "404 NOT FOUND"


    #response_body = ['%s: %s' % (key, value)
    #                for key, value in sorted(environ.items())]
    #response_body = '\n'.join(response_body)
    response_headers = [('Content-Type', 'text/html'),
                        ('Content-Length', str(len(response_body))),
                        ('Status', status)]
    start_response(status, response_headers)
    return [response_body]
