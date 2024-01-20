import tkinter as tk
import tkinter.filedialog as fd

def get_parameters():
    # create the main window for the dialog box
    root = tk.Tk()
    root.title("Enter Parameters")
    root.geometry("500x300")

    # create a label and entry widget for each parameter
    parameter_labels = ["Id File Path:", "Portraits Directory:", "Portraits per row:", "ID test (broken dont touch)", "Keep Order", 
    "Positive Integer:", "File Path:", "String:", "Checkbox:"]
    parameter_entries = []
    
#    inputGroup.add_argument("--id_file", required=True, help="Path to text file of id numbers separated by comma")
#inputGroup.add_argument("--portraits_dir", required=True, help="Path to card portraits")
#inputGroup.add_argument("--imgs_per_row", const=6, default=6, nargs="?", type=int, help="Number of portraits per row. Default is 6")
#inputGroup.add_argument("--id_test", action="store_true", help="this will test if your id file can find all portraits")
#inputGroup.add_argument("--keep_order", action="store_true", help="Preserves order of ids in text file")

    def show_tooltip(event):
        tooltip_label.config(text=event.widget.tooltip)
        tooltip_label.place(x=root.winfo_pointerx(), y=root.winfo_pointery())

    def hide_tooltip(event):
        tooltip_label.place_forget()
        
    for i, label in enumerate(parameter_labels):
        tk.Label(root, text=label).grid(row=i, column=0)
        entry = tk.Entry(root)
        print("label " + label)
        if i == 0:  # set default value for first parameter
            entry.insert(0, "6")
        if i == 3:  # add checkbox for fourth parameter
            var = tk.BooleanVar()
            var.set(False)
            checkbox = tk.Checkbutton(root, variable=var)
            checkbox.grid(row=i, column=1)
            parameter_entries.append(var)
        elif i != 3:  # add entry for other parameters
            entry.grid(row=i, column=1)
            parameter_entries.append(entry)
            
        label_widget = root.grid_slaves(row=i, column=0)[0]  # get label widget
        label_widget.tooltip = label  # set tooltip text
        label_widget.bind("<Enter>", show_tooltip)  # bind mouse hover events
        label_widget.bind("<Leave>", hide_tooltip)
        
    tooltip_label = tk.Label(root, bg="yellow", relief="solid", borderwidth=1, padx=5, pady=2)
    
    def validate_positive_integer(input_str):
        try:
            value = int(input_str)
            if value <= 0:
                raise ValueError("Positive integer required")
            return True
        except ValueError:
            return False

    def select_file_path():
        file_path = fd.askopenfilename(initialdir="/", title="Select file", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        parameter_entries[1].delete(0, tk.END)
        parameter_entries[1].insert(0, file_path)

    def submit():
        parameter_values = []
        for entry in parameter_entries:
            input_str = entry.get()
            if validate_positive_integer(input_str):
                parameter_values.append(int(input_str))
            else:
                parameter_values.append(input_str)
        root.destroy()
        global parameters
        parameters = parameter_values

    browse_button = tk.Button(root, text="Browse", command=select_file_path)
    browse_button.grid(row=1, column=2)

    submit_button = tk.Button(root, text="Submit", command=submit)
    submit_button.grid(row=len(parameter_labels), column=0, columnspan=2)

    # wait for the dialog to become visible
    root.wait_visibility()
    # grab focus to the first entry widget
    parameter_entries[0].focus_set()
    # start the event loop
    root.mainloop()

    return parameters if 'parameters' in globals() else None

print("hello world script")
parameters = get_parameters()
print(parameters)
import tkinter as tk
import tkinter.filedialog as fd

def get_parameters():
    # create the main window for the dialog box
    root = tk.Tk()
    root.title("Enter Parameters")
    root.geometry("500x300")

    # create a label and entry widget for each parameter
    parameter_labels = ["Positive Integer:", "File Path:", "String:", "Checkbox:"]
    parameter_entries = []
    
    def show_tooltip(event):
        tooltip_label.config(text=event.widget.tooltip)
        tooltip_label.place(x=root.winfo_pointerx(), y=root.winfo_pointery())

    def hide_tooltip(event):
        tooltip_label.place_forget()
        
    for i, label in enumerate(parameter_labels):
        tk.Label(root, text=label).grid(row=i, column=0)
        entry = tk.Entry(root)
        if i == 0:  # set default value for first parameter
            entry.insert(0, "6")
        if i == 3:  # add checkbox for fourth parameter
            var = tk.BooleanVar()
            var.set(False)
            checkbox = tk.Checkbutton(root, variable=var)
            checkbox.grid(row=i, column=1)
            parameter_entries.append(var)
        elif i != 3:  # add entry for other parameters
            entry.grid(row=i, column=1)
            parameter_entries.append(entry)
            
        label_widget = root.grid_slaves(row=i, column=0)[0]  # get label widget
        label_widget.tooltip = label  # set tooltip text
        label_widget.bind("<Enter>", show_tooltip)  # bind mouse hover events
        label_widget.bind("<Leave>", hide_tooltip)
        
    tooltip_label = tk.Label(root, bg="yellow", relief="solid", borderwidth=1, padx=5, pady=2)
    
    def validate_positive_integer(input_str):
        try:
            value = int(input_str)
            if value <= 0:
                raise ValueError("Positive integer required")
            return True
        except ValueError:
            return False

    def select_file_path():
        file_path = fd.askopenfilename(initialdir="/", title="Select file", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        parameter_entries[1].delete(0, tk.END)
        parameter_entries[1].insert(0, file_path)

    def submit():
        parameter_values = []
        for entry in parameter_entries:
            input_str = entry.get()
            if validate_positive_integer(input_str):
                parameter_values.append(int(input_str))
            else:
                parameter_values.append(input_str)
        root.destroy()
        global parameters
        parameters = parameter_values

    browse_button = tk.Button(root, text="Browse", command=select_file_path)
    browse_button.grid(row=1, column=2)

    submit_button = tk.Button(root, text="Submit", command=submit)
    submit_button.grid(row=len(parameter_labels), column=0, columnspan=2)

    # wait for the dialog to become visible
    root.wait_visibility()
    # grab focus to the first entry widget
    parameter_entries[0].focus_set()
    # start the event loop
    root.mainloop()

    return parameters if 'parameters' in globals() else None

print("hello world script")
parameters = get_parameters()
print(parameters)
