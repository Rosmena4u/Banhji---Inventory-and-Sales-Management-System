import hashlib #use to hash passwords using MD5 before comparing
import os  # Handle file paths and folder creation by connecting the python file with the .txt / .json files 
import time # use to create a time delay after too many failed logins
import inventory as inv # import the entire inventory module and give it a shorter nickname inv
from salemanagement import SalesSystem # import only the SaleSystem class from from salemanagement
from dashboard import Dashboard # imports only the Dashboard class from dashboard
 
DATA_DIR = "data" # we store all .txt and .json files in that folder
MAX_ATTEMPTS = 3 #Maximum number of wrong login attempts allowed before lockout
LOCK_TIME = 5 # Number of seconds the system waits after too many failed attempts

 
os.makedirs(DATA_DIR, exist_ok=True) # Creates the data folder if it does not already exist
 
#  LOGIN 
def login():
    attempts = 0  # Starts at 0 because no failed attempts have happened yet
 
    # Loop forever until the user logs in successfully
    # ask the user to enter their username and password
    while True:
        print("\n___________________________________________________________________Admin Login ________________________________________________________________")
        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()
 

         #only allow letters, numbers, _ and -
        safe_username = "".join(c for c in username if c.isalnum() or c in "_-")
        admin_file = os.path.join(DATA_DIR, f"{safe_username}.txt")
 

        # Check if data/admin1.txt file exists 
        if not os.path.exists(admin_file):
            print("Invalid username or password.\n")
            attempts += 1
        
         # File exists, so open it and read the username and password
        else:
            with open(admin_file, "r") as f:
                line = f.readline().strip()
                try:   # Try to separate the username and password and split into username and password by the comma
                    stored_username, stored_password_hash = line.split(",")
                except ValueError:
                    print(f"Admin file {admin_file} is corrupted.\n")
                    continue   # ask user to try again
  
             # Convert the entered password into a hash to compare with the stored hash
            password_hash = hashlib.md5(password.encode()).hexdigest()
            if password_hash == stored_password_hash:
                print(f"\nLogin successful! Welcome {username} to the Inventory System.\n")
                return safe_username
            else:
                print("Invalid username or password.\n")
                attempts += 1
 
        if attempts >= MAX_ATTEMPTS:
            print(f"Too many failed attempts. Waiting {LOCK_TIME} seconds...\n")
            for remaining in range(LOCK_TIME, 0, -1): # countdown from 5 to 1
                print(f"Time left: {remaining} seconds", end="\r")
                time.sleep(1)   # Wait 1 second before showing the next number
            print("\nYou can try logging in again.\n")
            attempts = 0
 
# each admin has their own files  
def get_data_files(username):

     # Creates the file path for the admin's inventory and sales files
    inventory_file = os.path.join(DATA_DIR, f"{username}_inventory.json")
    sales_file     = os.path.join(DATA_DIR, f"{username}_sales.txt")
 
     # Check both files and create them if they do not exist yet
    for file in [inventory_file, sales_file]:
        if not os.path.exists(file):
            open(file, "w").close()
 
    return inventory_file, sales_file
 
#Converts sales history into a format the Dashboard can read-
def build_dashboard_sales(sales_system):

    result = []  # Empty list to store the converted sales data\
    for sale in sales_system.sales_history:
        total_qty = sum(qty for _, qty in sale.items)
        total = sale.total()
        
        # Pulls the calculated profit stored in the sale object
        real_profit = sale.profit()
            
        result.append({
            'date'    : sale.date,
            'total'   : total,
            'quantity': total_qty,
            'profit'  : round(real_profit, 2),
            'customer': sale.customer.name
        })
    return result
 
#MAIN MENU 
def main_menu(username):
    inventory_file, sales_file = get_data_files(username)
 
    # Both modules share the SAME inventory file
    inv.init(inventory_file)
    sales_system = SalesSystem(sales_file, inventory_file)
 
    while True:
        print("_______________________________________________________________________Main Menu__________________________________________________________________")
        print("1. Dashboard / Reporting")
        print("2. Inventory Management")
        print("3. Sales Management")
        print("4. Exit")
 
        choice = input("Enter your choice (1-4): ").strip()
 
        if choice == "1":
            # Always build fresh dashboard data before showing
            dashboard_sales = build_dashboard_sales(sales_system)
            dashboard = Dashboard(inv.inventory, dashboard_sales)
            dashboard.show()
 
        elif choice == "2":
            inv.menu()
            sales_system.load_inventory()  
 
        elif choice == "3":
            sales_system.menu()
 
        elif choice == "4":
            print("Exiting system. Goodbye!")
            break
 
        else:
            print("Invalid choice. Please enter a number between 1 and 4.\n")
 
#  RUN 
if __name__ == "__main__":
    print("_____________________________________________Welcome to our Banji Inventory and Sales Management System_______________________________________\n")
    username = login()
    main_menu(username)