import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# TreeNode class for hierarchical categories with more fields (e.g., "Name", "Description", "Price Range")
class TreeNode:
    def __init__(self, name, description="", price_range=""):
        self.name = name
        self.description = description
        self.price_range = price_range
        self.children = []

    def add_child(self, child):
        self.children.append(child)

# HierarchicalTree class to handle categories
class HierarchicalTree:
    def __init__(self):
        self.root = TreeNode("All Orders")
        self.category_nodes = {"All Orders": self.root}

    def add_category(self, parent, name, description, price_range):
        new_node = TreeNode(name, description, price_range)
        parent.add_child(new_node)
        self.category_nodes[name] = new_node
        return new_node

    def display_tree(self, node, parent_item=""):
        if node is not None:
            parent_item = tree_view.insert(parent_item, "end", text=node.name, open=True)
            tree_view.item(parent_item, values=(node.description, node.price_range))  # Show description and price range
            for child in node.children:
                self.display_tree(child, parent_item)

# Main application class
class AVLTreeApp:
    def __init__(self):
        self.hierarchical_tree = HierarchicalTree()
        self.window = tk.Tk()
        self.window.title("T-Shirt Order System")
        self.window.state('zoomed')  # Maximize the window
        self.window.config(bg="#f4f4f9")
        self.create_widgets()
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        # Input fields for category details
        self.label_category_name = tk.Label(self.window, text="Category Name:", bg="#f4f4f9", font=("Arial", 12))
        self.label_category_name.grid(row=0, column=0, padx=10, pady=10)
        self.entry_category_name = tk.Entry(self.window, font=("Arial", 12))
        self.entry_category_name.grid(row=0, column=1, padx=10, pady=10)

        self.label_description = tk.Label(self.window, text="Description:", bg="#f4f4f9", font=("Arial", 12))
        self.label_description.grid(row=1, column=0, padx=10, pady=10)
        self.entry_description = tk.Entry(self.window, font=("Arial", 12))
        self.entry_description.grid(row=1, column=1, padx=10, pady=10)

        self.label_price_range = tk.Label(self.window, text="Price Range:", bg="#f4f4f9", font=("Arial", 12))
        self.label_price_range.grid(row=2, column=0, padx=10, pady=10)
        self.entry_price_range = tk.Entry(self.window, font=("Arial", 12))
        self.entry_price_range.grid(row=2, column=1, padx=10, pady=10)

        # Parent category selector
        self.label_parent_category = tk.Label(self.window, text="Parent Category:", bg="#f4f4f9", font=("Arial", 12))
        self.label_parent_category.grid(row=3, column=0, padx=10, pady=10)
        self.parent_category_combobox = ttk.Combobox(self.window, font=("Arial", 12))
        self.parent_category_combobox.grid(row=3, column=1, padx=10, pady=10)
        self.parent_category_combobox['values'] = ['All Orders']  # Default value is only the root
        self.parent_category_combobox.set('All Orders')  # Default value

        # Button to add new category
        self.add_category_button = tk.Button(self.window, text="Add Category", command=self.add_category, font=("Arial", 12), bg="#4CAF50", fg="white")
        self.add_category_button.grid(row=4, column=0, columnspan=2, pady=20)

        # Treeview to display hierarchical data
        global tree_view
        tree_view = ttk.Treeview(self.window, columns=("Description", "Price Range"), height=10)
        tree_view.heading("Description", text="Description")
        tree_view.heading("Price Range", text="Price Range")
        tree_view.grid(row=5, column=0, columnspan=2, pady=20, padx=10, sticky="nsew")

        # Display initial hierarchical structure
        self.hierarchical_tree.display_tree(self.hierarchical_tree.root)

    def add_category(self):
        category_name = self.entry_category_name.get()
        description = self.entry_description.get()
        price_range = self.entry_price_range.get()
        parent_category = self.parent_category_combobox.get()

        if category_name and description and price_range:
            if parent_category == 'All Orders':
                parent_node = self.hierarchical_tree.root
            else:
                parent_node = self.get_category_node(parent_category)

            if parent_node:
                new_node = self.hierarchical_tree.add_category(parent_node, category_name, description, price_range)
                self.hierarchical_tree.display_tree(self.hierarchical_tree.root)  # Refresh the tree display
                self.update_parent_category_combobox()  # Update the parent category combobox
            else:
                messagebox.showwarning("Parent Not Found", "The selected parent category does not exist.")
        else:
            messagebox.showwarning("Input Error", "Please fill in all the fields")

    def get_category_node(self, category_name):
        # Return the category node from the hierarchical tree
        return self.hierarchical_tree.category_nodes.get(category_name)

    def update_parent_category_combobox(self):
        # Update the parent category combobox with all existing categories
        self.parent_category_combobox['values'] = list(self.hierarchical_tree.category_nodes.keys())

    def on_closing(self):
        if messagebox.askyesno("Quit", "Do you want to quit?"):
            self.window.destroy()

    def run(self):
        self.window.mainloop()

# Run the application
if __name__ == "__main__":
    app = AVLTreeApp()
    app.run()
