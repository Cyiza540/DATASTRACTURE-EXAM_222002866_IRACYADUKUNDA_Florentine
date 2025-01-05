import tkinter as tk
from tkinter import messagebox

# Binary Tree Node class
class OrderNode:
    def __init__(self, order_id, customer_name, phone_number, design):
        self.order_id = order_id
        self.customer_name = customer_name
        self.phone_number = phone_number
        self.design = design
        self.left = None
        self.right = None

# Binary Tree class
class OrderBinaryTree:
    def __init__(self):
        self.root = None

    def insert(self, order_id, customer_name, phone_number, design):
        new_node = OrderNode(order_id, customer_name, phone_number, design)
        if not self.root:
            self.root = new_node
        else:
            self._insert_recursive(self.root, new_node)

    def _insert_recursive(self, current, new_node):
        if new_node.order_id < current.order_id:
            if current.left:
                self._insert_recursive(current.left, new_node)
            else:
                current.left = new_node
        else:
            if current.right:
                self._insert_recursive(current.right, new_node)
            else:
                current.right = new_node

    def search(self, order_id):
        return self._search_recursive(self.root, order_id)

    def _search_recursive(self, current, order_id):
        if not current:
            return None
        if current.order_id == order_id:
            return current
        elif order_id < current.order_id:
            return self._search_recursive(current.left, order_id)
        else:
            return self._search_recursive(current.right, order_id)

# Initialize Binary Tree
order_tree = OrderBinaryTree()

# Array for t-shirt sizes
tshirt_sizes = ["Small", "Medium", "Large", "X-Large"]

# Array for t-shirt designs
tshirt_designs = ["Classic", "Modern", "Graphic", "Custom"]

# Tkinter GUI
class TShirtOrderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Custom T-Shirt Design & Order System")

        # Maximize the window but keep the title visible
        self.root.state('zoomed')

        # Set background color
        self.root.configure(bg="#e6f2ff")  # Lighter blue

        # Styles for labels and buttons
        label_style = {"font": ("Arial", 16, "bold"), "bg": "#e6f2ff"}
        button_style = {"font": ("Arial", 14, "bold"), "bg": "#00509e", "fg": "white", "relief": "raised", "bd": 5}

        # Customer Name
        tk.Label(root, text="Customer Name:", **label_style).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.customer_name_entry = tk.Entry(root, font=("Arial", 14))
        self.customer_name_entry.grid(row=0, column=1, padx=10, pady=10)

        # Phone Number
        tk.Label(root, text="Phone Number:", **label_style).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.phone_number_entry = tk.Entry(root, font=("Arial", 14))
        self.phone_number_entry.grid(row=1, column=1, padx=10, pady=10)

        # T-Shirt Design
        tk.Label(root, text="Select T-Shirt Design:", **label_style).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.design_var = tk.StringVar(value=tshirt_designs[0])
        self.design_menu = tk.OptionMenu(root, self.design_var, *tshirt_designs)
        self.design_menu.configure(font=("Arial", 14))
        self.design_menu.grid(row=2, column=1, padx=10, pady=10)

        # T-Shirt Size
        tk.Label(root, text="Select T-Shirt Size:", **label_style).grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.size_var = tk.StringVar(value=tshirt_sizes[0])
        self.size_menu = tk.OptionMenu(root, self.size_var, *tshirt_sizes)
        self.size_menu.configure(font=("Arial", 14))
        self.size_menu.grid(row=3, column=1, padx=10, pady=10)

        # Buttons
        tk.Button(root, text="Place Order", command=self.place_order, **button_style).grid(row=4, column=0, columnspan=2, pady=10)
        tk.Button(root, text="Search Order", command=self.search_order, **button_style).grid(row=5, column=0, columnspan=2, pady=10)

        # Search Order ID
        tk.Label(root, text="Order ID to Search:", **label_style).grid(row=6, column=0, padx=10, pady=10, sticky="w")
        self.search_order_entry = tk.Entry(root, font=("Arial", 14))
        self.search_order_entry.grid(row=6, column=1, padx=10, pady=10)

        # Output Box
        self.output_box = tk.Text(root, height=10, width=60, font=("Arial", 14), bg="#d6eaf8")
        self.output_box.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

        self.order_id_counter = 1  # To generate unique order IDs

        # Bind the window close event to the confirmation function
        self.root.protocol("WM_DELETE_WINDOW", self.close_window)

    def place_order(self):
        customer_name = self.customer_name_entry.get()
        phone_number = self.phone_number_entry.get()
        design = self.design_var.get()
        size = self.size_var.get()

        if not customer_name or not phone_number:
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return

        if len(phone_number) != 10 or not phone_number.startswith(("078", "079", "073", "072")) or not phone_number.isdigit():
            messagebox.showerror("Invalid Phone Number", "Phone number must be 10 digits and start with 078, 079, 073, or 072.")
            return

        order_id = self.order_id_counter
        self.order_id_counter += 1

        order_tree.insert(order_id, customer_name, phone_number, f"{design} ({size})")
        self.output_box.insert(tk.END, f"[Order Placed] ID {order_id}, {customer_name}, {phone_number}, {design} ({size})\n", "order")

        # Clear input fields
        self.customer_name_entry.delete(0, tk.END)
        self.phone_number_entry.delete(0, tk.END)

    def search_order(self):
        try:
            order_id = int(self.search_order_entry.get())
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter a valid Order ID.")
            return

        order = order_tree.search(order_id)
        if order:
            self.output_box.insert(tk.END, f"[Order Found] ID {order.order_id}, {order.customer_name}, {order.phone_number}, {order.design}\n", "search")
        else:
            self.output_box.insert(tk.END, f"[Search Failed] Order ID {order_id} not found.\n", "search")

        self.search_order_entry.delete(0, tk.END)

    def close_window(self):
        # Confirmation message when trying to close the window
        if messagebox.askyesno("Quit", "Do you want to quit?"):
            self.root.quit()

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = TShirtOrderApp(root)

    # Style configuration for output box tags
    app.output_box.tag_configure("order", foreground="green")
    app.output_box.tag_configure("search", foreground="blue")

    root.mainloop()
