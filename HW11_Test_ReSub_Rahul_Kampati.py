##!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 27 ‎November ‎2019, ‏‎09:30:00

@author: Kampati Rahul

Testing the Creation of data repository of courses, students, faculty members and majors.
"""

import unittest
from HW11_ReSub_Rahul_Kampati import Repository


fp = "C:/Users/HP/Desktop/redo_10/file_09/test"


class TestRepository(unittest.TestCase):
    """ Testing the File Generators """

    


    def test_instructor_info_dict(self):
        """ Test the info of the instructor """
        test = Repository(fp)
        self.assertEqual(list(test.instructor_dict.keys()), ["98765"])

    def test_major_info_dict(self):
        """ Test the info of the majors """
        test = Repository(fp)
        print(test.majors_dict.keys())
        self.assertEqual(list(test.majors_dict.keys()), ["SFEN"])

    def test_student_dict(self):
        """ Test the info of the student"""
        test = Repository(fp)
        self.assertEqual(list(test.student_dict.keys()), ["10103"])


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)