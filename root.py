from http.server import BaseHTTPRequestHandler, HTTPServer

class RedirectHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(302)
        self.send_header('Location', 'https://www.youtube.com/embed/4eZSP4uh2uI')
        self.end_headers()

    def do_HEAD(self):
        self.send_response(302)
        self.send_header('Location', 'https://www.youtube.com/embed/4eZSP4uh2uI')
        self.end_headers()

if __name__ == "__main__":
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, RedirectHandler)
    httpd.serve_forever()