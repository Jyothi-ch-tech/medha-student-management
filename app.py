import streamlit as st
import mysql.connector
import pandas as pd

# Database Connection
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="medha",
    database="medha_db"
)

cursor = mydb.cursor()

# Page Config
st.set_page_config(
    page_title="Medha Student Management",
    page_icon="🎓",
    layout="wide"
)

# Title
st.title("🎓 Medha Student Management System")
st.markdown("---")

# Sidebar
menu = st.sidebar.selectbox(
    "Select Operation",
    ["Add Student", "Display Students", "Search Student", "Update Student", "Delete Student"]
)

# Add Student
if menu == "Add Student":

    st.header("Add Student")

    mssid = st.text_input("Enter MSS ID")
    name = st.text_input("Enter Name")
    batch = st.number_input("Enter Batch", min_value=1, max_value=2100)
    dist = st.text_input("Enter DIST")

    if st.button("Add Student"):

        try:
            sql = "INSERT INTO students VALUES (%s, %s, %s, %s)"
            values = (mssid, name, batch, dist)

            cursor.execute(sql, values)
            mydb.commit()

            st.success("Student Added Successfully")

        except mysql.connector.Error as err:
            st.error(err)

# Display Students
elif menu == "Display Students":

    st.header("All Students")

    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()

    df = pd.DataFrame(data, columns=["MSSID", "Name", "Batch", "DIST"])

    st.dataframe(df, use_container_width=True)

# Search Student
elif menu == "Search Student":

    st.header("Search Student")

    mssid = st.text_input("Enter MSS ID")

    if st.button("Search"):

        sql = "SELECT * FROM students WHERE mssid=%s"
        value = (mssid,)

        cursor.execute(sql, value)
        student = cursor.fetchone()

        if student:

            st.success("Student Found")

            st.write(f"MSSID : {student[0]}")
            st.write(f"Name : {student[1]}")
            st.write(f"Batch : {student[2]}")
            st.write(f"DIST : {student[3]}")

        else:
            st.error("Student Not Found")

# Update Student
elif menu == "Update Student":

    st.header("Update Student")

    mssid = st.text_input("Enter MSS ID")
    name = st.text_input("Enter New Name")
    batch = st.number_input("Enter New Batch", min_value=1, max_value=2100)
    dist = st.text_input("Enter New DIST")

    if st.button("Update Student"):

        sql = """
        UPDATE students
        SET name=%s, batch=%s, dist=%s
        WHERE mssid=%s
        """

        values = (name, batch, dist, mssid)

        cursor.execute(sql, values)
        mydb.commit()

        if cursor.rowcount > 0:
            st.success("Student Updated Successfully")
        else:
            st.error("Student Not Found")

# Delete Student
elif menu == "Delete Student":

    st.header("Delete Student")

    mssid = st.text_input("Enter MSS ID")

    if st.button("Delete Student"):

        sql = "DELETE FROM students WHERE mssid=%s"
        value = (mssid,)

        cursor.execute(sql, value)
        mydb.commit()

        if cursor.rowcount > 0:
            st.success("Student Deleted Successfully")
        else:
            st.error("Student Not Found")
