import mysql.connector
from tkinter import *
from tkinter import messagebox, ttk

# Database connection parameters
DB_HOST = "localhost"
DB_USER = "root"
DB_PASS = "jocelyn1530"
DB_NAME = "ecommerce"

class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME
        )
        self.cursor = self.connection.cursor()

    def close(self):
        self.cursor.close()
        self.connection.close()

    def add_product(self, name, description, price):
        self.cursor.execute("INSERT INTO products (name, description, price) VALUES (%s, %s, %s)", 
                            (name, description, price))
        self.connection.commit()

    def update_product(self, product_id, name, description, price):
        self.cursor.execute("UPDATE products SET name=%s, description=%s, price=%s WHERE id=%s", 
                            (name, description, price, product_id))
        self.connection.commit()

    def delete_product(self, product_id):
        self.cursor.execute("DELETE FROM products WHERE id=%s", (product_id,))
        self.connection.commit()

    def fetch_products(self):
        self.cursor.execute("SELECT * FROM products")
        return self.cursor.fetchall()

    def search_products(self, search_term):
        self.cursor.execute("SELECT * FROM products WHERE name LIKE %s", (f"%{search_term}%",))
        return self.cursor.fetchall()

class ProductManagementSystem:
    def __init__(self, root, username):
        self.root = root
        self.username = username 
        self.root.title("Product Management System")
        self.root.geometry("800x600")
        self.db = Database()

        # UI Elements
        self.setup_ui()

    def setup_ui(self):
        # Title
        title_label = Label(self.root, text="Product Management System", font=("Helvetica", 24, "bold"), bg="#3F51B5", fg="white")
        title_label.pack(fill=X)

        self.product_tree = ttk.Treeview(self.root, columns=("ID", "Name", "Description", "Price"), show='headings')
        self.product_tree.heading("ID", text="Product ID")
        self.product_tree.heading("Name", text="Product Name")
        self.product_tree.heading("Description", text="Description")
        self.product_tree.heading("Price", text="Price")
        self.product_tree.pack(fill=X, padx=20, pady=20)

        # Center-align data in each column
        self.product_tree.column("ID", anchor="center")
        self.product_tree.column("Name", anchor="center")
        self.product_tree.column("Description", anchor="center")
        self.product_tree.column("Price", anchor="center")
    
        self.load_products()

        # Entry fields for product details
        self.product_id = IntVar()
        self.name = StringVar()
        self.description = StringVar()
        self.price = StringVar()

        form_frame = Frame(self.root, bg="#E8EAF6")
        form_frame.pack(pady=10)

        # Input Fields
        Label(form_frame, text="Product ID", bg="#E8EAF6").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        Entry(form_frame, textvariable=self.product_id, state='readonly', width=30).grid(row=0, column=1, padx=10, pady=5)

        Label(form_frame, text="Name", bg="#E8EAF6").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        Entry(form_frame, textvariable=self.name, width=30).grid(row=1, column=1, padx=10, pady=5)

        Label(form_frame, text="Description", bg="#E8EAF6").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        Entry(form_frame, textvariable=self.description, width=30).grid(row=2, column=1, padx=10, pady=5)

        Label(form_frame, text="Price", bg="#E8EAF6").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        Entry(form_frame, textvariable=self.price, width=30).grid(row=3, column=1, padx=10, pady=5)

        # Buttons
        button_frame = Frame(form_frame, bg="#E8EAF6")
        button_frame.grid(row=4, columnspan=2, pady=10)

        Button(button_frame, text="Add Product", command=self.add_product, bg="#4CAF50", fg="white").grid(row=0, column=0, padx=5)
        Button(button_frame, text="Update Product", command=self.update_product, bg="#2196F3", fg="white").grid(row=0, column=1, padx=5)
        Button(button_frame, text="Delete Product", command=self.delete_product, bg="#F44336", fg="white").grid(row=0, column=2, padx=5)

        self.product_tree.bind('<ButtonRelease-1>', self.on_tree_select)

        if self.username != "admin":
            for widget in form_frame.winfo_children():
                widget.grid_forget()
            Label(form_frame, text="You are logged in as a Regular User.", bg="#E8EAF6").grid(row=0, column=0, columnspan=2)
            order_button = Button(form_frame, text="Order Product", command=self.order_product, bg="#FFC107", fg="white")
            order_button.grid(row=4, column=0, pady=10)
            
            # Logout button (visible to all users)
            logout_button = Button(form_frame, text="Logout", command=self.logout, bg="#F44336", fg="white")
            logout_button.grid(row=4, column=1, pady=10)

        else:
            # Logout button for admin
            logout_button = Button(self.root, text="Logout", command=self.logout, bg="#F44336", fg="white")
            logout_button.pack(pady=10, side="bottom")

        self.product_tree.focus_set()

    def load_products(self):
        for row in self.product_tree.get_children():
            self.product_tree.delete(row)
        products = self.db.fetch_products()
        for product in products:
            self.product_tree.insert("", "end", values=product)

    def on_tree_select(self,_):
        selected_item = self.product_tree.selection()[0]
        item_values = self.product_tree.item(selected_item, "values")
        self.product_id.set(item_values[0])
        self.name.set(item_values[1])
        self.description.set(item_values[2])
        self.price.set(item_values[3])

    def add_product(self):
        self.db.add_product(self.name.get(), self.description.get(), self.price.get())
        self.load_products()

    def update_product(self):
        self.db.update_product(self.product_id.get(), self.name.get(), self.description.get(), self.price.get())
        self.load_products()

    def delete_product(self):
        self.db.delete_product(self.product_id.get())
        self.load_products()   

    def logout(self):
        self.root.destroy()
        login_root = Tk()
        ProductManagementSystemLogin(login_root)
        login_root.mainloop()

    def order_product(self):
        selected_item = self.product_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a product to order")
            return
        item_values = self.product_tree.item(selected_item, "values")
        print(item_values)

        if len(item_values) >= 4:  # Adjust based on the actual number of values
            product_id, product_name, description, price = item_values[:4]  
        else:
            messagebox.showerror("Error", "Unexpected product details format.")
            return
        
        # Open Order Window
        self.order_window = Toplevel(self.root)
        self.order_window.title("Order Product")
        self.order_window.geometry("400x400")

        Label(self.order_window, text=f"Order: {product_name}", font=("Helvetica", 14, "bold")).pack(pady=10)
        Label(self.order_window, text=f"Product Name: {product_name}", font=("Helvetica", 14, "bold")).pack(pady=10)
        Label(self.order_window, text=f"Description: {description}", wraplength=350, justify="left").pack(pady=5)
        Label(self.order_window, text=f"Price: ${price}", font=("Helvetica", 12)).pack(pady=5)
        Label(self.order_window, text="Quantity").pack(pady=5)

        quantity_var = IntVar(value=1)
        quantity_entry = Entry(self.order_window, textvariable=quantity_var, width=5)
        quantity_entry.pack()

        Label(self.order_window, text="Select Payment Method").pack(pady=10)
        
        payment_methods = ["Net Banking", "Credit Card", "Debit Card", "Cash"]
        self.payment_var = StringVar(value=payment_methods[0])
        
        payment_menu = OptionMenu(self.order_window, self.payment_var, *payment_methods)
        payment_menu.pack(pady=10)

        place_order_button = Button(self.order_window, text="Place Order", command=self.place_order, bg="#FFC107", fg="white")
        place_order_button.pack(pady=20)

    def place_order(self):
        # Logic for placing the order with selected payment method
        selected_payment = self.payment_var.get()
        messagebox.showinfo("Order Placed", f"Order has been placed successfully with {selected_payment} payment method.")
        self.order_window.destroy()


