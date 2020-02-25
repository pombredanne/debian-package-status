# This server module is the main module for the debian-package-status project.
# It calls the other modules in the package and serves the returned data as a website.

from http.server import HTTPServer, BaseHTTPRequestHandler     # Used to create HTTP web server
from socketserver import ThreadingMixIn
import htmlbuilder                                             # Used to build HTML elements
from os import path
import dpkg                                                    # Used to access pre-parsed file data
import argparse                                                # Used to parse command line arguments


def main():
    # TODO: Specify status file location when running from command line
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--ipaddress', help='IP address of the server (localhost by default).')
    parser.add_argument('-p', '--port', help='Port that server should serve (80 by default).')
    parser.add_argument('-f', '--file', help='Filepath to dpkg status file (usually /var/lib/dpkg/status). By default status.real is used')
    args = parser.parse_args()

    ip_address = 'localhost'
    port = 80
    dpkg_status_filepath = 'status.real'

    if args.ipaddress is not None:
        ip_address = args.ipaddress
    if args.port is not None:
        port = args.port
    if args.file is not None:
        dpkg_status_filepath = args.file

    print(f'ip_address: {ip_address}')
    print(f'port: {port}')
    print(f'dpkg_status_filepath: {dpkg_status_filepath}')


    package_manager = dpkg.Dpkg(dpkg_status_filepath) # Initialize data with given file

    # Start server
    #server_address = ('192.168.56.1', 80) # Woody's Wifi: '192.168.6.21' LAN: 192.168.56.1
    server_address = (ip_address, port)
    #httpd = HTTPServer(server_address, Serv) # Single Threaded Server
    httpd = ThreadedHTTPServer(server_address, Serv) # Multi Threaded Server
    httpd.serve_forever()

class Serv(BaseHTTPRequestHandler):

    def do_GET(self):

        page_data = None

        #print(f'self.path: {self.path}')
        url_split = self.path.split('/')
        #print(len(url_split))
        #print(url_split)
        filename, extension = path.splitext(self.path)
        #print(f'filename: {filename}')
        #print(f'extension: {extension}')
        script_dir = path.dirname(__file__)
        #print(f'script_dir: {script_dir}')

        # Handle requests for root page
        if self.path in ['/','/packages', '/index']:
            self.path = '/index.html'
            page_data = dpkg.Dpkg.index_html # We are at homepage
            print(f'Sorted packages: {dpkg.Dpkg.package_names}')
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
            print(dpkg.Dpkg.packages)

            # Lookup package in list of dicts
            package = next((item for item in dpkg.Dpkg.packages if item['Name'] == url_split[2]), None)

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


# Use threading to handle simultaneous requests
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread"""


if __name__ == "__main__":
    main() # get command line arguments
