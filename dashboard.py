import datetime
import os

class Dashboard:
    def __init__(self, inventory, sales_management):
        # connect to inventory and sales_management
        self.inventory = inventory
        self.sales_management = sales_management
        # Set default view to current month
        self.view_month = 3 
        self.view_year = 2026
        # Index 0 is empty so that index 1 matches January, 2 matches February, etc. - index 0 or month 0 would be empty
        self.months = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

    def get_month_totals(self, month_num, year_num):
        #filter sales data and calculate 
        m_sales = [s for s in self.sales_management if s['date'].month == month_num and s['date'].year == year_num]
        rev = sum(s['total'] for s in m_sales)
        profit = sum(s['profit'] for s in m_sales)
        return m_sales, rev, profit

    def calculate_report_data(self):
        # each weeks for displaying bar chart
        month_sales, _, _ = self.get_month_totals(self.view_month, self.view_year)
        weeks_rev = [0.0] * 6  # Calendar months can span across 6 different weeks - ex: in august, there are 6 weeks
        weeks_qty = [0] * 6
        total_profit = 0

        if month_sales:
            # currently using this year
            year = self.view_year
            first_of_month = datetime.datetime(year, self.view_month, 1)
            # %W - Monday as first day of the week
            start_week_num = int(first_of_month.strftime("%W"))

            for s in month_sales:
                current_week_num = int(s['date'].strftime("%W"))
                # calculate which row of the month the sale belongs to (0-5)
                idx = current_week_num - start_week_num
                
                if 0 <= idx < 6:
                    weeks_rev[idx] += s['total']
                    weeks_qty[idx] += s['quantity']
                    total_profit += s['profit']
        
        return month_sales, weeks_rev, weeks_qty, total_profit

    def show(self):
        # UI
        while True:
            # clears terminal screen first
            os.system('cls' if os.name == 'nt' else 'clear')
            
            month_sales, weeks_rev, weeks_qty, total_profit = self.calculate_report_data()
            month_name = self.months[self.view_month]

            # overview
            rev = sum(weeks_rev)
            orders = len(month_sales)
            # count how many different people bought something - if meytan bought something on Monday and Friday, her name remains as 1 customer
            cust_count = len(set(s['customer'] for s in month_sales))
            # find the highest sales week to scale the chart - use 1 if empty to avoid math errors
            max_qty = max(weeks_qty) if max(weeks_qty) > 0 else 1

            # Inventory Logic: Sum all variant quantities and check for lows
            stock = 0
            low_stock_alerts = []
            for product in self.inventory.values():     # look into every products
                for v in product["variants"]:           # plus every variants
                    stock += v["quantity"]
                    if v["quantity"] < 5:
                        low_stock_alerts.append(f"{product['name']} ({v['name']})")

            # how it will lookkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk
            print(f"\n=================== MONTHLY DASHBOARD ===================")
            print(f"  {month_name} {self.view_year} Overview")
            
            print(f"╔{'═' * 52}╗")
            print(f"║ TOTAL REVENUE: ${rev:<35.2f}║") # <35.2f left-align
            print(f"║{' ' * 52}║")
            
            # ASCII Weekly Bar Chart
            for i in range(len(weeks_rev)):
                # calculate bar length relative to the highest quantity during th whole week
                bar_len = int((weeks_qty[i] / max_qty) * 15)
                bar = "█" * bar_len
                line = f" Week {i+1}: {bar:<15} QTY: {weeks_qty[i]:<3}  ${weeks_rev[i]:>10.2f}"
                print(f"║ {line:<50} ║")
                
            print(f"╚{'═' * 52}╝")

            # more informations in dashboard
            print(f"╔════════════╗ ╔════════════╗ ╔════════════╗ ╔════════════╗")
            print(f"║   PROFIT   ║ ║   ORDERS   ║ ║ CUSTOMERS  ║ ║   STOCK    ║")
            print(f"║ ${total_profit:^9.0f} ║ ║{orders:^12}║ ║{cust_count:^12}║ ║{stock:^12}║")
            print(f"╚════════════╝ ╚════════════╝ ╚════════════╝ ╚════════════╝")

            if low_stock_alerts:
                print(f"\n⚠️  RESTOCK ALERT: {', '.join(low_stock_alerts)}")

            print(f"\nWould you like to:")
            print(f"[1] Weekly Revenue Detail")
            print(f"[2] Change Month View")
            print(f"[3] Run Strategic Business Analysis")
            print(f"[4] Return to Menu")
            
            choice = input("Select >> ")
            if choice == '1':
                self.show_week_detail(month_sales)
            elif choice == '2':
                try:
                    # it displays month 3 of 2026 instead of month3(of 2025)+month3(of 2026)
                    m = int(input("Enter Month Number (1-12): "))
                    y = int(input("Enter Year (e.g. 2025): "))
                    if 1 <= m <= 12: 
                        self.view_month = m
                        self.view_year = y
                except: print("Invalid input.")
            elif choice == '3':
                self.show_analysis()
            elif choice == '4':
                break

    # displays a week details (Monday - Sunday)
    def show_week_detail(self, month_sales):
        # check if we have any sales to look at. if these isn't, exit early
        if not month_sales:
            print("\nNo sales data for this month.")
            input("Press Enter to return...")
            return

        try:
            # ask the user which week they want to see (example: 1st week, 2nd week..)
            w_num = int(input("Which week? (1-6): "))
            # clear the terminal screen
            os.system('cls' if os.name == 'nt' else 'clear')
            
            # finding which week of the year
            year = self.view_year
            first_of_month = datetime.datetime(year, self.view_month, 1)
            target_week_of_year = int(first_of_month.strftime("%W")) + (w_num - 1)

            print(f"══ {self.months[self.view_month]} Week {w_num} Daily Breakdown ══")
            days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]        # a week got 7 days from Monday to Sunday
            daily_qty = [0] * 7     
            daily_rev = [0.0] * 7

            for s in month_sales:
                if int(s['date'].strftime("%W")) == target_week_of_year:    # Monday is the first day of the week
                    d_idx = s['date'].weekday() 
                    daily_qty[d_idx] += s['quantity']
                    daily_rev[d_idx] += s['total']
            
            max_d = max(daily_qty) if max(daily_qty) > 0 else 1
            print(f"╔═══════════════════════════════════════════╗")
            for i, d_name in enumerate(days):
                d_bar = "█" * int((daily_qty[i]/max_d)*15)
                print(f"║ {d_name}: {d_bar:<15} QTY: {daily_qty[i]:<3} ${daily_rev[i]:>10.0f} ║")
            print(f"╚═══════════════════════════════════════════╝")
            input("\nPress Enter to return...")
        except (ValueError, IndexError):
            print("Please enter a valid week number.")
            input("Press Enter to return...")

    def show_analysis(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        curr_sales, curr_rev, curr_profit = self.get_month_totals(self.view_month, self.view_year)
        
        # Calculate previous month and year
        if self.view_month > 1:
            prev_month = self.view_month - 1
            prev_year = self.view_year
        else:
            prev_month = 12
            prev_year = self.view_year - 1

        _, prev_rev, _ = self.get_month_totals(prev_month, prev_year)
        
        # display current sales
        daily_totals = {}
        for s in curr_sales:
            d_str = s['date'].strftime("%d %b %Y")
            daily_totals[d_str] = daily_totals.get(d_str, 0) + s['total']
        
        peak_day = max(daily_totals, key=daily_totals.get) if daily_totals else "N/A"
        peak_val = daily_totals.get(peak_day, 0)

        # compare previous year and this year
        diff = curr_rev - prev_rev
        growth = (diff / prev_rev * 100) if prev_rev > 0 else 100.0
        status = "BETTER" if growth >= 0 else "WORSE"

        print(f"\n================== BUSINESS ANALYSIS ====================")
        print(f"╔═════════════════════════════════════════════════╗")
        print(f"║ PEAK SALES DAY: {peak_day:<32}║")
        print(f"║ DAILY RECORD  : ${peak_val:<31.2f}║")
        print(f"╠═════════════════════════════════════════════════╣")
        print(f"║ THIS MONTH    : ${curr_rev:<31.2f}║") # Added current month revenue
        print(f"║ PREVIOUS MONTH: ${prev_rev:<31.2f}║")
        print(f"║ VS LAST MONTH : {growth:>+6.1f}% comparison{' ':<14}║")
        print(f"╚═════════════════════════════════════════════════╝")
        
        # prints data from previous month, this month, comparison
        print("INSIGHTS:")
        if prev_rev == 0:
            print(f" - This is your first month with data! No previous comparison.")
        else:
            print(f" - Performance is {abs(growth):.2f}% {status} than last month.")
            print(f" - You earned ${abs(diff):.2f} {'more' if diff >= 0 else 'less'} than in {self.months[prev_month]}.")
        input("\nPress Enter to return...")