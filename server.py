# Server file for debian-package-status
from http.server import HTTPServer, BaseHTTPRequestHandler
import fileparser
import htmlbuilder

# Load and parse data that we want to serve
status_file = 'status.real' # filepath to the /var/lib/dpkg/status file
packages = fileparser.control_file_to_list(status_file)

# sort packages alphabetically
packages_sorted = sorted(packages, key=lambda k: k['Package'])

for x in packages_sorted:
    print(x)

packages_list_HTML = htmlbuilder.list_dict_to_HTML_list(packages_sorted, 'Package')
page_HTML = htmlbuilder.buildHTMLPage('Debian Package Status', packages_list_HTML)
print(page_HTML)

class Serv(BaseHTTPRequestHandler):

    def do_GET(self):
        # root of website is index.html
        if self.path == '/':
            self.path = '/index.html'

        # TODO: Generate HTML page for given package
        if self.path == '/packages':
            pass

        # Create index.html by reading in status.real
        # status.real is an example /var/lib/dpkg/status file from Github: https://gist.github.com/lauripiispanen/29735158335170c27297422a22b48caa

        try: # Build HTML to serve

            #pageHTML = open('status.real', 'r').read()

            print(page_HTML)
            self.send_response(200)
        except:
            f = "File not found"
            self.send_response(404)

        self.end_headers()
        self.wfile.write(bytes(page_HTML, 'utf-8'))



# Start server
httpd = HTTPServer(('localhost', 8080), Serv)
httpd.serve_forever()