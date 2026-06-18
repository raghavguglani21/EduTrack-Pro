#hostel management system using sql python and file handling(txt,csv)
# to add student details, search student details, add teacher details, apply attendance date and class vise in csv and to view attendance report in csv file

import csv
from datetime import datetime, timedelta

def add_student():
    print("give details of new student")
    admno = int(input("Enter student admission number: "))
    name = input("Enter student name: ")
    age = input("Enter student age: ")
    gen=input("Enter gender of student(b/g): ").upper()
    clas = int(input("Enter student class: "))
    roll_no=int(input("Enter student roll number: "))
    phno=int(input("Enter student phone number: "))
    with open('students.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([admno, name, age, gen, clas, roll_no, phno])
        print("Student added successfully!")


def search_student():
    admno = int(input("Enter student admission number to search: "))
    with open('students.csv', 'r') as file:
        rd = csv.reader(file)
        for row in rd:
            if int(row[0]) == admno:
                print(f"Student found: {row}")
                return
        print("Student not found.")
        

def add_teacher():
    print("Give details of new teacher")
    emp_id = input("Enter teacher employee ID: ")
    password = input("Enter teacher emp_id password: ")
    name = input("Enter teacher name: ")
    subject = input("Enter subject taught: ").lower()
    print("did teacher is a class teacher? (y/n)")
    ch=input()
    if ch.lower() == 'y':
        cl=int(input("Enter class assigned: "))
    else:
        cl=None
    with open('teachers.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([emp_id, password, name, subject, cl])
        print("Teacher added successfully!")


def apply_attendance():
    emp_id = int(input("Enter teacher employee ID: "))
    password = input("Enter teacher emp_id password: ")
    with open('teachers.csv', 'r') as file:
        rd = csv.reader(file)
        for row in rd:
            if int(row[0]) == emp_id and row[1] == password:
                print(f"Welcome {row[2]}!")
                class_assigned = row[4]
                if class_assigned:
                    print(f"You are assigned to class {class_assigned}.")
                    date = input("Enter attendance date (YYYY-MM-DD): ")
                    with open('students.csv', 'r') as sfile:
                        srd = csv.reader(sfile)
                        for srow in srd:
                            if int(srow[4]) == int(class_assigned):
                                print(f"Mark attendance for {srow[1]} (Roll No: {srow[5]}): (p/a)")
                                status = input().lower()
                                with open(f'attendance_{date}_class{class_assigned}.csv', 'a', newline='') as afile:
                                    awriter = csv.writer(afile)
                                    awriter.writerow([srow[1], srow[5], status])
                    print("Attendance applied successfully!")
                else:
                    print("You are not assigned to any class.")
                return
        print("Invalid employee ID or password.")


def mess_attendance():
    choice = input("the teacher applying for morning attendance(m) or afternoon attendance(a) or night attendance(n) (m/a/n): ")
    if choice == 'm':
        a="Morning"
    elif choice == 'a':
        a="Afternoon"
    elif choice == 'n':
        a="Night"
    if choice not in ['m', 'a', 'n']:
        print("Invalid choice.")
        return
    date = input("Enter attendance date (YYYY-MM-DD): ")
    with open('students.csv', 'r') as file:
        rd = csv.reader(file)
        for row in rd:
            print(f"Mark {a} attendance for {row[1]} (admno No: {row[0]}): (p/a)")
            status = input().lower()
            with open(f'{a}_attendance_{date}.csv', 'a', newline='') as afile:
                awriter = csv.writer(afile)
                awriter.writerow([row[1], row[0], status])
    print(f"{a} attendance applied successfully!")
    return

def view_attendance_report():
    date = input("Enter attendance date (YYYY-MM-DD): ")
    emp_id = int(input("Enter teacher employee ID: "))
    password = input("Enter teacher emp_id password: ")
    with open('teachers.csv', 'r') as file:
        rd = csv.reader(file)
        for row in rd:
            if int(row[0]) == emp_id and row[1] == password:
                print(f"Welcome {row[2]}!")
                class_assigned = row[4]
                if class_assigned:
                    print(f"Attendance report for class{class_assigned} on {date}:")
                    with open(f'attendance_{date}_class{class_assigned}.csv', 'r') as afile:
                        ard = csv.reader(afile)
                        for arow in ard:
                            print(arow)
                else:
                    print("You are not assigned to any class.")
                return
        
            elif row[3].lower() == 'principal':
                print(f"Welcome {row[2]}!")
                print("which class report do you want to view?")
                class_num = int(input("Enter class number: "))
                print("of which date you want to view attendance report?")
                date = input("Enter attendance date (YYYY-MM-DD): ")
                print(f"Attendance report for class{class_num} on {date}:")
                with open(f'attendance_{date}_class{class_num}.csv', 'r') as afile:
                    ard = csv.reader(afile)
                    for arow in ard:
                        print(arow)
            else:
                print("Invalid employee ID or password.")

def view_mess_attendance_report():
    date = input("Enter attendance date (YYYY-MM-DD): ")
    choice = input("the teacher applying for morning attendance(m) or afternoon attendance(a) or night attendance(n) (m/a/n): ")
    a='morning'
    if choice == 'm':
        a="Morning"
    elif choice == 'a':
        a="Afternoon"
    elif choice == 'n':
        a="Night"
    if choice not in ['m', 'a', 'n']:
        print("Invalid choice.")
        return
    with open(f'{a}_attendance_{date}.csv', 'r') as afile:
        ard = csv.reader(afile)
        for arow in ard:
            print(arow)
        
def del_student():
    admno = int(input("Enter student admission number to delete: "))
    with open('students.csv', 'r') as file:
        rd = csv.reader(file)
        for row in rd:
            if int(row[0]) == admno:
                print(f"Student found: {row}")
                confirm = input("Are you sure you want to delete this student? (y/n): ")
                if confirm.lower() == 'y':
                    with open('students.csv', 'w', newline='') as wfile:
                        wwriter = csv.writer(wfile)
                        for wrow in rd:
                            if int(wrow[0]) != admno:
                                wwriter.writerow(wrow)
                    print("Student deleted successfully!")
                else:
                    print("Deletion cancelled.")
                return
            
def del_teacher():
    emp_id = int(input("Enter teacher employee ID to delete: "))
    ps=input("Enter teacher emp_id password: ")
    with open('teachers.csv', 'r') as file:
        r=csv.reader(file)
        for rw in r:
            if int(rw[0]) == emp_id and rw[1] == ps:
                print(f"Teacher found: {rw}")
                confirm = input("Are you sure you want to delete this teacher? (y/n): ")
                if confirm.lower() == 'y':
                    with open('teachers.csv', 'w', newline='') as wfile:
                        w=csv.writer(wfile)
                        for wrow in r:
                            if int(wrow[0]) != emp_id:
                                w.writerow(wrow)
                    print("Teacher deleted successfully!")
                else:
                    print("Deletion cancelled.")
                return
            
    
def update_student():
    admno = int(input("Enter student admission number to update: "))
    with open('students.csv', 'r') as file:
        r=csv.reader(file)
        rows = list(r)
        for rw in range(len(rows)):
            if int(rows[rw][0]) == admno:
                print(f"Student found: {rows[rw]}")
                name = input("Enter new name (leave blank to keep current): ")
                age = input("Enter new age (leave blank to keep current): ")
                gen=input("Enter new gender of student(b/g) (leave blank to keep current): ").upper()
                clas = input("Enter new class (leave blank to keep current): ") 
                roll_no=input("Enter new roll number (leave blank to keep current): ")
                phno=input("Enter new phone number (leave blank to keep current): ")
                if name:
                    rows[rw][1] = name
                if age:
                    rows[rw][2] = age
                if gen:
                    rows[rw][3] = gen
                if clas:
                    rows[rw][4] = clas
                if roll_no:
                    rows[rw][5] = roll_no
                if phno:
                    rows[rw][6] = phno
        with open('students.csv', 'w', newline='') as wfile:
            w=csv.writer(wfile)
            for row in rows:
                w.writerow(row)
            print("Student details updated successfully!")


def update_teacher():
    emp_id = int(input("Enter teacher employee ID to update: "))
    ps=input("Enter teacher emp_id password: ")
    with open('teachers.csv', 'r') as file:
        r=csv.reader(file)
        rows = list(r)
        for rw in range(len(rows)):
            if int(rows[rw][0]) == emp_id and rows[rw][1] == ps:
                print(f"Teacher found: {rows[rw]}")
                name = input("Enter new name (leave blank to keep current): ")
                subject = input("Enter new subject taught (leave blank to keep current): ").lower()
                print("is teacher a class teacher? (y/n)")
                ch=input()
                if ch.lower() == 'y':
                    cl=int(input("Enter new class assigned (leave blank to keep current): "))
                else:
                    cl=None
                if name:
                    rows[rw][2] = name
                if subject:
                    rows[rw][3] = subject
                if ch.lower() == 'y' and cl is not None:
                    rows[rw][4] = cl
                elif ch.lower() == 'n':
                    rows[rw][4] = None
        with open('teachers.csv', 'w', newline='') as wfile:
            w=csv.writer(wfile)
            for row in rows:
                w.writerow(row)
            print("Teacher details updated successfully!")


def generate_attendance_report():
    date = input("Enter attendance date (YYYY-MM-DD): ")
    class_num = int(input("Enter class number: "))
    tc=''
    print(f"Attendance report for class{class_num} on {date}:")
    with open('teachers.csv', 'r') as file:
        rd = csv.reader(file)
        for row in rd:
            if row[4] == class_num:
                tc=row[2]

    with open(f'attendance_{date}_class{class_num}.csv', 'r') as afile:
        ard = csv.reader(afile)
        pcount = 0
        acount = 0
        for arow in ard:
            if arow[2].lower() == 'p':
                pcount += 1
            elif arow[2].lower() == 'a':
                acount += 1
        t=pcount + acount
        print(f"Class: {class_num} \t\t Date: {date} ")
        print(f"Class teacher: {tc}")
        print(f"Total Students: {t} ")
        print(f"Present: {pcount} ")
        print(f"Absent: {acount} ")


def mess_att_summ():
    date = input("Enter attendance date (YYYY-MM-DD): ")
    choice = input("the teacher applying for morning attendance(m) or afternoon attendance(a) or night attendance(n) (m/a/n): ")
    a='morning'
    if choice == 'm':   
        a="Morning"
    elif choice == 'a':
        a="Afternoon"
    elif choice == 'n':
        a="Night"
    pc=0
    ac=0
    with open(f"{a}_attendance_{date}.csv",'r') as f:
        rd=csv.reader(f)
        for r in rd:
            if r[2]=='p':
                pc+=1
            elif r[2]=='a':
                ac+=1
    t=pc+ac

    print(f"MESS ATTENDANCE\t\t DATE:{date}")
    print(f"Total Students: {t} ")
    print(f"Present: {pc} ")
    print(f"Absent: {ac} ")


def student_att_report():
    cl=int(input("enter class of student: "))
    with open("teachers.csv",r) as f:
        rd=csv.reader(f)
        t=0
        for i in rd:
            if i[4]==cl:
                t=i
        if t!=0:
            print('class found')
        em=input("enter your emp id")
        ps=input("enter pass")
        if t[0]==em and t[1]==ps:
            print("entry successful")
            try:
                st=int(input("enter admno. of student to see attendance report"))
            except Exception as err:
                print(f"exception as {err}")
            with open('students.csv','r') as t:
                deta=None
                sl=csv.reader(t)
                for i in sl:
                    if i[0]==st:
                        print("student found") 
                        print(i)
                        deta=i


            std=input("(FROM)enter start date of attendance(YYYY-MM-DD)")
            end=input("(TO)enter end date of attendance(YYYY-MM-DD)")
            
            start = datetime.strptime(std, "%Y-%m-%d")
            end = datetime.strptime(end, "%Y-%m-%d")


    present = 0
    absent = 0

    current = start

    while current <= end:
        date_str = current.strftime("%Y-%m-%d")
        filename = f"attendance_{date_str}_class{cl}.csv"

        try:
            with open(filename, "r") as f:
                rd = csv.reader(f)

                for row in rd:
                    # row = [student_name, roll_no, status]
                    if row[0] ==deta[1]:
                        if row[2].lower() == 'p':
                            present += 1
                        elif row[2].lower() == 'a':
                            absent += 1
                        break

        except FileNotFoundError:
            pass

        current += timedelta(days=1)

    total = present + absent

    print("\n------ STUDENT ATTENDANCE REPORT ------")
    print("Student Name :", deta[1])
    print("Admission No :", deta[0])
    print("Class        :", cl)
    print("Period       :", std, "to", end)
    print("Present Days :", present)
    print("Absent Days  :", absent)
    print("Total Days   :", total)

    if total > 0:
        percentage = (present / total) * 100
        print(f"Attendance % : {percentage:.2f}%")


def main():
    while True:
        print("\nHostel Management System")
        print("1. Add Student Details")
        print("2. Search Student Details")
        print("3. Add Teacher Details")
        print("4. Apply Attendance")
        print("5. Apply Mess Attendance")
        print("6. View Class Attendance")
        print("7. View Mess Attendance ")
        print("8. Delete Student")
        print("9. Delete Teacher")
        print("10. Update Student Details")
        print("11. Update Teacher Details")
        print("12. summarise class Attendance")
        print("13. Summarise mess attendance ")
        print('14. student attendance report using start and end date')
        print("15. Exit")
        
        choice = input("Enter your choice (1-14): ")
        
        if choice == '1':
            add_student()
        elif choice == '2':
            search_student()
        elif choice == '3':
            add_teacher()
        elif choice == '4':
            apply_attendance()
        elif choice == '5':
            mess_attendance()
        elif choice == '6':
            view_attendance_report()
        elif choice == '7':
            view_mess_attendance_report()
        elif choice == '8':
            del_student()
        elif choice == '9':
            del_teacher()
        elif choice == '10':
            update_student()
        elif choice == '11':
            update_teacher()
        elif choice == '12':
            generate_attendance_report()
        elif choice=='13':
            mess_att_summ()
        elif choice=='14':
            student_att_report()        
        elif choice == '15':
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

