import json  # Import JSON module to read/write data in JSON format
import os    # Import OS module to check if files exist

# CONFIGURATION 
inventory = {}  # Dictionary to store all products and their variants
LOW_STOCK_LIMIT = 5  # Quantity threshold for marking as "LOW STOCK"
ALLOWED_COLORS = ["black", "white", "blue", "red", "yellow", "grey", "pink"]  # Allowed variant colors
FILENAME = "inventory.txt"  # Default file name for inventory data

#INITIALIZATION 
def init(filename):
    #Set the inventory file for this session and load existing data
    global FILENAME  # Declare that we will use the global FILENAME variable
    FILENAME = filename  # Assign the given filename to FILENAME
    load_data()  # Call load_data() to load inventory from file

#  FILE FUNCTIONS 
def save_data():
    #Save the current inventory dictionary to a JSON file
    try:  # Try block to catch any errors during saving
        with open(FILENAME, "w") as file:  # Open the file in write mode
            json.dump(inventory, file, indent=4)  # Write inventory to file as JSON with indentation
    except Exception as e:  # Catch any exception
        print(f"Error saving data: {e}")  # Print error message

def load_data():
    #Load inventory data from the file, handling missing or corrupt files
    global inventory  # Use the global inventory variable

    if not os.path.exists(FILENAME):  # Check if the file exists
        print(f"{FILENAME} not found. A new one will be created when you save.")  # Notify user file is missing
        inventory = {}  # Initialize empty inventory
        return  # Exit function

    try:  # Try block to catch errors when reading file
        with open(FILENAME, "r") as file:  # Open the file in read mode
            content = file.read().strip()  # Read the content and remove leading/trailing spaces
            if not content:  # Check if file is empty
                inventory = {}  # Start with empty inventory
            else:
                inventory = json.loads(content)  # Load JSON content into inventory

    except json.JSONDecodeError:  # If JSON is invalid
        print("Error: inventory file is corrupted. Starting with empty inventory.")  # Print error message
        inventory = {}  # Reset inventory
    except Exception as e:  # Catch any other unexpected errors
        print(f"Unexpected error loading file: {e}")  # Print error
        inventory = {}  # Reset inventory

#VALIDATION FUNCTIONS 
def get_valid_color():
    #Prompt user to enter a valid color from ALLOWED_COLORS
    while True:  # Keep looping until a valid color is entered
        color = input(f"Enter color {ALLOWED_COLORS}: ").strip().lower()  # Read input, remove spaces, lowercase
        if color in ALLOWED_COLORS:  # Check if color is allowed
            return color  # Return valid color
        print("Invalid color.")  # Print message if invalid

def get_valid_quantity():
    #Prompt user to enter a valid numeric quantity
    while True:  # Loop until valid quantity is entered
        qty = input("Enter quantity: ").strip()  # Read input and remove spaces
        if qty.isdigit():  # Check if input is a number
            return int(qty)  # Convert string to int and return
        print("Quantity must be a number.")  # Print error if invalid

def get_valid_price(prompt="Enter price: "):
    #Prompt user to enter a valid price (float)
    while True:  # Loop until valid price is entered
        try:
            price = float(input(prompt))  # Try converting input to float
            return price  # Return valid price
        except ValueError:  # If conversion fails
            print("Price must be a number.")  # Print error

def is_variant_code_valid(code):
    #Check if a variant code is unique across all products
    for product in inventory.values():  # Loop through each product
        for v in product["variants"]:  # Loop through each variant
            if v["code"] == code:  # Check if variant code matches
                return False  
    return True  # Code is unique, return True

