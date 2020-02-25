# This module handles the file i/o and conversion of the dpkg/status file
# into Python data structures.

import graph

# Convert Debian control file to a list of dictionaries
# where each dictionary in the list is a Debian control file paragraph
def control_file_to_list(filepath):

    paragraph_list = [] # store a list of paragraphs

    # open file and process each line
    with open(filepath, encoding='utf-8') as f:
        paragraph = {} # Treat each paragraph as a Python dictionary
        key = ''

        for line in f:

            # detect end of paragraph
            if line == '\n':
                paragraph_list.append(paragraph)  # append paragraph to list
                paragraph = {}  # reset current paragraph
                continue

            # Multiline field exists if first character in line is a space or tab character
            # Append line to the most recently added field in the dictionary
            if line[0] == ' ' or line[0] == '\t':
                paragraph[key] = paragraph[key] + line
                continue

            # New field in paragraph exists if we have arrived here
            key_value_list = line.split(':', 1) # split each line by first occurring ':'
            key = key_value_list[0]
            value = key_value_list[1].strip()   # remove leading whitespace from value
            paragraph[key] = value              # add key-value pair to current paragraph dictonary

    return(paragraph_list)


# Remove unnecessary fields from list of packages and add reverse-dependencies field
def clean_packages(packages_raw):

    # Get reverse dependencies for each package
    dependencies = graph.list_of_dicts_to_graph(packages_raw, remove_version_number=True)
    reverse_dependencies = graph.invert_graph(dependencies)

    # Clean up package data so that it only contains fields of interest
    packages = []
    package_names = []
    for dic in packages_raw:
        package_name = dic.get('Package', '')
        package_description = dic.get('Description', '')
        package_dependencies = dependencies.get(package_name, '')
        package_reverse_dependencies = reverse_dependencies.get(package_name, '')

        if package_name == '':
            raise Exception('Could not find package in dictionary.')

        packages.append({'Name': package_name,
                         'Description': package_description,
                         'Dependencies': package_dependencies,
                         'Reverse-Dependencies': package_reverse_dependencies})

        package_names.append(package_name)

    return packages



