from tkinter import *
from tkinter import ttk
import mysql.connector
import csv
from tkinter import messagebox

# Build GUI:

root = Tk()
root.title("UCCD.Tanta Commerce")
root.geometry("450x700")
root.configure(background='white')

# Connect to mysql:
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="uccdpassword",
    database="UCCD")

# Check the connection:
# print(mydb)

# Create a cursor & initialize it for DB:
my_cursor = mydb.cursor()

# Create DB:
my_cursor.execute("CREATE DATABASE IF NOT EXISTS UCCD")

# Drop table:
# my_cursor.execute("DROP DATABASE IF EXISTS test")

# Test to see if the DB was created:
# my_cursor.execute("SHOW DATABASES")
# for db in my_cursor:
#    print(db)

# Create table:
my_cursor.execute("""CREATE TABLE IF NOT EXISTS BIS (Full_name VARCHAR(200)NOT NULL, National_ID VARCHAR(14)PRIMARY 
KEY, Gender ENUM('Male', 'Female')NOT NULL, Birthdate DATE NOT NULL, Email VARCHAR(100)NOT NULL, Mobile VARCHAR(
15)NOT NULL, City VARCHAR(50)NOT NULL, Graduation_year INT(4)NOT NULL, Faculty VARCHAR(100)NOT NULL, Major VARCHAR(
150)NOT NULL, Grade ENUM('Excellent', 'Very good', 'Fair')NOT NULL, Has_disability ENUM('Yes', 'No')NOT NULL, 
Kind_of_disability VARCHAR(150), Previous_courses VARCHAR(200), Current_courses VARCHAR(200), Future_courses VARCHAR(
200));""")


# sql5 = ("DELETE FROM BIS WHERE Full_name = 'mohammad';")
# my_cursor.execute(sql5)
# mydb.commit()

# Alter table:
# my_cursor.execute("ALTER TABLE BIS MODIFY COLUMN Grade ENUM('Excellent', 'Very good', 'Good', 'Fair');")

# Show the table:
# my_cursor.execute("SELECT * FROM BIS")
# print(my_cursor.description)
# for thing in my_cursor.description:
#    print(thing)

# Create clear text fields:
def Clear_fields():
    Full_name_box.delete(0, END)
    National_ID_box.delete(0, END)
    # Gender_box.delete(0, END)
    Birthdate_box.delete(0, END)
    Email_box.delete(0, END)
    Mobile_box.delete(0, END)
    City_box.delete(0, END)
    Graduation_year_box.delete(0, END)
    Faculty_box.delete(0, END)
    # Grade_box.delete(0, END)
    Major_box.delete(0, END)
    # Has_disability_box.delete(0, END)
    Kind_of_disability_box.delete(0, END)
    Previous_courses_box.delete(1.0, END)
    Current_courses_box.delete(1.0, END)
    Future_courses_box.delete(1.0, END)


