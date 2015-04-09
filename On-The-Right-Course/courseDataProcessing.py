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


# Name of data file
file_name = 'course_enrollments_2002-2014spring_anonymized.csv'

def get_data_as_lists(file_name):
    """
    separates the data from the file into its columns, each column is a list
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

    return gradStatus, gradYear, ID, academicYear, gender, academicStatus, major, courseNum, courseSect, courseTitle, professor


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
            course_semester_taken.append((courseNum[i],1.0))
        elif academicStatus[i]=='FR':
            course_semester_taken.append((courseNum[i],1.5))
        elif academicStatus[i]=='SO' and ('FA' in academicYear[i]):
            course_semester_taken.append((courseNum[i],2.0))
        elif academicStatus[i]=='SO' and ('SP' in academicYear[i]):
            course_semester_taken.append((courseNum[i],2.5))
        elif academicStatus[i]=='JR' and ('FA' in academicYear[i]):
            course_semester_taken.append((courseNum[i],3.0))
        elif academicStatus[i]=='JR' and ('SP' in academicYear[i]):
            course_semester_taken.append((courseNum[i],3.5))
        elif academicStatus[i]=='SR' and ('FA' in academicYear[i]):
            course_semester_taken.append((courseNum[i],4.0))
        elif academicStatus[i]=='SR' and ('SP' in academicYear[i]):
            course_semester_taken.append((courseNum[i],4.5))

    return course_semester_taken


def semester_dict(course_semester_taken, sem_number):
    """ 
    returns the courses taken in a certain semester along with their
    frequency taken
    """

    sem_courses = {}
    for element in course_semester_taken:
        if element[1] == sem_number:
            course = element[0]
            count = sem_courses.get(course,0)
            sem_courses[course] = count + 1

    return sem_courses

def capped_percent(sem_courses):
    """
    sem_courses: dictionary of courses with the number of people enrolled in
    at a specified semester
    returns percentage # of ppl in the semester who have taken the 
    course as an ordered list of tuples (courseNum, percentage)
    """
    # # number of registration occurrences in a semester
    # stuNum = len(sem_courses)
    # # find length of a list of a single semester (find how many students are in a semester)
    # # (sem_courses for a specific semester_num)/(number from above)
    # # =percentage
    # pass

#################################################### NOT PERCENTAGE YET
    # split the dictionary into two lists
    # sort list of courses by most popular
    ordered_sem_courses = sorted(sem_courses, key=sem_courses.__getitem__, reverse=True)
    # make list that contains the number associated with the course
    percentage = []
    for course in ordered_sem_courses:
        percentage.append(sem_courses[course])

    capped_sem_courses = ordered_sem_courses[:10]
    capped_percentages = percentage[:10]

    return capped_sem_courses, capped_percentages


def plot():
    trace1 = Bar(
        x = capped_percent(semester_dict(course_time(academicStatus,academicYear),1.0))[1],
        y = capped_percent(semester_dict(course_time(academicStatus,academicYear),1.0))[0],
        name='Sem 1',
        orientation='h'
        )
    trace2 = Bar(
        x = capped_percent(semester_dict(course_time(academicStatus,academicYear),1.5))[1],
        y = capped_percent(semester_dict(course_time(academicStatus,academicYear),1.5))[0],
        name='Sem 1.5',
        orientation='h'
        )
    trace3 = Bar(
        x = capped_percent(semester_dict(course_time(academicStatus,academicYear),2.0))[1],
        y = capped_percent(semester_dict(course_time(academicStatus,academicYear),2.0))[0],
        name='Sem 2.0',
        orientation='h'
        )
    trace4 = Bar(
        x = capped_percent(semester_dict(course_time(academicStatus,academicYear),2.5))[1],
        y = capped_percent(semester_dict(course_time(academicStatus,academicYear),2.5))[0],
        name='Sem 2.5',
        orientation='h'
        )
    trace5 = Bar(
        x = capped_percent(semester_dict(course_time(academicStatus,academicYear),3.0))[1],
        y = capped_percent(semester_dict(course_time(academicStatus,academicYear),3.0))[0],
        name='Sem 3.0',
        orientation='h'
        )
    trace6 = Bar(
        x = capped_percent(semester_dict(course_time(academicStatus,academicYear),3.5))[1],
        y = capped_percent(semester_dict(course_time(academicStatus,academicYear),3.5))[0],
        name='Sem 3.5',
        orientation='h'
        )
    trace7 = Bar(
        x = capped_percent(semester_dict(course_time(academicStatus,academicYear),4.0))[1],
        y = capped_percent(semester_dict(course_time(academicStatus,academicYear),4.0))[0],
        name='Sem 4.0',
        orientation='h'
        )
    trace8 = Bar(
        x = capped_percent(semester_dict(course_time(academicStatus,academicYear),4.5))[1],
        y = capped_percent(semester_dict(course_time(academicStatus,academicYear),4.5))[0],
        name='Sem 4.5',
        orientation='h'
        )
    data = Data([trace1, trace2, trace3, trace4, trace5, trace6, trace7, trace8])
    layout = Layout(
        barmode='group'
        )
    fig = Figure(data=data, layout=layout)
    plot_url = py.plot(fig, filename='grouped-bar')


if __name__ == '__main__':
    
    gradStatus, gradYear, ID, academicYear, gender, academicStatus, major, courseNum, courseSect, courseTitle, professor = get_data_as_lists(file_name)

    # print semester_dict(course_time(academicStatus,academicYear),1.5)
    # print len(semester_dict(course_time(academicStatus,academicYear),1.5))
    # print len(ID)
    plot()