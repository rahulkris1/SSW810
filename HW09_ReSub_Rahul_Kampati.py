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
		return [self.cwid, self.name, sorted(self.course_grade_dict.keys())]

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

class Repository:
	def __init__(self, directory):
		""" repository class to hold the students, instructors and grades data"""
		self.directory = directory
		self.student_dict = {}
		self.instructor_dict = {}
		self.student_analyser()
		self.instructor_analyser()
		self.grades_analyser()
		self.students_summary()
		self.instructors_summary()

	def student_analyser(self):
		""" Analyse Students.txt data file"""
		if not os.path.exists(self.directory):
			raise FileNotFoundError("Directory not found")

		file_students = os.path.join(self.directory, 'students.txt')

		for cwid, name, major in self.file_reading_gen(file_students, 3, "\t", False):
			self.student_dict[cwid] = Student(cwid, name, major)
		

	def instructor_analyser(self):
		""" Analyse Instructors.txt data file"""
		if not os.path.exists(self.directory):
			raise FileNotFoundError("Directory not found")

		file_instructors = os.path.join(self.directory, 'instructors.txt')

		for cwid, name, dept in self.file_reading_gen(file_instructors, 3, "\t", False):
			self.instructor_dict[cwid] = Instructor(cwid, name, dept)

	def grades_analyser(self):
		""" Analyse grades.txt data file"""
		if not os.path.exists(self.directory):
			raise FileNotFoundError("Directory not found")

		file_grades = os.path.join(self.directory, 'grades.txt')

		for studentCwid, course, grade, instructorCwid in self.file_reading_gen(file_grades, 4, "\t", False):
			if studentCwid in self.student_dict.keys():
				self.student_dict[studentCwid].course_grade_student(course, grade)
			else:
				print(f"Invalid student cwid {studentCwid}")

			if instructorCwid in self.instructor_dict.keys():
				self.instructor_dict[instructorCwid].num_course_students(course)

			else:
				print(f"Invalid Instructor id {instructorCwid}")


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
						raise ValueError(f"File path has {len(header_info.split(sep))} invalid number of fields instead of {fields}")

				for line in fp:
					if len(line.split(sep)) != fields:
						raise ValueError(f" file has {len(next(fp.split(sep)))} fields instead of {fields} ")

					else:
						line = line.strip().split(sep)
						yield tuple(line)


	def students_summary(self):
		""" Summarising the students data"""
		tb_student = PrettyTable(field_names = ["CWID", "Name", "Completed Courses"])
		for inst_student in self.student_dict.values():
			tb_student.add_row(inst_student.prettyTable_student())
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


def main():
    try:
        Repository("C:/Users/HP/Desktop/redo/file_09")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main() 





