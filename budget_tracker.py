import json

class Transaction:
    """
        This class represents a single transaction in the budget

    Attributes:
        id (int): unique id for each transaction
        date (str): The date of the transaction (DD-MM-YYYY)
        category (str): The category the transaction falls under (ex: Groceries, Income)
        amount (float): The value of the transaction (positive = income, negative = expense)
        description (str): A short note/memo regarding the transaction
"""
    #class level variable to keep track of where UID assignment
    #across user profiles
    id_assigner = 1

    def __init__(self, date, category, amount, description):

        #Class level variable to assign each transaction a unique id
        self.id = Transaction.id_assigner

        Transaction.id_assigner += 1

        self.date = date
        self.category = category
        self.amount = amount
        self.description = description


class BudgetTracker:

    """
    This class represents a BudgetTracker object. A budget tracker will have a list of transactions 
    and provides basic functionality, including: printing a report, viewing total spending, 
    spending by category, and descriptions/notes regarding a specific transaction.

    """
    def __init__(self):
        self.transactions = []

    def add_transaction(self, date, category, amount, description):
        """
        Adds a transaction to the list with the given data

        Args:
            date (str): Date of the transaction
            category (str): Type/category of the transaction
            amount (float): Amount (positive for income, negative for expenses)
            description (str): Short description/memo
        """

        transaction = Transaction(date, category, amount, description)
        self.transactions.append(transaction)

    def get_net_spending(self):
        """
        Calculates net balance (total income - total expenses)

        Returns:
            float: The current net balance
        """

        total = 0

        for transaction in self.transactions:
            total += transaction.amount

        return total
    
    def get_total_income(self):
        """
        Calculates the total income from all transactions

        Returns:
            float: Sum of all positive amounts (income)
        """

        total = 0

        for transaction in self.transactions:
            if transaction.amount > 0:
                total += transaction.amount

        return total
    
    def get_total_expenses(self):
        """
        Calculates the total expenses from all transactions

        Returns:
            float: Sum of all negative amounts (expenses)
        """

        total = 0

        for transaction in self.transactions:
            if transaction.amount < 0:
                total += transaction.amount

        return total
    
    
    def get_spending_by_category(self):
        """
        Summarizes total expenses for each category

        Returns:
            dict: A dictionary where keys are categories and values are total amounts
        """

        #Generates a dict with spending by category
        spending = {}

        for transaction in self.transactions:

            if transaction.amount < 0:
                if transaction.category in spending:

                    spending[transaction.category] += transaction.amount

                else:

                    spending[transaction.category] = transaction.amount

        return spending
    
    def get_transactions_by_month(self, month, year):
        """
            Filters transactions by the given month and year

        Args:
            month (int): The month (MM)
            year (int): The year (YYYY)

        Returns:
            list: A list of transactions from the specified month and year
        """

        #Iterates thru the transaction list, and if a transaction date matches the parameter time frame,
        #add it to the resulting list of transactions 
        results = []

        for transaction in self.transactions:

            transaction_day, transaction_month, transaction_year = transaction.date.split("-")
        
        #Converts date information from str to int
            if int(transaction_month) == month and int(transaction_year) == year:
                results.append(transaction)

        return results
    
    def save_to_json(self, filename):
        """
        Saves the current budget to a JSON file

        Args:
            filename (str): Name of the JSON file to create/rewrite
        """

        data = []

        for transaction in self.transactions:
            data.append({
                "id" : transaction.id,
                "date": transaction.date,
                "category": transaction.category,
                "amount": transaction.amount,
                "description": transaction.description
            })

        with open(filename, "w") as f:
            #saves json file in human readable form 
            #in case its needed for debugging
            json.dump(data, f, indent=4)


    def load_from_json(self, filename):
        """
        Loads in data from saved budget profile from JSON file 

        Args:
            filename (str): Name of the JSON file to read in
        """

        #Loads in budget data from a json file
        with open(filename, "r") as f:
            data = json.load(f)

        self.transactions = []
        max_id = 0

        for item in data:

            transaction = Transaction(item["date"], item["category"], item["amount"], item["description"])
            transaction.id = item["id"]
            self.transactions.append(transaction)

            if transaction.id > max_id:
                max_id = transaction.id

        #Brings the class-level id_assigner up to where it left of for a specific user
        Transaction.id_assigner = max_id + 1

    def print_all_transactions(self):
        """
        Prints all transactions in the tracker with index and details

        If no transactions exist, prints msg notifying user in the CLI
        """

        if not self.transactions:
            print("No transactions recorded.")
            return

        for i, t in enumerate(self.transactions):
            print(f"Index: {i} || [UID {t.id}] Date: {t.date} | Category: {t.category} | Amount: ${t.amount:.2f} | Memo: {t.description}")

    def remove_transaction(self, index):
        """
        Removes a transaction at the specified index, if valid

        Args:
            index (int): Index of the transaction to remove

        Returns:
            Transaction object if successful, or None for an invalid index
        """

        #If within the length/bounds of the transaction list
        if 0 <= index < len(self.transactions):
            removed = self.transactions.pop(index)
            #print the removed transaction for confirmation
            print(f"\nRemoved transaction: {removed.description} (${removed.amount:.2f}) on {removed.date}\n")
            #return for unit testing purposes
            return removed
        else:
            print("\nInvalid transaction index. No transaction has been removed.\n")
            return None




    


