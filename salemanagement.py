import json  # used to handle JSON data for inventory
from datetime import datetime  # used for date and time
import os  # used for file checking

# CLASSES

# Product class to store product information
class Product:
    def __init__(self, name, price, cost_price, stock): 
        self.name = name        # product name
        self.price = price      # product price
        self.cost_price = cost_price # product cost (cost_price in File 2)
        self.stock = stock      # product stock quantity

# Customer class to store customer information
class Customer:
    def __init__(self, name, phone):
        self.name = name        # customer name
        self.phone = phone      # customer phone number

# Sale class represents a transaction
class Sale:
    def __init__(self, customer, date=None, items=None):
        self.customer = customer               
        # Stores the customer who made the purchase.
        # Expected to be a Customer object or identifier.

        self.items = items if items else []    
        # list of (product, quantity), If no items are provided, it initializes as an empty list.

        self.date = date if date else datetime.now() 
        # sale date (If no date is given, it uses the current time)
        self._profit = 0
        # A private variable to track the profit earned from this sale.

    # calculate total price of sale (price × quantity) for every item
    def total(self):
        return sum(product.price * qty for product, qty in self.items)
    
    # returns calculated profit
    #_profit is calculated when items are added in `make_sale`.
    # Using a method like this allows controlled access to the private variable
    def profit(self):
        return self._profit

    # display receipt
    def receipt(self):
        print("\n------ RECEIPT ------")
        print("Customer:", self.customer.name)
        print("Phone:", self.customer.phone)
        print("Date:", self.date.strftime("%Y-%m-%d %H:%M:%S"))
        print("---------------------")
        for product, qty in self.items:
            subtotal = product.price * qty
            print(f"{product.name} | Qty: {qty} | Price: {product.price} | Subtotal: {subtotal}")
        print("---------------------")
        print("TOTAL:", self.total())
        print("---------------------\n")

