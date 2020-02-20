# This is the HTTP server script for the debian-package-status project

from http.server import HTTPServer, BaseHTTPRequestHandler     # Used to create HTTP web server
import fileparser                                              # Used to parse Debian control files
import htmlbuilder                                             # Used to build HTML elements


# Initialize website
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

page_HTML = None


class Serv(BaseHTTPRequestHandler):

    def do_GET(self):

        url_split = self.path.split('/')

        # root of website is index.html
        if self.path == '/':
            self.path = '/index.html'
            page_HTML = index_HTML # We are at homepage
            self.send_response(200)

        # TODO: Generate HTML page for given package
        if url_split[1] == 'packages':
            print(f'Package page requested: {self.path}')

            # Lookup package in list of dicts
            package = next((item for item in packages if item['Package'] == url_split[2]), None)

            if package == None: # package not found
                page_HTML = None
            else: # package found
                print(package)
                page_HTML = package # TODO: Convert dictionary to HTML table
                self.send_response(200)


        # Could not find requested page
        if page_HTML == None:
            page_HTML = "404: File not found"
            self.send_response(404)

        self.end_headers()
        self.wfile.write(bytes(page_HTML, 'utf-8'))



# Start server
httpd = HTTPServer(('localhost', 8080), Serv)
httpd.serve_forever()