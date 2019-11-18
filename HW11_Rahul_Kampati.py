#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 10 ‎November ‎2019, ‏‎09:30:00

@author: Kampati Rahul

Updation of data repository of courses, students, faculty members.
"""

import os
from collections import defaultdict
from prettytable import PrettyTable
import sqlite3

class Student():
    """
    Student class having details of a particular student & methods like add course detials & grade for that student
    """
    def __init__(self, cwid, name, major):
        """ Student details repository class """
        self.cwid = cwid
        self.name = name
        self.major = major
        self.courses_grade_information = defaultdict(str)
    
    def add_course_grade(self,course, grade):
        """add student grades to repository"""
        self.courses_grade_information[course] = grade

    def pretty_table_student(self):
        """ Pretty Table to print details of student"""
        return [self.cwid, self.name, self.major,self.courses_grade_information]

class Instructor():
    def __init__(self, cwid, name, dept):
        """ Instructor details repository class """
        self.cwid = cwid
        self.name = name
        self.dept = dept
        self.courses = defaultdict(int)
    
    def add_course_noofstudents(self, course):
        """add courses taught by instructor to repository"""
        self.courses[course] = self.courses[course] + 1

    def pretty_table_instructor(self):
        """ Pretty Table to print details of Instructor"""
        return [self.cwid, self.name, self.dept], self.courses
class Majors():
    """Major class with details of the majors and their required and elective courses."""

    def __init__(self, mjr):
        self.mjr = mjr
        self.req = set()
        self.elec = set()

    def add_required(self, course):
        self.req = self.req.union(set(course))

    def add_elective(self, course):
        self.elec = self.elec.union(set(course))

class Container:
    def __init__(self, directory):

        self.directory = directory
        self.student_info = {}
        self.insructors_info = {}
        self.majors_info = {}
        self.analyze_files()
        self.students_summary()
        self.instructor_summary()
        self.major_summary()
        self.db_table_instructor("C:/Users/HP/Desktop/Inclas/GIT/SSW810/810_startup.db")

    def analyze_files(self):
        """ analyse txt files"""
        if not os.path.exists(self.directory):
            raise FileNotFoundError(f"No such directory {self.directory}")

        students_file = 'students.txt'
        instructors_file = 'instructors.txt'
        grades_file = 'grades.txt'
        Majors_file = 'majors.txt'

        if students_file in os.listdir(self.directory):
            for cwid, name, major in self.file_reading_gen(os.path.join(self.directory, students_file), 3, "\t", True): 
                self.student_info[cwid] = Student(cwid, name, major)
        else:
            raise FileNotFoundError(
                f"Unable to open {students_file} for reading")
        
        if instructors_file in os.listdir(self.directory):
            for cwid, name, dept in self.file_reading_gen(os.path.join(self.directory, instructors_file), 3, "\t", True): 
                self.insructors_info[cwid] = Instructor(cwid, name, dept)
        else:
            raise FileNotFoundError(
                f"Unable to open {instructors_file} for reading")

        if grades_file in os.listdir(self.directory):
            for studentCwid, course, grade, instructorCwid in  self.file_reading_gen(os.path.join(self.directory, grades_file), 4, "\t", True):
                if studentCwid in self.student_info.keys():
                    self.student_info[studentCwid].add_course_grade(course, grade)
                if instructorCwid in self.insructors_info.keys():
                    self.insructors_info[instructorCwid].add_course_noofstudents(course) 
        else:
            raise FileNotFoundError(f"Unable to open {grades_file} for reading")
        
        if Majors_file in os.listdir(self.directory):
            dict = defaultdict(lambda: defaultdict(set))
            for dept, flag, course in self.file_reading_gen(os.path.join(self.directory, Majors_file), 3, "\t", True):
                dict[dept][flag].add(course)

            for dept, courses in dict.items():
                
                mjr_new = Majors(dept)
                
                for flag, course in courses.items():
                    if flag == 'R':
                        mjr_new.add_required(course)
                    if flag == 'E':
                        mjr_new.add_elective(course)
                self.majors_info[dept] = mjr_new
        else:
            raise FileNotFoundError(
                f"Unable to open {Majors_file} for reading")

    def file_reading_gen(self, path, fields, sep=',', header=False):
        """ generator for reading files"""
        try:
            fp = open(path, "r")

        except FileNotFoundError:
            raise FileNotFoundError(f"Unable to open {path} for reading")

        else:
            with fp:
                ln_num = 0
                if header and len(next(fp).split(sep)) != fields:
                    fp.seek(0)
                    raise ValueError(
                        f"'{path}' has {len(fp.readline().split(sep))} fields on line 0 but expected fields are {fields}")

                if header:
                    ln_num = ln_num + 1

                for line in fp:
                    line = line.strip().split(sep)
                    ln_num += 1
                    if len(line) != fields:
                        raise ValueError(
                            f"'{path}' has {len(line)} fields on line {ln_num} but expected fields are {fields}")
                    yield tuple(line)

    def students_summary(self):
        """ summary of student using pretty table"""
        PassGrades = ['A','A-','B+','B','B-','C+','C']
        pt = PrettyTable(field_names = ['CWID', 'Name', 'Major','Completed Courses','Remaining Required','Remaining Electives'])
        print(f"Students")
        for student in self.student_info.values():
            tst = student.pretty_table_student()
            courses_cmpltd = set([Course for Course, grade in tst[3].items() if grade in PassGrades])
            tst[3] = sorted(courses_cmpltd)
            remaining_rqd = self.majors_info[tst[2]].req.difference(tst[3])
            if len(self.majors_info[tst[2]].elec.intersection(tst[3]))>0:
                remaining_elecs = None
            else:
                remaining_elecs = self.majors_info[tst[2]].elec - courses_cmpltd
            tst.append(remaining_rqd)
            tst.append(remaining_elecs)
            pt.add_row(tst)
        print(pt)

    def instructor_summary(self):
        """ summary of instructors using pretty table"""
        pt = PrettyTable(field_names = ['CWID', 'Name', 'Dept', 'Course', 'Students'])
        print(f"Instructor Summary")
        for instructor_instance in self.insructors_info.values():
            info_inst, courses = instructor_instance.pretty_table_instructor()
            for course, noof_students in courses.items():
                info_inst.extend([course, noof_students])
                pt.add_row(info_inst)
                info_inst = info_inst[0:3]
            
        print(pt)

    def major_summary(self):
        """summary of majors using pretty table"""
        pt = PrettyTable(field_names = ['Dept', 'Required', 'Elective'])
        for dept, major in self.majors_info.items():
            pt.add_row([dept, major.req, major.elec])
        print(pt)

    def db_table_instructor(self, path_DB):
        try:
            db_file = sqlite3.connect(path_DB)
        except Exception as e:
            print(e)
        else:
            query = """ select I.CWID, I.Name , I.Dept, G.Course, count(*) as Students from instructors I join
                grades G  on I.CWID = G.InstructorCWID GROUP BY G.InstructorCWID,G.Course order by  CWID desc;"""


            Tb_pt = PrettyTable(field_names = ['CWID', 'Name', 'Dept', 'Course', 'Students'])
                
            try:
                lst_db =[]
                print(f"\nInstructor Summary From DataBase")
                for row in db_file.execute(query):
                    Tb_pt.add_row(list(row))
                    lst_db.append(list(row))
                print(Tb_pt)
            except Exception as e:
                print(e)
            else:
                pass
            return lst_db

def main():
    try:
        Container('C:/Users/HP/Desktop/Inclas/GIT/SSW810')
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main() 