# Submit student to DB:
def Add_student():
    sql_command = """INSERT INTO BIS (Full_name, National_ID, Gender, Birthdate, Email, Mobile, City, 
    Graduation_year, Faculty, Grade, Major, Has_disability, Kind_of_disability, Previous_courses, Current_courses, 
    Future_courses) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    values = (Full_name_box.get(), National_ID_box.get(), Gender_box.get(), Birthdate_box.get(),
              Email_box.get(), Mobile_box.get(), City_box.get(), Graduation_year_box.get(), Faculty_box.get(),
              Grade_box.get(), Major_box.get(), Has_disability_box.get(), Kind_of_disability_box.get(),
              Previous_courses_box.get("1.0", END), Current_courses_box.get("1.0", END),
              Future_courses_box.get("1.0", END))
    my_cursor.execute(sql_command, values)
    # Commit the changes to DB:
    mydb.commit()
    # Clear the fields:
    Clear_fields()


# WRITE TO CSV EXCEL FUNCTION:
def write_to_csv(result):
    with open('students.csv', 'w') as f:
        w = csv.writer(f, dialect='excel')
        for record in result:
            w.writerow(record)
    messagebox.showinfo("Export to CSV", "Export Completed")


# Search students
def search_students():
    search_students = Tk()
    search_students.title("Search For Students")
    search_students.geometry("500x150")
    search_students.configure(background='white')

    # create function to delete record
    def delete_now():
        # delete a record
        res = messagebox.askquestion("Delete Data", "Are you sure?")
        if res == 'yes':
            sql3 = ("DELETE FROM BIS WHERE National_ID=" + National_ID_box2.get())
            National_ID = National_ID_box.get()
            my_cursor.execute(sql3, National_ID)
            mydb.commit()
            edit_students.destroy()
        elif res == 'no':
            pass

    def clear():
        searched_label.grid_forget()
        mylabel.grid_forget()

    def update():
        sql_command = """UPDATE BIS SET Full_name = %s, National_ID = %s, Gender = %s, Birthdate = %s,
                 Email = %s, Mobile = %s, City = %s, Graduation_year = %s, Faculty = %s, Major = %s, Grade = %s, 
                  Has_disability = %s, Kind_of_disability = %s, Previous_courses = %s, Current_courses = %s,
                   Future_courses = %s WHERE National_ID = %s"""
        Full_name = Full_name_box2.get()
        National_ID = National_ID_box2.get()
        Gender = Gender_box2.get()
        Birthdate = Birthdate_box2.get()
        Email = Email_box2.get()
        Mobile = Mobile_box2.get()
        City = City_box2.get()
        Graduation_year = Graduation_year_box2.get()
        Faculty = Faculty_box2.get()
        Major = Major_box2.get()
        Grade = Grade_box2.get()
        Has_disability = Has_disability_box2.get()
        Kind_of_disability = Kind_of_disability_box2.get()
        Previous_courses = Previous_courses_box2.get(1.0, END)
        Current_courses = Current_courses_box2.get(1.0, END)
        Future_courses = Future_courses_box2.get(1.0, END)

        National_ID_value = National_ID_box2.get()

        inputs = (Full_name, National_ID, Gender, Birthdate, Email, Mobile,
                  City, Graduation_year, Faculty, Major, Grade, Has_disability,
                  Kind_of_disability, Previous_courses, Current_courses,
                  Future_courses, National_ID_value)
        my_cursor.execute(sql_command, inputs)
        mydb.commit()

        edit_students.destroy()

    def edit_now(National_ID, index):
        global edit_students
        edit_students = Tk()
        edit_students.title("Edit")
        edit_students.geometry("450x590")
        edit_students.configure(background='white')

        sql2 = "SELECT * FROM BIS WHERE National_ID = %s"
        name2 = (National_ID,)
        result2 = my_cursor.execute(sql2, name2)
        result2 = my_cursor.fetchall()
        index += 1
        # Create main form to enter customer data:
        Full_name_label = Label(edit_students, text="Full Name", bg="white")
        Full_name_label.grid(row=index + 1, column=0, sticky=W, padx=10, pady=10)
        National_ID_label = Label(edit_students, text="National ID", bg="white")
        National_ID_label.grid(row=index + 2, column=0, sticky=W, padx=10)
        Gender_label = Label(edit_students, text="Gender", bg="white")
        Gender_label.grid(row=index + 3, column=0, sticky=W, padx=10)
        Birthdate_label = Label(edit_students, text="Date Of Birth", bg="white")
        Birthdate_label.grid(row=index + 4, column=0, sticky=W, padx=10)
        Email_label = Label(edit_students, text="Email", bg="white")
        Email_label.grid(row=index + 5, column=0, sticky=W, padx=10)
        Mobile_label = Label(edit_students, text="Phone Number", bg="white")
        Mobile_label.grid(row=index + 6, column=0, sticky=W, padx=10)
        City_label = Label(edit_students, text="City", bg="white")
        City_label.grid(row=index + 7, column=0, sticky=W, padx=10)
        Graduation_year_label = Label(edit_students, text="Graduation year", bg="white")
        Graduation_year_label.grid(row=index + 8, column=0, sticky=W, padx=10)
        Grade_label = Label(edit_students, text="Grade", bg="white")
        Grade_label.grid(row=index + 9, column=0, sticky=W, padx=10)
        Faculty_label = Label(edit_students, text="Faculty", bg="white")
        Faculty_label.grid(row=index + 10, column=0, sticky=W, padx=10)
        Major_label = Label(edit_students, text="Major/Department", bg="white")
        Major_label.grid(row=index + 11, column=0, sticky=W, padx=10)
        Has_disability_label = Label(edit_students, text="Has Disability?", bg="white")
        Has_disability_label.grid(row=index + 12, column=0, sticky=W, padx=10)
        Kind_of_disability_label = Label(edit_students, text="Kind Of Disability", bg="white")
        Kind_of_disability_label.grid(row=index + 13, column=0, sticky=W, padx=10)
        Previous_courses_label = Label(edit_students, text="Previous Courses", bg="white")
        Previous_courses_label.grid(row=index + 14, column=0, sticky=W, padx=10)
        Current_courses_label = Label(edit_students, text="Current Courses", bg="white")
        Current_courses_label.grid(row=index + 15, column=0, sticky=W, padx=10)
        Future_courses_label = Label(edit_students, text="Future Courses", bg="white")
        Future_courses_label.grid(row=index + 16, column=0, sticky=W, padx=10)

        # Create entry boxes:
        global Full_name_box2
        Full_name_box2 = Entry(edit_students, width=30)
        Full_name_box2.grid(row=index + 1, column=1, pady=10)
        Full_name_box2.insert(0, result2[0][0])

        global National_ID_box2
        National_ID_box2 = Entry(edit_students, width=30)
        National_ID_box2.grid(row=index + 2, column=1, pady=5)
        National_ID_box2.insert(0, result2[0][1])

        global Gender_box2
        Gender_box2 = Entry(edit_students, width=30)
        Gender_box2.grid(row=index + 3, column=1, pady=5)
        Gender_box2.insert(0, result2[0][2])

        global Birthdate_box2
        Birthdate_box2 = Entry(edit_students, width=30)
        Birthdate_box2.grid(row=index + 4, column=1, pady=5)
        Birthdate_box2.insert(0, result2[0][3])

        global Email_box2
        Email_box2 = Entry(edit_students, width=30)
        Email_box2.grid(row=index + 5, column=1, pady=5)
        Email_box2.insert(0, result2[0][4])

        global Mobile_box2
        Mobile_box2 = Entry(edit_students, width=30)
        Mobile_box2.grid(row=index + 6, column=1, pady=5)
        Mobile_box2.insert(0, result2[0][5])

        global City_box2
        City_box2 = Entry(edit_students, width=30)
        City_box2.grid(row=index + 7, column=1, pady=5)
        City_box2.insert(0, result2[0][6])

        global Graduation_year_box2
        Graduation_year_box2 = Entry(edit_students, width=30)
        Graduation_year_box2.grid(row=index + 8, column=1, pady=5)
        Graduation_year_box2.insert(0, result2[0][7])

        global Grade_box2
        Grade_box2 = Entry(edit_students, width=30)
        Grade_box2.grid(row=index + 9, column=1, pady=5)
        Grade_box2.insert(0, result2[0][10])

        global Faculty_box2
        Faculty_box2 = Entry(edit_students, width=30)
        Faculty_box2.grid(row=index + 10, column=1, pady=5)
        Faculty_box2.insert(0, result2[0][8])

        global Major_box2
        Major_box2 = Entry(edit_students, width=30)
        Major_box2.grid(row=index + 11, column=1, pady=5)
        Major_box2.insert(0, result2[0][9])

        global Has_disability_box2
        Has_disability_box2 = Entry(edit_students, width=30)
        Has_disability_box2.grid(row=index + 12, column=1, pady=5)
        Has_disability_box2.insert(0, result2[0][11])

        global Kind_of_disability_box2
        Kind_of_disability_box2 = Entry(edit_students, width=30)
        Kind_of_disability_box2.grid(row=index + 13, column=1, pady=5)
        Kind_of_disability_box2.insert(0, result2[0][12])

        global Previous_courses_box2
        Previous_courses_box2 = Text(edit_students, height=2, width=23)
        Previous_courses_box2.grid(row=index + 14, column=1, pady=5)
        Previous_courses_box2.insert(1.0, result2[0][13])

        global Current_courses_box2
        Current_courses_box2 = Text(edit_students, height=2, width=23)
        Current_courses_box2.grid(row=index + 15, column=1, pady=5)
        Current_courses_box2.insert(1.0, result2[0][14])

        global Future_courses_box2
        Future_courses_box2 = Text(edit_students, height=2, width=23)
        Future_courses_box2.grid(row=index + 16, column=1, pady=5)
        Future_courses_box2.insert(1.0, result2[0][15])

        save_record = Button(edit_students, text="Save", borderwidth=5, relief="groove", bg="gray", fg="white",
                             command=update)
        save_record.grid(row=index + 18, column=1, padx=10, pady=10)

        # Create A Delete Button
        delete_button = Button(edit_students, text="Delete", borderwidth=5, relief="groove", bg="red", fg="white",
                               command=delete_now)
        delete_button.grid(row=index + 18, column=2, sticky=W, padx=10, pady=10)

    def search_now():
        global index
        global mylabel
        global searched_label
        selected = drop.get()
        sql = ""
        if selected == "Search By...":
            mylabel = Label(search_students, text="Pick a drop down selection!", bg="white")
            mylabel.grid(row=3, column=0)

        if selected == "Name":
            sql = "SELECT * FROM BIS WHERE Full_name = %s ORDER BY Full_name"

        if selected == "National ID":
            sql = "SELECT * FROM BIS WHERE National_ID = %s ORDER BY Full_name"

        if selected == "Mobile":
            sql = "SELECT * FROM BIS WHERE Mobile = %s ORDER BY Full_name"

        if selected == "City":
            sql = "SELECT * FROM BIS WHERE City = %s ORDER BY Full_name"

        if selected == "Graduation Year":
            sql = "SELECT * FROM BIS WHERE Graduation_year = %s ORDER BY Full_name"

        if selected == "Faculty":
            sql = "SELECT * FROM BIS WHERE Faculty = %s ORDER BY Full_name"

        if selected == "Grade":
            sql = "SELECT * FROM BIS WHERE Grade = %s ORDER BY Full_name"

        if selected == "Major/Department":
            sql = "SELECT * FROM BIS WHERE Major = %s ORDER BY Full_name"

        searched = search_box.get()
        # sql = "SELECT * FROM BIS WHERE Full_name = %s"
        name = (searched,)
        result = my_cursor.execute(sql, name)
        result = my_cursor.fetchall()

        if not result:
            result = "Record Not Found..."
            searched_label = Label(search_students, text=result, bg="white")
            searched_label.grid(row=2, column=0)

        else:
            global search_result
            search_result = Tk()
            search_result.title("Search Result")
            search_result.geometry("1100x800")
            search_result.configure(background='white')
            search_students.destroy()

            # Create a main frame
            main_frame = Frame(search_result, bg="white")
            main_frame.grid(row=0, column=0, sticky='nsew')

            # Create a canvas
            my_canvas = Canvas(main_frame, highlightthickness=0, width=1350, height=688, bg="white")
            my_canvas.grid(row=0, column=0, sticky='w')

            # add a verical scroll bar to the canvas
            my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
            my_scrollbar.grid(row=0, column=1, rowspan=2000, sticky='ns')

            # add a horizontal scroll bar to the canvas
            my_scrollbar3 = ttk.Scrollbar(main_frame, orient=HORIZONTAL, command=my_canvas.xview)
            my_scrollbar3.grid(row=1, column=0, sticky='ew')

            # configure the canvas
            my_canvas.configure(yscrollcommand=my_scrollbar.set)
            my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

            my_canvas.configure(xscrollcommand=my_scrollbar3.set)
            my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

            my_canvas.grid_columnconfigure(0, weight=1)
            my_canvas.grid_rowconfigure(0, weight=1)

            main_frame.grid_columnconfigure(0, weight=1)
            main_frame.grid_rowconfigure(0, weight=1)

            # Create another frame inside the canvas
            second_frame = Frame(my_canvas, width=1345, height=700, bg="white")

            # Add that new frame to a window in the canvas
            my_canvas.create_window((0, 0), window=second_frame, anchor="nw")

            second_frame.grid_columnconfigure(0, weight=1)
            second_frame.grid_rowconfigure(0, weight=1)

            # Create a label to define the data:
            Full_name_label5 = Label(second_frame, text="Full Name", bg="Gray", fg="white", borderwidth=4,
                                     relief="ridge")
            Full_name_label5.grid(row=0, column=1, padx=10, pady=30)
            National_ID_label5 = Label(second_frame, text="National ID", bg="Gray", fg="white", borderwidth=4,
                                       relief="ridge")
            National_ID_label5.grid(row=0, column=2, padx=10)
            Gender_label5 = Label(second_frame, text="Gender", bg="Gray", fg="white", borderwidth=4, relief="ridge")
            Gender_label5.grid(row=0, column=3, padx=10)
            Birthdate_label5 = Label(second_frame, text="Date Of Birth", bg="Gray", fg="white", borderwidth=4,
                                     relief="ridge")
            Birthdate_label5.grid(row=0, column=4, padx=10)
            Email_label5 = Label(second_frame, text="Email", bg="Gray", fg="white", borderwidth=4, relief="ridge")
            Email_label5.grid(row=0, column=5, padx=10)
            Mobile_label5 = Label(second_frame, text="Phone Number", bg="Gray", fg="white", borderwidth=4,
                                  relief="ridge")
            Mobile_label5.grid(row=0, column=6, padx=10)
            City_label5 = Label(second_frame, text="City", bg="Gray", fg="white", borderwidth=4, relief="ridge")
            City_label5.grid(row=0, column=7, padx=10)
            Graduation_year_label5 = Label(second_frame, text="Graduation year", bg="Gray", fg="white", borderwidth=4,
                                           relief="ridge")
            Graduation_year_label5.grid(row=0, column=8, padx=10)
            Grade_label5 = Label(second_frame, text="Grade", bg="Gray", fg="white", borderwidth=4, relief="ridge")
            Grade_label5.grid(row=0, column=11, padx=10)
            Faculty_label5 = Label(second_frame, text="Faculty", bg="Gray", fg="white", borderwidth=4, relief="ridge")
            Faculty_label5.grid(row=0, column=9, padx=10)
            Major_label5 = Label(second_frame, text="Major/Department", bg="Gray", fg="white", borderwidth=4,
                                 relief="ridge")
            Major_label5.grid(row=0, column=10, padx=10)
            Has_disability_label5 = Label(second_frame, text="Has Disability?", bg="Gray", fg="white", borderwidth=4,
                                          relief="ridge")
            Has_disability_label5.grid(row=0, column=12, padx=10)
            Kind_of_disability_label5 = Label(second_frame, text="Kind Of Disability", bg="Gray", fg="white",
                                              borderwidth=4, relief="ridge")
            Kind_of_disability_label5.grid(row=0, column=13, padx=10)
            Previous_courses_label5 = Label(second_frame, text="Previous Courses", bg="Gray", fg="white", borderwidth=4,
                                            relief="ridge")
            Previous_courses_label5.grid(row=0, column=14, padx=10)
            Current_courses_label5 = Label(second_frame, text="Current Courses", bg="Gray", fg="white", borderwidth=4,
                                           relief="ridge")
            Current_courses_label5.grid(row=0, column=15, padx=10)
            Future_courses_label5 = Label(second_frame, text="Future Courses", bg="Gray", fg="white", borderwidth=4,
                                          relief="ridge")
            Future_courses_label5.grid(row=0, column=16, padx=10)

            for index, x in enumerate(result):
                num = 0
                index += 2
                National_ID_reference = str(x[1])
                edit_button = Button(second_frame, text="Edit", bg="gray", fg="black", borderwidth=6, relief='groove',
                                     command=lambda National_ID_reference=National_ID_reference: edit_now(
                                         National_ID_reference, index))
                edit_button.grid(row=index, column=num, pady=10)
                for y in x:
                    searched_label = Label(second_frame, text=y, bg='white')
                    searched_label.grid(row=index, column=num + 1, padx=5)
                    num += 1
            csv_button1 = Button(second_frame, text="Export to CSV", bg="green", fg="white", borderwidth=5,
                                 relief='flat', command=lambda: write_to_csv(result))
            csv_button1.grid(row=index + 1, column=0)

    # Entry box to search for student:
    search_box = Entry(search_students)
    search_box.grid(row=0, column=1, padx=10, pady=10)
    # Entry box label search for student:
    search_box_label = Label(search_students, text="Search :", bg="white")
    search_box_label.grid(row=0, column=0, padx=50, pady=10)
    # Entry box search button for student:
    search_button = Button(search_students, text="Search Students", bg="black", fg="white", borderwidth=5,
                           relief='raised', command=search_now)
    search_button.grid(row=1, column=0, padx=50)
    clear_fields_button2 = Button(search_students, text="Clear", bg="red", fg="white", borderwidth=5, relief='raised',
                                  command=clear)
    clear_fields_button2.grid(row=1, column=2, padx=10)
    # Drop box:
    drop = ttk.Combobox(search_students,
                        values=["Search By...", "Name", "National ID", "Mobile", "City", "Graduation Year", "Faculty",
                                "Grade", "Major/Department"])
    drop.current(0)
    drop.grid(row=0, column=2)


# List students:
def list_students():
    global index
    list_students_query = Tk()
    list_students_query.title("Students' List")
    list_students_query.geometry("1000x600")
    list_students_query.configure(background='white')

    # def Student_no():
    #     my_cursor.execute("SELECT COUNT(*) FROM BIS")
    #     for index, x in enumerate(result):
    #         num = 0
    #         index += 2
    #         for y in x:
    #             num += 1

    # Create a main frame
    main_frame1 = Frame(list_students_query, bg="white")
    main_frame1.grid(row=0, column=0, sticky="nsew")

    main_frame1.grid_columnconfigure(0, weight=1)
    main_frame1.grid_rowconfigure(0, weight=1)

    # Create a canvas
    my_canvas1 = Canvas(main_frame1, highlightthickness=0, width=1350, height=688, bg="white")
    my_canvas1.grid(row=0, column=0, sticky="nsew")

    # add a scroll bar to the canvas
    my_scrollbar1 = ttk.Scrollbar(main_frame1, orient=VERTICAL, command=my_canvas1.yview)
    my_scrollbar1.grid(row=0, column=1, sticky="ns")

    my_scrollbar2 = ttk.Scrollbar(main_frame1, orient=HORIZONTAL, command=my_canvas1.xview)
    my_scrollbar2.grid(row=1, column=0, sticky='ew')

    # configure the canvas
    my_canvas1.configure(yscrollcommand=my_scrollbar1.set)
    my_canvas1.bind('<Configure>', lambda e: my_canvas1.configure(scrollregion=my_canvas1.bbox("all")))

    my_canvas1.configure(xscrollcommand=my_scrollbar2.set)
    my_canvas1.bind('<Configure>', lambda e: my_canvas1.configure(scrollregion=my_canvas1.bbox("all")))

    # Create another frame inside the canvas
    second_frame1 = Frame(my_canvas1, width=1100, height=800, bg="white")

    # Add that new frame to a window in the canvas
    my_canvas1.create_window((0, 0), window=second_frame1, anchor="nw")

    # Create a label to define the data:
    Full_name_label4 = Label(second_frame1, text="Full Name", bg="Gray", fg="white", borderwidth=4, relief="ridge")
    Full_name_label4.grid(row=0, column=0, padx=10, pady=30)
    National_ID_label4 = Label(second_frame1, text="National ID", bg="Gray", fg="white", borderwidth=4, relief="ridge")
    National_ID_label4.grid(row=0, column=1, padx=10)
    Gender_label4 = Label(second_frame1, text="Gender", bg="Gray", fg="white", borderwidth=4, relief="ridge")
    Gender_label4.grid(row=0, column=2, padx=10)
    Birthdate_label4 = Label(second_frame1, text="Date Of Birth", bg="Gray", fg="white", borderwidth=4, relief="ridge")
    Birthdate_label4.grid(row=0, column=3, padx=10)
    Email_label4 = Label(second_frame1, text="Email", bg="Gray", fg="white", borderwidth=4, relief="ridge")
    Email_label4.grid(row=0, column=4, padx=10)
    Mobile_label4 = Label(second_frame1, text="Phone Number", bg="Gray", fg="white", borderwidth=4, relief="ridge")
    Mobile_label4.grid(row=0, column=5, padx=10)
    City_label4 = Label(second_frame1, text="City", bg="Gray", fg="white", borderwidth=4, relief="ridge")
    City_label4.grid(row=0, column=6, padx=10)
    Graduation_year_label4 = Label(second_frame1, text="Graduation year", bg="Gray", fg="white", borderwidth=4,
                                   relief="ridge")
    Graduation_year_label4.grid(row=0, column=7, padx=10)
    Grade_label4 = Label(second_frame1, text="Grade", bg="Gray", fg="white", borderwidth=4, relief="ridge")
    Grade_label4.grid(row=0, column=10, padx=10)
    Faculty_label4 = Label(second_frame1, text="Faculty", bg="Gray", fg="white", borderwidth=4, relief="ridge")
    Faculty_label4.grid(row=0, column=8, padx=10)
    Major_label4 = Label(second_frame1, text="Major/Department", bg="Gray", fg="white", borderwidth=4, relief="ridge")
    Major_label4.grid(row=0, column=9, padx=10)
    Has_disability_label4 = Label(second_frame1, text="Has Disability?", bg="Gray", fg="white", borderwidth=4,
                                  relief="ridge")
    Has_disability_label4.grid(row=0, column=11, padx=10)
    Kind_of_disability_label4 = Label(second_frame1, text="Kind Of Disability", bg="Gray", fg="white", borderwidth=4,
                                      relief="ridge")
    Kind_of_disability_label4.grid(row=0, column=12, padx=10)
    Previous_courses_label4 = Label(second_frame1, text="Previous Courses", bg="Gray", fg="white", borderwidth=4,
                                    relief="ridge")
    Previous_courses_label4.grid(row=0, column=13, padx=10)
    Current_courses_label4 = Label(second_frame1, text="Current Courses", bg="Gray", fg="white", borderwidth=4,
                                   relief="ridge")
    Current_courses_label4.grid(row=0, column=14, padx=10)
    Future_courses_label4 = Label(second_frame1, text="Future Courses", bg="Gray", fg="white", borderwidth=4,
                                  relief="ridge")
    Future_courses_label4.grid(row=0, column=15, padx=10)

    # Query the DB:
    my_cursor.execute("SELECT * FROM BIS ORDER BY Full_name")

    result = my_cursor.fetchall()
    for index, x in enumerate(result):
        num = 0
        for y in x:
            lookup_label = Label(second_frame1, text=y, bg='white')
            lookup_label.grid(row=index + 1, column=num, padx=10, pady=5)
            num += 1
    csv_button = Button(second_frame1, text="Export to CSV", bg="green", fg="white", borderwidth=5, relief='flat',
                        command=lambda: write_to_csv(result))
    csv_button.grid(row=index + 2, column=0)

    # counter button
    # counter_button = Button(second_frame1, text="Number Of Students", bg="Gray", fg="white",
    #                         command= Student_no)
    # counter_button.grid(row=0, column=17, padx=10, pady=30)


# Create a label:
title_label = Label(root, text="*UCCD.Tanta Commerce*", bg="white", fg="brown", font=("frontierswoman", 11, "bold"))
title_label.grid(row=0, column=1, columnspan=1, pady="10")

# Create main form to enter customer data:
Full_name_label = Label(root, text="Full Name", bg="white")
Full_name_label.grid(row=1, column=0, sticky=W, padx=10)
National_ID_label = Label(root, text="National ID", bg="white")
National_ID_label.grid(row=2, column=0, sticky=W, padx=10)
Gender_label = Label(root, text="Gender", bg="white")
Gender_label.grid(row=3, column=0, sticky=W, padx=10)
Birthdate_label = Label(root, text="Date Of Birth", bg="white")
Birthdate_label.grid(row=4, column=0, sticky=W, padx=10)
Email_label = Label(root, text="Email", bg="white")
Email_label.grid(row=5, column=0, sticky=W, padx=10)
Mobile_label = Label(root, text="Phone Number", bg="white")
Mobile_label.grid(row=6, column=0, sticky=W, padx=10)
City_label = Label(root, text="City", bg="white")
City_label.grid(row=7, column=0, sticky=W, padx=10)
Graduation_year_label = Label(root, text="Graduation year", bg="white")
Graduation_year_label.grid(row=8, column=0, sticky=W, padx=10)
Grade_label = Label(root, text="Grade", bg="white")
Grade_label.grid(row=9, column=0, sticky=W, padx=10)
Faculty_label = Label(root, text="Faculty", bg="white")
Faculty_label.grid(row=10, column=0, sticky=W, padx=10)
Major_label = Label(root, text="Major/Department", bg="white")
Major_label.grid(row=11, column=0, sticky=W, padx=10)
Has_disability_label = Label(root, text="Has Disability?", bg="white")
Has_disability_label.grid(row=12, column=0, sticky=W, padx=10)
Kind_of_disability_label = Label(root, text="Kind Of Disability", bg="white")
Kind_of_disability_label.grid(row=13, column=0, sticky=W, padx=10)
Previous_courses_label = Label(root, text="Previous Courses", bg="white")
Previous_courses_label.grid(row=14, column=0, sticky=W, padx=10)
Current_courses_label = Label(root, text="Current Courses", bg="white")
Current_courses_label.grid(row=15, column=0, sticky=W, padx=10)
Future_courses_label = Label(root, text="Future Courses", bg="white")
Future_courses_label.grid(row=16, column=0, sticky=W, padx=10)

# Create entry boxes:
Full_name_box = Entry(root, width=30)
Full_name_box.grid(row=1, column=1)
National_ID_box = Entry(root, width=30)
National_ID_box.grid(row=2, column=1, pady=5)
Gender_box = IntVar()
Gender_box_Male = Radiobutton(root, text="Male", variable=Gender_box, bg="white", font=("arial", 10), value=1)
Gender_box_Female = Radiobutton(root, text="Female", variable=Gender_box, bg="white", font=("arial", 10), value=2)
Gender_box_Male.grid(row=3, column=1, sticky=W)
Gender_box_Female.grid(row=3, column=2, sticky=W)
Birthdate_box = Entry(root, width=30)
Birthdate_box.grid(row=4, column=1, pady=5)
Email_box = Entry(root, width=30)
Email_box.grid(row=5, column=1, pady=5)
Mobile_box = Entry(root, width=30)
Mobile_box.grid(row=6, column=1, pady=5)
City_box = Entry(root, width=30)
City_box.grid(row=7, column=1, pady=5)
Graduation_year_box = Entry(root, width=30)
Graduation_year_box.grid(row=8, column=1, pady=5)
Grade = ["Excellent", "Very good", "Good", "Fair"]  # Dropdown menu options
Grade_box = StringVar(root)  # datatype of menu text
drop = OptionMenu(root, Grade_box, *Grade)
drop.config(bg="white")
drop.grid(row=9, column=1, pady=5)
Faculty_box = Entry(root, width=30)
Faculty_box.grid(row=10, column=1, pady=5)
Major_box = Entry(root, width=30)
Major_box.grid(row=11, column=1, pady=5)
Has_disability_box = IntVar()
Has_disability_box_YES = Radiobutton(root, text="Yes", variable=Has_disability_box, bg="white", font=("arial", 10),
                                     value=1)
Has_disability_box_NO = Radiobutton(root, text="No", variable=Has_disability_box, bg="white", font=("arial", 10),
                                    value=2)
Has_disability_box_YES.grid(row=12, column=1, sticky=W)
Has_disability_box_NO.grid(row=12, column=2, sticky=W)
Kind_of_disability_box = Entry(root, width=30, font=('Arial', 10))
Kind_of_disability_box.grid(row=13, column=1, pady=5)
Previous_courses_box = Text(root, height=2, width=30, font=('Arial', 10))
Previous_courses_box.grid(row=14, column=1, pady=5)
Current_courses_box = Text(root, height=2, width=30, font=('Arial', 10))
Current_courses_box.grid(row=15, column=1, pady=5)
Future_courses_box = Text(root, height=2, width=30, font=('Arial', 10))
Future_courses_box.grid(row=16, column=1, pady=5)

# Create buttons:
add_student_button = Button(root, text="Add Student", bg="gray", fg="black", borderwidth=5, relief='groove',
                            command=Add_student)
add_student_button.grid(row=19, column=1, pady=10, sticky='w')
clear_fields_button = Button(root, text="Clear Fields", bg="red", fg="white", borderwidth=5, relief='raised',
                             command=Clear_fields)
clear_fields_button.grid(row=18, column=0, sticky=W, padx=10)

# List students button:
list_students_button = Button(root, text="List", bg="gray", fg="black", borderwidth=5, relief='groove',
                              command=list_students)
list_students_button.grid(row=19, column=0, sticky=W, padx=10)

# search students:
search_students_button = Button(root, text="Search/Edit", bg="black", fg="white", borderwidth=5, relief='raised',
                                command=search_students)
search_students_button.grid(row=20, column=0, sticky=W, padx=10)

# Launch the GUI:
root.mainloop()
