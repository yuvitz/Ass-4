import os
import sqlite3
import sys

def print_table(list_of_tuples):
    for item in list_of_tuples:
        print(item)

def fill_classroom(courses_list, cursor, iterationNo, room, dbcon):
    for course in courses_list:
        if room[0] == course[4]:
            print("({}) {}: {} is schedule to start".format(iterationNo, room[1],course[1]))
            cursor.execute("UPDATE classrooms SET current_course_id=? WHERE id=?", (course[0], room[0]))
            dbcon.commit()
            cursor.execute("UPDATE classrooms SET current_course_time_left=? WHERE id=?", (course[5], room[0]))
            dbcon.commit()
            cursor.execute("SELECT count FROM students WHERE grade=?", (course[2],))
            num_of_students = cursor.fetchone()[0]
            if (num_of_students - course[3]) < 0:
                cursor.execute("UPDATE students SET count=? WHERE grade=?", (0, course[2]))
                dbcon.commit()
            else:
                cursor.execute("UPDATE students SET count=? WHERE grade=?", (num_of_students - course[3], course[2]))
                dbcon.commit()
            return
    cursor.execute("UPDATE classrooms SET current_course_id=? WHERE id=?", (0, room[0]))
    dbcon.commit()
    cursor.execute("UPDATE classrooms SET current_course_time_left=? WHERE id=?", (0, room[0]))
    dbcon.commit()


def main(args):
    databaseexisted = os.path.isfile('schedule.db')
    if databaseexisted==True:
        dbcon = sqlite3.connect('schedule.db')
        iterationNo=0
        cursor=dbcon.cursor()
        cursor.execute("SELECT * FROM courses")
        courses_list=cursor.fetchall()
        cursor.execute("SELECT * FROM classrooms")
        classrooms_list = cursor.fetchall()
        cursor.execute("SELECT * FROM students")
        students_list = cursor.fetchall()
        while databaseexisted and len(courses_list)>0:
            for room in classrooms_list:
                if room[3] == 0:
                    fill_classroom(courses_list, cursor, iterationNo, room, dbcon)
                else:
                    cursor.execute("SELECT course_name FROM courses WHERE id=?",(room[2],))
                    course_name = cursor.fetchone()
                    if not course_name == None:
                        cursor.execute("SELECT current_course_time_left FROM classrooms WHERE id=?", (room[0],))
                        current_time_left = cursor.fetchone()
                        if(current_time_left[0] != 1):
                            cursor.execute("UPDATE classrooms SET current_course_time_left=? WHERE id=?", ((current_time_left[0]-1), room[0]))
                            dbcon.commit()
                            print('({}) {}: occupied by {}'.format(iterationNo, room[1], course_name[0]))
                        else:
                            print('({}) {}: {} is done'.format(iterationNo, room[1], course_name[0]))
                            cursor.execute("SELECT id FROM courses WHERE class_id=?", (room[0],))
                            room_id = cursor.fetchone()
                            cursor.execute("DELETE FROM courses WHERE id=?", (room[2],))
                            dbcon.commit()
                            cursor.execute("SELECT * FROM courses")
                            courses_list = cursor.fetchall()
                            fill_classroom(courses_list, cursor, iterationNo, room, dbcon)
            iterationNo += 1
            cursor.execute("SELECT * FROM classrooms")
            classrooms_list = cursor.fetchall()
            cursor.execute("SELECT * FROM students")
            students_list = cursor.fetchall()
            cursor.execute("SELECT * FROM courses")
            courses_list = cursor.fetchall()
            databaseexisted = os.path.isfile('schedule.db')
            # printing all tables
            print('courses')
            cursor.execute("SELECT * FROM courses")
            print_table(cursor.fetchall())
            print('classrooms')
            cursor.execute("SELECT * FROM classrooms")
            print_table(cursor.fetchall())
            print('students')
            cursor.execute("SELECT * FROM students")
            print_table(cursor.fetchall())

if __name__ == '__main__':
    main(sys.argv)