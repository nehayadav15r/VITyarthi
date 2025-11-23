<h1>📌 VITyarthi - Python-Based Expense Tracker</h1>

<div class="section">
<h2>📘 Project Overview</h2>
<p><b>VITyarthi</b> is a simple command-line based personal expense tracker created in Python.  
It helps users record expenses, set budgets, filter data, generate reports, and visualize spending trends using bar charts.</p>
</div>

<div class="section">
<h2>🎯 Features</h2>
<ul>
    <li>Add and store expenses with date, category, amount, and note</li>
    <li>Set and update category-wise budgets</li>
    <li>View expense summary reports</li>
    <li>Filter expenses by date or category</li>
    <li>Automatic budget alerts when overspending occurs</li>
    <li>Export complete expense data to CSV</li>
</ul>
</div>

<div class="section">
<h2>🛠️ Technology Stack</h2>
<ul>
    <li>Python 3</li>
    <li>CSV module for data storage</li>
    <li>Datetime for date processing</li>
    <li>Matplotlib for bar graphs</li>
    <li>OS module for file handling</li>
</ul>
</div>

<div class="section">
<h2>📂 File Structure</h2>
<pre>
├── VITyarthi.py
├── expenses.csv
├── budgets.csv
└── README.html
</pre>
</div>

<div class="section">
<h2>📄 How It Works</h2>
<p>The program stores data in two CSV files:</p>

<h3>1. <code>expenses.csv</code></h3>
<ul>
    <li>date</li>
    <li>category</li>
    <li>amount</li>
    <li>note</li>
</ul>

<h3>2. <code>budgets.csv</code></h3>
<ul>
    <li>category</li>
    <li>limit</li>
</ul>
</div>

<div class="section">
<h2>🔧 Installation</h2>
<pre>
pip install matplotlib
</pre>
</div>

<div class="section">
<h2>▶️ Running the Program</h2>
<pre>
python VITyarthi.py
</pre>
</div>

<div class="section">
<h2>📜 Main Menu Options</h2>
<ul>
    <li><b>1. Add Expense</b> – Add a new expense entry.</li>
    <li><b>2. View Report</b> – View total spending by category + bar graph.</li>
    <li><b>3. Filter Expenses</b> – Filter by date or category.</li>
    <li><b>4. Set Budget</b> – Assign spending limits for categories.</li>
    <li><b>5. Export Report</b> – Export a CSV file with all expenses.</li>
    <li><b>6. Exit</b> – Close the program.</li>
</ul>
</div>

<div class="section">
<h2>🧠 Code Used</h2>
<p>Below is the full Python source code for this project:</p>

<pre>
import csv
from datetime import datetime
import matplotlib.pyplot as plt
import os

