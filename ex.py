import pandas as pd
import datetime
import os
import matplotlib.pyplot as plt
import logging


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class ExpenseTracker:
    def __init__(self, file_path="expenses.csv"):
        self.file_path = file_path
        self.budget = 0
        self.load_budget()
        self.ensure_file_exists()

    def ensure_file_exists(self):
        
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as f:
                f.write("Date,Name,Amount,Category\n")

    def load_budget(self):
      
        try:
            self.budget = float(input("Enter your monthly budget: "))
        except ValueError:
            print("Invalid input. Setting budget to 50000.")
            self.budget = 50000

    def add_expense(self):
        
        name = input("Enter expense name: ")
        while True:
            try:
                amount = float(input("Enter expense amount: "))
                break
            except ValueError:
                print("Invalid amount! Please enter a number.")

        categories = ["Food", "Travel", "Entertainment", "Accommodation", "Shopping", "Misc"]
        while True:
            print("\nSelect a category:")
            for i, category in enumerate(categories, start=1):
                print(f"{i}. {category}")
            try:
                category_index = int(input(f"Choose category [1-{len(categories)}]: ")) - 1
                if 0 <= category_index < len(categories):
                    category = categories[category_index]
                    break
                else:
                    print("Invalid category. Try again.")
            except ValueError:
                print("Please enter a valid number.")

        date = datetime.date.today().strftime("%Y-%m-%d")
        new_expense = {"Date": date, "Name": name, "Amount": amount, "Category": category}

        
        df = pd.DataFrame([new_expense])
        df.to_csv(self.file_path, mode="a", header=False, index=False)
        logging.info("Expense added successfully!")

    def display_expenses(self):
        
        try:
            df = pd.read_csv(self.file_path)
            print("\nExpense Records:")
            print(df.to_string(index=False))
        except Exception as e:
            logging.error(f"Error reading expenses file: {e}")

    def summarize_expenses(self):
        
        try:
            df = pd.read_csv(self.file_path)
            total_spent = df["Amount"].sum()
            remaining_budget = self.budget - total_spent

            
            today = datetime.date.today()
            days_in_month = (today.replace(day=28) + datetime.timedelta(days=4)).day
            remaining_days = max(days_in_month - today.day, 1)
            daily_budget = remaining_budget / remaining_days

            print(f"\nTotal Spent: Rs.{total_spent:.2f}")
            print(f"Remaining Budget: Rs.{remaining_budget:.2f}")
            print(f"Per-Day Budget: Rs.{daily_budget:.2f}")

            
            category_summary = df.groupby("Category")["Amount"].sum()
            print("\nExpenses by Category:")
            print(category_summary.to_string())

        except Exception as e:
            logging.error(f"Error summarizing expenses: {e}")

    def filter_expenses_by_date(self):
        
        try:
            df = pd.read_csv(self.file_path)
            start_date = input("Enter start date (YYYY-MM-DD): ")
            end_date = input("Enter end date (YYYY-MM-DD): ")

           
            df["Date"] = pd.to_datetime(df["Date"])
            mask = (df["Date"] >= start_date) & (df["Date"] <= end_date)
            filtered_df = df.loc[mask]

            if filtered_df.empty:
                print("\nNo expenses found in the given date range.")
            else:
                print("\nFiltered Expenses:")
                print(filtered_df.to_string(index=False))
        except Exception as e:
            logging.error(f"Error filtering expenses: {e}")

    def delete_expense(self):
        
        try:
            df = pd.read_csv(self.file_path)
            print(df.to_string(index=False))
            name_to_delete = input("\nEnter the name of the expense to delete: ")
            
            df = df[df["Name"] != name_to_delete]
            df.to_csv(self.file_path, index=False)
            logging.info("Expense deleted successfully!")
        except Exception as e:
            logging.error(f"Error deleting expense: {e}")

    def visualize_expenses(self):
        
        try:
            df = pd.read_csv(self.file_path)
            category_summary = df.groupby("Category")["Amount"].sum()

            if category_summary.empty:
                print("\nNo expenses to visualize.")
                return

            plt.figure(figsize=(8, 5))
            category_summary.plot(kind="pie", autopct="%1.1f%%", startangle=140, colormap="viridis")
            plt.title("Expense Distribution by Category")
            plt.ylabel("")
            plt.show()
        except Exception as e:
            logging.error(f"Error visualizing expenses: {e}")

def main():
    tracker = ExpenseTracker()

    while True:
        print("\nExpense Tracker Menu:")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Summarize Expenses")
        print("4. Filter Expenses by Date")
        print("5. Delete an Expense")
        print("6. Visualize Expenses")
        print("7. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            tracker.add_expense()
        elif choice == "2":
            tracker.display_expenses()
        elif choice == "3":
            tracker.summarize_expenses()
        elif choice == "4":
            tracker.filter_expenses_by_date()
        elif choice == "5":
            tracker.delete_expense()
        elif choice == "6":
            tracker.visualize_expenses()
        elif choice == "7":
            print("Exiting Expense Tracker. Have a great day!")
            break
        else:
            print("Invalid choice. Please select again.")

if __name__ == "__main__":
    main()
