import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
import pyfiglet
import colorama
import sys

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
        print()
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
    Collects columns of data from sales worksheet, collecting
    the last 5 entries for each coat and returns the data
    as a list of lists.
    """
    sales = SHEET.worksheet("sales")

    columns = []
    for ind in range(1, 8):
        column = sales.col_values(ind)
        columns.append(column[-5:])

    return columns


def calc_store_data(data):
    """
    Calculate the average store for each item type, adding 10%
    """

    print("Calculating store data ...\n")
    new_store_data = []

    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        store_num = average * 1.1
        new_store_data.append(round(store_num))

    return new_store_data


def run_sales_data():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_warehouse_data = calc_warehouse_data(sales_data)
    update_worksheet(new_warehouse_data, "warehouse")
    sales_columns = last_5_entries_sales()
    store_data = calc_store_data(sales_columns)
    update_worksheet(store_data, "store")

# Welcome message


def welcome_message():
    """
    Welcome message for the user
    """
    result = pyfiglet.figlet_format("NewYork  Fashion Store", justify="center")
    print(result)
    print(colorama.Fore.YELLOW + "Welcome to NewYork-Fashion Data Automation")
    print(colorama.Style.RESET_ALL)

# Here its the menu for the app


def main_menu():
    """
    Creating the menu for the app
    """
    print("---------------")
    print("PLEASE PICK AN OPTION:")
    print()
    print("1. Instructions")
    print("2. View Data")
    print("3. Add Sales")
    print("4. Exit the App")
    print("---------------")

    try:
        selection = int(input("Chose an option: "))
    except Exception:
        print(colorama.Fore.RED + "This is no valid option!")
        print(colorama.Style.RESET_ALL)

    if selection == 1:
        instr()
    elif selection == 2:
        view_data()
    elif selection == 3:
        add_sales()
    elif selection == 4:
        print("You choose to exit the app. Goodbye!")
        sys.exit()
    else:
        print(colorama.Fore.RED + "Invalid choice. Enter 1-4\n")
        print(colorama.Style.RESET_ALL)
        main_menu()

# Instructions of the app so that the user know how to use it


def instr():
    """
    Instructions for the user to know how to use the app
    """
    print("INSTRUCTIONS:")
    print()
    print("From the main, if you want to view a data, you can input sales,")
    print(" warehouse or store and it will show the values for each area.")
    print(" To add sales data for the past 7 days, select 3 from the menu and")
    print(" put your sales figures in for each date, followed by a comma.\n")

# Function for user so that the user can see which sheet he wants


def view_data():
    """
    Creating view_data function so that the user can see which sheet he wants
    """
    print("Please Pick An Option: ")
    print("1. Sales Data")
    print("2. Warehouse Data")
    print("3. Store Data")
    print("------------------")

    try:
        selection = int(input("Chose an option: "))
    except Exception:
        print(colorama.Fore.RED + "This is no valid option!")
        print(colorama.Style.RESET_ALL)
        view_data()

    if selection == 1:
        worksheet = SHEET.worksheet('sales')
        data = pd.DataFrame(worksheet.get_all_records())
        print(data.shape)
        print(data.head)
        print(data.columns)
        main_menu()

    elif selection == 2:
        worksheet = SHEET.worksheet('warehouse')
        data = pd.DataFrame(worksheet.get_all_records())
        print(data.shape)
        print(data.head)
        print(data.columns)
        main_menu()

    elif selection == 3:
        worksheet = SHEET.worksheet('store')
        data = pd.DataFrame(worksheet.get_all_records())
        print(data.shape)
        print(data.head)
        print(data.columns)
        main_menu()

    else:
        print(colorama.Fore.RED + "Invalid choice. Enter 1-3\n")
        print(colorama.Style.RESET_ALL)
        view_data()

# If user will choose option 3 will be able to add sales data


def add_sales():
    """
    Calling functions so that the user could add sales data
    """
    run_sales_data()
    main_menu()


def main():
    """
    Creating user input so that user could choose again
    """
    welcome_message()
    main_menu()
    # User input
    options = ("y", "n")
    while True:
        print("-------------------------------")
        print("Do you want to add sales data?")
        print("Please answer with 'y' for yes and 'n' for no.")
        print("If you choose 'y' you will be able to add sales data.")
        print("If you choose 'n' you will be able to see menu of the again.")
        print("-------------------------------")

        user_input = input("Your answer: ")
        if user_input in options:
            break
        else:
            print(colorama.Fore.RED + 'Option not valid!')
            print(colorama.Style.RESET_ALL)

    # If user will type 'y', the app will ask him to type the sales numbers
    if user_input == "y":
        run_sales_data()
        main_menu()

    # I user will type 'n', the app will show the menu again
    elif user_input == "n":
        main_menu()


main()
print("Have a nice day!\n")