Expense_File = 'expenses.csv'
Budget_File = 'budgets.csv'
#loading expenses
def load_expenses():
    expenses = []
    try:
        with open(Expense_File, newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                row['amount'] = float(row['amount'])
                row['date'] = datetime.strptime(row['date'], '%Y-%m-%d')
                expenses.append(row)
    except FileNotFoundError:
        pass
    return expenses
#saving expenses
def save_expense(expense):
    file_exists = os.path.exists(Expense_File)
    with open(Expense_File, 'a', newline='') as file:
        fieldnames = ['date', 'category', 'amount', 'note']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(expense)
#loading budget
def load_budgets():
    budgets = {}
    try:
        with open(Budget_File, newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                budgets[row['category']] = float(row['limit'])
    except FileNotFoundError:
        pass
    return budgets
#Saving budget
def Save_budgets(budgets):
    with open(Budget_File, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['category', 'limit'])
        writer.writeheader()
        for cat, limit in budgets.items():
            writer.writerow({'category': cat, 'limit': limit})
#Adding expenses

def Add_expense():
    date_str = input("Enter date (YYYY-MM-DD): ")
    category = input("Enter category (e.g., Food, Transport): ")
    amount_str = input("Enter amount: ")
    note = input("Note (optional): ")

    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        amount = float(amount_str)
    except ValueError:
        print("Invalid date or amount format.")
        return

    expense = {'date': date_str, 'category': category, 'amount': amount, 'note': note}
    save_expense(expense)
    print("Expense added Succesfully.")
#Filtering expenses
def Filter_expenses(expenses):
    print("Filtering options: leave blank to skip")
    start_date_str = input("Start date (YYYY-MM-DD): ")
    end_date_str = input("End date (YYYY-MM-DD): ")
    category_filter = input("Category: ")

    filtered = expenses
    if start_date_str:
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            filtered = [e for e in filtered if e['date'] >= start_date]
        except ValueError:
            print("Invalid start date.")
    if end_date_str:
        try:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
            filtered = [e for e in filtered if e['date'] <= end_date]
        except ValueError:
            print("The end date is invalid.")
    if category_filter:
        filtered = [e for e in filtered if e['category'].lower() == category_filter.lower()]

    print(f"Filtered Expenses ({len(filtered)} entries):")
    for g in filtered:
        print(f"{g['date'].date()} - {g['category']} - {g['amount']:.2f} - {g['note']}")
    return filtered
#setting budget
def Set_budget(budgets):
    cat = input("Enter category to set budget for: ")
    limit_str = input(f"Set budget amount for '{cat}': ")
    try:
        limit = float(limit_str)
        budgets[cat] = limit
        Save_budgets(budgets)
        print(f"Budget set: {cat} - {limit:.2f}")
    except ValueError:
        print("The amount is invalid")
#Alets and budget check
def Check_budgets(expenses, budgets):
    summary = {}
    for exp in expenses:
        cat = exp['category']
        summary[cat] = summary.get(cat, 0) + exp['amount']

    alerts = []
    for cat, limit in budgets.items():
        spent = summary.get(cat, 0)
        if spent > limit:
            alerts.append(f"Alert! Spending for '{cat}' exceeded budget: {spent:.2f} / {limit:.2f}")

    for alert in alerts:
        print(alert)
#Report
def Gen_report(expenses):
    summary = {}
    for exp in expenses:
        cat = exp['category']
        summary[cat] = summary.get(cat, 0) + exp['amount']

    print("Expense Summary by Category:")
    for cat, total in summary.items():
        print(f"{cat}: {total:.2f}")

    categories = list(summary.keys())
    amounts = list(summary.values())

    plt.bar(categories, amounts)
    plt.ylabel('Amount')
    plt.title('Expenses by Category')
    plt.show()
#Export report
def Export_the_report(expenses):
    filename = input("Enter filename to export (e.g., report.csv): ")
    with open(filename, 'w', newline='') as file:
        fieldnames = ['date', 'category', 'amount', 'note']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for e in expenses:
            writer.writerow({
                'date': e['date'].strftime('%Y-%m-%d'),
                'category': e['category'],
                'amount': e['amount'],
                'note': e['note']
            })
    print(f"Report exported to {filename}")
#Main program
def main():
    budgets = load_budgets()
    expenses = load_expenses()

    while True:
        print("""
Options:
1. Add Expense
2. View Report
3. Filter Expenses
4. Set Budget
5. Export Report
6. Exit""")
        choice = input("Choose an option: ")
        if choice == '1':
            Add_expense()
            expenses = load_expenses()
            Check_budgets(expenses, budgets)
        elif choice == '2':
            Gen_report(expenses)
            Check_budgets(expenses, budgets)
        elif choice == '3':
            filtered = Filter_expenses(expenses)
            Check_budgets(filtered, budgets)
        elif choice == '4':
            Set_budget(budgets)
        elif choice == '5':
            Export_the_report(expenses)
        elif choice == '6':
            print("Exit program.")
            break
        else:
            print("The option is invalid. Try again.")

if __name__ == "__main__":
    main()
</pre>
</div>

<div class="section">
<h2>📈 Future Improvements</h2>
<ul>
    <li>Graphical User Interface (GUI)</li>
    <li>Monthly budget system</li>
    <li>Recurring expenses</li>
    <li>Pie charts and line graphs</li>
    <li>Edit/Delete existing entries</li>
</ul>
</div>

<div class="section">
<h2>🙌 Credits</h2>
<p>Developed by: <b>Neha Yadav</b></p>
</div>

</body>
</html>
