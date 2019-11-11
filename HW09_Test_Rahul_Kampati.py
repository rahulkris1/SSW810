#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 03 ‎November ‎2019, ‏‎09:30:00

@author: Kampati Rahul

Testing the Creation of data repository of courses, students, faculty members.
"""

import unittest
from HW09_Rahul_Kampati import Container

file_path = 'C:/Users/HP/Desktop/Inclas/GIT/SSW810/test/' 


class TestContainer(unittest.TestCase):
    """ Testing the File Generators """

    def test_student_info_dict(self):
        """ Test the info of the student"""
        test_path = Container(file_path)
        self.assertEqual(list(test_path.student_info.keys()), ["10103"])


    def test_instructor_info_dict(self):
        """ Test the info of the instructor """
        test_path = Container(file_path)
        self.assertEqual(list(test_path.insructors_info.keys()), ["98765"])

    def test_major_info_dict(self):
        """ Test the info of the instructor """
        test_path = Container(file_path)
        self.assertEqual(list(test_path.majors_info.keys()), ["SFEN"])



    

if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)
