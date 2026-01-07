import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import date

# ---------------- DATABASE ---------------- #
conn = sqlite3.connect("expenses.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    amount REAL,
    category TEXT,
    notes TEXT
)
""")
conn.commit()

# ---------------- FUNCTIONS ---------------- #
def add_expense():
    d = date_entry.get()
    amt = amount_entry.get()
    cat = category_combo.get()
    note = notes_entry.get()

    if amt == "" or cat == "":
        messagebox.showerror("Error", "Amount and Category are required")
        return

    cur.execute("INSERT INTO expenses (date, amount, category, notes) VALUES (?, ?, ?, ?)",
                (d, amt, cat, note))
    conn.commit()
    clear_fields()
    load_data()

def delete_expense():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Warning", "Select a record to delete")
        return

    values = tree.item(selected, 'values')
    cur.execute("DELETE FROM expenses WHERE id=?", (values[0],))
    conn.commit()
    load_data()

def load_data():
    for row in tree.get_children():
        tree.delete(row)

    cur.execute("SELECT * FROM expenses")
    rows = cur.fetchall()

    for row in rows:
        tree.insert("", tk.END, values=row)

def clear_fields():
    amount_entry.delete(0, tk.END)
    notes_entry.delete(0, tk.END)

# ---------------- UI ---------------- #
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("850x500")
root.resizable(False, False)

# ---------------- TOP FRAME ---------------- #
top = tk.Frame(root, pady=10)
top.pack()

tk.Label(top, text="Date").grid(row=0, column=0, padx=5)
date_entry = tk.Entry(top, width=12)
date_entry.grid(row=0, column=1)
date_entry.insert(0, date.today().strftime("%d/%m/%Y"))

tk.Label(top, text="Category").grid(row=0, column=2, padx=5)
category_combo = ttk.Combobox(top, values=["Food", "Bills", "Travel", "Shopping", "Transport"], width=15)
category_combo.grid(row=0, column=3)
category_combo.current(0)

tk.Label(top, text="Amount").grid(row=1, column=0, padx=5)
amount_entry = tk.Entry(top, width=12)
amount_entry.grid(row=1, column=1)

tk.Label(top, text="Notes").grid(row=1, column=2, padx=5)
notes_entry = tk.Entry(top, width=18)
notes_entry.grid(row=1, column=3)

tk.Button(top, text="Add Expense", command=add_expense, bg="green", fg="white", width=15)\
    .grid(row=2, column=1, pady=10)

tk.Button(top, text="Delete Selected", command=delete_expense, bg="red", fg="white", width=15)\
    .grid(row=2, column=3)

# ---------------- TABLE ---------------- #
columns = ("ID", "Date", "Amount", "Category", "Notes")

tree = ttk.Treeview(root, columns=columns, show="headings", height=15)
tree.pack(pady=10)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center")

load_data()

root.mainloop()
