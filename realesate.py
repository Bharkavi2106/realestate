import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime

mysqldb = mysql.connector.connect(host="localhost", user="root", database="realestate")
mycursor = mysqldb.cursor()
root = tk.Tk(className='Real Estate Management System')
root.geometry("800x800")
root.config(bg="light green")

moving_text = tk.Label(root, text="Real Estate Management", font=("Franklin Gothic Demi", 24), bg="light green")
moving_text.place(x=0, y=10)  # Start the label from the left edge of the window


# Function to move the text from right to left
def move_text():
    x = int(moving_text.place_info()['x'])

    # Calculate the width of the label using winfo_reqwidth()
    label_width = moving_text.winfo_reqwidth()

    x = (x + 1) % (root.winfo_width() + label_width)
    moving_text.place(x=x)
    moving_text.after(10, move_text)  # Adjust the delay for the desired speed


# Call the move_text function to start the animation
move_text()

global e1
global e2
global e3
global e4

# Add a variable to store the property status
propertystatus = StringVar()

tk.Label(root, text="Plot number", font=("Franklin Gothic Demi", 20)).place(x=100, y=60)
Label(root, text="Owner Name", font=("Franklin Gothic Demi", 20)).place(x=100, y=110)
Label(root, text="Size", font=("Franklin Gothic Demi", 20)).place(x=100, y=160)
Label(root, text="Price", font=("Franklin Gothic Demi", 20)).place(x=100, y=210)
Label(root, text="PropertyStatus", font=("Franklin Gothic Demi", 20)).place(x=100, y=260)

e1 = Entry(root)
e1.place(x=350, y=60, width=250, height=40)

e2 = Entry(root)
e2.place(x=350, y=110, width=250, height=40)

e3 = Entry(root)
e3.place(x=350, y=160, width=250, height=40)

e4 = Entry(root)
e4.place(x=350, y=210, width=250, height=40)

# Create a Combobox for property status
propertystatus_combobox = ttk.Combobox(root, textvariable=propertystatus, values=["Available", "Under Contract", "Sold"])
propertystatus_combobox.place(x=350, y=260, width=250, height=40)

# Function to clear the entry fields
def clear_fields():
    e1.delete(0, END)
    e2.delete(0, END)
    e3.delete(0, END)
    e4.delete(0, END)
    propertystatus_combobox.set("")

# Button to clear entry fields
clear_button = Button(root, text="Clear Fields", command=clear_fields, height=2, width=13,font=("Franklin Gothic Demi",12))
clear_button.place(x=400, y=390)

# Create a Text widget for displaying information
info_text = Text(root, font=("Franklin Gothic Demi", 14))
info_text.place(x=900, y=70, width=420, height=400)
info_text.config(state=DISABLED)  # Disable text editing

# Function to display information in the Text widget
def display_info():
    info_text.config(state=NORMAL)
    info_text.delete(1.0, END)
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    info_text.insert(END, "Welcome to Real Estate Management System!\n")
    info_text.insert(END, f"Current Date and Time: {current_date}\n")
    info_text.insert(END, "Select an action from the dropdown and click the buttons to manage plots.")
    info_text.config(state=DISABLED)

# Call the display_info function to display initial information
display_info()

# Function to perform actions (Add, Update, Delete, Search)
def perform_action():
    action = action_var.get()
    if action == "Add":
        Add()
    elif action == "Update":
        update()
    elif action == "Delete":
        delete()
    elif action == "Search":
        search()

# Function to add a property
def Add():
    plotid = e1.get()
    ownername = e2.get()
    size = e3.get()
    price = e4.get()
    status = propertystatus.get()

    try:
        sql = "INSERT INTO realestatemanagement (plotid, ownername, size, price, propertystatus) VALUES (%s, %s, %s, %s, %s)"
        val = (plotid, ownername, size, price, status)
        mycursor.execute(sql, val)
        mysqldb.commit()
        lastid = mycursor.lastrowid
        messagebox.showinfo("", "Plot added!")
        e1.delete(0, END)
        e2.delete(0, END)
        e3.delete(0, END)
        e4.delete(0, END)
        propertystatus_combobox.set("")
        e1.focus_set()

    except Exception as e:
        print(e)
        mysqldb.rollback()
        mysqldb.close()

