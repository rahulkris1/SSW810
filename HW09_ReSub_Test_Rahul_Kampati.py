#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 26 ‎November ‎2019, ‏‎09:30:00

@author: Kampati Rahul

Testing the Creation of data repository of courses, students, faculty members.
"""

import unittest
from HW09_ReSub_Rahul_Kampati import Repository


fp = "files/test" 


class TestRepository(unittest.TestCase):
    """ Testing the File Generators """

    def test_student_dict(self):
        """ Test the info of the student"""
        test = Repository(fp)
        self.assertEqual(list(test.student_dict.keys()), ["10103"])

    def test_instructor_info_dict(self):
        """ Test the info of the instructor """
        test = Repository(fp)
        self.assertEqual(list(test.instructor_dict.keys()), ["98765"])
    

if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)
