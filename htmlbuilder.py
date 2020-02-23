import fileparser

# This function builds a complete HTML Page using the provided title and body parameters
# The title and body parameters should be appropriately formatted HTML strings
def build_html_page(title='', body='', css_path='/css/styles.css'):

    pageHTML = '<!DOCTYPE html><html>\n'
    headHTML = '<head>\n\t' \
               f'<title>{title}</title>\n' \
               f'<link rel=\"stylesheet\" href=\"{css_path}\">' \
               '<meta charset="UTF-8"></head>\n'
    bodyHTML = f'<body>\n{str(body)}\n</body>'

    pageHTML = pageHTML + headHTML + bodyHTML + '\n</html>' # finalize HTML

    return pageHTML

def build_html_page(title='', body='', h1='', css_path='/css/styles.css'):

    pageHTML = '<!DOCTYPE html><html>\n'
    headHTML = '<head>\n\t' \
               f'<title>{title}</title>\n' \
               f'<link rel=\"stylesheet\" href=\"{css_path}\">' \
               '<meta charset="UTF-8"></head>\n'
    bodyHTML = f'<body>\n<h1>{h1}</h1>{str(body)}\n</body>'

    pageHTML = pageHTML + headHTML + bodyHTML + '\n</html>' # finalize HTML

    return pageHTML

# Converts a list of strings to an HTML list
# TODO: If using package name in url, test that package adheres to url syntax.
def list_to_html_list(package_list, add_hyperlink=True, ordered=True):

    list_html = ''

    # Don't build HTML if package_list is empty
    if package_list == {''}:
        return list_html

    for package_name in package_list:
        list_item = f'<li>{package_name}</li>'

        # Add hyperlink to list item
        if add_hyperlink:
            url = f'/packages/{package_name}'
            list_item = f'<a href=\"{url}\">{list_item}</a>'

        list_html += f'\t{list_item}\n'

    if ordered:
        list_html = f'<ol>\n{list_html}</ol>'
    else:
        list_html = f'<ul>\n{list_html}</ul>'

    return list_html


# Converts a python dictionary to HTML webpage
def dict_to_html(dict):

    # Pull data from dictionary
    header = dict.get('Name', '')
    description = dict.get('Description', '')
    description = description.replace('\n', '<br />') # Replace newlines with HTML line break
    dependencies = dict.get('Dependencies','')
    reverse_dependencies = dict.get('Reverse-Dependencies','')
    dependencies_html = list_to_html_list(dependencies, ordered=False)
    reverse_dependencies_html = list_to_html_list(reverse_dependencies, ordered=False)

    # Build HTML page from data
    # TODO: Some dependencies aren't install on the system, so only add links to packages that exist

    # Add html headers to data
    home_link_html = f'<a href=\"/\"><h1>Debian Packages (/var/lib/dpkg/status)</h1></a>' # Create link to homepage
    header_html = f'<h2>Package: {header}</h2>'
    description_html = '<h2>Description:</h2>' \
                       f'<p>{description}</p>'
    dependencies_html = '<h2>Dependencies:</h2>' \
                        f'{dependencies_html}'
    reverse_dependencies_html = '<h2>Reverse-Dependencies:</h2>' \
                        f'{reverse_dependencies_html}'

    body_html = home_link_html + header_html + description_html + dependencies_html + reverse_dependencies_html

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
    print(packages_list_HTML)

    for package in packages:
        package_html = dict_to_html(package)
        #print(package_html)

    zliblg = fileparser.find_package(packages, 'zlib1g')
    zliblg_html = dict_to_html(zliblg)
    #print(zliblg_html)