# Function to update a property
def update():
    plotid = e1.get()
    ownername = e2.get()
    size = e3.get()
    price = e4.get()
    status = propertystatus.get()

    try:
        sql = "UPDATE realestatemanagement SET ownername = %s, size = %s, price = %s, propertystatus = %s WHERE plotid = %s"
        val = (ownername, size, price, status, plotid)
        mycursor.execute(sql, val)
        mysqldb.commit()
        lastid = mycursor.lastrowid
        messagebox.showinfo("", "Plot Updated")

        e1.delete(0, END)
        e2.delete(0, END)
        e3.delete(0, END)
        e4.delete(0, END)
        propertystatus_combobox.set("")
        e1.focus_set()

    except Exception as e:
        print(e)
        mysqldb.rollback()
        mysqldb.close()

# Function to search for a property
def search():
    try:
        plotid = e1.get()
        sql = "SELECT plotid, ownername, size, price, propertystatus FROM realestatemanagement WHERE plotid = %s"
        val = (plotid,)
        mycursor.execute(sql, val)
        record = mycursor.fetchone()

        if record:
            info_text.config(state=NORMAL)
            info_text.delete(1.0, END)
            info_text.insert(END, f"Plot Number: {record[0]}\n")
            info_text.insert(END, f"Owner Name: {record[1]}\n")
            info_text.insert(END, f"Size: {record[2]}\n")
            info_text.insert(END, f"Price: {record[3]}\n")
            info_text.insert(END, f"Property Status: {record[4]}\n\n")
            info_text.config(state=DISABLED)
        else:
            messagebox.showinfo("", "Plot not found!")

    except Exception as e:
        print(e)
        mysqldb.close()

# Function to delete a property
def delete():
    plotid = e1.get()

    try:
        sql = "DELETE FROM realestatemanagement WHERE plotid = %s"
        val = (plotid,)
        mycursor.execute(sql, val)
        mysqldb.commit()
        lastid = mycursor.lastrowid
        messagebox.showinfo("", "Plot deleted!")

        e1.delete(0, END)
        e2.delete(0, END)
        e3.delete(0, END)
        e4.delete(0, END)
        propertystatus_combobox.set("")
        e1.focus_set()

    except Exception as e:
        print(e)
        mysqldb.rollback()
        mysqldb.close()

# Create a variable to store the selected action
action_var = StringVar()

# Dropdown to select the action (Add, Update, Delete, Search)
action_label = Label(root, text="Select Action", font=("Franklin Gothic Demi", 20))
action_label.place(x=100, y=320)

action_combobox = ttk.Combobox(root, textvariable=action_var, values=["Add", "Update", "Delete", "Search"])
action_combobox.place(x=350, y=320, width=250, height=40)

# Button to perform the selected action
action_button = Button(root, text="Perform Action",command=perform_action, height=2, width=13,font=("Franklin Gothic Demi",12))
action_button.place(x=210, y=390)

# Treeview to display property records
cols = ('Plot number', 'Owner Name', 'Size', 'Price', 'Status')
listBox = ttk.Treeview(root, columns=cols, show='headings', style="My.Treeview")

for col in cols:
    listBox.heading(col, text=col)
listBox.grid(row=1, column=0, columnspan=2)
listBox.place(x=100, y=550, height=200)

# Create a Treeview style
tree_style = ttk.Style()
tree_style.configure("My.Treeview", font=("Franklin Gothic Demi", 12))

# Function to populate the Treeview with property records
def show():
    try:
        sql = "SELECT plotid, ownername, size, price, propertystatus FROM realestatemanagement"
        mycursor.execute(sql)
        records = mycursor.fetchall()

        for record in records:
            listBox.insert("", "end", values=record)

    except Exception as e:
        print(e)

show()

root.mainloop()