# This module helps convert Dpkg data into HTML strings
# that can be sent by the server to clients' web browsers.

import dpkg      # Used to access pre-parsed Dpkg data

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
def list_to_html_list(package_list, add_hyperlink=True, ordered=True):

    list_html = ''

    # Don't build HTML if package_list is empty
    if package_list == {''}:
        return list_html

    for package_name in package_list:
        list_item = f'<li>{package_name}</li>'

        # Add hyperlink to list item
        # Only link reverse-dependencies and dependencies that exist in packages
        # For example: plymouth package has dependency upstart-job that isn't listed in status.real dpkg/status file
        if add_hyperlink and package_name in dpkg.Dpkg.package_names_set:
            url = f'/packages/{package_name}'
            list_item = f'<a href=\"{url}\">{list_item}</a>'

        list_html += f'\t{list_item}\n'

    if ordered:
        list_html = f'<ol>\n{list_html}</ol>'
    else:
        list_html = f'<ul>\n{list_html}</ul>'

    return list_html


# Converts a python dictionary to an HTML webpage
def dict_to_html(dict):

    # Pull data from dictionary
    header = dict.get('Name', '')
    description = dict.get('Description', '')
    description = description.replace('\n', '<br />') # Replace newlines with HTML line break
    dependencies = dict.get('Dependencies','')
    reverse_dependencies = dict.get('Reverse-Dependencies','')
    dependencies_html = list_to_html_list(dependencies, ordered=False)
    reverse_dependencies_html = list_to_html_list(reverse_dependencies, ordered=False)

    # If no dependency or reverse dependencies exist, then display 'None' instead of whitespace.
    if reverse_dependencies == '':
        reverse_dependencies_html = 'None'
    if dependencies_html == '':
        dependencies_html = 'None'

    # Add HTML headers to data
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


# Unit Tests (executed when script is run stand-alone)
if (__name__ == '__main__'):

    dpkg.Dpkg() # initialize Dpkg

    # Convert list of package names to HTML list to use on website homepage
    packages_list_HTML = list_to_html_list(dpkg.Dpkg.package_names, add_hyperlink=True)
    print(packages_list_HTML)

    for package in dpkg.Dpkg.packages:
        package_html = dict_to_html(package)
        print(package_html)

    zliblg = dpkg.Dpkg.get_package_by_name('zlib1g')
    zliblg_html = dict_to_html(zliblg)
    print(zliblg_html)
