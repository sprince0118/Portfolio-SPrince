import tkinter as tk
import json
from tkinter import simpledialog

class TreeApp:

    def __init__(self, master):
        self.master = master
        self.master.title("AVL Tree Traversal V2")
        
        # Get screen dimensions
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        # Set window size based on screen dimensions
        window_width = int(screen_width * 0.8)
        window_height = int(screen_height * 0.8)
        self.master.geometry(f"{window_width}x{window_height}")

        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(self.master, bg="white")
        self.canvas.grid(row=0, column=0, sticky="nsew")

        try:
            with open("rankTreeData.txt", "r") as reader:
                data = json.load(reader)
                self.mainTree = data.get('mainTree', {})
                self.root = data.get('root', "")
        except FileNotFoundError:
            with open("rankTreeData.txt", "w") as writer:
                json.dump({"mainTree": {}, "root": ""}, writer)
                self.mainTree = {}
                self.root = ""
        except json.JSONDecodeError:
            self.mainTree = {}
            self.root = ""

        self.display_tree()
        
        # Add buttons for in-order traversal and top 10 items
        # Add buttons for in-order traversal and top 10 items
        button_frame = tk.Frame(self.master)
        button_frame.grid(row=1, column=0, sticky="ew")
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

        self.additem_button = tk.Button(button_frame, text="Add Item", command=self.input_box)
        self.additem_button.grid(row=1, column=0, pady=10, padx=10, sticky="ew")

        self.top_10_button = tk.Button(button_frame, text="Remove Item", command=self.removeDialogue)
        self.top_10_button.grid(row=1, column=1, pady=10, padx=10, sticky="ew")

        self.traversal_button = tk.Button(button_frame, text="In-Order Traversal", command=self.traversal_in_order)
        self.traversal_button.grid(row=2, column=0, pady=10, padx=10, sticky="ew")

        self.top_10_button = tk.Button(button_frame, text="Top 10 Items", command=self.top_10_items)
        self.top_10_button.grid(row=2, column=1, pady=10, padx=10, sticky="ew")

        # Bind the configure event to handle window resizing
        self.master.bind("<Configure>", self.on_resize)


    def on_resize(self, event):
        self.canvas.config(width=event.width, height=event.height)
        self.display_tree()
  

    def removeDialogue(self):
        new_item = simpledialog.askstring("Input", "Enter an item to remove:")
        if new_item:
            if new_item in self.mainTree:
                self.removeNode(new_item)
            else:
                tk.messagebox.showerror("Error", "This item does not exist in the tree!")
                self.removeDialogue()
                return


    def input_box(self):
        new_item = simpledialog.askstring("Input", "Enter an item to add to the tree:")
        if new_item:
            if not self.mainTree:
                self.mainTree[new_item] = ["", "", 1]  # Third element is height
                self.root = new_item
                self.display_tree()
                self.save_tree()
                self.input_box()
            else:
                self.add_node(self.root, new_item)
                self.display_tree()
                self.save_tree()

    def add_node(self, current_node, new_item):
        # Check if the new item already exists in the tree
        if new_item in self.mainTree:
            tk.messagebox.showerror("Error", "This item already exists in the tree!")
            self.input_box()
            return

        if current_node is None:
            # Set the new item as the root if the tree is empty
            self.mainTree[new_item] = ["", "", 1]
            self.root = new_item
            self.display_tree()
            self.save_tree()
            return

        if self.mainTree.get(current_node) is None:
            self.mainTree[current_node] = ["", "", 1]

        window = tk.Toplevel(self.master)
        window.title("Comparison")
        label = tk.Label(window, text=f"Is '{new_item}' better or worse than '{current_node}'?")
        label.pack()

        def on_better():
            if self.mainTree[current_node][1] == "":    #blank destination (add to tree)
                self.mainTree[current_node][1] = new_item
                self.mainTree[new_item] = ["", "", 1]
                self.balance_tree(current_node)
                self.save_tree()
                self.display_tree()
                window.destroy()
                self.input_box()
            else:                                       #child at destination (continue comparisons)
                window.destroy()
                self.add_node(self.mainTree[current_node][1], new_item)

        def on_worse():
            if self.mainTree[current_node][0] == "":
                self.mainTree[current_node][0] = new_item
                self.mainTree[new_item] = ["", "", 1]
                self.balance_tree(current_node)
                self.save_tree()
                self.display_tree()
                window.destroy()
                self.input_box()
            else:
                window.destroy()
                self.add_node(self.mainTree[current_node][0], new_item)

        better_button = tk.Button(window, text="Better", command=on_better)
        better_button.pack(side=tk.RIGHT, padx=10)

        worse_button = tk.Button(window, text="Worse", command=on_worse)
        worse_button.pack(side=tk.LEFT, padx=10)

    def save_tree(self):
        with open("rankTreeData.txt", "w") as writer:
            data = {"mainTree": self.mainTree, "root": self.root}
            json.dump(data, writer)

    def get_height(self, node):
        if node is None or node == "":
            return 0
        return self.mainTree[node][2]

    def update_height(self, node):
        if node is None or node == "":
            return
        left_height = self.get_height(self.mainTree[node][0])
        right_height = self.get_height(self.mainTree[node][1])
        self.mainTree[node][2] = 1 + max(left_height, right_height)

    def get_balance(self, node):
        if not node:
            return 0
        return self.get_height(self.mainTree[node][0]) - self.get_height(self.mainTree[node][1])

    def balance_tree(self, node):
        stack = []
        #print("New balance~~~~~~~~~~~~~")
        while node:
            stack.append(node)
            #print(f"Adding {node}")
            node = self.get_parent(node)

        while stack:
            node = stack.pop(0)
            #print(f"popping {node}")
            self.update_height(node)
            balance = self.get_balance(node)
            parent = self.get_parent(node)
            #print(f"Balance: {balance}")

            if balance > 1:
                if self.get_balance(self.mainTree[node][0]) >= 0:  # Left-Left
                    #print("LL")
                    node = self.update_parent(node, self.rotate_right(node), parent)
                else:  # Left-Right
                    #print("LR")
                    self.mainTree[node][0] = self.rotate_left(self.mainTree[node][0])
                    node = self.update_parent(node, self.rotate_right(node), parent)
            elif balance < -1:
                if self.get_balance(self.mainTree[node][1]) <= 0:  # Right-Right
                    #print("RR")
                    node = self.update_parent(node, self.rotate_left(node), parent)
                    
                else:  # Right-Left
                    #print("RL")
                    self.mainTree[node][1] = self.rotate_right(self.mainTree[node][1])
                    node = self.update_parent(node, self.rotate_left(node), parent)
                    

            parent = self.get_parent(node)
            if parent is None:
                self.root = node

    def update_parent(self, original, new, parent):
        #print(f"Original: {original}, new: {new}, parent: {parent}")
        if parent is not None:
            if self.mainTree.get(parent)[0] == original:   #left
                self.mainTree[parent][0] = new
                #print("Parent left changing")
            else:   #must be right
                self.mainTree[parent][1] = new
                #print("Parent right changing")
        return new


    def get_parent(self, child):
        for parent, children in self.mainTree.items():
            if children[0] == child or children[1] == child:
                return parent
        return None

    def rotate_left(self, z):
        #print(f"Rotating left {z}")
        y = self.mainTree[z][1]
        T2 = self.mainTree[y][0]

        # Perform rotation
        self.mainTree[y][0] = z
        self.mainTree[z][1] = T2

        # Update heights
        self.update_height(z)
        self.update_height(y)

        return y

    def rotate_right(self, z):
        #print(f"Rotating right {z}")
        y = self.mainTree[z][0]
        T3 = self.mainTree[y][1]

        # Perform rotation
        self.mainTree[y][1] = z
        self.mainTree[z][0] = T3

        # Update heights
        self.update_height(z)
        self.update_height(y)

        return y

    def get_max_depth(self, node):
        if node is None or node == "":
            return 0
        left_child = self.mainTree.get(node)[0]
        right_child = self.mainTree.get(node)[1]
        return 1 + max(self.get_max_depth(left_child), self.get_max_depth(right_child))



    def removeNode(self, node):

        #print("Removing node...")

        if node is None or node == "":
            print("Node to remove not found.")
            return
        left_child = self.mainTree.get(node)[0]
        right_child = self.mainTree.get(node)[1]
        parent = self.get_parent(node)

        if left_child == "" and right_child == "":
            #print("Both children blank")
            self.update_parent(node, "", parent)
            self.mainTree.pop(node)
            if node == self.root:
                self.root = ""

        elif left_child == "":
            #print("Left child blank")
            self.update_parent(node, right_child, parent)
            if node == self.root:
                self.root = right_child
            self.mainTree.pop(node)
            
        elif right_child == "":
            #print("Right child blank")
            self.update_parent(node, left_child, parent)
            if node == self.root:
                self.root = left_child
            self.mainTree.pop(node)

        else:
            #print("Both children populated")
            self.update_parent(node, right_child, parent)
            if node == self.root:
                self.root = right_child
            #add to lowest point of right_child
            self.addToLowest(left_child, right_child)
            self.mainTree.pop(node)
            self.balance_tree(left_child)

        self.save_tree()
        self.display_tree()


    def addToLowest(self, nodeToAdd, target):
        if self.mainTree.get(target)[0] == "":
            self.mainTree[target][0] = nodeToAdd
        else:
            self.addToLowest(nodeToAdd, self.mainTree[target][0])



    def display_tree(self):
        self.canvas.delete("all")
        if self.root != "":
            max_depth = self.get_max_depth(self.root)
            initial_offset_x = self.canvas.winfo_width() / (0.9 * max_depth + 1)  # Dynamic X offset
            initial_offset_y = self.canvas.winfo_height() / (max_depth + 1)  # Dynamic Y offset
            font_size = 15 - int(max_depth/1.25)  # Dynamic font size
            self.draw_tree(self.root, self.canvas.winfo_width() // 2, 20, initial_offset_x, initial_offset_y, font_size)

    def draw_tree(self, node, x, y, offset_x, offset_y, font_size):
        if node:
            self.canvas.create_text(x, y, text=node, tags="node", font=("Arial", font_size))

            left_child = self.mainTree[node][0]
            right_child = self.mainTree[node][1]

            if left_child:
                self.canvas.create_line(x, y, x - offset_x, y + offset_y, tags="line")
                self.draw_tree(left_child, x - offset_x, y + offset_y, offset_x // 2, offset_y, font_size)

            if right_child:
                self.canvas.create_line(x, y, x + offset_x, y + offset_y, tags="line")
                self.draw_tree(right_child, x + offset_x, y + offset_y, offset_x // 2, offset_y, font_size)


    def collect_items(self, node, items):
            if node is None or node == "":
                return
            left_child = self.mainTree.get(node)[0]
            right_child = self.mainTree.get(node)[1]

            self.collect_items(left_child, items)
            items.insert(0, node)
            self.collect_items(right_child, items)

            

    def traversal_in_order(self):

        print(f"Traversing {len(self.mainTree)} items~~~~~~~~~~~~~~")

        items = []
        if self.root is not None:
            self.collect_items(self.root, items)

        count = 1
        for item in items:
            print(f"{count}. {item}")
            count += 1

    def top_10_items(self):

        items = []
        if self.root:
            self.collect_items(self.root, items)

        top_10 = items[:10]
        print("Top 10 Items:~~~~~~~~~~~~~~~~~~~~~")
        count = 1
        for item in top_10:
            print(f"{count}. {item}")
            count += 1

if __name__ == "__main__":
    root = tk.Tk()
    app = TreeApp(root)
    root.mainloop()
