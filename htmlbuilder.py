import fileparser

# This function builds a complete HTML Page using the provided title and body parameters
# The title and body parameters should be appropriately formatted HTML strings
def build_html_page(title='', body=''):

    pageHTML = '<!DOCTYPE html><html>\n'
    headHTML = '<head>\n\t<title>' + str(title) + '</title>\n<meta charset="UTF-8"></head>\n'
    bodyHTML = '<body>\n' + str(body) + '\n</body>'

    pageHTML = pageHTML + headHTML + bodyHTML + '\n</html>' # finalize HTML

    return pageHTML

def build_html_page(title='', body='', h1=''):

    pageHTML = '<!DOCTYPE html><html>\n'
    headHTML = '<head>\n\t<title>' + str(title) + '</title>\n<meta charset="UTF-8"></head>\n'
    bodyHTML = '<body>\n' + '<h1>' + h1 + '</h1>' + str(body) + '\n</body>'

    pageHTML = pageHTML + headHTML + bodyHTML + '\n</html>' # finalize HTML

    return pageHTML

# Converts a list of strings to an HTML list
# TODO: If using package name in url, test that package adheres to url syntax.
def list_to_html_list(package_list, add_hyperlink=True, ordered=True):

    list_html = ''

    # Don't build HTML if package_list is empty
    if package_list == {''}:
        return list_html

    for str in package_list:
        list_item = '<li>' + str + '</li>'

        # Add hyperlink to list item
        if add_hyperlink:
            url = '/packages/' + str
            list_item = '<a href=\"' + url + '\">' + list_item + '</a>'

        list_html += '\t' + list_item + '\n'

    if ordered:
        list_html = '<ol>\n' + list_html + '</ol>'
    else:
        list_html = '<ul>\n' + list_html + '</ul>'

    return list_html


# Converts a python dictionary to HTML webpage
def dict_to_html(dict):

    # Pull data from dictionary
    header = dict.get('Name', '')
    description = dict.get('Description', '') # TODO: Convert \n to <br> for newlines
    dependencies = dict.get('Dependencies','')
    reverse_dependencies = dict.get('Reverse-Dependencies','')

    # Build HTML page from data
    header_html = '<h1>Package: {}</h1>'.format(header)
    description_html = '<h2>Description:</h2>' \
                       '<p>{}</p>'.format(description)
    dependencies_html = '<h2>Dependencies:</h2>' \
                        '{}'.format(list_to_html_list(dependencies, ordered=False))
    reverse_dependencies_html = '<h2>Reverse-Dependencies:</h2>' \
                        '{}'.format(list_to_html_list(reverse_dependencies, ordered=False))

    body_html = header_html + description_html + dependencies_html + reverse_dependencies_html

    return body_html


# TODO Unit Tests (executed when script is run stand-alone)
if (__name__ == '__main__'):
    # Initialize website
    # Load and parse data that we want to serve
    status_file = 'status.real'  # filepath to the /var/lib/dpkg/status file
    packages_raw = fileparser.control_file_to_list(status_file)
    packages = fileparser.clean_packages(packages_raw)    # remove unused fields and add reverse-dependency fields
    packages = sorted(packages, key=lambda k: k['Name'])  # sort packages alphabetically
    package_names = fileparser.get_package_names(packages)

    # Convert list of package names to HTML list to use on website homepage
    packages_list_HTML = list_to_html_list(package_names, add_hyperlink=True)
    #print(packages_list_HTML)

    for package in packages:
        package_html = dict_to_html(package)
        #print(package_html)

    zliblg = fileparser.find_package(packages, 'zlib1g')
    zliblg_html = dict_to_html(zliblg)
    print(zliblg_html)
