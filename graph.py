# Package dependencies can be viewed as a graph
# This module implements useful graph functions

# Convert list of dictionaries to graph
def list_of_dicts_to_graph(list_of_dicts):
    graph = {} # dictionary where key is a vertex, values are adjacent vertices

    for dic in list_of_dicts:
        package_name = dic.get('Package', '')
        dependencies = dic.get('Depends','').split(', ')

        # Remove version from dependencies
        # Assumes version is given after package name, separated by a single space
        temp_dependencies = []
        for item in dependencies:
            dependency = item.split(' ')[0]
            temp_dependencies.append(dependency)
        dependencies = temp_dependencies
        dependencies = set(dependencies) # Treat dependencies as unique

        graph[package_name] = dependencies

    return(graph)

# Invert edge direction on a provided graph, where edges are one-directional
# Graph is a dictionary where a key is a package name, and value is a set of dependencies
def invert_graph(graph):
    inverted_graph = {}

    # Iterate over all packages
    for package_name in graph:
        # Get dependencies
        dependencies = graph.get(package_name, '')
        # Iterate over all dependencies of the current package
        for dependency in dependencies:
            if inverted_graph.get(dependency, None) == None: # dependency does not exist in inverted_graph
                inverted_graph[dependency] = {package_name} # add new set
            else: # Dependency exists in inverted_graph, add package to set
                inverted_graph[dependency].add(package_name)

    return(inverted_graph)

# TODO Unit Tests (executed when script is run stand-alone)
if (__name__ == '__main__'):
    import fileparser
    status_file = 'status.real'  # filepath to the /var/lib/dpkg/status file
    packages = fileparser.control_file_to_list(status_file)

    dependency_graph = list_of_dicts_to_graph(packages)
    reverse_dependency_graph = invert_graph(dependency_graph)

    print(dependency_graph == invert_graph(reverse_dependency_graph))