# This server module is the main module for the debian-package-status project.
# It implements an HTTP server that hosts data from a dpkg/status file.

from http.server import HTTPServer, BaseHTTPRequestHandler  # Used to create HTTP web server
from socketserver import ThreadingMixIn                     # Used to extend web server to handle multithreaded requests
import argparse                                             # Used to parse command line arguments
import os                                                   # Used to get filepath information
import dpkg                                                 # Used to access pre-parsed file data
import htmlbuilder                                          # Used to build HTML elements
import sys                                                  # Used to handle keyboard interrupts

def main():

    # Get arguments from command line
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--ipaddress',
                        help='IP address of the server (localhost by default).')
    parser.add_argument('-p', '--port', type=int,
                        help='Port that server should serve (80 by default).')
    parser.add_argument('-f', '--file',
                        help='Filepath to dpkg status file (usually /var/lib/dpkg/status). '
                             'By default status.real is used.')
    args = parser.parse_args()

    # Default parameters
    ip_address = 'localhost'
    port = 80
    dpkg_status_filepath = 'status.real'

    if args.ipaddress is not None:
        ip_address = args.ipaddress
    if args.port is not None:
        port = args.port
    if args.file is not None:
        dpkg_status_filepath = args.file

    print('Initializing web server with the following parameters:')
    print(f'ip_address: {ip_address}')
    print(f'port: {port}')
    print(f'dpkg_status_filepath: {dpkg_status_filepath}')

    dpkg.Dpkg(dpkg_status_filepath) # Initialize data with given file

    # Start server
    server_address = (ip_address, port)
    httpd = ThreadedHTTPServer(server_address, Serv) # Multi Threaded Server
    httpd.serve_forever()

class Serv(BaseHTTPRequestHandler):

    def do_GET(self):

        page_data = None # Initialize response string

        # Parse URL to know what is being requested
        url_split = self.path.split('/')
        filename, extension = os.path.splitext(self.path)
        script_dir = os.path.dirname(__file__) # Get absolute directory where this server is being executed.

        # Handle requests for root page
        if self.path in ['/','/packages', '/index']:
            self.path = '/index.html'
            page_data = dpkg.Dpkg.index_html # We are at homepage
            self.send_response(200)


        # Handle requests for css
        if extension == '.css':
            css_path = 'css/styles.css'
            try:
                with open(css_path) as f:
                    self.send_response(200)                       # send_response() must be called before send_header()
                    self.send_header('Content-type', 'text/css')  # set MIME type to css
                    page_data = f.read()

            except IOError:
                self.send_error(404)


        # Handle requests for webpages about specific dpkg packages
        if url_split[1] == 'packages' and len(url_split) > 2:

            # See if requested package exists to serve
            package_name = url_split[2]

            if package_name not in dpkg.Dpkg.package_names_set: # package not found
                page_data = None
            else: # package found
                package = dpkg.Dpkg.get_package_by_name(package_name)
                body_html = htmlbuilder.dict_to_html(package)
                page_data = htmlbuilder.build_html_page(title=package['Name'], body=body_html)
                self.send_response(200)


        # Could not process request
        if page_data == None:
            page_data = "404: File not found"
            self.send_response(404)

        self.end_headers()
        self.wfile.write(bytes(page_data, 'utf-8'))


# Use threading to handle simultaneous requests
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread"""


if __name__ == "__main__":
    try:
        main() # get command line arguments
    except KeyboardInterrupt: # Gracefully exit program when keyboard interrupt is given (Ctrl-C)
        print('Server interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

