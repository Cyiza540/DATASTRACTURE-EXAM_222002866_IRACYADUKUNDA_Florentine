import tkinter as tk
from tkinter import messagebox

class Node:
    def __init__(self, orderID, customerName):
        self.orderID = orderID
        self.customerName = customerName
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def insert(self, root, orderID, customerName):
        if not root:
            return Node(orderID, customerName)
        
        if orderID < root.orderID:
            root.left = self.insert(root.left, orderID, customerName)
        else:
            root.right = self.insert(root.right, orderID, customerName)
        
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
        result.append(f"Order ID: {root.orderID}, Customer: {root.customerName}")
        self.preOrder(root.left, result)
        self.preOrder(root.right, result)

class AVLTreeApp:
    def __init__(self, root):
        self.root = root
        self.tree = AVLTree()
        self.window = tk.Tk()
        self.window.title("Online Custom T-Shirt Order System")
        
        # Maximize the window
        self.window.state('zoomed')
        
        self.window.config(bg="#f0f0f0")
        self.create_widgets()
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        # Title Label
        self.title_label = tk.Label(self.window, text="AVL Tree - Custom T-Shirt Orders", font=("Arial", 18), bg="#f0f0f0")
        self.title_label.grid(row=0, column=0, columnspan=2, pady=20)

        # Order ID Input
        self.order_id_label = tk.Label(self.window, text="Order ID:", font=("Arial", 12), bg="#f0f0f0")
        self.order_id_label.grid(row=1, column=0, padx=10, pady=5)
        self.order_id_entry = tk.Entry(self.window, font=("Arial", 12))
        self.order_id_entry.grid(row=1, column=1, padx=10, pady=5)

        # Customer Name Input
        self.customer_name_label = tk.Label(self.window, text="Customer Name:", font=("Arial", 12), bg="#f0f0f0")
        self.customer_name_label.grid(row=2, column=0, padx=10, pady=5)
        self.customer_name_entry = tk.Entry(self.window, font=("Arial", 12))
        self.customer_name_entry.grid(row=2, column=1, padx=10, pady=5)

        # Insert Order Button
        self.insert_button = tk.Button(self.window, text="Insert Order", font=("Arial", 12), bg="#4CAF50", fg="white", command=self.insert_order)
        self.insert_button.grid(row=3, column=0, columnspan=2, pady=20)

        # Show AVL Tree Button
        self.show_button = tk.Button(self.window, text="Show AVL Tree", font=("Arial", 12), bg="#2196F3", fg="white", command=self.show_tree)
        self.show_button.grid(row=4, column=0, columnspan=2, pady=20)

        # Tree Display Area
        self.tree_display = tk.Label(self.window, text="", font=("Arial", 12), bg="#f0f0f0", justify=tk.LEFT)
        self.tree_display.grid(row=5, column=0, columnspan=2, pady=10)

    def insert_order(self):
        try:
            order_id = int(self.order_id_entry.get())
            customer_name = self.customer_name_entry.get().strip()

            if not customer_name:
                raise ValueError("Customer name cannot be empty")

            self.root = self.tree.insert(self.root, order_id, customer_name)
            messagebox.showinfo("Success", "Order inserted successfully!")
            self.order_id_entry.delete(0, tk.END)
            self.customer_name_entry.delete(0, tk.END)
        except ValueError as ve:
            messagebox.showerror("Input Error", f"Invalid input: {ve}")

    def show_tree(self):
        result = []
        self.tree.preOrder(self.root, result)
        tree_output = "\n".join(result)
        self.tree_display.config(text=tree_output if tree_output else "No orders yet.")

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