# SALES SYSTEM 
class SalesSystem:
    def __init__(self, sales_file, inventory_file):
        self.SALES_FILE = sales_file        # file to store sales data
        self.INVENTORY_FILE = inventory_file  # file to store inventory
        self.inventory = {}                 # dictionary for inventory data
        self.sales_history = []             # list of all sales
        self.product_map = []               # map for selecting products
        self.load_inventory()               # load inventory from file
        self.load_sales()                   # load sales from file

    # load inventory from JSON file
    def load_inventory(self):
        try:
            with open(self.INVENTORY_FILE, "r") as f:
                content = f.read().strip()
                # Converts the JSON text into a Python dictionary using json.loads()
                self.inventory = json.loads(content) if content else {}
        except (FileNotFoundError, json.JSONDecodeError):
            # If the file doesn’t exist, it just creates an empty inventory {}
            self.inventory = {}

    # save inventory to JSON file
    def save_inventory(self):
        with open(self.INVENTORY_FILE, "w") as f:
            # indent=4 makes the file pretty and readable
            json.dump(self.inventory, f, indent=4)

    # display all products and variants
    def show_products(self):
        print("\nAvailable Products")
        index = 1
        self.product_map = []  # reset product map
        for p_code, product in self.inventory.items():
            for v in product["variants"]:
                # Ensure the display shows stock correctly
                print(index, f"{product['name']} - {v['name']} | Price: {v['price']} | Stock: {v['quantity']}")
                self.product_map.append((product, v)) # store mapping
                index += 1

    # process selling products
    def make_sale(self):
        self.load_inventory() # refresh inventory
        
        # input customer info
        name = input("Customer name: ")
        phone = input("Customer phone: ")
        customer = Customer(name, phone)
        
        sale = Sale(customer) # create new sale

        while True:
            self.show_products()
            try:
                index = int(input("Choose product number: ")) - 1  # Subtract 1 from index because Python lists are 0-based
                qty = int(input("Quantity: "))
            except ValueError:
                print("Invalid input")
                continue

            # If the index is out of range (not in the product list), restart loop

            if index < 0 or index >= len(self.product_map):
                print("Invalid product")
                continue

             # Retrieve the selected product and variant from the product map
            product_data, variant = self.product_map[index]

            # check stock availability
            # Get cost price for profit calculation, default to 0 if not available

            if qty <= variant["quantity"]:
                cp = variant.get("cost_price", 0.0)

                # create temporary product object
                temp_product = Product(
                    product_data["name"] + " - " + variant["name"], #full product name
                    variant["price"],
                    cp, # selling price
                    variant["quantity"]  # current stock
                )
                sale.items.append((temp_product, qty)) # add product and quantity to sale
                
                # PROFIT CALCULATION
                sale._profit += (temp_product.price - temp_product.cost_price) * qty
                
                variant["quantity"] -= qty              # reduce stock
                self.save_inventory()                  # save updated inventory
                print("Product added")
            else:
                print("Not enough stock")

            # ask to continue adding products
            if input("Add more? (y/n): ").lower() != "y":
                break

        # save sale
        self.sales_history.append(sale)
        self.save_sales_to_file()
        sale.receipt() # print receipt

    # save sales data to file
    def save_sales_to_file(self):
        with open(self.SALES_FILE, "w") as f:
            for sale in self.sales_history:
                 # Save customer info
                f.write(f"Customer:{sale.customer.name}\n")
                f.write(f"Phone:{sale.customer.phone}\n")
                f.write(f"Date:{sale.date.strftime('%Y-%m-%d %H:%M:%S')}\n")
                # Save each product in the sale
                for product, qty in sale.items:
                    # Save with cost_price as the 4th column
                    f.write(f"{product.name}|{qty}|{product.price}|{product.cost_price}\n")
                 # Save total and profit
                f.write(f"TOTAL:{sale.total()}\n")
                f.write(f"PROFIT:{sale.profit()}\n")
                f.write("END\n")

    # load sales from file
    def load_sales(self):
        if not os.path.exists(self.SALES_FILE):
            return # If file does not exist, do nothing

        with open(self.SALES_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()

        sale_data = None   # Temporary storage for customer info
        items = []   # Temporary list for items in a sale
        for line in lines:
            line = line.strip()
            if not line: continue   # Skip empty lines

             # Read customer info
            if line.startswith("Customer:"):
                sale_data = {"customer": line.split(":", 1)[1].strip()}
                # Splits the line at the first ":" only (using split(":", 1)).
                # [1] gets the part after the colon, which is the actual customer name.
                # .strip() removes any extra spaces before or after the name.
                # Creates a temporary dictionary 'sale_data' to store customer info for this sale.
    
                items = []
            elif line.startswith("Phone:"):
                 # Checks if the current line contains the customer's phone number
                sale_data["phone"] = line.split(":", 1)[1].strip()
                 # Splits the line at ":" and stores the phone number in the same 'sale_data' dictionary.
            elif line.startswith("Date:"):
                 # Checks if the current line contains the sale date.
    
                sale_data["date"] = datetime.strptime(line.split("Date:")[1].strip(), "%Y-%m-%d %H:%M:%S")
             # Read product info
            elif "|" in line and not line.startswith("TOTAL") and not line.startswith("PROFIT"):
                parts = line.split("|")
                if len(parts) >= 3:
                    full_name = parts[0]
                    qty = int(parts[1])
                    price = float(parts[2])
                    
                    # --- LIVE LOOKUP FOR COST_PRICE FROM INVENTORY ---
                    found_cost = 0.0
                    if " - " in full_name:
                        p_name, v_name = full_name.split(" - ", 1)
                        for product in self.inventory.values():
                            if product["name"] == p_name:
                                for v in product["variants"]:
                                    if v["name"] == v_name:
                                        found_cost = v.get("cost_price", 0.0)
                                        break
                    
                    # Store product info in temporary list
                    items.append({"name": full_name, "qty": qty, "price": price, "cost_price": found_cost})
            elif line == "END":
                if sale_data:
                     # Create customer and sale objects
                    customer = Customer(sale_data["customer"], sale_data["phone"])
                    sale_obj = Sale(customer, sale_data["date"])
                    
                    current_profit = 0
                    for item in items:
                        current_profit += (item["price"] - item["cost_price"]) * item["qty"]
                        p = Product(item["name"], item["price"], item["cost_price"], stock=0)
                        sale_obj.items.append((p, item["qty"]))
                    
                    sale_obj._profit = current_profit
                    self.sales_history.append(sale_obj)

    # show all previous sales
    def show_sales_history(self):
        if not self.sales_history: 
            print("No sales yet")
            return
        print("\n--- Sales History ---")
        for i, s in enumerate(self.sales_history, start=1):
             # Show index, customer, total amount, profit, and date
            print(f"{i}. {s.customer.name} | Total: {s.total()} | Profit: {s.profit()} | Date: {s.date.strftime('%Y-%m-%d %H:%M')}")

    # show today's sales summary
    def daily_sales_report(self):
        today = datetime.now().date()
        total_rev = total_prof = 0
        print("\n--- Daily Sales Report ---")
        for s in self.sales_history:
            if s.date.date() == today:
                 # Show each sale today
                print(s.customer.name, "| Total:", s.total())
                total_rev += s.total()
                total_prof += s.profit()
        print(f"Total Revenue Today: {total_rev} | Total Profit Today: {total_prof}")

    # delete all sales history
    def clear_sales_history(self):
        confirm = input("Are you sure you want to delete ALL sales history? (y/n): ")
        if confirm.lower() == "y":
            self.sales_history = []  # Clear in-memory list
            open(self.SALES_FILE, "w").close() # Clear the sales file
            print("All sales deleted")
        else:
            print("Operation cancelled.")

    def menu(self):
        while True:
            print("\n===== SALES SYSTEM =====")
            print("1. Sell Product")
            print("2. View Sales History")
            print("3. Daily Sales Report")
            print("4. Clear Sales History")
            print("5. Back to Main Menu") # Aligned choice 5 with File 1's return logic

            choice = input("Choose option: ")
            if choice == '1': self.make_sale() # Sell products
            elif choice == '2': self.show_sales_history() # Show all past sales
            elif choice == '3': self.daily_sales_report()  # Show today's report
            elif choice == '4': self.clear_sales_history() # Clear all sales
            elif choice == '5': 
                print("Returning to main menu...")
                break
            else:
                print("Invalid option")