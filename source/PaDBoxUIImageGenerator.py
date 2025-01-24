import tkinter as tk
import tkinter.filedialog as fd
import tkinter.messagebox as mb
#import os
#print(os.getcwd())
#import sys
#print("D:\\Desktop\\Coding\\PaDBox\\source")
#sys.path.insert(1, "D:\\Desktop\\Coding\\PaDBox\\source") # based on comments you should use **1 not 0**
#from PaDBoxImageGenerator import PaDBoxImageGenerator # imports correct file

import PaDBoxImageGenerator

STATUS_TYPES = ["Waiting for submission", "Checking parameters", "Reading IDs", "Generating PaDBox.png image"]

def main():
    # create the main window for the dialog box
    root = tk.Tk()
    root.title("Enter Parameters")
    root.geometry("500x300")

    # create a label and entry widget for each parameter
    parameter_labels = ["Id File Path:", "Portraits Directory:", "Portraits per row:", "ID test (broken dont touch)", "Keep Order"]
    parameter_entries = []
    current_status = tk.StringVar()
    current_status.set("Status: " + STATUS_TYPES[0])

    # Tooltip dictionary
    tooltips = {
        "Id File Path:": "Path to text file of id numbers separated by comma",
        "Portraits Directory:": "Path to card portraits",
        "Portraits per row:": "Number of portraits per row. Default is 6",
        "ID test (broken dont touch)": "BROKEN This will test if your id file can find all portraits",
        "Keep Order": "Preserves order of ids in the text file rather than sort by attribute color"
    }

    def show_tooltip(event):
        tooltip_label.config(text=tooltips[event.widget.tooltip])
        tooltip_label.place(x=10, y=175)  # Fixed x-coordinate
        #submit_button.winfo_y() + submit_button.winfo_height() Doesnt currently do anything unless you pack canvas

    def hide_tooltip(event):
        tooltip_label.place_forget()

    def validate_positive_integer(P):
        if P.isdigit() and int(P) > 0:
            submit_button.config(state="normal")  # Enable the submit button when the input is a positive integer
            return True
        submit_button.config(state="disabled")  # Disable the submit button for non-positive integers
        return True  
       
    for i, label in enumerate(parameter_labels):
        tk.Label(root, text=label).grid(row=i, column=0)
        entry = tk.Entry(root)
    
        if label.__eq__("Portraits per row:"):  # set default value for Portraits per row
            entry.insert(i, "6")
        if label.__eq__("Checkbox:") or label.__eq__("ID test (broken dont touch)") or label.__eq__("Keep Order"):  # add checkbox with default unchecked false
            var = tk.BooleanVar()
            var.set(False)
            checkbox = tk.Checkbutton(root, variable=var)
            checkbox.grid(row=i, column=1)
            parameter_entries.append(var)
        else:  # add entry for other parameters
            entry.grid(row=i, column=1)
            parameter_entries.append(entry)
            
            if label.__eq__("Portraits per row:"):  # validate positive integer for "Portraits per row:"
                entry.config(validate="key", validatecommand=(root.register(validate_positive_integer), "%P"))

        label_widget = root.grid_slaves(row=i, column=0)[0]  # get label widget
        label_widget.tooltip = label  # set tooltip text
        label_widget.bind("<Enter>", show_tooltip)  # bind mouse hover events
        label_widget.bind("<Leave>", hide_tooltip)
        
    tooltip_label = tk.Label(root, bg="yellow", relief="solid", borderwidth=1, padx=5, pady=0)

    def select_file_path(entry_index):
        file_path = fd.askopenfilename(initialdir="/", title=f"Select file for File Path {entry_index}", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        parameter_entries[entry_index].delete(0, tk.END)
        parameter_entries[entry_index].insert(0, file_path)

    def select_directory_path(entry_index):
        directory_path = fd.askdirectory(initialdir="/", title=f"Select directory for Directory Path {entry_index}")
         # Add trailing slash if it is missing
        if directory_path and not directory_path.endswith('/'):
            directory_path += '/'
        parameter_entries[entry_index].delete(0, tk.END)
        parameter_entries[entry_index].insert(0, directory_path)

    def submit(current_status):
        parameter_values = []
        for i, entry in enumerate(parameter_entries):
            input_value  = entry.get()
            if parameter_labels[i] == "Portraits per row:":
                input_value = int(entry.get())
            parameter_values.append(input_value)
        #old behavior was destroy on submit. Closing the mainloop and the window. 
        #Instead get the parameters and then move onto the PaDBox generation.
        global parameters
        #parameter_values.append(True)
        parameters = parameter_values
        on_submit(parameters, current_status)

    browse_button_1 = tk.Button(root, text="Browse for Id txt file", command=lambda: select_file_path(0))
    browse_button_1.grid(row=0, column=2)

    browse_button_directory_1 = tk.Button(root, text="Browse for portraits folder", command=lambda: select_directory_path(1))
    browse_button_directory_1.grid(row=1, column=2)

    submit_button = tk.Button(root, text="Submit", command= lambda: submit(current_status), state="normal") #start ui with submit disabled since you need to select paths. 
    submit_button.grid(row=len(parameter_labels), column=0, columnspan=1, pady=2)

   
    #new updating text way
    status_label = tk.Label(root, textvariable=current_status, width=30, justify="left", anchor="w", bd=1, relief="solid")
    status_label.pack
    #other option to move toward middle is columnspan 2 for submit button and 3 for status label.
    status_label.grid(row=len(parameter_labels)+2, column=0, columnspan=2) #manual grid position that is very ugly.
    #.place(x=10, y=submit_button.winfo_y() + submit_button.winfo_height() + 5)
    
#Status:
#current_status = StringVar()
#Label(master, textvariable=v).pack()

#v.set("New Text!")

    # wait for the dialog to become visible
    root.wait_visibility()
    # grab focus to the first entry widget
    parameter_entries[0].focus_set()
    # start the event loop
    root.mainloop()

    return parameters if 'parameters' in globals() else None

def call_PaDBox(parameters, status):
    if(False): #true if test run read
        testIds()
    else:
        status.set("Status: " + STATUS_TYPES[2])
        PaDBoxImageGenerator.readIdFile(parameters[0]) #id file
        status.set("Status: " + STATUS_TYPES[3])
        PaDBoxImageGenerator.generateBoxCollage(parameters[2]) #number of portraits per row

#check if all required parameters are filled in. "Id File Path:", "Portraits Directory:", "Portraits per row:"
def check_input(parameters, status):
    status.set("Status: " + STATUS_TYPES[1])
    #strip the first two for empty space before checking if empty. 
    if(parameters[0].strip() and parameters[1].strip() and parameters[2]):
        return True
    else:
        #if a required parameter is empty. Throw up an error box.
        mb.showerror("Error", "You are missing a required parameter") 
        return False

#called when submit button clicked. 
#Sets arguments, checks parameters, then calls and starts the image generation
def on_submit(parameters, status):
    PaDBoxImageGenerator.setArgs(parameters[0], parameters[1], parameters[2], parameters[3], parameters[4])
    if(check_input(parameters, status)):
        call_PaDBox(parameters)
        mb.showinfo("Complete","PaDBox.png has been generated")
        print("image complete")

def testPrint():
    print("yo test print")
    print(parameters)

start = main()
#print(parameters) #was used for debug

#set args used in PaDBox Generator code because I didn't want to refactor and can just use it's set args for some of the globals
#reminder of the order: "Id File Path:", "Portraits Directory:", "Portraits per row:", "ID test (broken dont touch)", "Keep Order"

#check if all required parameters are filled and then otherwise call the image generation.
#if(check_input(parameters)):
#    call_PaDBox(parameters)
#    mb.showinfo("Complete","PaDBox.png has been generated")
#    print("image complete")

print("Program complete")