class ProductManagementSystemLogin:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("400x350")

        # Material Design style
        self.root.configure(bg="#3F51B5")

        self.username = StringVar()
        self.password = StringVar()

        # Title
        Label(self.root, text="Login", font=("Helvetica", 24, "bold"), bg="#3F51B5", fg="white").pack(pady=30)

        # Input Fields with floating labels
        username_frame = Frame(self.root, bg="#3F51B5")
        username_frame.pack(pady=5)
        username_label = Label(username_frame, text="Username", fg="white", bg="#3F51B5")
        username_label.grid(row=0, column=0, sticky="w")
        self.username_entry = Entry(username_frame, textvariable=self.username, width=30)
        self.username_entry.grid(row=1, column=0)

        password_frame = Frame(self.root, bg="#3F51B5")
        password_frame.pack(pady=5)
        password_label = Label(password_frame, text="Password", fg="white", bg="#3F51B5")
        password_label.grid(row=0, column=0, sticky="w")
        self.password_entry = Entry(password_frame, textvariable=self.password, show="*", width=30)
        self.password_entry.grid(row=1, column=0)

        Button(self.root, text="Login", command=self.login, bg="white", fg="#3F51B5", font=("Helvetica", 14)).pack(pady=30)


    def login(self):
        username = self.username.get()
        password = self.password.get()

        if username == "admin" and password == "joce":
            self.root.destroy()
            admin_root = Tk()
            ProductManagementSystem(admin_root, "admin")
            admin_root.mainloop()
        elif username == "user" and password == "indhu":
            self.root.destroy()
            user_root = Tk()
            ProductManagementSystem(user_root, "user")
            user_root.mainloop()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")


if __name__ == "__main__":
    root = Tk()
    app = ProductManagementSystemLogin(root)
    root.mainloop()
