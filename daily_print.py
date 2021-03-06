from pymodm import connect, MongoModel, fields
from datetime import datetime
import csv


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
        file (string): the file location of the csv file
    Returns:
        list of strings: a list containing all rows from the csv file
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


def load_data(file):
    """Reads a csv file and transfers the data into a database
    This function runs both the read_file(), which reads a csv file into
    a list, and process_file, which reads each element of a list and creates
    a pymongo entry for every line.
    Args:
        file (string): the file location of the csv file
    Returns:
        str: "data processed" if successful.
    """
    data = read_file(file)
    status = process_file(data)
    return status


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


def print_today(print_ready, today, print_time):
    """Returns a list of all products that must be printed today
    This function returns the issue key of all products in the list
    print_ready, where the desired ship date is less than the given print
    time away from the given date and time.
    Args:
        none
    Returns:
        list of strings: a list of issue keys for products that must be
        printed today.
    """
    to_print = []
    print_time = print_time * 24 * 60 * 60
    today_datetime = datetime.strptime(today, '%d/%b/%y %H:%M %p')
    for key in print_ready:
        item = Product.objects.raw({"_id": key}).first()
        ship_time = item.desired_ship_date
        ship_datetime = datetime.strptime(ship_time, '%d/%b/%y %H:%M %p')
        time_til_ship = ship_datetime - today_datetime
        if (time_til_ship.total_seconds() <= print_time):
            to_print.append(item.issue_key)
            print(ship_time)
    return to_print


def products_to_print(today):
    """Runs several functions to returns a list of all products that must be
    printed today
    This function returns the issue key of all products that must be printed
    today, including brackets in printer queue and IDB products ready to print,
    that are less than 5 and 2 days respectively from their desired ship date.
    Args:
        today (string): a string in a format convertible to a datetime object
        at the desired latest start print time
    Returns:
        list of strings: a list of issue keys for products that must be
        printed today.
    """
    bracket_ready, idb_ready = ready_to_print()
    brackets_to_print = print_today(bracket_ready, today, 5)
    idb_to_print = print_today(idb_ready, today, 2)
    to_print = brackets_to_print + idb_to_print
    return to_print


def convert_to_csv(items, filename):
    """Writes entries in database to a csv file
    This function searches for all entries in the pymongo database for items
    with an issue key listed in the given list, and writes their data into
    a csv file.
    Args:
        items (list of strings): a list of all issue keys for products to
        be included.
        filename (string): the filename of the csv file to be written to
    Returns:
        string: "Items recorded in <filename>", if successful
    """
    columns = ["Issue Type", "Issue key", "Status", "Labels",
               "Status Last Changed", "Desired Ship Date", "Priority"]
    with open(filename, 'w') as f:
        write = csv.writer(f)
        write.writerow(columns)
        for key in items:
            item = Product.objects.raw({"_id": key}).first()
            write.writerow([item.issue_type, item.issue_key, item.status, 
                           item.labels, item.status_last_changed,
                           item.desired_ship_date, item.priority])
    return "Items recorded in {}".format(filename)


if __name__ == "__main__":
    initialize_server()
    
    file = 'Exercise'
    file_loc = 'data\\{}.csv'.format(file)
    load_data(file_loc)
    
    to_print = products_to_print("27/Jan/22 5:00 PM")
    
    print(convert_to_csv(to_print, "to_print.csv"))
    