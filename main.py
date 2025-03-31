import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

def init_db():
    conn = sqlite3.connect('business_orders.db')
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY,
    customer_name TEXT NOT NULL,
    order_details TEXT NOT NULL,
    status TEXT NOT NULL)
    """)
    conn.commit()
    conn.close()

def add_order():
    conn = sqlite3.connect('business_orders.db')
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO orders (customer_name, order_details, status) VALUES (?, ?, 'Новый')",
        (customer_name_entry.get(), order_details_entry.get()))

    conn.commit()
    conn.close()

    customer_name_entry.delete(0, tk.END)
    order_details_entry.delete(0, tk.END)
    view_orders()

def view_orders():
    for i in tree.get_children():
        tree.delete(i)

    conn = sqlite3.connect('business_orders.db')
    cur = conn.cursor()

    cur.execute("SELECT * FROM orders")
    rows = cur.fetchall()

    for row in rows:
        tree.insert("", tk.END, values=row)

    conn.close()

def complete_order():
    selected_item = tree.selection()

    if selected_item:
        order_id = tree.item(selected_item, 'values')[0]

        conn = sqlite3.connect('business_orders.db')
        cur = conn.cursor()

        cur.execute("UPDATE orders SET status='Завершён' WHERE id=?", (order_id,))

        conn.commit()
        conn.close()

        view_orders()
    else:
        messagebox.showwarning("Предупреждение", "Выберите заказ для завершения")

app = tk.Tk()
app.title("Система управления заказами")
app.geometry("600x400")

# Создание стиля
style = ttk.Style()
style.configure("TLabel", font=("Helvetica", 12), padding=5)
style.configure("TButton", font=("Helvetica", 12), padding=5)
style.configure("Treeview.Heading", font=("Helvetica", 12, 'bold'))
style.configure("Treeview", font=("Helvetica", 10))

# Цвет фона
app.configure(bg="#f0f0f0")

header_frame = tk.Frame(app, bg="#f0f0f0")
header_frame.pack(pady=10)

tk.Label(header_frame, text="Имя клиента", bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5)
customer_name_entry = tk.Entry(header_frame, font=("Helvetica", 12))
customer_name_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(header_frame, text="Детали заказа", bg="#f0f0f0").grid(row=1, column=0, padx=5, pady=5)
order_details_entry =tk.Entry(header_frame, font=("Helvetica", 12))
order_details_entry.grid(row=1, column=1, padx=5, pady=5)

button_frame = tk.Frame(app, bg="#f0f0f0")
button_frame.pack(pady=10)

add_button = ttk.Button(button_frame, text="Добавить заказ", command=add_order)
add_button.grid(row=0, column=0, padx=5, pady=5)

complete_button = ttk.Button(button_frame, text="Завершить заказ", command=complete_order)
complete_button.grid(row=0, column=1, padx=5, pady=5)

columns = ("id", "customer_name", "order_details", "status")
tree = ttk.Treeview(app, columns=columns, show="headings", height=10)

for column in columns:
    tree.heading(column, text=column)
    tree.column(column, anchor=tk.CENTER)

tree.pack(pady=10)

init_db()
view_orders()
app.mainloop()