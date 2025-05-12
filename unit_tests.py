import unittest
from budget_tracker import BudgetTracker

class TestBudgetTracker(unittest.TestCase):

    def test_add_transaction(self):

        budget = BudgetTracker()

        budget.add_transaction("01-05-2025", "Food", -10.00, "Groceries")
        #Check length of transactions list
        self.assertEqual(len(budget.transactions), 1)
        #Check that category value is stored as expected
        self.assertEqual(budget.transactions[0].category, "Food")
        #Check that tracker value is stored as expected
        self.assertEqual(budget.transactions[0].amount, -10.00)

    def test_spending_by_category(self):

        budget = BudgetTracker()

        budget.add_transaction("01-05-2025", "Food", -10.00, "Chipotle")
        budget.add_transaction("02-05-2025", "Food", -20.00, "Trader Joe's")
        budget.add_transaction("02-05-2025", "Transportation", -5.00, "DC Metro")

        spending = budget.get_spending_by_category()

        #Confirm total category spending adds and stores values as expected
        self.assertEqual(spending["Food"], -30.00)
        self.assertEqual(spending["Transportation"], -5.00)

    def test_generate_monthly_report(self):

        budget = BudgetTracker()

        budget.add_transaction("01-05-2025", "Food", -10.00, "Lunch")
        budget.add_transaction("15-05-2025", "Income", 1000.00, "Paycheck")
        budget.add_transaction("30-04-2025", "Transport", -15.00, "Uber")

        may_transactions = budget.get_transactions_by_month(5, 2025)

        #Check length of transactions list and confirm it's 2 for May
        self.assertEqual(len(may_transactions), 2)

        #Generate a new list with only the transaction values, for verification purposes
        amounts = [transaction.amount for transaction in may_transactions]

        #Verify both May transactions are in the list
        self.assertIn(-10.00, amounts)
        self.assertIn(1000.00, amounts)

        #Verify the April transaction is not in the list
        self.assertNotIn(-15.00, amounts)

    def test_transaction_refund(self):

        budget = BudgetTracker()

        budget.add_transaction("10-05-2025", "Refund", 25.00, "Returned Item")
        self.assertEqual(budget.transactions[0].amount, 25.00)
        self.assertTrue(budget.transactions[0].amount > 0)

    def test_remove_transaction(self):

        budget = BudgetTracker()
        budget.add_transaction("01-05-2025", "Food", -10.00, "Lunch")
        budget.add_transaction("02-05-2025", "Transport", -5.00, "Bus fare")

        #Remove the first transaction at index 0
        removed = budget.remove_transaction(0)
        self.assertEqual(removed.description, "Lunch")

        #Test length of the transactions list after removal operation
        self.assertEqual(len(budget.transactions), 1)

        #Confirm that the remaining transactions have been shifted up accordingly
        self.assertEqual(budget.transactions[0].description, "Bus fare")

    def test_get_net_spending(self):

        budget = BudgetTracker()

        budget.add_transaction("01-05-2025", "Income", 100.00, "Pay")
        budget.add_transaction("02-05-2025", "Food", -30.00, "Groceries")
        
        self.assertEqual(budget.get_net_spending(), 70.00)


    def test_get_total_income_and_expenses(self):

        budget = BudgetTracker()

        budget.add_transaction("01-05-2025", "Income", 200.00, "Freelance")
        budget.add_transaction("02-05-2025", "Bills", -50.00, "Electricity")

        self.assertEqual(budget.get_total_income(), 200.00)
        self.assertEqual(budget.get_total_expenses(), -50.00)


if __name__ == "__main__":
    unittest.main()
