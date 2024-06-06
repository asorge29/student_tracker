# Student Tracker

## Description

Simple CLI app made with python to access and manage a sql database containing multiple students as well as their classes and grades.

## Usage

*This assumes that you already have a local instance of MySQL server running.*

Clone the repo and install the needed python packages from `requirements.txt`. Next, change the credentials in the first few lines of `main.py` to match the credentials to your MySQL server. Open MySQL Workbench and run the sql script `student_tracker.sql`. Finally, run `main.py` and use the arrow keys to navigate the menus.

## Functions

- Create multiple student accounts
- Keep track of classes and grades
- Calculate your GPA
- Export a transcript

## Purpose

Built this to learn the basics of MySQL and its integration with python for a software development certification.