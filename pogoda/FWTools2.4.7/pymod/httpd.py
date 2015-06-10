#!/usr/bin/env python

import sys
import CGIHTTPServer
import BaseHTTPServer

if __name__ == '__main__':

    if sys.argv[1:]:
        port = int(sys.argv[1])
    else:
        port = 80
    server_address = ('', port)

    handler = CGIHTTPServer.CGIHTTPRequestHandler
    handler.cgi_directories.append( '/bin' )
    httpd = BaseHTTPServer.HTTPServer(server_address,
                                      CGIHTTPServer.CGIHTTPRequestHandler)

    sa = httpd.socket.getsockname()
    print "Serving HTTP on", sa[0], "port", sa[1], "..."
    httpd.serve_forever()
