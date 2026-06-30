import csv
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="EduTrack Pro",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 EduTrack Pro")

def load_students():
    try:
        return pd.read_csv("students.csv", header=None)
    except:
        return pd.DataFrame(columns=["admno","name","age","gender","class","roll","phone"])


def load_teachers():
    try:
        return pd.read_csv("teachers.csv", header=None)
    except:
        return pd.DataFrame()

# Sidebar
menu = st.sidebar.selectbox(
    "Menu",
    [
        "Dashboard",
        "Students",
        "Teachers",
        "Attendance",
        "Reports"
    ]
)

# Dashboard Page
if menu == "Dashboard":
    st.header("Dashboard")
    st.write("Welcome to EduTrack Pro")

# Students Page
if menu == "Students":

    st.header("Student Management")

    operation = st.selectbox(
        "Operation",
        [
            "Add Student",
            "Search Student",
            "View All Students",
            "Update Student",
            "Delete Student"
        ]
    )

    if operation == "Add Student":

        st.subheader("➕ Add Student")

        admno = st.text_input("Admission Number")

        name = st.text_input("Student Name")

        age = st.number_input(
            "Age",
            min_value=1,
            max_value=100
        )

        gender = st.selectbox(
            "Gender",
            ["Male", "Female"]
        )

        clas = st.number_input(
            "Class",
            min_value=1,
            max_value=12
        )

        roll = st.number_input(
            "Roll Number",
            min_value=1
        )

        phone = st.text_input("Phone Number")

        if st.button("Add Student"):
            

            with open(
                "students.csv",
                "a",
                newline=""
            ) as file:

                writer = csv.writer(file)

                writer.writerow([
                    admno,
                    name,
                    age,
                    gender,
                    clas,
                    roll,
                    phone
                ])

            st.success("Student Added Successfully")

    elif operation == "Search Student":

        st.subheader("🔍 Search Student")

        search_adm = st.text_input(
            "Enter Admission Number"
        )

        if st.button("Search"):

            found = False

            with open("students.csv", "r") as file:

                reader = csv.reader(file)

                for row in reader:

                    if row[0] == search_adm:

                        found = True

                        st.success("Student Found")


                        st.markdown("### 👨‍🎓 Student Profile")
                        col1, col2 = st.columns(2)

                        with col1:
                            st.info(f"**Admission No:** {row[0]}")
                            st.info(f"**Name:** {row[1]}")
                            st.info(f"**Age:** {row[2]}")

                        with col2:
                            st.info(f"**Class:** {row[4]}")
                            st.info(f"**Roll No:** {row[5]}")
                            st.info(f"**Phone:** {row[6]}")

                        break

            if not found:
                st.error("Student Not Found")


    elif operation == "View All Students":

        st.subheader("📋 All Students")

        df = pd.read_csv(
            "students.csv",
            header=None
        )

        df.columns = [
            "Admission No",
            "Name",
            "Age",
            "Gender",
            "Class",
            "Roll No",
            "Phone"
        ]

        st.dataframe(
            df,
            use_container_width=True
        )



    elif operation == "Delete Student":

        st.subheader("🗑 Delete Student")

        delete_adm = st.text_input(
            "Enter Admission Number"
        )

        if st.button("Delete Student"):

            students = []
            found = False

            with open("students.csv", "r") as file:

                reader = csv.reader(file)

                for row in reader:

                    if row[0] == delete_adm:
                        found = True
                        continue

                    students.append(row)

            with open(
                "students.csv",
                "w",
                newline=""
            ) as file:

                writer = csv.writer(file)
                writer.writerows(students)

            if found:
                st.success("✅ Student Deleted Successfully")
            else:
                st.error("❌ Student Not Found")



if menu == "Dashboard":
    st.header("📊 Dashboard Overview")

    col1, col2, col3 = st.columns(3)

    students = load_students()
    teachers = load_teachers()

    # Add column names if data exists
    if len(students) > 0:
        students.columns = [
            "Roll No",
            "Name",
            "Age",
            "Section",
            "Class",
            "Marks",
            "Phone No"
        ]

    with col1:
        st.metric("Students", len(students))

    with col2:
        st.metric("Teachers", len(teachers))

    with col3:
        st.metric("Classes", students["Class"].nunique() if len(students) > 0 else 0)

    st.subheader("📌 Recent Students")

    st.dataframe(
        students[[
            "Roll No",
            "Name",
            "Age",
            "Section",
            "Class",
            "Phone No"
        ]].tail(5),
        use_container_width=True
    )


