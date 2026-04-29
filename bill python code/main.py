import tkinter as tk
from tkinter import messagebox
import datetime
import database

# Create database tables
database.create_tables()

# -------- GLOBAL LIST --------
products = []

# Main window
root = tk.Tk()
root.title("Inventory & Billing System")
root.geometry("800x600") # Increased size slightly to fit the dates
root.configure(bg="#2b2b2b")

# -------- TITLE --------
tk.Label(root, text="Smart Inventory & Billing System",
         font=("Arial", 16, "bold"),
         bg="#2b2b2b", fg="white").pack(pady=15)

# -------- INPUT FRAME --------
frame = tk.Frame(root, bg="#2b2b2b")
frame.pack(pady=10)

tk.Label(frame, text="Product Name", bg="#2b2b2b", fg="white").grid(row=0, column=0, padx=10, pady=5)
entry_name = tk.Entry(frame, bg="#3c3f41", fg="white", insertbackground="white")
entry_name.grid(row=0, column=1, padx=10, pady=5)

tk.Label(frame, text="Price", bg="#2b2b2b", fg="white").grid(row=1, column=0, padx=10, pady=5)
entry_price = tk.Entry(frame, bg="#3c3f41", fg="white", insertbackground="white")
entry_price.grid(row=1, column=1, padx=10, pady=5)

tk.Label(frame, text="Quantity", bg="#2b2b2b", fg="white").grid(row=2, column=0, padx=10, pady=5)
entry_qty = tk.Entry(frame, bg="#3c3f41", fg="white", insertbackground="white")
entry_qty.grid(row=2, column=1, padx=10, pady=5)

# -------- FUNCTIONS --------

def load_products():
    """Loads and displays all products in the database."""
    global products
    products = database.get_products()

    listbox.delete(0, tk.END)
    for p in products:
        # p[4] accesses the new date_added column
        listbox.insert(tk.END, f"{p[1]} | ₹{p[2]} | Qty: {p[3]} | Added: {p[4]}")


def add_product():
    global products
    name = entry_name.get()
    price = entry_price.get()
    qty = entry_qty.get()

    if name and price and qty:
        # Generate the current date and time
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        database.add_product(name, float(price), int(qty), now)
        
        # Fetch the latest data to get the DB-assigned ID
        all_prods = database.get_products()
        new_product = all_prods[-1] 
        
        # Append the new product to our current session list and display
        products.append(new_product)
        listbox.insert(tk.END, f"{new_product[1]} | ₹{new_product[2]} | Qty: {new_product[3]} | Added: {new_product[4]}")

        entry_name.delete(0, tk.END)
        entry_price.delete(0, tk.END)
        entry_qty.delete(0, tk.END)
        entry_name.focus()
    else:
        messagebox.showerror("Error", "Fill all fields")


def delete_product():
    global products
    selected = listbox.curselection()
    if selected:
        index = selected[0]
        product = products[index]
        database.delete_product(product[0])
        
        # Remove the item from the current session display
        del products[index]
        listbox.delete(index)


def update_product():
    global products
    selected = listbox.curselection()

    if not selected:
        messagebox.showerror("Error", "Select a product first")
        return

    index = selected[0]
    product = products[index]

    try:
        new_name = entry_name.get() if entry_name.get() else product[1]
        new_price = float(entry_price.get()) if entry_price.get() else product[2]
        new_qty = int(entry_qty.get()) if entry_qty.get() else product[3]

        database.update_product(product[0], new_name, new_price, new_qty)
        
        # Fetch updated data
        all_prods = database.get_products()
        updated_product = next((p for p in all_prods if p[0] == product[0]), None)
        
        if updated_product:
            # Update the item in-place in our session list and display
            products[index] = updated_product
            listbox.delete(index)
            listbox.insert(index, f"{updated_product[1]} | ₹{updated_product[2]} | Qty: {updated_product[3]} | Added: {updated_product[4]}")

    except ValueError:
        messagebox.showerror("Error", "Enter valid numbers")


# -------- AUTO FILL --------
def on_select(event):
    selected = listbox.curselection()
    if selected:
        product = products[selected[0]]

        entry_name.delete(0, tk.END)
        entry_name.insert(0, product[1])

        entry_price.delete(0, tk.END)
        entry_price.insert(0, product[2])

        entry_qty.delete(0, tk.END)
        entry_qty.insert(0, product[3])


def generate_bill():
    total = 0
    # If nothing is selected, calculate total for the whole session
    items_to_bill = listbox.curselection() if listbox.curselection() else range(len(products))
    
    if not items_to_bill:
        messagebox.showinfo("Bill", "No items to bill!")
        return

    for i in items_to_bill:
        # Added quantity multiplication to make the billing accurate
        total += (products[i][2] * products[i][3])

    # Generate the timestamp for the bill
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Save to the new database table
    database.save_bill(total, now)

    messagebox.showinfo("Bill Generated", f"Date & Time: {now}\n\nTotal Amount: ₹{total}")


def view_past_bills():
    bills = database.get_bills()
    if not bills:
        messagebox.showinfo("Past Bills", "No bills have been generated yet.")
        return
        
    history = "--- Bill History ---\n\n"
    for b in bills:
        history += f"Bill ID: {b[0]} | Total: ₹{b[1]} | Date: {b[2]}\n"
        
    messagebox.showinfo("Past Bills", history)


def clear_fields():
    global products
    products.clear() # Empty the underlying list data
    
    entry_name.delete(0, tk.END)
    entry_price.delete(0, tk.END)
    entry_qty.delete(0, tk.END)

    listbox.delete(0, tk.END)   # clears display
    entry_name.focus()


# -------- BUTTON FRAME --------
btn_frame = tk.Frame(root, bg="#2b2b2b")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Add Product", width=15, command=add_product).grid(row=0, column=0, padx=5, pady=5)
tk.Button(btn_frame, text="Update Product", width=15, command=update_product).grid(row=0, column=1, padx=5, pady=5)

tk.Button(btn_frame, text="Delete Product", width=15, command=delete_product).grid(row=1, column=0, padx=5, pady=5)

tk.Button(btn_frame, text="Clear All", width=15,
          bg="#d32f2f", fg="white",
          command=clear_fields).grid(row=1, column=1, padx=5, pady=5)

tk.Button(btn_frame, text="Generate Bill", width=15, command=generate_bill).grid(row=2, column=0, padx=5, pady=5)

# Show All Button
tk.Button(btn_frame, text="Show All", width=15, 
          bg="#4caf50", fg="white", 
          command=load_products).grid(row=2, column=1, padx=5, pady=5)

# View Past Bills Button
tk.Button(btn_frame, text="View Past Bills", width=32, bg="#1976d2", fg="white", command=view_past_bills).grid(row=3, column=0, columnspan=2, pady=5)

# -------- LISTBOX --------
listbox = tk.Listbox(root, width=95, height=12, bg="#1e1e1e", fg="white", exportselection=False)
listbox.pack(pady=15)

listbox.bind("<<ListboxSelect>>", on_select)

root.mainloop()