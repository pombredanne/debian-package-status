# This function builds a complete HTML Page using the provided title and body parameters
# The title and body parameters should be appropriately formatted HTML strings
def buildHTMLPage(title='', body=''):

    pageHTML = '<!DOCTYPE html><html>\n'
    headHTML = '<head>\n\t<title>' + str(title) + '</title>\n<meta charset="UTF-8"></head>\n'
    bodyHTML = '<body>\n' + str(body) + '\n</body>'

    pageHTML = pageHTML + headHTML + bodyHTML + '\n</html>' # finalize HTML

    return pageHTML

# Converts a list of dicts to an HTML list for a given key
# TODO: Make hyperlinks to descriptions in lists
def list_dict_to_HTML_list(list_of_dicts, key):
    strHTML = '<ol>\n'
    for dict in list_of_dicts:
        item = '\t<li>' + dict[key] + '</li>\n'
        strHTML += item
    strHTML += '</ol>'

    return(strHTML)