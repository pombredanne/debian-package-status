# This is the HTTP server script for the debian-package-status project

from http.server import HTTPServer, BaseHTTPRequestHandler     # Used to create HTTP web server
import fileparser                                              # Used to parse Debian control files
import htmlbuilder                                             # Used to build HTML elements
import graph                                                   # Used to generate reverse dependencies

# Initialize website
# Load and parse data that we want to serve
status_file = 'status.real' # filepath to the /var/lib/dpkg/status file
packages_raw = fileparser.control_file_to_list(status_file)
packages = fileparser.clean_packages(packages_raw)      # remove unused fields and add reverse-dependency fields
packages = sorted(packages, key=lambda k: k['Name']) # sort packages alphabetically
package_names = fileparser.get_package_names(packages)

# Convert list of package names to HTML list to use on website homepage
packages_list_HTML = htmlbuilder.list_to_html_list(package_names,  add_hyperlink=True)
index_html = htmlbuilder.build_html_page(title = 'Debian Packages',
                                         body = packages_list_HTML,
                                         h1 = 'Debian Packages (/var/lib/dpkg/status)')

page_html = None


class Serv(BaseHTTPRequestHandler):

    def do_GET(self):

        url_split = self.path.split('/')
        print(len(url_split))
        print(url_split)

        # root of website is index.html
        if self.path in ['/','/packages', '/index']:
            self.path = '/index.html'
            page_html = index_html # We are at homepage
            self.send_response(200)

        # TODO: http://localhost:8080/packages/whiptail-provider does not work
        # TODO: Only link reverse-dependencies and dependencies that exist in packages
        if url_split[1] == 'packages' and len(url_split) > 2:
            print(f'Package page requested: {self.path}')
            print(packages)

            # Lookup package in list of dicts
            package = next((item for item in packages if item['Name'] == url_split[2]), None)

            if package == None: # package not found
                page_html = None
            else: # package found
                body_html = htmlbuilder.dict_to_html(package)
                page_html = htmlbuilder.build_html_page(title=package['Name'], body=body_html)
                self.send_response(200)


        # Could not find requested page
        if page_html == None:
            page_html = "404: File not found"
            self.send_response(404)

        self.end_headers()
        self.wfile.write(bytes(page_html, 'utf-8'))



# Start server
httpd = HTTPServer(('localhost', 8080), Serv)
httpd.serve_forever()