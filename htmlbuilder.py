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
            url = '/packages?name=' + str
            list_item = '<a href=\"' + url + '\">' + list_item + '</a>'

        list_HTML += '\t' + list_item + '\n'

    if link == True:
        list_HTML = '<ol>\n' + list_HTML + '</ol>'

    return(list_HTML)


# TODO: Converts a python dictionary to an HTML table
def dict_to_HTML_table(dict):
    pass