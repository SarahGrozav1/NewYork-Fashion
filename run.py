import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('new_york_fashion')

#Create function to get data string from user

def get_sales_data():
    """
    Get sales figures input from the user
    """
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be seven numbers, separated by commas.")
        print("Example: 25,35,45,57,50,30,16\n")

        data_str = input("Enter your data here: ")
    
        sales_data = data_str.split(",")
        

#Adjust get_sales_data function so that it repeat its request
#for data if the input provided is not valid

        if validate_data(sales_data):
            print("Data is valid")
            break

    return sales_data

#Function to handle the validation

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
                f"You need to write exactly 7 values, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

#If there are no errors, it will return True

    return True

data = get_sales_data()
