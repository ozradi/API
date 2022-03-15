# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time

hostName = "localhost"
serverPort = 1234
CONTENT_ENCODING = "utf-8"
HTML_TAG = "<html>"
HTML_CLOSE_TAG = "</html>"
HEAD_TAG = "<head>"
HEAD_CLOSE_TAG = "</head>"
TITLE_TAG = "<title>"
TITLE_CLOSE_TAG = "</title>"
BODY_TAG = "<body>"
BODY_CLOSE_TAG = "</body>"
P_TAG = "<p>"
P_CLOSE_TAG = "</p>"


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        headline = HTML_TAG + HEAD_TAG + TITLE_TAG + "Filtered Hackernews" + TITLE_CLOSE_TAG + HEAD_CLOSE_TAG
        self.wfile.write(bytes(headline, CONTENT_ENCODING))
        self.wfile.write(bytes(BODY_TAG, CONTENT_ENCODING))
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, CONTENT_ENCODING))
        self.wfile.write(bytes("<p>This is an example web server.</p>", CONTENT_ENCODING))
        self.wfile.write(bytes(BODY_CLOSE_TAG + HTML_CLOSE_TAG, CONTENT_ENCODING))

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
