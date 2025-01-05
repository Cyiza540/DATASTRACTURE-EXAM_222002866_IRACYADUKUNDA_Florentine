import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Node class to represent each order in the AVL Tree
class Node:
    def __init__(self, orderID, customerName, orderDetails):
        self.orderID = orderID
        self.customerName = customerName
        self.orderDetails = orderDetails
        self.left = None
        self.right = None
        self.height = 1

# AVL Tree class to handle order insertions and deletions
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

        # Balancing the tree after insertion
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

        # If the number of orders exceeds the limit, remove the oldest order
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

# GUI class to display the orders and interact with the AVL tree
class AVLTreeApp:
    def __init__(self, root, maxOrders=5):
        self.root = root
        self.maxOrders = maxOrders
        self.tree = AVLTree()
        self.window = tk.Tk()
        self.window.title("Online Custom T-Shirt Order System")
        self.window.state('zoomed')  # Maximize the window
        self.window.config(bg="#f4f4f9")
        self.create_widgets()
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        # Input fields for order details
        self.label_orderID = tk.Label(self.window, text="Order ID:", bg="#f4f4f9", font=("Arial", 12))
        self.label_orderID.grid(row=0, column=0, padx=10, pady=10)
        self.entry_orderID = tk.Entry(self.window, font=("Arial", 12))
        self.entry_orderID.grid(row=0, column=1, padx=10, pady=10)

        self.label_customerName = tk.Label(self.window, text="Customer Name:", bg="#f4f4f9", font=("Arial", 12))
        self.label_customerName.grid(row=1, column=0, padx=10, pady=10)
        self.entry_customerName = tk.Entry(self.window, font=("Arial", 12))
        self.entry_customerName.grid(row=1, column=1, padx=10, pady=10)

        self.label_orderDetails = tk.Label(self.window, text="Order Details:", bg="#f4f4f9", font=("Arial", 12))
        self.label_orderDetails.grid(row=2, column=0, padx=10, pady=10)
        self.entry_orderDetails = tk.Entry(self.window, font=("Arial", 12))
        self.entry_orderDetails.grid(row=2, column=1, padx=10, pady=10)

        # Button to add the order to the tree
        self.add_order_button = tk.Button(self.window, text="Add Order", command=self.add_order, font=("Arial", 12), bg="#4CAF50", fg="white")
        self.add_order_button.grid(row=3, column=0, columnspan=2, pady=20)

        # Treeview to display orders
        self.tree_display = ttk.Treeview(self.window, columns=("Order ID", "Customer Name", "Order Details"), show="headings", height=10)
        self.tree_display.heading("Order ID", text="Order ID")
        self.tree_display.heading("Customer Name", text="Customer Name")
        self.tree_display.heading("Order Details", text="Order Details")
        self.tree_display.grid(row=6, column=0, columnspan=2, pady=20, padx=10)

    def add_order(self):
        orderID = self.entry_orderID.get()
        customerName = self.entry_customerName.get()
        orderDetails = self.entry_orderDetails.get()

        if orderID and customerName and orderDetails:
            self.root = self.tree.insert(self.root, int(orderID), customerName, orderDetails, self.maxOrders)
            self.show_tree()  # Refresh the tree display
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields")

        # Clear the input fields after submission
        self.entry_orderID.delete(0, tk.END)
        self.entry_customerName.delete(0, tk.END)
        self.entry_orderDetails.delete(0, tk.END)

    def show_tree(self):
        # Clear the treeview
        for row in self.tree_display.get_children():
            self.tree_display.delete(row)

        # Fetch orders from the AVL tree and display them
        result = []
        self.tree.preOrder(self.root, result)
        
        for order in result:
            self.tree_display.insert("", "end", values=(order[0], order[1], order[2]))

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
