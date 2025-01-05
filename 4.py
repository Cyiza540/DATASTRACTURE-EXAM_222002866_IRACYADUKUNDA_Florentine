import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class Node:
    def __init__(self, orderID, customerName, orderDetails):
        self.orderID = orderID
        self.customerName = customerName
        self.orderDetails = orderDetails
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def insert(self, root, orderID, customerName, orderDetails, maxOrders):
        if not root:
            return Node(orderID, customerName, orderDetails)
        
        if orderID < root.orderID:
            root.left = self.insert(root.left, orderID, customerName, orderDetails, maxOrders)
        else:
            root.right = self.insert(root.right, orderID, customerName, orderDetails, maxOrders)

        root.height = 1 + max(self.getHeight(root.left), self.getHeight(root.right))
        balance = self.getBalance(root)

        if balance > 1 and orderID < root.left.orderID:
            return self.rotateRight(root)

        if balance < -1 and orderID > root.right.orderID:
            return self.rotateLeft(root)

        if balance > 1 and orderID > root.left.orderID:
            root.left = self.rotateLeft(root.left)
            return self.rotateRight(root)

        if balance < -1 and orderID < root.right.orderID:
            root.right = self.rotateRight(root.right)
            return self.rotateLeft(root)

        # Check for max orders and remove the oldest (smallest orderID)
        if self.countNodes(root) > maxOrders:
            root = self.removeOldest(root)

        return root

    def rotateLeft(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.getHeight(z.left), self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left), self.getHeight(y.right))
        return y

    def rotateRight(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self.getHeight(z.left), self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left), self.getHeight(y.right))
        return y

    def getHeight(self, root):
        if not root:
            return 0
        return root.height

    def getBalance(self, root):
        if not root:
            return 0
        return self.getHeight(root.left) - self.getHeight(root.right)

    def preOrder(self, root, result):
        if not root:
            return
        result.append((root.orderID, root.customerName, root.orderDetails))
        self.preOrder(root.left, result)
        self.preOrder(root.right, result)

    def countNodes(self, root):
        if not root:
            return 0
        return 1 + self.countNodes(root.left) + self.countNodes(root.right)

    def removeOldest(self, root):
        if root.left:
            root.left = self.removeOldest(root.left)
        else:
            root = root.right
        return root

class AVLTreeApp:
    def __init__(self, root, maxOrders=5):
        self.root = root
        self.maxOrders = maxOrders
        self.tree = AVLTree()
        self.window = tk.Tk()
        self.window.title("Online Custom T-Shirt Order System")

        # Maximize the window
        self.window.state('zoomed')
        
        self.window.config(bg="#f4f4f9")
        self.create_widgets()
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        # Title Label
        self.title_label = tk.Label(self.window, text="AVL Tree - Custom T-Shirt Orders", font=("Arial", 20, 'bold'), bg="#f4f4f9", fg="#333")
        self.title_label.grid(row=0, column=0, columnspan=2, pady=20)

        # Order ID Input
        self.order_id_label = tk.Label(self.window, text="Order ID:", font=("Arial", 14), bg="#f4f4f9", fg="#555")
        self.order_id_label.grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.order_id_entry = tk.Entry(self.window, font=("Arial", 14), width=30)
        self.order_id_entry.grid(row=1, column=1, padx=10, pady=10)

        # Customer Name Input
        self.customer_name_label = tk.Label(self.window, text="Customer Name:", font=("Arial", 14), bg="#f4f4f9", fg="#555")
        self.customer_name_label.grid(row=2, column=0, padx=10, pady=10, sticky='e')
        self.customer_name_entry = tk.Entry(self.window, font=("Arial", 14), width=30)
        self.customer_name_entry.grid(row=2, column=1, padx=10, pady=10)

        # Order Details Input
        self.order_details_label = tk.Label(self.window, text="Order Details:", font=("Arial", 14), bg="#f4f4f9", fg="#555")
        self.order_details_label.grid(row=3, column=0, padx=10, pady=10, sticky='e')
        self.order_details_entry = tk.Entry(self.window, font=("Arial", 14), width=30)
        self.order_details_entry.grid(row=3, column=1, padx=10, pady=10)

        # Insert Order Button
        self.insert_button = tk.Button(self.window, text="Insert Order", font=("Arial", 14), bg="#4CAF50", fg="white", command=self.insert_order)
        self.insert_button.grid(row=4, column=0, columnspan=2, pady=20)

        # Show AVL Tree Button
        self.show_button = tk.Button(self.window, text="Show Orders", font=("Arial", 14), bg="#2196F3", fg="white", command=self.show_tree)
        self.show_button.grid(row=5, column=0, columnspan=2, pady=20)

        # Tree Display Area (Table for Orders)
        self.tree_display = ttk.Treeview(self.window, columns=("Order ID", "Customer Name", "Order Details"), show="headings", height=10)
        self.tree_display.heading("Order ID", text="Order ID")
        self.tree_display.heading("Customer Name", text="Customer Name")
        self.tree_display.heading("Order Details", text="Order Details")
        self.tree_display.grid(row=6, column=0, columnspan=2, pady=20, padx=10)

        # Style for the Treeview
        self.tree_display.tag_configure('oddrow', background="#f9f9f9")
        self.tree_display.tag_configure('evenrow', background="#f1f1f1")

    def insert_order(self):
        try:
            order_id = int(self.order_id_entry.get())
            customer_name = self.customer_name_entry.get().strip()
            order_details = self.order_details_entry.get().strip()

            if not customer_name or not order_details:
                raise ValueError("Customer name and order details cannot be empty")

            self.root = self.tree.insert(self.root, order_id, customer_name, order_details, self.maxOrders)
            messagebox.showinfo("Success", "Order inserted successfully!")
            self.order_id_entry.delete(0, tk.END)
            self.customer_name_entry.delete(0, tk.END)
            self.order_details_entry.delete(0, tk.END)
        except ValueError as ve:
            messagebox.showerror("Input Error", f"Invalid input: {ve}")

    def show_tree(self):
        # Clear existing rows in Treeview
        for row in self.tree_display.get_children():
            self.tree_display.delete(row)

        result = []
        self.tree.preOrder(self.root, result)

        # Insert rows in Treeview for each order
        for index, order in enumerate(result):
            row_tag = 'oddrow' if index % 2 == 0 else 'evenrow'
            self.tree_display.insert("", tk.END, values=(order[0], order[1], order[2]), tags=(row_tag,))

    def on_closing(self):
        if messagebox.askyesno("Quit", "Do you want to quit?"):
            self.window.destroy()

    def run(self):
        self.window.mainloop()

# Run the application
if __name__ == "__main__":
    root_node = None
    app = AVLTreeApp(root_node)
    app.run()
