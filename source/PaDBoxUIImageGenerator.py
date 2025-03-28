import tkinter as tk
import tkinter.filedialog as fd
import tkinter.messagebox as mb
from tkinter import PhotoImage

import PaDBoxImageGenerator

STATUS_TYPES = ["Waiting for submission", "Checking parameters", "Reading IDs", "Generating PaDBox.png image"]

def main():
    # create the main window for the dialog box
    root = tk.Tk()
    root.title("PaDBox Image Generator")
    root.geometry("500x200")

    # create a label and entry widget for each parameter
    parameter_labels = ["Id File Path:", "Portraits Directory:", "Portraits per row:", "Keep Order"] # "ID test (broken dont touch)" removed
    parameter_entries = []
    current_status = tk.StringVar()

#Tooltip section
    # Tooltip dictionary
    tooltips = {
        "Id File Path:": "Path to text file of id numbers separated by comma",
        "Portraits Directory:": "Path to card portraits",
        "Portraits per row:": "Number of portraits per row. Default is 6",
        #"ID test (broken dont touch)": "BROKEN This will test if your id file can find all portraits",
        "Keep Order": "Preserves order of ids in the text file rather than sort by attribute color"
    }

    def show_tooltip(event):
        tooltip_label.config(text=tooltips[event.widget.tooltip])
        tooltip_label.place(x=10, y=200)  # Fixed x-coordinate
        #submit_button.winfo_y() + submit_button.winfo_height() Doesnt currently do anything unless you pack canvas

    def hide_tooltip(event):
        tooltip_label.place_forget()

    tooltip_label = tk.Label(root, bg="yellow", relief="solid", borderwidth=1, padx=5, pady=0)

#helper function for parameter generation/input
    #validates
    def validate_positive_integer(P):
        if P.isdigit() and int(P) > 0:
            submit_button.config(state="normal")  # Enable the submit button when the input is a positive integer
            return True
        submit_button.config(state="disabled")  # Disable the submit button for non-positive integers
        return True  
       
#label generation for parameters.   
    for i, label in enumerate(parameter_labels):
        tk.Label(root, text=label).grid(row=i, column=0)
        entry = tk.Entry(root)
    
        if label.__eq__("Portraits per row:"):  # set default value for Portraits per row
            entry.insert(i, "6")
        if label.__eq__("Checkbox:") or label.__eq__("Keep Order"):  # add checkbox with default unchecked false
            # or label.__eq__("ID test (broken dont touch)") | Removed
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
       
#functions for paramter input and submit button
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
        parameters = parameter_values
        on_submit(parameters, current_status)

#buttons
    #button for id file selection
    browse_button_1 = tk.Button(root, text="Browse for Id txt file", command=lambda: select_file_path(0))
    browse_button_1.grid(row=0, column=2)

    #button for protraits folder selection
    browse_button_directory_1 = tk.Button(root, text="Browse for portraits folder", command=lambda: select_directory_path(1))
    browse_button_directory_1.grid(row=1, column=2)

    #submit button
    submit_button = tk.Button(root, text="Submit", command= lambda: submit(current_status), state="normal") #start ui with submit disabled since you need to select paths. 
    submit_button.grid(row=len(parameter_labels), column=0, columnspan=1, pady=2)

    #additional labels
    #status label
    status_label = tk.Label(root, textvariable=current_status, width=30, justify="left", anchor="w", bd=1, relief="solid")
    status_label.pack
    status_label.grid(row=len(parameter_labels)+2, column=0, columnspan=2) #manual grid position which is bad practice
 
    #line rider image.
    linerider_image = PhotoImage(file="../resources/UIResources/avatar.png")
    linerider_label = status_label = tk.Label(root, image=linerider_image)
    linerider_label.pack
    linerider_label.grid(row=3, column=2, rowspan=5) 
    #Can make it go back to touching the submit button if desired by increasing rowspan to a high number like 100. 
    
#utility and functions for post-parameter submission
    #updates the status label/message
    def set_status(status, status_message):
        status.set("Status: " + status_message)
        root.update_idletasks() #required otherwise the status doesn't actually update on the UI between steps

    #check for all required parameters.
    def check_input(parameters, status):
        set_status(status, STATUS_TYPES[1])
        #strip the first two for empty space before checking if empty. 
        #order of parameters in the if statement: "Id File Path:", "Portraits Directory:", "Portraits per row:"
        if(parameters[0].strip() and parameters[1].strip() and parameters[2]):
            return True
        else:
            #if a required parameter is empty. Throw up an error box.
            mb.showerror("Error", "You are missing a required parameter") 
            set_status(status, STATUS_TYPES[0]) #reset status
            return False

    #makes the function calls to the PaDBoxImageGenerator.
    def call_PaDBox(parameters, status):
        if(False): #true if test run read
            testIds()
        else:
            #step 1 is to read the Id File
            set_status(status, STATUS_TYPES[2]) #I suppose this could be moved inside the try, no particular reason.
            try:
                PaDBoxImageGenerator.readIdFile(parameters[0]) #id file
                #once processed, begin the PaDBox image generation
                set_status(status, STATUS_TYPES[3])
                PaDBoxImageGenerator.generateBoxCollage(parameters[2]) #number of portraits per row
                set_status(current_status, STATUS_TYPES[0]) #reset status
                mb.showinfo("Complete","PaDBox.png has been generated")
            except Exception as e:
                 mb.showerror("Error", e)   
         
    #Sets arguments, checks parameters, then starts by calling the image generation helper funection. 
    def on_submit(parameters, status):
        #set args used in PaDBox Generator code
        #order: "Id File Path:", "Portraits Directory:", "Portraits per row:", "ID test (broken dont touch)", "Keep Order"
        PaDBoxImageGenerator.setArgs(parameters[0], parameters[1], parameters[2], False, parameters[3])
        #check if all required parameters are filled and then otherwise call the image generation.
        if(check_input(parameters, status)):
            #begin PaDBox image gen helper function.
            call_PaDBox(parameters, status)

#final setup for UI and begin mainloop
    #set default status
    set_status(current_status, STATUS_TYPES[0])
    root.resizable(True, True) #allow main window to be resizable.
    # wait for the dialog to become visible
    root.wait_visibility()
    # grab focus to the first entry widget
    parameter_entries[0].focus_set()
    # start the event loop
    root.mainloop()

    return parameters if 'parameters' in globals() else None

def testPrint():
    print("yo test print")
    print(parameters)

start = main()

print("Program complete")

