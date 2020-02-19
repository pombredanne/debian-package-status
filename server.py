# This is the HTTP server script for the debian-package-status project

from http.server import HTTPServer, BaseHTTPRequestHandler     # Used to create HTTP web server
from urllib.parse import urlparse                              # Used to parse url's
import fileparser
import htmlbuilder

# Load and parse data that we want to serve
status_file = 'status.real' # filepath to the /var/lib/dpkg/status file
packages = fileparser.control_file_to_list(status_file)

# Sort packages alphabetically
packages_sorted = sorted(packages, key=lambda k: k['Package'])

# Extract package names to list
package_names = []
for dict in packages_sorted:
    package_names.append(dict['Package'])

# Convert list to HTML for index page
packages_list_HTML = htmlbuilder.list_to_HTML_list(package_names, link = True)
index_HTML = htmlbuilder.buildHTMLPage(title = 'Debian Package Status', body = packages_list_HTML)

page_HTML = ''

class Serv(BaseHTTPRequestHandler):

    def do_GET(self):
        # root of website is index.html
        if self.path == '/':
            self.path = '/index.html'
            page_HTML = index_HTML # We are at homepage

        # TODO: Generate HTML page for given package
        if self.path == '/packages':
            print("Package page requested.")
            pass

        # Create index.html by reading in status.real
        # status.real is an example /var/lib/dpkg/status file from Github: https://gist.github.com/lauripiispanen/29735158335170c27297422a22b48caa

        try: # Build HTML to serve
            print(page_HTML)
            self.send_response(200)
        except:
            page_HTML = "File not found"
            self.send_response(404)

        self.end_headers()
        self.wfile.write(bytes(page_HTML, 'utf-8'))



# Start server
httpd = HTTPServer(('localhost', 8080), Serv)
httpd.serve_forever()