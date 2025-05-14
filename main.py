from budget_tracker import BudgetTracker

def print_budget_menu():
    """ Displays a menu of options that the user can choose from when using the budget tracker. """

    print("\n --- Budget Home Menu ---\n")
    print("1 - Add a new transaction/income")
    print("2 - View all transactions")
    print("3 - View total income")
    print("4 - Total expenses")
    print("5 - Current balance")
    print("6 - View all-time spending by category")
    print("7 - Transactions by month")
    print("8 - Save budget to file")
    print("9 - Load budget from file")
    print("10 - Remove a transaction")
    print("0 - Exit\n")

def run_cli():
    """
    Runs the CLI loop for interacting with the budget tracker
    until user exits by inputting 0
    """
    budget = BudgetTracker()

    #loop keeps budget tracker continuing going after every
    #user action until exit clause is activated
    while True:

        #upon the start of every new loop, always 
        #show meny and prompt for choice
        print_budget_menu()
        choice = input("Enter your choice: ")

        if choice == '1':

            #User enters transaction info
            date = input("Enter the date (DD-MM-YYYY): ")
            category = input("Enter the category: ")
            amount = float(input("Enter the amount (negative for expenses): "))
            description = input("Enter the memo: ")

            budget.add_transaction(date, category, amount, description)

            print("\n\nTransaction successfully added.\n\n")

        elif choice == '2':

            #print all existing transactions without the index, if exists
            if not budget.transactions:
                print("\nNo transactions exist.")
            else:
                print("\nAll Transactions:")
                for transactions in budget.transactions:
                    print(f"[ID {transactions.id}] {transactions.date} | {transactions.category} | ${transactions.amount:.2f} | {transactions.description}")

        elif choice == '3':

            print(f"\nTotal income: ${budget.get_total_income():.2f}")

        elif choice == '4':

            print(f"\nTotal expenses: ${budget.get_total_expenses():.2f}")

        elif choice == '5':

            print(f"\nNet balance: ${budget.get_net_spending():.2f}")

        elif choice == '6':

            spending = budget.get_spending_by_category()

            #if no existing data exists
            if not spending:

                print("\nNo expense data available.")

            else:

                print("\nSpending by Category:\n")

                for category, amount in spending.items():
                    print(f"{category}: ${amount:.2f}")

        elif choice == '7':

            month = int(input("Enter month (as number): "))
            year = int(input("Enter year: "))

            results = budget.get_transactions_by_month(month, year)

            #if no transactions exist
            if not results:
                print("No transactions found for that month and year.")
            else:
                print(f"\nTransactions for {month}-{year}:")

                #iterate thru the results list and print each transaction
                for transactions in results:

                    print(f"[ID {transactions.id}] {transactions.date} | {transactions.category} | ${transactions.amount:.2f} | {transactions.description}")

        elif choice == "8":

            #user must enter exact name of file to load
            filename = input("Enter filename to save (ex: 'your_name_.json')): ")
            budget.save_to_json(filename)

            print(f"Transactions saved to {filename}")

        elif choice == "9":

            #user must enter exact name of file to load
            filename = input("Enter filename to load (ex: 'your_name_.json')): ")
            budget.load_from_json(filename)

            print(f"Transactions loaded from {filename}")

        elif choice == "10":

            #shows list with indices (used to identify which transaction to remove)
            budget.print_all_transactions()  
            index = input("\nEnter the index of the transaction to remove (DO NOT ENTER THE UID): ")

            #confirms the string is only digits
            if index.isdigit():

                #cast to index value to integer and input as parameter
                budget.remove_transaction(int(index))
                
            else:
                #if user enters non-integer characters
                print("Please enter a valid number.")


        elif choice == '0':
            exit()

if __name__ == "__main__":
    run_cli()
