import os
import json
import gzip
import tkinter as tk
from tkinter import filedialog, ttk, scrolledtext

class JSONLViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("JSONL Viewer")
        self.root.geometry("800x600")  # Set initial size of the window

        # Configure row and column weights for resizing
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Create the main frame
        self.frame = ttk.Frame(root, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure frame for resizing
        self.frame.grid_rowconfigure(1, weight=1)  # Listbox row
        self.frame.grid_rowconfigure(2, weight=1)  # Text areas start from this row onwards
        self.frame.grid_columnconfigure(1, weight=1)  # Right column with text areas

        # Create a button to open the JSONL file
        self.open_button = ttk.Button(self.frame, text="Open JSONL File", command=self.load_jsonl)
        self.open_button.grid(row=0, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E))

        # Create a frame to hold the listbox and its scrollbar
        listbox_frame = ttk.Frame(self.frame)
        listbox_frame.grid(row=1, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Create a listbox to display each JSON object
        self.listbox = tk.Listbox(listbox_frame, height=10, width=50)
        self.listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.listbox.bind("<<ListboxSelect>>", self.on_select)

        # Add a vertical scrollbar to the listbox
        listbox_scrollbar = ttk.Scrollbar(listbox_frame, orient="vertical", command=self.listbox.yview)
        self.listbox.configure(yscrollcommand=listbox_scrollbar.set)
        listbox_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # Configure the listbox frame for resizing
        listbox_frame.grid_rowconfigure(0, weight=1)
        listbox_frame.grid_columnconfigure(0, weight=1)

        # Create fields for task_id and multiline text areas for other fields
        self.task_id = self.create_label_entry("Task ID:", 2)
        self.test = self.create_text_area("Test:", 3)
        self.detail_description = self.create_text_area("Detail Description:", 4)
        self.prompt = self.create_text_area("Prompt:", 5)
        self.solution = self.create_text_area("Solution:", 6)

    def create_label_entry(self, label_text, row):
        """Create a label and an entry field for single-line text."""
        label = ttk.Label(self.frame, text=label_text)
        label.grid(row=row, column=0, pady=5, sticky=tk.W)
        entry = ttk.Entry(self.frame, width=60)
        entry.grid(row=row, column=1, pady=5, sticky=(tk.W, tk.E))
        return entry

    def create_text_area(self, label_text, row):
        """Create a label and a scrolled text area for multi-line text."""
        label = ttk.Label(self.frame, text=label_text)
        label.grid(row=row, column=0, pady=5, sticky=tk.W)
        text_area = scrolledtext.ScrolledText(self.frame, wrap=tk.WORD, width=60, height=5)
        text_area.grid(row=row, column=1, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.frame.grid_rowconfigure(row, weight=1)  # Allow text areas to resize vertically
        return text_area

    def load_jsonl_old(self):
        """Load the JSONL or JSONL.GZ file and populate the listbox with task_ids."""
        file_path = filedialog.askopenfilename(filetypes=[("JSONL files", "*.jsonl"), ("GZipped JSONL files", "*.jsonl.gz")])
        if not file_path:
            return
        
        try:
            # Check file extension to handle plain and gzipped files
            if file_path.endswith(".gz"):
                with gzip.open(file_path, 'rt', encoding='utf-8') as file:
                    self.data = [json.loads(line) for line in file]
            else:
                with open(file_path, 'r', encoding='utf-8') as file:
                    self.data = [json.loads(line) for line in file]
            
            self.populate_listbox()

        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to load file: {e}")
    
    def load_jsonl(self):
        """Load the JSONL or JSONL.GZ file and populate the listbox with task_ids."""
        # Set the initial directory to the current working directory
        initial_directory = os.getcwd()
        
        file_path = filedialog.askopenfilename(
            initialdir=initial_directory,
            filetypes=[("JSONL files", "*.jsonl"), ("GZipped JSONL files", "*.jsonl.gz")]
        )
        if not file_path:
            return

        try:
            # Check file extension to handle plain and gzipped files
            if file_path.endswith(".gz"):
                with gzip.open(file_path, 'rt', encoding='utf-8') as file:
                    self.data = [json.loads(line) for line in file]
            else:
                with open(file_path, 'r', encoding='utf-8') as file:
                    self.data = [json.loads(line) for line in file]

            self.populate_listbox()

        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to load file: {e}")

    def populate_listbox(self):
        """Populate the listbox with task_id values."""
        self.listbox.delete(0, tk.END)
        for index, item in enumerate(self.data):
            task_id = item.get("task_id", f"Task {index + 1}")
            self.listbox.insert(tk.END, task_id)

    def on_select(self, event):
        """Display the selected JSON object's fields in the respective text areas."""
        selected_index = self.listbox.curselection()
        if selected_index:
            index = selected_index[0]
            selected_item = self.data[index]

            # Update fields
            self.task_id.delete(0, tk.END)
            self.task_id.insert(tk.END, selected_item.get("task_id", ""))

            self.test.delete(1.0, tk.END)
            self.test.insert(tk.END, selected_item.get("test", ""))

            self.detail_description.delete(1.0, tk.END)
            self.detail_description.insert(tk.END, selected_item.get("detail_description", ""))

            self.prompt.delete(1.0, tk.END)
            self.prompt.insert(tk.END, selected_item.get("prompt", ""))

            self.solution.delete(1.0, tk.END)
            self.solution.insert(tk.END, selected_item.get("solution", ""))

if __name__ == "__main__":
    root = tk.Tk()
    app = JSONLViewer(root)
    root.mainloop()

