import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Define Order class with attributes like order_id, customer_name, priority
class Order:
    def __init__(self, order_id, customer_name, priority):
        self.order_id = order_id
        self.customer_name = customer_name
        self.priority = priority

# Merge Sort function to sort orders by priority
def merge_sort(orders):
    if len(orders) > 1:
        mid = len(orders) // 2  # Find the middle point
        left_half = orders[:mid]
        right_half = orders[mid:]

        # Recursively split and sort the halves
        merge_sort(left_half)
        merge_sort(right_half)

        i = j = k = 0

        # Merge the two halves
        while i < len(left_half) and j < len(right_half):
            if left_half[i].priority < right_half[j].priority:  # Sort in descending order
                orders[k] = left_half[i]
                i += 1
            else:
                orders[k] = right_half[j]
                j += 1
            k += 1

        # If there are remaining elements in left_half
        while i < len(left_half):
            orders[k] = left_half[i]
            i += 1
            k += 1

        # If there are remaining elements in right_half
        while j < len(right_half):
            orders[k] = right_half[j]
            j += 1
            k += 1

# Main application class
class AVLTreeApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("T-Shirt Order System")
        self.window.state('zoomed')  # Maximize the window
        self.window.config(bg="#f4f4f9")
        self.orders = [
            Order(101, "Alice", 2),
            Order(102, "Bob", 5),
            Order(103, "Charlie", 3),
            Order(104, "David", 1),
            Order(105, "Eve", 4)
        ]
        self.create_widgets()
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        # Display Orders Button
        self.display_orders_button = tk.Button(self.window, text="Display Sorted Orders", command=self.display_sorted_orders, font=("Arial", 12), bg="#4CAF50", fg="white")
        self.display_orders_button.grid(row=0, column=0, pady=20)

        # Treeview to display sorted orders
        global tree_view
        tree_view = ttk.Treeview(self.window, columns=("Order ID", "Customer Name", "Priority"), height=10)
        tree_view.heading("Order ID", text="Order ID")
        tree_view.heading("Customer Name", text="Customer Name")
        tree_view.heading("Priority", text="Priority")
        tree_view.grid(row=1, column=0, columnspan=2, pady=20, padx=10, sticky="nsew")

    def display_sorted_orders(self):
        # Sort orders based on priority using Merge Sort
        merge_sort(self.orders)

        # Clear the treeview before displaying
        for row in tree_view.get_children():
            tree_view.delete(row)

        # Insert sorted orders into the treeview
        for order in self.orders:
            tree_view.insert("", "end", values=(order.order_id, order.customer_name, order.priority))

    def on_closing(self):
        if messagebox.askyesno("Quit", "Do you want to quit?"):
            self.window.destroy()

    def run(self):
        self.window.mainloop()

# Run the application
if __name__ == "__main__":
    app = AVLTreeApp()
    app.run()