#ADD PRODUCT 
def add_product():
    product_name = input("Enter product name: ").strip()  # Read product name and remove spaces
    product_code = input("Enter product code: ").strip()  # Read product code and remove spaces

    if product_code not in inventory:  # Check if product code already exists
        inventory[product_code] = {"name": product_name, "variants": []}  # Add product with empty variants

    count_str = input("How many variants to add? ").strip()  # Ask how many variants
    count = int(count_str) if count_str.isdigit() else 0  # Convert input to int, default 0 if invalid

    for i in range(count):  # Loop for each variant to add
        print(f"\nVariant {i+1}")  # Show variant number
        variant_name = input("Enter variant name: ")  # Read variant name

        while True:  # Loop to ensure variant code is unique
            variant_code = input("Enter variant code: ").strip()  # Read variant code
            if variant_code in inventory or not is_variant_code_valid(variant_code):  # Check uniqueness
                print("Code already used. Try another.")  # Print message if code exists
            else:
                break  

        color = get_valid_color()  
        qty = get_valid_quantity()  
        price = get_valid_price("Enter selling price: ")  
        cost_price = get_valid_price("Enter cost price (Buy price): ")  

        # Add variant data to product
        inventory[product_code]["variants"].append({
            "name": variant_name,
            "code": variant_code,
            "color": color,
            "quantity": qty,
            "price": price,
            "cost_price": cost_price 
        })

    save_data()  # Save inventory after adding product
    print("Product added!\n")  

# VIEW PRODUCTS 
def view_products():
    if not inventory:  
        print("\n📭 Inventory is currently empty.") 
        return  


    print("\n" + "=" * 115)  
    print(f"{'P-Code':<10}{'Product Name':<15}{'Variant Name':<20}{'V-Code':<10}{'Color':<10}{'Qty':<8}{'Price':<10}{'Cost':<10}{'Status'}")
    print("-" * 115) 

    for p_code, product in sorted(inventory.items(), key=lambda x: x[0].lower()):  # Sort products by code
        first = True  # to print product name only once
        sorted_variants = sorted(product["variants"], key=lambda x: x["code"].lower())  # Sort variants by code

        for v in sorted_variants:  # Loop through each variant
            status = "LOW STOCK" if v["quantity"] < LOW_STOCK_LIMIT else ""  
            cost_val = v.get("cost_price", 0.0)  # Get cost price safely

            if first:  # If first variant, print product name
                print(f"{p_code:<10}{product['name']:<20}{v['code']:<10}{v['name']:<20}{v['color']:<10}{v['quantity']:<8}${v['price']:<9}{status}")
                first = False  # Reset after first variant
            else:  # when first turn to false leave product name blank
                print(f"{'':<15}{'':<10}{v['name']:<20}{v['code']:<10}{v['color']:<10}{v['quantity']:<8}${v['price']:<9.2f}${cost_val:<9.2f}{status}")
    print("=" * 115)  

#SEARCH 
def search_code():
    code = input("Enter product or variant code: ").strip()  

    if code in inventory:  # Check if it is a product code
        product = inventory[code]  # Get product data
        print(f"\n PRODUCT FOUND: {product['name']}")  
        for v in product["variants"]:  # Loop through variants
            status = "LOW STOCK" if v["quantity"] < LOW_STOCK_LIMIT else ""  
            cost_val = v.get("cost_price", 0.0)  # Get cost safely
            print(f"   -> {v['name']} | Code: {v['code']} | Color: {v['color']} | Qty: {v['quantity']} | Price: ${v['price']} | Cost: ${cost_val} {status}")
        return  

    for p_code, product in inventory.items():  # Loop through products to find variant code
        for v in product["variants"]:
            if v["code"] == code:  # Check if variant code matches
                status = "LOW STOCK" if v["quantity"] < LOW_STOCK_LIMIT else ""  
                cost_val = v.get("cost_price", 0.0)  # Get cost safely
                print(f"\n VARIANT FOUND: {v['name']} (Part of: {product['name']})")  # Print variant info
                print(f"   Color: {v['color']} | Qty: {v['quantity']} | Price: ${v['price']} | Cost: ${cost_val} | {status}")
                return  

    print("Code not found")  

