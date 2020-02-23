# This is the HTTP server script for the debian-package-status project

from http.server import HTTPServer, BaseHTTPRequestHandler     # Used to create HTTP web server
import fileparser                                              # Used to parse Debian control files
import htmlbuilder                                             # Used to build HTML elements
import graph                                                   # Used to generate reverse dependencies
from os import path
import dpkg

# Convert list of package names to HTML list to use on website homepage
packages_list_HTML = htmlbuilder.list_to_html_list(dpkg.package_names,  add_hyperlink=True)
index_html = htmlbuilder.build_html_page(title = 'Debian Packages',
                                         body = packages_list_HTML,
                                         h1 = 'Debian Packages (/var/lib/dpkg/status)')


class Serv(BaseHTTPRequestHandler):

    def do_GET(self):

        page_data = None

        print(f'self.path: {self.path}')
        url_split = self.path.split('/')
        print(len(url_split))
        print(url_split)
        filename, extension = path.splitext(self.path)
        print(f'filename: {filename}')
        print(f'extension: {extension}')
        script_dir = path.dirname(__file__)
        print(f'script_dir: {script_dir}')

        # Handle requests for root page
        if self.path in ['/','/packages', '/index']:
            self.path = '/index.html'
            page_data = index_html # We are at homepage
            self.send_response(200)

        # Handle requests for css
        if extension == '.css':
            css_path = script_dir + self.path
            print(css_path)
            try:
                with open(css_path) as f:
                    self.send_response(200)                       # send_response() must be called before send_header()
                    self.send_header('Content-type', 'text/css')  # set MIME type to css
                    page_data = f.read()
                    print(page_data)


            except IOError:
                self.send_error(404)

        # TODO: http://localhost:8080/packages/whiptail-provider does not work

        # Handle requests for pages about specific dpkg packages
        if url_split[1] == 'packages' and len(url_split) > 2:
            print(f'Package page requested: {self.path}')
            print(dpkg.packages)

            # Lookup package in list of dicts
            package = next((item for item in dpkg.packages if item['Name'] == url_split[2]), None)

            if package == None: # package not found
                page_data = None
            else: # package found
                body_html = htmlbuilder.dict_to_html(package)
                page_data = htmlbuilder.build_html_page(title=package['Name'], body=body_html)
                self.send_response(200)


        # Could not find requested page
        if page_data == None:
            page_data = "404: File not found"
            self.send_response(404)

        self.end_headers()
        self.wfile.write(bytes(page_data, 'utf-8'))

# TODO: Fix multiple connection issues. Use threading!

# Start server
server_address = ('192.168.1.21', 80)
httpd = HTTPServer(server_address, Serv)
httpd.serve_forever()