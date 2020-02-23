# dpkg is a singleton object that allows access to pre-parsed data from the dpkg package manager

import fileparser

# TODO: Specify status file location when running from command line
filepath = 'status.real' # filepath to the /var/lib/dpkg/status file
packages_raw = fileparser.control_file_to_list(filepath)
packages = fileparser.clean_packages(packages_raw)  # remove unused fields and add reverse-dependency fields
packages = sorted(packages, key=lambda k: k['Name'])  # sort packages alphabetically
package_names = fileparser.get_package_names(packages)

# Create a set that we can reference so we don't have to iterate over the
# list of dictionaries find if a package exists
package_names_set = set(package_names)

# Finds the first package in a list of packages with the given name and returns it
def find_package(name):
    for dic in packages:
        if dic.get('Name') == name:
            return dic