#UPDATE PRODUCT
def update_product():
    code = input("Enter product code to update: ").strip()  
    if code not in inventory:  # Check if product exists
        print("Product not found")  
        return 

    product = inventory[code]  # Get product data
    while True:  # Loop menu until user exits
        print(f"\nEditing Product: {product['name']}")  # Show current product
        print("1. Update Name")
        print("2. Update Code")
        print("3. Back")
        choice = input("Choose option: ") 

        if choice == "1":
            product["name"] = input("Enter new name: ")  # Update product name
            print("Name updated")  
        elif choice == "2":
            new_code = input("Enter new code: ").strip()  # Read new product code
            if new_code in inventory:  # Check if code exists
                print("That product code already exists.")  
            else:
                inventory[new_code] = inventory.pop(code)  # Rename key(code) in dictionary
                code = new_code  # Update current code
                print("Code updated") 
        elif choice == "3":  
            break
        save_data()  

def update_variant():
    code = input("Enter variant code to update: ").strip()  # Read variant code
    found_v = None  # Initialize variable to store found variant
    for product in inventory.values():  # Loop through products
        for v in product["variants"]:  # Loop through variants
            if v["code"] == code:  # Check if code matches
                found_v = v  # Save variant
                break
    if not found_v:  # If variant not found
        print("Variant not found") 
        return  # Exit function

    while True:  # Show variant update menu
        print(f"\nEditing Variant: {found_v['name']}")  # Display current variant
        print("1. Name \n 2. Code \n 3. Color \n 4. Qty \n 5. Price \n 6. Cost Price \n 7. Exit")  
        choice = input("Choose option: ")  

        if choice == "1":
            found_v["name"] = input("New name: ")  # Update variant name
        elif choice == "2":
            new_c = input("New code: ").strip()  # Update variant code
            if is_variant_code_valid(new_c):  # Check if code is unique
                found_v["code"] = new_c
            else:
                print("Code taken")  # Print message if code exists
        elif choice == "3":
            found_v["color"] = get_valid_color()  # Update color
        elif choice == "4":
            found_v["quantity"] = get_valid_quantity()  # Update quantity
        elif choice == "5":
            found_v["price"] = get_valid_price("New selling price: ")  # Update selling price
        elif choice == "6":
            found_v["cost_price"] = get_valid_price("New cost price: ")  # Update cost price
        elif choice == "7":  
            break
        save_data() 

#DELETE
def delete():
    print("\n1. Delete Product (All variants) | 2. Delete Single Variant | 3. Cancel")  # Show delete menu
    choice = input("Choice: ")  
    if choice == "1":  # Delete entire product
        code = input("Enter Product Code: ") 
        if code in inventory:  # Check if product exists
            del inventory[code]  # Delete product
            save_data() 
            print("Product deleted")  
    elif choice == "2":  # Delete a variant
        code = input("Enter Variant Code: ")  
        for product in inventory.values():  # Loop through products
            for v in product["variants"]:  # Loop through variants
                if v["code"] == code:  # Check if code matches
                    product["variants"].remove(v)  # Remove variant
                    save_data() 
                    print(" Variant deleted")  
                    return 
        print("Not found")  

#MENU 
def menu():
    while True:  # Loop menu until user exits
        print("\n===== បញ្ជី (Banhji) Inventory =====")  
        print("1. Add Product")  
        print("2. View Products")  
        print("3. Search") 
        print("4. Update Product") 
        print("5. Update Variant") 
        print("6. Delete") 
        print("7. Back to Main Menu")  

        choice = input("Select (1-7): ").strip()  

        if choice == "1": add_product()  
        elif choice == "2": view_products()  
        elif choice == "3": search_code() 
        elif choice == "4": update_product() 
        elif choice == "5": update_variant() 
        elif choice == "6": delete() 
        elif choice == "7": 
            print("Returning to main menu...")  
            break
        else:
            print("Invalid selection")  
#MAIN 
if __name__ == "__main__":  # Only run if this file is executed directly
    init("inventory.txt")  # Initialize inventory
    menu()  
