from argparse import ArgumentParser
from http.server import HTTPServer, BaseHTTPRequestHandler
from os import system


def make_output(text:str,  name:str)->str:
    return "<!DOCTYPE html><html><head><title>"+name+"</title><style>html{font-family: sans-serif;font-weight: 400;font-size: 18pt;line-height: 1.5;color: #c3c3c3;background-color: #121212;}body{margin:auto;max-width:66ch;padding:3ch;}br{content: '';margin: 2em;display: block;font-size: 24%;}</style></head><body>"+text+"</body></html>"

def read_file(name:str)->str:
    with open(name,"r") as file:
        return file.read().replace("\n","<br>")

class S(BaseHTTPRequestHandler):
    html = bytes()

    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write(self.html)

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        self._set_headers()


def run(port:int)->None:
    addr = ("localhost",port)
    httpd = HTTPServer(addr,S)
    httpd.serve_forever()

if __name__ == "__main__":
    parser = ArgumentParser(prog="txt to html server", description="reads a plain text file and inserts it into as html template, serves it on localhost and opens it in the defualt web-browser")
    parser.add_argument("file",help="the file to be run")
    parser.add_argument("-p","--port",default=8001,type=int,help="The port to use. Default is 8001.")
    args = parser.parse_args()
    S.html = make_output(read_file(args.file),args.file).encode('ascii', 'xmlcharrefreplace')
    system(f"xdg-open http://localhost:{args.port}")
    run(args.port)
