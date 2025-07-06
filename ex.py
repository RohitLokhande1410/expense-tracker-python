from flask import Flask, render_template, request, redirect, url_for, send_file
import pandas as pd
import os
import datetime
import matplotlib.pyplot as plt

app = Flask(__name__)
FILE_PATH = "expenses.csv"
CATEGORIES = ["Food", "Travel", "Entertainment", "Accommodation", "Shopping", "Misc"]

def ensure_file_exists():
    if not os.path.exists(FILE_PATH):
        with open(FILE_PATH, "w") as f:
            f.write("Date,Name,Amount,Category\n")

def generate_chart():
    """Generates a pie chart from the current expenses."""
    df = pd.read_csv(FILE_PATH)
    if df.empty:
        return None
    category_summary = df.groupby("Category")["Amount"].sum()
    plt.figure(figsize=(6,6))
    category_summary.plot(kind="pie", autopct="%1.1f%%", startangle=140, colormap="viridis")
    plt.title("Expense Distribution by Category")
    plt.ylabel("")
    plt.tight_layout()
    chart_path = "static/expense_chart.png"
    plt.savefig(chart_path)
    plt.close()
    return chart_path

@app.route("/")
def index():
    ensure_file_exists()
    df = pd.read_csv(FILE_PATH)
    total_spent = df["Amount"].sum() if not df.empty else 0
    chart_path = generate_chart()  # Generate or update chart every time index loads
    return render_template("index.html", expenses=df.to_dict(orient="records"), total_spent=total_spent, chart=chart_path)

@app.route("/add", methods=["POST"])
def add_expense():
    name = request.form.get("name")
    amount = float(request.form.get("amount"))
    category = request.form.get("category")
    date = datetime.date.today().strftime("%Y-%m-%d")
    new_expense = {"Date": date, "Name": name, "Amount": amount, "Category": category}
    df = pd.DataFrame([new_expense])
    df.to_csv(FILE_PATH, mode="a", header=False, index=False)
    return redirect(url_for("index"))

@app.route("/delete/<name>")
def delete_expense(name):
    df = pd.read_csv(FILE_PATH)
    df = df[df["Name"] != name]
    df.to_csv(FILE_PATH, index=False)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