# Teachers Page
if menu == "Teachers":

    st.header("👨‍🏫 Teacher Management")

    option = st.selectbox(
        "Operation",
        ["Add Teacher", "View Teachers", "Update Teacher", "Delete Teacher"]
    )

    # ---------------- ADD ----------------
    if option == "Add Teacher":

        emp_id = st.text_input("Employee ID")
        password = st.text_input("Password", type="password")
        name = st.text_input("Teacher Name")
        subject = st.text_input("Subject")

        class_assigned = st.text_input(
            "Assigned Class (Enter 0 for Principal)"
        )

        if st.button("Add Teacher"):

            with open("teachers.csv", "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([
                    emp_id,
                    password,
                    name,
                    subject,
                    class_assigned
                ])

            st.success("Teacher Added Successfully")

    # ---------------- VIEW ----------------
    elif option == "View Teachers":

        df = load_teachers()

        df.columns = [
            "Employee ID",
            "Password",
            "Name",
            "Subject",
            "Class"
        ]

        st.dataframe(df)

    # ---------------- UPDATE ----------------
    elif option == "Update Teacher":

        df = load_teachers()

        emp_id = st.text_input("Enter Employee ID")

        if st.button("Search Teacher"):

            teacher = df[df[0].astype(str) == emp_id]

            if teacher.empty:
                st.error("Teacher Not Found")

            else:

                teacher = teacher.iloc[0]

                st.session_state.update_teacher = teacher

        if "update_teacher" in st.session_state:

            teacher = st.session_state.update_teacher

            password = st.text_input(
                "Password",
                value=str(teacher[1])
            )

            name = st.text_input(
                "Name",
                value=str(teacher[2])
            )

            subject = st.text_input(
                "Subject",
                value=str(teacher[3])
            )

            class_assigned = st.text_input(
                "Class",
                value=str(teacher[4])
            )

            if st.button("Save Changes"):

                index = df[df[0].astype(str) == emp_id].index[0]

                df.loc[index] = [
                    emp_id,
                    password,
                    name,
                    subject,
                    class_assigned
                ]

                df.to_csv(
                    "teachers.csv",
                    index=False,
                    header=False
                )

                del st.session_state["update_teacher"]

                st.success("Teacher Updated Successfully")

    # ---------------- DELETE ----------------
    elif option == "Delete Teacher":

        df = load_teachers()

        emp_id = st.text_input("Enter Employee ID")

        if st.button("Delete Teacher"):

            if emp_id.lower() == "principal":

                st.error("Principal cannot be deleted.")

            else:

                new_df = df[df[0].astype(str) != emp_id]

                if len(new_df) == len(df):

                    st.error("Teacher Not Found")

                else:

                    new_df.to_csv(
                        "teachers.csv",
                        index=False,
                        header=False
                    )

                    st.success("Teacher Deleted Successfully")
# ========================= ATTENDANCE PAGE =========================
# ========================= ATTENDANCE PAGE =========================
if menu == "Attendance":

    st.header("📅 Attendance System")

    students = load_students()
    teachers = load_teachers()

    students[4] = pd.to_numeric(students[4], errors="coerce")

    if "attendance_login" not in st.session_state:
        st.session_state.attendance_login = False

    if "teacher_id" not in st.session_state:
        st.session_state.teacher_id = ""

    # ---------------- LOGIN ----------------
    if not st.session_state.attendance_login:

        st.subheader("🔐 Teacher Login")

        emp_id = st.text_input("Teacher ID")
        password = st.text_input("Password", type="password")

        if st.button("Login"):

            teacher = teachers[
                (teachers[0].astype(str).str.strip() == emp_id.strip()) &
                (teachers[1].astype(str).str.strip() == password.strip())
            ]

            if teacher.empty:
                st.error("Invalid ID or Password")

            else:
                st.session_state.attendance_login = True
                st.session_state.teacher_id = emp_id.strip()
                st.rerun()

    # ---------------- AFTER LOGIN ----------------
    else:

        teacher = teachers[
            teachers[0].astype(str).str.strip() ==
            st.session_state.teacher_id
        ]

        if teacher.empty:
            st.error("Teacher not found.")
            st.session_state.attendance_login = False
            st.rerun()

        teacher = teacher.iloc[0]

        emp_id = str(teacher[0]).strip()
        teacher_name = str(teacher[2]).strip()
        subject = str(teacher[3]).strip().lower()
        assigned_class = str(teacher[4]).strip()

        st.success(f"Welcome {teacher_name}")

        # Principal
        if subject == "principal":

            classes = sorted(
                students[4].dropna().astype(int).unique().tolist()
            )

            class_num = st.selectbox(
                "Select Class",
                classes
            )

        # Teacher
        else:

            class_num = int(float(assigned_class))

            st.info(f"Assigned Class : {class_num}")

        # ---------------- STUDENTS ----------------

        filtered = students[
            students[4].astype(int) == int(class_num)
        ]

        if filtered.empty:
            st.warning("No students found for this class.")
            st.stop()

        attendance = {}

        st.subheader("Mark Attendance")

        for _, row in filtered.iterrows():

            attendance[row[0]] = st.radio(
                f"{row[1]} (Roll {row[5]})",
                ["Present", "Absent"],
                horizontal=True,
                key=f"{row[0]}"
            )

        date = st.date_input("Attendance Date")

        if st.button("💾 Save Attendance"):

            filename = f"attendance_{class_num}_{date}.csv"

            with open(filename, "w", newline="") as f:

                writer = csv.writer(f)

                writer.writerow([
                    "Admission No",
                    "Name",
                    "Roll",
                    "Status"
                ])

                for _, row in filtered.iterrows():

                    writer.writerow([
                        row[0],
                        row[1],
                        row[5],
                        attendance[row[0]]
                    ])

            st.success("Attendance Saved Successfully!")

        if st.button("Logout"):

            st.session_state.attendance_login = False
            st.session_state.teacher_id = ""
            st.rerun()

