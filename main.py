#Store student details
students=[]

#Save student data to file
def save_students():
    file=open("students.txt","w")

    for student in students:
        file.write(student["Name"]+","+student["Rollno"]+"\n")
    file.close()

#Load students from file
try:
    file=open("students.txt","r")

    for line in file:
        name,rollno=line.strip().split(",")
        students.append({"Name": name,"Rollno": rollno})
    file.close()
except FileNotFoundError:
    pass

while True:
    print("\n======STUDENT MANAGEMENT SYSTEM=====")
    print("\n1.Add Student")
    print("2.View Students")
    print("3.Search Student")
    print("4.Delete Student")
    print("5.Update/Edit Student")
    print("6.Exit")

    choice=input("Enter choice: ")

    if choice=="1":
        name=input("Enter the student name: ")
        rollno=input("Enter the student roll number: ")
        students.append({"Name": name,"Rollno": rollno})
        save_students()
        print("Student added successfully!")

    elif choice=="2":
        if(len(students)==0):
            print("No Students Found")
        else:
            for student in students:
                print("Name:",student["Name"])
                print("Roll:",student["Rollno"])
                print("-----")

    elif choice=="3":
        if len(students)==0:
            print("No Students added yet")
        else:
            search_name=input("Enter name to search: ")
            for student in students:
                if search_name==student["Name"]:
                    print("Name:",student["Name"])
                    print("Roll:",student["Rollno"])
                    break
                else:
                    print("Student not found")

    elif choice=="4":
        delete_name=input("Enter student name to delete: ")
        for student in students:
            if delete_name==student["Name"]:
                students.remove(student)
                save_students()
                print("Student deleted successfully!")
                break
        else:
            print("Student not found")

    elif choice=="5":
        old_name=input("Enter student name to update: ")
        for student in students:
            if old_name==student["Name"]:
                new_name=input("Enter new name: ")
                new_rollno=input("Enter new roll number: ")

                student["Name"]=new_name
                student["Rollno"]=new_rollno
                save_students()

                print("Student updated successfully!")
                break
            else:
                print("Student not found")
    elif choice=="6":
        print("Exiting...")
        break

    else:
        print("Invalid choice")
        
