#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 26 ‎November ‎2019, ‏‎08:00
@author: Kampati Rahul

Creation of a data repository for students and instructors to keep track of data
"""

import os
from collections import defaultdict
from prettytable import PrettyTable
import sqlite3

class Student:
	def __init__(self, cwid, name, major):
		""" Students class to hold students data"""
		self.cwid = cwid
		self.name = name
		self.major = major
		self.course_grade_dict = defaultdict(str)

	def course_grade_student(self, course, grade):
		""" Assign grade of each course"""
		self.course_grade_dict[course] = grade

	def prettyTable_student(self):
		""" Structuring data for pretty table for students"""
		return [self.cwid, self.name, self.major, self.course_grade_dict]


class Instructor:
	def __init__(self, cwid, name, dept):
		""" instructors class to hold students data"""
		self.cwid = cwid
		self.name = name
		self.dept = dept
		self.course_inst_dict = defaultdict(int)

	def num_course_students(self, course):
		""" Assign number of students under each professor"""
		self.course_inst_dict[course] += 1

	def prettyTable_instructor(self):
		""" Structuring data for pretty table for students"""
		for course in self.course_inst_dict:
			yield [self.cwid, self.name, self.dept, course, self.course_inst_dict[course]]


class Majors():
	def __init__(self, dept):
		""" Majors class to analyse the data"""
		self.dept = dept
		self.courses_reqd = []
		self.courses_elec = []

	def reqd_courses(self, course):
		self.courses_reqd = sorted(course)

	def elec_courses(self, course):
		self.courses_elec = sorted(course)


class Repository:
	def __init__(self, directory):
		""" repository class to hold the students, instructors and grades data"""
		self.directory = directory
		self.student_dict = {}
		self.instructor_dict = {}
		self.majors_dict = {}
		self.majors_analyser()
		self.student_analyser()
		self.instructor_analyser()
		self.grades_analyser()
		self.students_summary()
		self.instructors_summary()
		self.majors_summary()
		self.table_instructor_db("C:/Users/HP/Desktop/Inclas/GIT/SSW810/810_startup.db")


	def student_analyser(self):
		""" Analyse Students.txt data file"""
		if not os.path.exists(self.directory):
			raise FileNotFoundError("Directory not found")

		file_students = os.path.join(self.directory, 'students.txt')

		for cwid, name, major in self.file_reading_gen(file_students, 3, ";", True):
			self.student_dict[cwid] = Student(cwid, name, major)
		

	def instructor_analyser(self):
		""" Analyse Instructors.txt data file"""
		if not os.path.exists(self.directory):
			raise FileNotFoundError("Directory not found")

		file_instructors = os.path.join(self.directory, 'instructors.txt')

		for cwid, name, dept in self.file_reading_gen(file_instructors, 3, "|", True):
			self.instructor_dict[cwid] = Instructor(cwid, name, dept)


	def grades_analyser(self):
		""" Analyse grades.txt data file"""
		if not os.path.exists(self.directory):
			raise FileNotFoundError("Directory not found")

		file_grades = os.path.join(self.directory, 'grades.txt')

		for studentCwid, course, grade, instructorCwid in self.file_reading_gen(file_grades, 4, "|", True):
			if studentCwid in self.student_dict.keys():
				self.student_dict[studentCwid].course_grade_student(course, grade)
			else:
				print(f"Invalid student cwid {studentCwid}")

			if instructorCwid in self.instructor_dict.keys():
				self.instructor_dict[instructorCwid].num_course_students(course)

			else:
				print(f"Invalid Instructor id {instructorCwid}")


	def majors_analyser(self):
		""" Analyse majors.txt data file"""
		if not os.path.exists(self.directory):
			raise FileNotFoundError("Directory not found")

		file_majors = os.path.join(self.directory, 'majors.txt')
		d2_m = defaultdict(lambda: defaultdict(list))

		for major, flag, course in self.file_reading_gen(file_majors, 3, "\t", True):
			d2_m[major][flag].append(course)

		for major, courses in d2_m.items():
			mjr = Majors(major)
			for flag, course in courses.items():
				if flag == 'R':
					mjr.reqd_courses(course)
				if flag == 'E':
					mjr.elec_courses(course)
			self.majors_dict[major] = mjr


	def file_reading_gen(self, path, fields, sep, header=False):
		"""Generator function that reads a flie and returns one line at a time."""

		try:
			fp = open(path, 'r')

		except FileNotFoundError:
			raise FileNotFoundError("Unable to open the file path provided")

		else:
			with fp:
				if header:
					header_info = next(fp)
					if len(header_info.split(sep)) != fields:
						raise ValueError(f"File path has {len(header_info.split(sep))} {fp} invalid number of fields instead of {fields}")

				for line in fp:
					if len(line.split(sep)) != fields:
						raise ValueError(f" file has {len(next(fp.split(sep)))} fields instead of {fields} ")

					else:
						line = line.strip().split(sep)
						yield tuple(line)

	
	def students_summary(self):
		""" Summarising the students data"""
		pass_grades = ['A','A-','B+','B','B-','C+','C']
		tb_student = PrettyTable(field_names = ["CWID", "Name", "Major", "Completed Courses", "Remaining Required", "Electives"])
		completed_courses = []
		for student_inst in self.student_dict.values():
			student_lst = student_inst.prettyTable_student()
			completed_courses = []		
			completed_courses=[course for course, grade in student_lst[3].items() if grade in pass_grades]
			reqd_courses = set(self.majors_dict[student_lst[2]].courses_reqd) - set(completed_courses)
			remain_elec = [value for value in completed_courses if value in self.majors_dict[student_lst[2]].courses_elec]

			if len(remain_elec) != 0 :
				remain_elec = None
			else:
				remain_elec = [value for value in self.majors_dict[student_lst[2]].courses_elec]
			student_lst.pop(3)
			student_lst.append(sorted(completed_courses))
			student_lst.append(reqd_courses)
			student_lst.append(remain_elec)
			tb_student.add_row(student_lst)
		
		print("Student Summary")
		print(tb_student)

	def instructors_summary(self):
		""" Summarising the Instructors data"""
		tb_instructor = PrettyTable(field_names = ["CWID", "Name", "Dept", "Course", "Students"])
		for inst_instructor in self.instructor_dict.values():
			for instructor_data in inst_instructor.prettyTable_instructor():
				tb_instructor.add_row(instructor_data)
		print("Instructor Summary")
		print(tb_instructor)

	def majors_summary(self):
		""" Summarising the Instructors data"""
		tb_majors = PrettyTable(field_names = ["Dept", "Required", "Electives"])
		for dept, inst_mjr in self.majors_dict.items():
			tb_majors.add_row([dept, inst_mjr.courses_reqd, inst_mjr.courses_elec])

		print(tb_majors)

	def table_instructor_db(self, fp):
		"""Instructor Summary From DataBase"""
		try:
			db_fp = sqlite3.connect(fp)
		except Exception as e:
			print(e)
		else:
			query = """select CWID, Name , Dept, Course, count(*) as students from instructors join grades on CWID = InstructorCWID GROUP BY InstructorCWID, Course order by CWID desc;"""


			db_pt = PrettyTable(field_names = ['CWID', 'Name', 'Dept', 'Course', 'Students'])
			    
			try:
			    
			    print(f"\nInstructor Summary From DataBase")
			    for row in db_fp.execute(query):
			        db_pt.add_row(list(row))
			        
			    print(db_pt)
			except Exception as e:
			    print(e)
			
			


def main():
    try:
        Repository("C:/Users/HP/Desktop/redo_10/file_09")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main() 
