import gspread
from google.oauth2.service_account import Credentials
import pyfiglet
import colorama

result = pyfiglet.figlet_format("NewYork  Fashion Store", justify="center")
print(result)


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('new_york_fashion')

# Create function to get data string from user

def get_sales_data():
    """
    Get sales figures input from the user
    """
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be seven numbers, separated by commas.")
        print("Example: 25,35,45,57,50,30,16\n")

        data_str = input("Enter your data here:\n")

        sales_data = data_str.split(",")


# Adjust get_sales_data function so that it repeat its request
# for data if the input provided is not valid

        if validate_data(sales_data):
            print(colorama.Fore.GREEN + "Data is valid")
            print(colorama.Style.RESET_ALL)
            break

    return sales_data

# Function to handle the validation


def validate_data(values):
    """
    Converts all string values into integers.
    If strig cannot be converted or if there
    aren't 7 values, raises ValueError.
    """
    try:
        [int(value) for value in values]
        if len(values) != 7:
            raise ValueError(
             f"You need to write exactly 7 values, you provided {len(values)}")
    except ValueError as e:
        print(colorama.Fore.RED + f"Invalid data: {e}, please try again.\n")
        print(colorama.Style.RESET_ALL)
        return False

# If there are no errors, it will return True

    return True

# Updating the worksheet


def update_worksheet(data, worksheet):
    """
    Receives a list of integers to be inserted into worksheet
    Update the relevant worksheet with the data provided
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_for_updating = SHEET.worksheet(worksheet)
    worksheet_for_updating.append_row(data)
    print(colorama.Fore.GREEN +
          f"{worksheet} worksheet updated successfully\n")
    print(colorama.Style.RESET_ALL)

# Defining function to calculate warehouse data


def calc_warehouse_data(sales_row):
    """
    Compare sales with store and calculate the warehouse for each item type.
    """
    print("Calculating warehouse data...\n")
    store = SHEET.worksheet("store").get_all_values()
    store_row = store[-1]

    warehouse_data = []
    for store, sales in zip(store_row, sales_row):
        warehouse = int(store) - sales
        warehouse_data.append(warehouse)

    return warehouse_data


def last_5_entries_sales():
    """
    Collects collumns of data from sales worksheet, collecting
    the last 5 entries for each coat and returns the data
    as a list of lists.
    """
    sales = SHEET.worksheet("sales")

    columns = []
    for ind in range(1, 8):
        column = sales.col_values(ind)
        columns.append(column[-5:])

    return columns


def calc_stock_data(data):
    """
    Calculate the average stock for each item type, adding 10%
    """

    print("Calculating stock data ...\n")
    new_stock_data = []

    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))

    return new_stock_data


def main():
    """
    Run all program functions
    """

    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_warehouse_data = calc_warehouse_data(sales_data)
    update_worksheet(new_warehouse_data, "warehouse")
    sales_columns = last_5_entries_sales()
    stock_data = calc_stock_data(sales_columns)
    update_worksheet(stock_data, "store")


print(colorama.Fore.YELLOW + "Welcome to NewYork-Fashion Data Automation")
print(colorama.Style.RESET_ALL)
main()
