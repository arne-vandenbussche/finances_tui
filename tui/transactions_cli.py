import db.db_transactions
import sys


def show_all_transactions():
    transactions = db.db_transactions.get_all_transactions()
    if len(transactions) == 0:
        print("There aren't any transactions in this database.")
    for transaction in transactions:
        print(transaction)


def add_transaction():
    print("Our apologies. We haven't implemented this function yet.")


def export_transactions_to_csv():
    print("Our apologies. The function to export to csv has not been implemented yet.")


def exit_program():
    sys.exit(0)


def menu():
    print(
"""
1. Show all transactions.
2. Add a transaction.
3. Export all transactions to a csv file.
4. Leave the application.
""")
    successful_choice = False
    while not successful_choice:
        try:
            choice = int(input("Enter the number of your choice: "))
            print(f"This was your choice: {choice}")
            if choice in (1, 2, 3, 4):
                successful_choice = True
            else:
                print("You have to give a number from 1 to 4.")
        except ValueError:
            print("You must enter a whole number from 1 to 4.")
    if choice == 1:
        show_all_transactions()
    elif choice == 2:
        add_transaction()
    elif choice == 3:
        export_transactions_to_csv()
    else:
        exit_program()
