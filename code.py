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