# On the Right Course
# Aditi Joshi and Jessica Sutantio
# Software Design Final Project


""" From all of the Olin registaration data, we will be creating a visualization 
displaying the most commong courses taken during a student's Olin career. 
Users will be able to filter the data so that they may visualize the informaiton 
based on major and/ or semester.
"""

import csv
import plotly.plotly as py
from plotly.graph_objs import *
import pandas as pd
import numpy as np

# Name of data file
file_name = 'course_enrollments_2002-2014spring_anonymized.csv'


def course_time(academicStatus,academicYear):
    """
    academicStatus: list denoting freshman, sophomore, junior, and senior status
    academicYear: list denoting semester based off year courses are taken
    returns: course_semester_taken, which is a list of tuples with courseNumbers 
    being paired with the semester they are taken
    """

    # Calculating semester and paring courses with semester
    course_semester_taken = []
    for i in range(len(academicStatus)):
        if (academicStatus[i]=='TF') or (academicStatus[i]=='FF'):
            course_semester_taken.append(1.0)
        elif academicStatus[i]=='FR':
            course_semester_taken.append(1.5)
        elif academicStatus[i]=='SO' and ('FA' in academicYear[i]):
            course_semester_taken.append(2.0)
        elif academicStatus[i]=='SO' and ('SP' in academicYear[i]):
            course_semester_taken.append(2.5)
        elif academicStatus[i]=='JR' and ('FA' in academicYear[i]):
            course_semester_taken.append(3.0)
        elif academicStatus[i]=='JR' and ('SP' in academicYear[i]):
            course_semester_taken.append(3.5)
        elif academicStatus[i]=='SR' and ('FA' in academicYear[i]):
            course_semester_taken.append(4.0)
        elif academicStatus[i]=='SR' and ('SP' in academicYear[i]):
            course_semester_taken.append(4.5)
        else:
            course_semester_taken.append(np.nan)

    return course_semester_taken


def get_df(file_name):
    """
    file_name: csv file that contains the course data
    separates the data from the file into its columns, each column is a list
    returns: df-data frame that holds all the organized data from file_name
    """

    # labelling of data lists
    gradStatus = []
    gradYear = []
    ID = []
    academicYear = []
    gender = []
    academicStatus = []
    major = []
    courseNum = []
    courseSect = []
    courseTitle = []
    professor = []

    # opens csv file and sorts the data into the lists
    with open(file_name, 'rb') as csvfile:
        data = csv.reader(csvfile, delimiter=',')
        for courseData in data:
            gradStatus.append(courseData[0])
            gradYear.append(courseData[1])
            ID.append(courseData[2])
            academicYear.append(courseData[3])
            gender.append(courseData[4])
            academicStatus.append(courseData[5])
            major.append(courseData[6] + courseData[7]) # includes concentration
            courseNum.append(courseData[8]) # seems to output a ton of spaces after #
            courseSect.append(courseData[9])
            courseTitle.append(courseData[10] + courseData[11]) # includes subtitle
            professor.append(courseData[11])

    semester = course_time(academicStatus,academicYear)

    df = pd.DataFrame({'gradStatus': gradStatus, 'gradYear': gradYear, 'ID': ID, 'academicYear': academicYear, 'gender': gender, 'semester': semester, 'major': major, 'courseNum': courseNum, 'courseSect': courseSect, 'courseTitle': courseTitle, 'professor': professor})

    return df


def major_filter(df, major):
    """
    this method takes in each student's ID and their major. If their major is 
    undefined at any point, the function will take in the first major it finds
    for that ID 

    ['Undeclared              ' 
     'Mechanical Engineering  '
     'Engineering             '
     'Undeclared              Systems                 '
     'Engineering             Systems                 '
     'Undeclared              Computing               '
     'Engineering             Computing               '
     'Undeclared              Materials Science       '
     'Mechanical Engineering  Materials Science       '
     'Engineering             Materials Science       '
     'Mechanical Engineering  Computing               '
     'Undeclared              Bioengineering          '
     'Engineering             Bioengineering          '
     "Electr'l & Computer Engr"
     'Undeclared              Self Designed           '
     'Engineering             Self Designed           '
     'Mechanical Engineering  Bioengineering          '
     "Electr'l & Computer EngrComputing               "
     "Electr'l & Computer EngrSystems                 "
     'Mechanical Engineering  Systems                 '
     'Mechanical Engineering  Self Designed           '
     "Electr'l & Computer EngrSelf Designed           "
     'Undeclared              Design                  '
     'Mechanical Engineering  Design                  '
     'Engineering             Design                  '
     'Undeclared              Robotics                '
     'Mechanical Engineering  Robotics                '
     'Engineering             Robotics                '
     'Exchange Student        Computing               '
     "Electr'l & Computer EngrRobotics                "]

    """

    # all majors that they can list from: ME, ECE, E:C, E:Robo, E:Bio, E:MatSci, E:Design, E:Systems
    major_convert = {'ME': 'Mechanical Engineering  ', 'ECE': "Electr'l & Computer Engr", 'E:C': 'Engineering             Computing               ', 'E:Robo': 'Engineering             Robotics                ', 'E:Bio': 'Engineering             Bioengineering          ', 'E:MatSci': 'Engineering             Materials Science       ', 'E:Design': 'Engineering             Design                  ', 'E:Systems': 'Engineering             Systems                 '}
    major = major_convert[major]

    # finds all the unique ids and all ids
    uniqueIDs = df.ID.unique()
    uniquemajors = df.major.unique()

    # find the start and end indices of the unique IDs 
    for idNum in uniqueIDs:
        IDindex = df[df['ID']==idNum].index.tolist()
        # print IDindex
        startID = IDindex[0]
        endID = IDindex[-1]
        # find the last updated major of the student
        latestMajor = df['major'][endID]
        # change all previous majors to be the same as last updated major
        df.loc[startID:endID+1, 'major'] = latestMajor

    # create a new dataframe that shows all data for only the specified major
    major_df = df[df.major == major]

    return major_df


