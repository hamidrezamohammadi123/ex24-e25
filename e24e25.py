""" 
Create a relational database for a university system that includes three tables:
Students, Courses, and Enrollments. 
The database should track the students, the courses offered, and the enrollments of students in these courses.

1. StudentsFields: StudentID(Primary Key), FirstName, LastName, DateOfBirth, Email
2. CoursesFields: CourseID(Primary Key), CourseName, Instructor
3. EnrollmentsFields: EnrollmentID(Primary Key), StudentID(Foreign Key), CourseID(Foreign Key), EnrollmentDate

1. Data InsertionInsert sample data into the Students, Courses, and Enrollments tables.Ensure that the data is consistent and follows the relationships between the tables.
2. Querying Student EnrollmentsWrite a query to find the names of all students and the count of courses they are enrolled in.The output should be a list of students and the number of courses they're taking.
3. Data RemovalWrite a SQL statement to remove students who are enrolled in less than 2 courses.Ensure the integrity of the database after the removal.
4. Updating Course NamesWrite an update statement to change all courses with "Java" in their name to "Python."Confirm the update with a select statement.

"""


 
import mysql.connector

#----------------------------------------    Create a connection object
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Mhm789987456654",
    database="University"
)


cursor = conn.cursor()

#-----------------------------------------   Create the tables
def create_tables():
    # -----------------------    Students table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Students (
            StudentID INT PRIMARY KEY,
            FirstName VARCHAR(50),
            LastName VARCHAR(50),
            DateOfBirth DATE,
            Email VARCHAR(100)
        )
    """)

    # -----------------------    Courses table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Courses (
            CourseID INT PRIMARY KEY,
            CourseName VARCHAR(50),
            Instructor VARCHAR(50)
        )
    """)

    # -----------------------    Enrollments table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Enrollments (
            EnrollmentID INT PRIMARY KEY,
            StudentID INT,
            CourseID INT,
            EnrollmentDate DATE,
            FOREIGN KEY (StudentID) REFERENCES Students(StudentID),
            FOREIGN KEY (CourseID) REFERENCES Courses(CourseID)
        )
    """)

    conn.commit()
    print("Tables created successfully")

# ------------------------------------------ Insert data into the tables
def insert_data():
    # ------------  how many to insert ?
    student_count = int(input("How many students ? "))
    course_count = int(input("How many courses ? "))
    enrollment_count = int(input("How many enrollments ? "))


    # ---------------------------------------    student details
    for i in range(student_count):

        # Get data
        student_id = int(input(f"Enter the student ID for student {i+1}: "))        
        first_name = input(f"Enter the first name for student {i+1}: ")
        last_name = input(f"Enter the last name for student {i+1}: ")
        date_of_birth = input(f"Enter the date of birth (YYYY-MM-DD) for student {i+1}: ")
        email = input(f"Enter the email for student {i+1}: ")

        # Insert the student data 
        cursor.execute("""
            INSERT INTO Students (StudentID, FirstName, LastName, DateOfBirth, Email)
            VALUES (%s, %s, %s, %s, %s)
        """, (student_id, first_name, last_name, date_of_birth, email))

        
    # --------------------------------    Loop for the course details
    for i in range(course_count):
        # Get the course ID, course name and instructor from the user
        course_id = int(input(f"Enter the course ID for course {i+1}: "))
        course_name = input(f"Enter the course name for course {i+1}: ")
        instructor = input(f"Enter the instructor for course {i+1}: ")

        # Insert the course data into the Courses table
        cursor.execute("""
            INSERT INTO Courses (CourseID, CourseName, Instructor)
            VALUES (%s, %s, %s)
        """, (course_id, course_name, instructor))


    # ---------------------------------    Loop for the enrollment details
    for i in range(enrollment_count):
        # Get data
        enrollment_id = int(input(f"Enter the enrollment ID for enrollment {i+1}: "))
        student_id = int(input(f"Enter the student ID for enrollment {i+1}: "))
        course_id = int(input(f"Enter the course ID for enrollment {i+1}: "))
        enrollment_date = input(f"Enter the enrollment date (YYYY-MM-DD) for enrollment {i+1}: ")
        # Insert the enrollment data 
        cursor.execute("""
            INSERT INTO Enrollments (EnrollmentID, StudentID, CourseID, EnrollmentDate)
            VALUES (%s, %s, %s, %s)
        """, (enrollment_id, student_id, course_id, enrollment_date))

   
    conn.commit()
    print("Data inserted successfully")

# -----------------------------------     Query the student enrollments
def query_enrollments():
    cursor.execute("""
        SELECT s.FirstName, s.LastName, COUNT(e.CourseID) AS CourseCount
        FROM Students s
        JOIN Enrollments e
        ON s.StudentID = e.StudentID
        GROUP BY s.StudentID
    """)
   
    results = cursor.fetchall()
    print("Student Enrollments:")

    for row in results:
        print(row)

#  -------------------------------------    Remove students who are enrolled in less than 2 courses
def remove_students():
    # Execute a query to find the student IDs of those who are enrolled in less than 2 courses
    cursor.execute("""
        SELECT s.StudentID
        FROM Students s
        JOIN Enrollments e
        ON s.StudentID = e.StudentID
        GROUP BY s.StudentID
        HAVING COUNT(e.CourseID) < 2
    """)
    
    results = cursor.fetchall()
    
    for row in results:
        student_id = row[0]
        # Delete the student 
        cursor.execute("""
            DELETE FROM Students
            WHERE StudentID = %s
        """, (student_id,))
        
        # Delete the enrollments 
        cursor.execute("""
            DELETE FROM Enrollments
            WHERE StudentID = %s
        """, (student_id,))

    
    conn.commit()
    print("Students removed successfully")

# ------------------------------------------      Update the course names
def update_courses():

    #  Change the course names with "Java" to "Python"
    cursor.execute("""
        UPDATE Courses
        SET CourseName = REPLACE(CourseName, 'Java', 'Python')
        WHERE CourseName LIKE '%Java%'
    """)

    
    conn.commit()
    print("Courses updated successfully")


    # Confirm the update
    cursor.execute("""
        SELECT * FROM Courses
    """)
    
    results = cursor.fetchall()
    print("Courses after update:")
    for row in results:
        print(row)

# -----------------------------------------  Close the connection
def close_connection():
    # Close the cursor
    cursor.close()
    # Close the connection
    conn.close()
    # Print a message
    print("Connection closed")

# ------------------------------------------   Display the menu
def display_menu():
    
    print("Please choose one of the following options:")
    print("1. Create the tables")
    print("2. Insert data into the tables")
    print("3. Query the student enrollments")
    print("4. Remove students who are enrolled in less than 2 courses")
    print("5. Update the course names with Java to Python")
    print("6. Exit the program")
    
    choice = input("Enter your choice: ")
    
    return choice

#  ------------------------------------         Main function


def main():
    print("Welcome to the university database program")
    
    while True:                              # Loop until the user chooses to exit 
        
        choice = display_menu()
        if choice == "1":
             create_tables()        # Create the tables
        elif choice == "2":
             insert_data()            # Insert data
        elif choice == "3":
             query_enrollments()      #Query the student enrollments
        elif choice == "4":
             remove_students()        # Remove students who are enrolled in less than 2 courses
        elif choice == "5":
             update_courses()         # Update the course names with Java to Python
        elif choice == "6":
             break                    # Exit the program
        else:
             print("Invalid choice, please try again")  

main()  
    