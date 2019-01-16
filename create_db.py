import os
import sqlite3
import sys

def print_table(list_of_tuples):
    for item in list_of_tuples:
        print(item)


# Creating all the tables and parsing the config file
def main(args):
    databaseexisted = os.path.isfile('schedule.db')
    dbcon = sqlite3.connect('schedule.db')
    with dbcon:
        cursor=dbcon.cursor()
        if not databaseexisted:
            #Creating tables
            cursor.execute(""" CREATE TABLE students(
            					      			    grade TEXT PRIMARY KEY,
	                                             	count INTEGER NOT NULL)""")
            cursor.execute(""" CREATE TABLE courses(
    												id INTEGER PRIMARY KEY, 
		                                            course_name TEXT NOT NULL,
		                                            student TEXT NOT NULL,
		                                            number_of_students INTEGER NOT NULL,
		                                            class_id INTEGER REFERENCES classrooms(id),
		                                            course_length INTEGER NOT NULL)""")
            cursor.execute(""" CREATE TABLE classrooms(
	        											id INTEGER PRIMARY KEY,
		                                                location TEXT NOT NULL,
		                                                current_course_id INTEGER NOT NULL,
		                                                current_course_time_left INTEGER NOT NULL)""")

        	#parsing the config file:
            config = args[1]
            with open(config) as inputfile:
                for line in inputfile:
                    lst=list()
                    lst=line.split(',')
                    if lst[0] == 'C':
                        cursor.execute("INSERT INTO courses VALUES (?, ?, ?, ?, ?, ?)",
                        (int(lst[1]),lst[2].strip(),lst[3].strip(),int(lst[4]),int(lst[5]),int(lst[6])))
                    elif lst[0] == 'S':
                        cursor.execute("INSERT INTO students VALUES (?, ?)",
                                       (lst[1].strip(), int(lst[2])))
                    elif lst[0] == 'R':
                        cursor.execute("INSERT INTO classrooms VALUES (?, ?, ?, ?)",
                                       (int(lst[1]), lst[2].strip(' \n'), 0, 0))
            # Printing all tables
            cursor.execute("SELECT * FROM courses")
            print('courses')
            print_table(cursor.fetchall())
            cursor.execute("SELECT * FROM classrooms")
            print('classrooms')
            print_table(cursor.fetchall())
            cursor.execute("SELECT * FROM students")
            print('students')
            print_table(cursor.fetchall())
if __name__=='__main__':
    main(sys.argv)
