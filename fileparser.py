# Convert Debian control file to a list of dictionaries
# where each dictionary in the list is a Debian control file paragraph
def control_file_to_list(filepath):

    paragraph_list = [] # store a list of paragraphs

    # open file and process each line
    with open(filepath, encoding='utf-8') as f:
        paragraph = {} # Treat each paragraph as a Python dictionary
        key = ''
        value = ''

        for line in f:

            # detect end of paragraph
            if line == '\n':
                #print(paragraph)
                paragraph_list.append(paragraph)  # append paragraph to list
                paragraph = {}  # reset current paragraph
                continue

            # Multiline field if first character in line is a space or tab character
            # Append line to the most recently added field in the dictionary
            if line[0] == ' ' or line[0] == '\t':
                paragraph[key] = paragraph[key] + line
                continue

            # New field in paragraph
            key_value_list = line.split(':', 1) # split each line by first occurring ':'
            key = key_value_list[0]
            value = key_value_list[1].strip()   # remove leading whitespace from value
            paragraph[key] = value              # add key-value pair to current paragraph dictonary

    return(paragraph_list)
