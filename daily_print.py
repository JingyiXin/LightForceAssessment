from pymodm import connect
connect("mongodb+srv://<username>:<password>@<clustername>-ba348.mongodb.net/<folder>?retryWrites=true&w=majority")

from pymodm import MongoModel, fields

class Product(MongoModel):
    issue_type = fields.CharField()
    issue_key = fields.CharField(primary_key=True)
    status = fields.CharField()
    labels = fields.CharField()
    status_last_changed = fields.CharField()
    desired_ship_date = fields.CharField()
    priority = fields.CharField()


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
    data = data[1:]
    return data


def process_file(data):
    """Loads a list of strings into database
    This function reads each element of a list and creates a pymongo entry
    for every line. Each entry includes the issue type, issue key, status,
    labels, last changed time, desired ship date, and priority.
    Args:
        data (list): list of strings, each string from a line in a csv file
    Returns:
        str: "data processed" if successful.
    """
    
    for i, line in enumerate(data):
        line = line.strip("\n")
        line = line.split(",")
        item = Product(issue_type=line[0], issue_key=line[1], status=line[2], 
                       labels=line[3], status_last_changed=line[4],
                       desired_ship_date=line[5], priority=line[6])
        item.save()

    return "data processed"

if __name__ == "__main__":
    file = 'Exercise'
    file_loc = 'data\\{}.csv'.format(file)
    data = read_file(file_loc)
    analysis_status = process_file(data)
    