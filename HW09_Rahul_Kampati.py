#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 03 ‎November ‎2019, ‏‎09:30:00

@author: Kampati Rahul

Creation of data repository of courses, students, faculty members.
"""

import os
from collections import defaultdict
from prettytable import PrettyTable

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
        return [self.cwid, self.name, sorted(self.courses_grade_information.keys())]

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

class Container:
    def __init__(self, directory):

        self.directory = directory
        self.student_info = {}
        self.insructors_info = {}
        self.analyze_files()
        self.students_summary()
        self.instructor_summary()

    def analyze_files(self):

        if not os.path.exists(self.directory):
            raise FileNotFoundError(f"No such directory {self.directory}")

        students_file = 'students.txt'
        instructors_file = 'instructors.txt'
        grades_file = 'grades.txt'

        if students_file in os.listdir(self.directory):
            for cwid, name, major in self.file_reading_gen(os.path.join(self.directory, students_file), 3, "\t", False): 
                self.student_info[cwid] = Student(cwid, name, major)
        else:
            raise FileNotFoundError(
                f"Unable to open {students_file} for reading")
        
        if instructors_file in os.listdir(self.directory):
            for cwid, name, dept in self.file_reading_gen(os.path.join(self.directory, instructors_file), 3, "\t", False): 
                self.insructors_info[cwid] = Instructor(cwid, name, dept)
        else:
            raise FileNotFoundError(
                f"Unable to open {instructors_file} for reading")

        if grades_file in os.listdir(self.directory):
            for studentCwid, course, grade, instructorCwid in  self.file_reading_gen(os.path.join(self.directory, grades_file), 4, "\t", False):
                if studentCwid in self.student_info.keys():
                    self.student_info[studentCwid].add_course_grade(course, grade)
                if instructorCwid in self.insructors_info.keys():
                    self.insructors_info[instructorCwid].add_course_noofstudents(course) 
        else:
            raise FileNotFoundError(f"Unable to open {grades_file} for reading")

    def file_reading_gen(self, path, fields, sep=',', header=False):

        try:
            file_path = open(path, "r")

        except FileNotFoundError:
            raise FileNotFoundError(f"Unable to open {path} for reading")

        else:
            with file_path:
                ln_num = 0
                if header and len(next(file_path).split(sep)) != fields:
                    file_path.seek(0)
                    raise ValueError(
                        f"'{path}' has {len(file_path.readline().split(sep))} fields on line 0 but expected fields are {fields}")

                if header:
                    ln_num = ln_num + 1

                for line in file_path:
                    line = line.strip().split(sep)
                    ln_num += 1
                    if len(line) != fields:
                        raise ValueError(
                            f"'{path}' has {len(line)} fields on line {ln_num} but expected fields are {fields}")
                    yield tuple(line)

    def students_summary(self):
        """ summary of student """
        pt = PrettyTable(field_names = ['CWID', 'Name', 'Completed Courses'])
        print(f"Student Summary")
        for student_instance in self.student_info.values():
            pt.add_row(student_instance.pretty_table_student())

        print(pt)

    def instructor_summary(self):
        pt = PrettyTable(field_names = ['CWID', 'Name', 'Dept', 'Course', 'Students'])
        print(f"Instructor Summary")
        for instructor_instance in self.insructors_info.values():
            info_inst, courses = instructor_instance.pretty_table_instructor()
            for course, noof_students in courses.items():
                info_inst.extend([course, noof_students])
                pt.add_row(info_inst)
                info_inst = info_inst[0:3]
            
        print(pt)

def main():
    try:
        Container('C:/Users/HP/Desktop/Inclas/HW09/')
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main() 