if menu == "Reports":
    st.header("📊 Reports System")

    option = st.selectbox(
        "Select Report Type",
        ["Class Report", "Student Report"]
    )

    students = load_students()

    # ---------------- CLASS REPORT ----------------
    if option == "Class Report":

        date = st.text_input("Enter Date (YYYY-MM-DD)")
        class_num = st.number_input("Class", min_value=1, max_value=12)

        if st.button("Generate Class Report"):

            file = f"attendance_{date}_class{class_num}.csv"

            try:
                df = pd.read_csv(file, header=None)
                df.columns = ["Admno", "Name", "Roll", "Status"]

                st.subheader(f"📘 Class {class_num} Report - {date}")

                st.dataframe(df)

                present = (df["Status"].str.lower() == "present").sum()
                absent = (df["Status"].str.lower() == "absent").sum()
                total = present + absent

                col1, col2, col3 = st.columns(3)
                col1.metric("Present", present)
                col2.metric("Absent", absent)
                col3.metric("Total", total)

            except:
                st.error("No attendance file found")

    # ---------------- STUDENT REPORT ----------------
    elif option == "Student Report":

        st.subheader("👤 Student Attendance Report")

        admno = st.text_input("Enter Admission Number")

        class_num = st.number_input("Class", min_value=1, max_value=12)

        start_date = st.date_input("Start Date")
        end_date = st.date_input("End Date")

        if st.button("Generate Student Report"):

            # 🔍 Get student details
            student_info = students[students[0].astype(str) == str(admno)]

            if student_info.empty:
                st.error("Student not found")
                st.stop()

            student_info = student_info.iloc[0]

            name = student_info[1]
            age = student_info[2]
            gender = student_info[3]
            roll = student_info[5]
            phone = student_info[6]

            present = 0
            absent = 0

            current = start_date

            while current <= end_date:

                file = f"attendance_{current}_class{class_num}.csv"

                try:
                    df = pd.read_csv(file, header=None)
                    df.columns = ["Admno", "Name", "Roll", "Status"]

                    record = df[df["Admno"].astype(str) == str(admno)]

                    if not record.empty:
                        status = record.iloc[0]["Status"].lower()

                        if status == "present":
                            present += 1
                        elif status == "absent":
                            absent += 1

                except:
                    pass

                current += pd.Timedelta(days=1)

            total = present + absent

            # 📌 OUTPUT
            st.subheader("📌 Student Details")

            st.write(f"**Admission No:** {admno}")
            st.write(f"**Name:** {name}")
            st.write(f"**Class:** {class_num}")
            st.write(f"**Roll No:** {roll}")
            st.write(f"**Gender:** {gender}")
            st.write(f"**Phone:** {phone}")

            st.subheader("📊 Attendance Summary")

            col1, col2, col3 = st.columns(3)
            col1.metric("Present Days", present)
            col2.metric("Absent Days", absent)
            col3.metric("Total Days", total)

            if total > 0:
                st.success(f"Attendance %: {(present/total)*100:.2f}%")