def capped_percent(df, sem):
    """
    df: data frame that contains all the course registration data as an array
    returns percentage # of ppl in the semester who have taken the 
    course as an ordered list of tuples (courseNum, percentage)
    """

    # create a new dataframe that shows all data for only the specified semester
    sem_df = df[df.semester==sem]

    # counts the number of students registered in specified semester
    numStudents = sem_df.ID.nunique()

    # count the number of people (all gradYears) registered for a course
    courseFreq = sem_df.groupby('courseNum').ID.nunique()
    
    # calcs the % by dividing the number of registered students per course by total number of students
    percentages = (courseFreq/numStudents)*100
    
    # sort the Series by highest to lowest percentage
    percentages.sort(ascending=False)

    # limit the list of courses to the top 10
    capped_percentages = percentages.head(10)

    # list of courses
    courses = capped_percentages.index.values
    
    # list of percentages
    list_percent = capped_percentages.tolist()

    # combine them back into a dataframe
    capped_percents = pd.DataFrame({'courseNum': courses, 'Percent': list_percent})

    return capped_percents


def df_to_list(df):
    """
    takes a dataframe and splits all the columns into separate lists
    """

    df_list = []
    header_list = list(df)
    for header in header_list:
        df_list.append(df[header].tolist())

    return df_list


def find_all_sem(df, major):
    """
    finds all of the semester capped percentages for a specific major 
    and returns them as lists
    """

    df = major_filter(df, major)

    sem1 = df_to_list(capped_percent(df, 1.0))
    sem2 = df_to_list(capped_percent(df, 1.5))
    sem3 = df_to_list(capped_percent(df, 2.0))
    sem4 = df_to_list(capped_percent(df, 2.5))
    sem5 = df_to_list(capped_percent(df, 3.0))
    sem6 = df_to_list(capped_percent(df, 3.5))
    sem7 = df_to_list(capped_percent(df, 4.0))
    sem8 = df_to_list(capped_percent(df, 4.5))

    return sem1, sem2, sem3, sem4, sem5, sem6, sem7, sem8


def add_percent_symbol(list_percent):
    """
    takes a list of the percentages and returns a list of the rounded #s with
    the percent symbol
    """

    list_percentages = []
    for element in list_percent:
        list_percentages.append(str(int(element))+'%')

    return list_percentages


def plot(sem1, sem2, sem3, sem4, sem5, sem6, sem7, sem8):

    trace1 = Bar(
        x = sem1[0],
        y = sem1[1],
        name='Sem 1',
        orientation='h'
        )

    trace2 = Bar(
        x = sem2[0],
        y = sem2[1],
        name='Sem 1.5',
        orientation='h'
        )

    trace3 = Bar(
        x = sem3[0],
        y = sem3[1],
        name='Sem 2.0',
        orientation='h'
        )

    trace4 = Bar(
        x = sem4[0],
        y = sem4[1],
        name='Sem 2.5',
        orientation='h'
        )

    trace5 = Bar(
        x = sem5[0],
        y = sem5[1],
        name='Sem 3.0',
        orientation='h'
        )

    trace6 = Bar(
        x = sem6[0],
        y = sem6[1],
        name='Sem 3.5',
        orientation='h'
        )

    trace7 = Bar(
        x = sem7[0],
        y = sem7[1],
        name='Sem 4.0',
        orientation='h'
        )

    trace8 = Bar(
        x = sem8[0],
        y = sem8[1],
        name='Sem 4.5',
        orientation='h'
        )

    data = Data([trace1, trace2, trace3, trace4, trace5, trace6, trace7, trace8])

    layout = Layout(
        barmode='group'
        )

    fig = Figure(data=data, layout=layout)

    plot_url = py.plot(fig, filename='grouped-bar')

################################################### TYPES OF INPUTS
"""
0. Display all 8 semesters by default
    Dropdown list will filter by major and semester
    1. If filter by major
    > display all 8 semesters for the major
        1a. If filter by semester
        > display to 10 courses (zoom in) for the major
    2. If filter by semester
    > display top 10 courses (zoom in)
        2a. If filter by major
        > change top 10 courses to be major specific

Always output top 10 course list by percentage

"""

if __name__ == '__main__':
    df = get_df(file_name)

    sem1, sem2, sem3, sem4, sem5, sem6, sem7, sem8 = find_all_sem(df, 'ME')

    plot(sem1, sem2, sem3, sem4, sem5, sem6, sem7, sem8)
