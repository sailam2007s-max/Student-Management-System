from tkinter import*
from tkinter import ttk
from tkinter import messagebox
import sqlite3

conn=sqlite3.connect("student.db")
cursor=conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS students(name TEXT,roll INTEGER PRIMARY KEY,dept TEXT)""")
conn.commit()

students=[]

def add_student():
    name = name_entry.get().strip()
    roll = roll_entry.get().strip()
    dept = dept_entry.get().strip()

    # Check empty fields
    if name == "" or roll == "" or dept == "":
        messagebox.showerror("Error", "Please fill all fields!")
        return

    # Check duplicate roll number
    cursor.execute("SELECT * FROM students WHERE roll=?", (roll,))
    existing = cursor.fetchone()

    if existing:
        messagebox.showerror("Error", "Roll Number already exists!")
        return

    try:
        # Insert into database
        cursor.execute(
            "INSERT INTO students (name, roll, dept) VALUES (?, ?, ?)",
            (name, roll, dept)
        )
        conn.commit()

        # Refresh table
        load_students()

        # Clear entry fields
        name_entry.delete(0, END)
        roll_entry.delete(0, END)
        dept_entry.delete(0, END)

        # Success message
        messagebox.showinfo("Success", "Student Added Successfully!")

    except Exception as e:
        messagebox.showerror("Error", str(e))

def search_student():

    name = name_entry.get()
    roll = roll_entry.get()
    dept = dept_entry.get()

    if name == "" or roll == "" or dept == "":
        messagebox.showerror("Error", "Please fill all fields!")
        return

    cursor.execute(
        "SELECT * FROM students WHERE name=? AND roll=? AND dept=?",
        (name, roll, dept)
    )

    student = cursor.fetchone()

    if student is None:
        messagebox.showerror("Error", "Student Not Found!")
        return

    for item in table.get_children():
        values = table.item(item)["values"]

        if values[0] == name and str(values[1]) == str(roll) and values[2] == dept:
            table.selection_set(item)
            table.focus(item)
            table.see(item)
            break

    messagebox.showinfo("Success", "Student Found!")
    
def delete_student():

    selected = table.selection()

    if not selected:
        messagebox.showerror("Error", "Please select a student from the table to delete!")
        return

    confirm = messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete this student?"
    )

    if not confirm:
        return

    values = table.item(selected[0])["values"]
    roll = values[1]

    try:
        cursor.execute("DELETE FROM students WHERE roll=?", (roll,))
        conn.commit()

        load_students()

        name_entry.delete(0, END)
        roll_entry.delete(0, END)
        dept_entry.delete(0, END)

        messagebox.showinfo("Success", "Student Deleted Successfully!")

    except Exception as e:
        messagebox.showerror("Error", str(e))

def update_student():
    name=name_entry.get()
    roll=roll_entry.get()
    dept=dept_entry.get()

    if name == "" or roll == "" or dept == "":
        messagebox.showerror("Error","Please fill all fields")
        return
    cursor.execute("UPDATE students SET name=?,dept=? WHERE roll=?",(name,dept,roll))
    conn.commit()

    load_students()
    messagebox.showinfo("Success","Student Updated Successfully!")

def clear_student():
    name_entry.delete(0,END)
    roll_entry.delete(0,END)
    dept_entry.delete(0,END)

def select_student(event):
    selected = table.focus()

    if selected:
        values = table.item(selected, "values")

        name_entry.delete(0, END)
        roll_entry.delete(0, END)
        dept_entry.delete(0, END)

        name_entry.insert(0, values[0])
        roll_entry.insert(0, values[1])
        dept_entry.insert(0, values[2])

def load_students():

    # Clear existing rows from Treeview
    for item in table.get_children():
        table.delete(item)

    # Load all students from SQLite
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()

    # Insert into Treeview
    for row in rows:
        table.insert("", END, values=row)

    # Update student count
    count_label.config(text=f"Total Students : {len(rows)}")

root=Tk()
def show_about():
    messagebox.showinfo(
        "About",
        "Student Management System\n\n"
        "Built using Python, Tkinter & SQLite\n\n"
        "Developed by Hemaa ❤️"
    )
def about():
    messagebox.showinfo(
        "About",
        "Student Management System\n\nDeveloped by Hemaa ❤️\n\nPython • Tkinter • SQLite"
    )
root.title("🎓 STUDENT MANAGEMENT SYSTEM")
root.geometry("950x700")
window_width = 950
window_height = 700

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)

root.geometry(f"{window_width}x{window_height}+{x}+{y}")

root.config(bg="#EAF6FF")
menu_bar = Menu(root)

help_menu = Menu(menu_bar, tearoff=0)
help_menu.add_command(label="About", command=show_about)

menu_bar.add_cascade(label="Help", menu=help_menu)

root.config(menu=menu_bar)
root.bind("<Return>", lambda event: add_student())

title = Label(
    root,
    text="🎓 STUDENT MANAGEMENT SYSTEM",
    font=("Segoe UI", 22, "bold"),
    bg="#EAF6FF",
    fg="#003366"
)
title.pack(pady=15)

subtitle = Label(
    root,
    text="Manage Student Records Efficiently",
    font=("Segoe UI", 11, "italic"),
    bg="#EAF6FF",
    fg="#666666"
)

subtitle.pack()

#Name
name_label=Label(root,text="Name",font=("Segoe UI",12,"bold"),bg="#EAF4FC")
name_label.place(x=80,y=100)
name_entry=Entry(root,font=("Segoe UI",12),width=30)
name_entry.place(x=220,y=100)

#Roll Number
roll_label=Label(root,text="Roll Number",font=("Segoe UI",12,"bold"),bg="#EAF4FC")
roll_label.place(x=80,y=150)
roll_entry=Entry(root,font=("Segoe UI",12),width=30)
roll_entry.place(x=220,y=150)

#Department
dept_label=Label(root,text="Department",font=("Segoe UI",12,"bold"),bg="#EAF4FC")
dept_label.place(x=80,y=200)
dept_entry=Entry(root,font=("Segoe UI",12),width=30)
dept_entry.place(x=220,y=200)

#Buttons

add_btn = Button(
    root,
    text="➕ Add",
    command=add_student,
    bg="#4CAF50",
    fg="white",
    font=("Segoe UI",11,"bold"),width=12)
add_btn.place(x=60,y=270)

search_btn = Button(
    root,
    text="🔍 Search",
    command=search_student,
    bg="#2196F3",
    fg="white",
    font=("Segoe UI", 11, "bold"),
    width=12
)
search_btn.place(x=190,y=270)

update_btn = Button(
    root,
    text="✏️ Update",
    command=update_student,
    bg="#FF9800",
    fg="white",
    font=("Segoe UI", 11, "bold"),
    width=12
)
update_btn.place(x=320,y=270)

delete_btn = Button(
    root,
    text="🗑 Delete",
    command=delete_student,
    bg="#F44336",
    fg="white",
    font=("Segoe UI", 11, "bold"),
    width=12
)
delete_btn.place(x=450,y=270)

clear_btn = Button(
    root,
    text="🧹 Clear",
    command=clear_student,
    bg="#9C27B0",
    fg="white",
    font=("Segoe UI", 11, "bold"),
    width=12
)
clear_btn.place(x=580,y=270)

style = ttk.Style()

style.theme_use("clam")

style.configure(
    "Treeview.Heading",
    background="#C09215",
    foreground="white",
    font=("Segoe UI", 11, "bold")
)

style.configure(
    "Treeview",
    font=("Segoe UI", 10),
    rowheight=28
)

style = ttk.Style()

style.theme_use("clam")

style.configure(
    "Treeview",
    background="white",
    foreground="black",
    rowheight=30,
    fieldbackground="white",
    font=("Segoe UI", 10)
)

style.configure(
    "Treeview.Heading",
    background="#1565C0",
    foreground="white",
    font=("Segoe UI", 11, "bold")
)

style.map(
    "Treeview",
    background=[("selected", "#90CAF9")],
    foreground=[("selected", "black")]
)

table=ttk.Treeview(root,columns=("Name","Roll","Department"),show="headings")

table.heading("Name",text="Name")
table.heading("Roll",text="Roll Number")
table.heading("Department",text="Department")

table.column("Name", anchor=CENTER)
table.column("Roll", anchor=CENTER)
table.column("Department", anchor=CENTER)

table.place(x=80,y=340,width=740,height=200)
table.bind("<ButtonRelease-1>", select_student)

count_label = Label(root, text="Total Students : 0",font=("Segoe UI", 11, "bold"))
count_label.place(x=80, y=550)

load_students()

footer = Label(
    root,
    text="Developed by Hemaa ❤️ |  Version 1.0",
    font=("Segoe UI", 15, "bold"),
    bg="#EAF6FF",
    fg="#1565C0"
)

footer.pack(side=BOTTOM, pady=10)

menubar = Menu(root)

file_menu = Menu(menubar, tearoff=0)
file_menu.add_command(label="Exit", command=root.destroy)

help_menu = Menu(menubar, tearoff=0)
help_menu.add_command(label="About", command=about)

menubar.add_cascade(label="File", menu=file_menu)
menubar.add_cascade(label="Help", menu=help_menu)

root.config(menu=menubar)
root.mainloop()