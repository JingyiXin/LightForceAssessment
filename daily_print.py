from pymodm import connect
from pymodm import MongoModel, fields

class Product(MongoModel):
    issue_type = fields.CharField()
    issue_key = fields.CharField(primary_key=True)
    status = fields.CharField()
    labels = fields.CharField()
    status_last_changed = fields.CharField()
    desired_ship_date = fields.CharField()
    priority = fields.CharField()


def initialize_server():
    """Initializes database connection
    This function should be run first to connect to the cloud database.
    Args:
        none
    Returns:
        none
    """
    print("Connecting to MongoDB...")
    connect("mongodb+srv://jx75:lightforce@lightforce.lp12b.mongodb.net/Light"
            "Force?retryWrites=true&w=majority")
    print("Connection attempt finished.")


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


def ready_to_print():
    """Returns a list of all products ready to print
    This function returns the issue key of all bracket products with the status
    "Brackets in Printer Queue" and all IDB products with the status "Ready to
    Print".
    Args:
        none
    Returns:
        list of strings: a list of issue keys for brackets in printer queue
        list of strings: a list of issue keys for IDB products ready to print
    """
    bracket_ready = []
    idb_ready = []
    for item in Product.objects.raw({"issue_type":"MakeBrackets"}):
        if (item.status == "Brackets in Printer Queue"):
            bracket_ready.append(item.issue_key)
    for item in Product.objects.raw({"issue_type":"MakeIDB"}):
        if (item.status == "Ready to Print"):
            idb_ready.append(item.issue_key)
    return bracket_ready, idb_ready


if __name__ == "__main__":
    initialize_server()
    file = 'Exercise'
    file_loc = 'data\\{}.csv'.format(file)
    # data = read_file(file_loc)
    # analysis_status = process_file(data)
    bracket_ready, idb_ready = ready_to_print()
    