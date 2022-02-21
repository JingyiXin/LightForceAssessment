def read_file(file):
    """Read a csv file into a list of strings
    This function reads each row in a csv file and adds it as an entry
    to a list. Each list element is a string.
    Args:
        file (string): the file location of the ECG trace in a csv file
    Returns:
        list: a list containing all rows from the csv file
    """
    with open(file, 'r') as f:
        data = f.readlines()
    return data

