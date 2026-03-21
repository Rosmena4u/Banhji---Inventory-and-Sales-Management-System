#### បញ្ជី - BANHJI Description
Banhji is a Python-based management tool built to move retail tracking away from messy  paper logs and manual spreadsheets. The system uses Object-Oriented Programming and JSON to automate stock updates and calculate exact profit margins instantly after every sale. By generating structured daily and monthly reports, it eliminates human error and gives small business owners a clear, real-time look at their inventory and financial performance.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)

#### Installation
To get the system running on your local machine, follow these four steps: 
  1. Clone the Repository 
    Open your terminal and run the following commands to download the project and navigate into the directory: 
    git clone https://github.com/yourusername/banji-inventory.git 
    cd banji-inventory 
  2. Install Python 
    Ensure you have Python 3.9 or a newer version installed. You can check your current version by running: 
    python --version 
  3. Run the Program 
    Start the application by executing the main script: 
    python main.py 
    cd banji-inventory 

#### Usage
This section explains how to run and use the system.

🔐 Creating an Admin Account

Before logging in, you need to create an admin account manually.

Step 1: Generate Password Hash

Create a Python file (e.g., create_hash.py) and add:

import hashlib

password = "yourpassword"  # Put your password here
hashed = hashlib.md5(password.encode()).hexdigest()
print(hashed)

Run the file, and you will see a hash output in the terminal.

Example:

9e3669d19b675bd57058fd4664205d2a

Copy this hash — you will need it in the next step.

Step 2: Create Admin File

Create a file called:

data/admin1.txt

Add your username and hashed password:

admin1,9e3669d19b675bd57058fd4664205d2a
Step 3: Login
- Login using your real password (not the hash)
- If you enter the wrong password 3 times, the system will lock for 5 seconds
🏠 Main Menu

After logging in:

1. Dashboard / Reporting
2. Inventory Management
3. Sales Management
4. Exit
📊 1. Dashboard / Reporting
- Weekly Revenue Detail

→ Shows day-by-day breakdown (Monday → Sunday)

- Change Month View

→ Select month (1–12)

- Run Strategic Business Analysis

→ Compares this month vs last month

→ Shows peak sales day

- Return to Menu
📦 2. Inventory Management
- Add Product

→ Add product name & code

→ Add variants (color, quantity, price)

- View Products

→ Displays all items in a table

→ ⚠️ Items with < 5 stock show LOW STOCK

- Search

→ Search by product code or variant code

- Update Product

Update Name

Update Code

- Update Variant

Name

Code

Color

Quantity

Price

- Delete
Delete Product

Delete Single Variant

- Back to Main Menu
💰 3. Sales Management
- Sell Product

→ Enter customer details

→ Select products & quantity

→ Receipt auto-generated

→ Stock updates automatically

- View Sales History

→ Shows all past sales

- Daily Sales Report

→ Displays today's sales + total revenue

- Clear Sales History

→ ⚠️ Permanently deletes all records

- Edit Receipt

Edit Customer Name

Edit Customer Phone

Edit Sale Date

- Back to Main Menu
    
#### Features
Secure Admin Login: Supports multiple users with MD5 password hashing and account lock after 3 failed attempts.
  1. Inventory Management (CRUD): Add, view, update, and delete products and variants (color, size, etc.), with low stock alerts.
  2. Sales Processing: Automatically generates receipts, updates stock, and calculates total and profit.
  3. Business Dashboard: Displays sales data using ASCII charts, including weekly revenue, peak sales days, and monthly growth.
  4. Data Persistence: Saves all data automatically using:.json for inventory and.txt for sales history

#### Project Structure
project/

├── main.py 			      # System entry & login

├── inventory.py	 	    # Product & stock management

├── salemanagement.py 	# Sales logic & classes

├── dashboard.py		     # Reports & analytics

└── data/ 			         # Data storage

├── admin1.txt		       # Encrypted login credentials

├── inventory.json		    # Inventory database

└── sales.txt			       # Sales history

#### Contributing
Core Contributors
  - Iv Meytan
  - Sarun Yohana
  - Thea Kanika
  - Meas Soklin

#### License
This project is licensed under the MIT License — see LICENSE for details.

#### Changelog
v1.0.0
- Initial release
- Secure admin login
- Inventory management (add/view/update/delete/search)
- Sales system with receipts
- Dashboard overview
v1.1.0
- Added low-stock alerts.
- Added daily and weekly sales reports
- Multi-Admin-Support


### Conclusion
## 💡 Lessons Learned & Reflections
- Object-Oriented Programming (OOP): Learned to organize the system into classes and objects to separate dashboard, inventory, and sales logic
- Module Integration: Learned how to connect multiple modules to ensure consistent data sharing across the entire system
- MD5 hashing: Learned how to hash passwords so they are never stored in plain text
- File handling: Learned how to use os to build file paths and create files automatically
- Module connection: Learned to connect multiple modules so they share the same data
- Data Visualization: Developed custom ASCII and Unicode bar charts to create real-time trend visualizations without external libraries.
- Time-Series Logic: Learned how to apply the datetime library to convert raw data into weekly and monthly calculations for comparative business analysis.
- Data Persistence with JSON: Learned to use JSON for structured data storage, ensuring inventory and sales records are saved and retrieved correctly.
> "This project was a journey of persistent problem-solving. While we faced constant challenges, the process was incredibly rewarding. These obstacles pushed us to turn theoretical concepts into a functional business tool, ultimately deepening our technical skills and proving that we can overcome new challenges through dedicated learning."

