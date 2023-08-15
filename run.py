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

def sales_data():
    """
    Get sales figures input from the user
    """
    print("Please enter sales data from the last market.")
    print("Data should be seven numbers, separated by commas.")
    print("Example: 25,35,45,57,50,30,16\n")

    data_str = input("Enter your data here: ")
    print(f"The data provvided is {data_str}")

sales_data()
