# This function builds a complete HTML Page using the provided title and body parameters
# The title and body parameters should be appropriately formatted HTML strings
def buildHTMLPage(title='', body=''):

    pageHTML = '<!DOCTYPE html><html>\n'
    headHTML = '<head>\n\t<title>' + str(title) + '</title>\n<meta charset="UTF-8"></head>\n'
    bodyHTML = '<body>\n' + str(body) + '\n</body>'

    pageHTML = pageHTML + headHTML + bodyHTML + '\n</html>' # finalize HTML

    return pageHTML

# Converts a list of strings to an HTML list
# TODO: If using package name in url, test that package adheres to url syntax.
def list_to_HTML_list(list, link=True):

    list_HTML = ''
    for str in list:
        list_item = '<li>' + str + '</li>'

        # Add hyperlink to list item
        if link == True:
            url = '/packages/' + str
            list_item = '<a href=\"' + url + '\">' + list_item + '</a>'

        list_HTML += '\t' + list_item + '\n'

    if link == True:
        list_HTML = '<ol>\n' + list_HTML + '</ol>'

    return(list_HTML)


# TODO: Converts a python dictionary to HTML
def dict_to_HTML(dict):
    str_HTML = ''
    header = dict.get('Package', '')
    description = dict.get('Description', '')
    dependencies = dict.get('Depends','').split(', ')

    # Remove version from dependencies
    temp_dependencies = []
    for item in dependencies:
        dependency = item.split(' ')[0]
        temp_dependencies.append(dependency)
    dependencies = temp_dependencies

    print(f'Header: {header}')
    #print(f'Description: {description}')
    print(f'Dependencies: {dependencies}')

    # TODO: Create graph of reverse packages


# TODO Unit Tests (executed when script is run stand-alone)
if (__name__ == '__main__'):
    import fileparser
    status_file = 'status.real' # filepath to the /var/lib/dpkg/status file
    packages = fileparser.control_file_to_list(status_file)

    # Sort packages alphabetically
    packages_sorted = sorted(packages, key=lambda k: k['Package'])


    # Extract package names to list
    package_names = []
    for dic in packages_sorted:
        package_names.append(dic['Package'])
        dict_to_HTML(dic)