# -*- coding: utf-8 -*-
"""

Notes:
    This is a python wrapper for a database of entries for the telescopes in the Napier Building.
    The main function you'll use is the lookup function for a star, observe(name)


Database table has columns

STAR_NUMBER (int)
RA (string)
DEC (string)
SIZE (int) (Some don't have this)
MAG (real)
TYPE_AND_DESCRIPTION (string)
ALT_NAME (string)
Q_TAGS (string)
COMMON_NAME (string)
COMMENTS (string)

"""

# Get sqlite to manage the database
import sqlite3
import numpy as np

# Declare a global database variable
SC_GLOBAL_DATABASE = ""

"""
SQL Interface functions
"""

#Executes a given SQL command and returns the result 
def exec_no_feedback(cmd):
    #print(cmd)
    global SC_GLOBAL_DATABASE

    if SC_GLOBAL_DATABASE == "":
        print("Global database not initialised! Calling sc_open() automatically!")
        sc_open()

    c = SC_GLOBAL_DATABASE.cursor()
    try:
        c.execute(cmd)
        result = c.fetchall()
        return result
    except:
        print("Error executing SQL command!")
        return

# Executes a given SQL command, returns the result and prints it to stdout
def exec_with_feedback(cmd):
    result = exec_no_feedback(cmd)
    for r in result:
        print(r)
    return result

def sc_open():
    global SC_GLOBAL_DATABASE
    SC_GLOBAL_DATABASE = sqlite3.connect("StarCatalog.db")

def sc_close():
    global SC_GLOBAL_DATABASE
    SC_GLOBAL_DATABASE.close()
    SC_GLOBAL_DATABASE = ""

"""
Making and deleting tables
"""

# Creates a tab;e "starchart" with all the right columns
def make_table():
    global SC_GLOBAL_DATABASE
    sql_cmd = "CREATE TABLE starchart ( STAR_NUMBER INTEGER PRIMARY KEY, RA STRING, DEC STRING, SIZE INTEGER, MAG DECIMAL(2), TYPE_AND_DESCRIPTION STRING, ALT_NAME STRING, Q_TAGS STRING, COMMON_NAME STRING, COMMENTS STRING)"
    cursor = SC_GLOBAL_DATABASE.cursor()
    cursor.execute(sql_cmd)
    SC_GLOBAL_DATABASE.commit()

# Deletes the table if something went wrong :(
def kill_table():
    global SC_GLOBAL_DATABASE
    SC_GLOBAL_DATABASE.cursor().execute("DROP TABLE starchart")
    SC_GLOBAL_DATABASE.commit()

# Given a CSV of all of the data, input it into the database. Must be a fresh table
def gen_from_csv(file):
    data = np.genfromtxt(fname=file, delimiter=",", dtype=str)
    #print(data)
    for x in data:
        if x[3] == "":
            x[3] = 0
        add_star(num=int(x[0]), ra=x[1], dec=x[2], size=x[3], mag=float(x[4]), type_and_desc=x[5], alt_name=x[6], q_tags=x[7], common_name=x[8], comments="")


"""
Adding/updating/removing objects from the database
"""
# Adds a star given the full input data, some are defaulted to 0 or null
def add_star(num, ra, dec, size, mag, type_and_desc, alt_name, q_tags, common_name, comments):
    global SC_GLOBAL_DATABASE
    sql_cmd = "INSERT INTO starchart VALUES ({}, \'{}\', \'{}\', {}, {}, \'{}\', \'{}\', \'{}\', \'{}\', \'{}\');"
    sql_cmd = sql_cmd.format(num, ra, dec, size, mag, type_and_desc, alt_name, q_tags, common_name, comments)
    exec_no_feedback(sql_cmd)
    SC_GLOBAL_DATABASE.commit()

# Quickly adds a star from the important information
def add_star_quick(num, ra, dec, mag, alt_name, common_name):
    add_star(num, ra, dec, 0, mag, "", alt_name, "", common_name, "")

# Updates a star given all of the information
def update_all(num, ra, dec, size, mag, type_and_desc, alt_name, q_tags, common_name, comments):
    global SC_GLOBAL_DATABASE
    sql_cmd = "UPDATE starchart SET RA=\'{}\', DEC=\'{}\', SIZE={}, MAG={}, TYPE_AND_DESC=\'{}\', ALT_NAME=\'{}\', Q_TAGS=\'{}\', COMMON_NAME=\'{}\', COMMENTS=\'{}\' WHERE STAR_NUMBER={}"
    sql_cmd = sql_cmd.format(ra, dec, size, mag, type_and_desc, alt_name, q_tags, common_name, comments, num)
    exec_with_feedback(sql_cmd)
    SC_GLOBAL_DATABASE.commit()

def update_column(num, value, column):
    global SC_GLOBAL_DATABASE
    sql_cmd = "UPDATE starchart SET " + column + "WHERE STAR_NUMBER IS {}"
    sql_cmd = sql_cmd.format(value, num)
    #print(sql_cmd)
    exec_with_feedback(sql_cmd)
    SC_GLOBAL_DATABASE.commit()

# With this block of functions, it updates a single column by passing in the ocrrect column name 
# and string/int substitution. SQL breaks if strings don't have their own quotes,
# which is why this approach was taken since users don't know what needs string quotes and what doesn't
def update_ra(num, value):
    update_column(num, value, "RA=\'{}\'")

def update_dec(num, value):
    update_column(num, value, "DEC=\'{}\'")

def update_size(num, value):
    update_column(num, value, "SIZE={}")

def update_mag(num, value):
    update_column(num, value, "MAG={}")
    
def update_type_and_desc(num, value):
    update_column(num, value, "TYPE_AND_DESC=\'{}\'")

def update_alt_name(num, value):
    update_column(num, value, "ALT_NAME=\'{}\'")
    
def update_q_tags(num, value):
    update_column(num, value, "Q_TAGS=\'{}\'")

def update_common_name(num, value):
    update_column(num, value, "COMMON_NAME=\'{}\'")

def update_comments(num, value):
    update_column(num, value, "COMMENTS=\'{}\'")
    

"""
Retrieving data
"""
# Retrieves al the stars data in a data matrix
def get_all():
    sql_cmd = "SELECT * FROM starchart"
    exec_with_feedback(sql_cmd)

# Retrieves data matrix about all stars matching the name given as a matrix
def get_star_from_name(name):
    sql_cmd = "SELECT * FROM starchart WHERE COMMON_NAME LIKE \'%{}%\' OR ALT_NAME LIKE \'%{}%\'".format(name, name)
    #sql_cmd = "SELECT * FROM starchart WHERE COMMON_NAME LIKE \'%{}%\'".format(name)
    return exec_no_feedback(sql_cmd)

# Retrieves star data in a matrix
def get_star_from_number(num):
    sql_cmd = "SELECT * FROM starchart WHERE STAR_NUMBER IS {}".format(num)
    return exec_no_feedback(sql_cmd)

"""
Human Commands
"""

# Gets human readable data about a star matching the name given
def observe(name):
    res = get_star_from_name(name)
    c = 0
    if res == None or len(res) < 1:
        print("No matches were found for \'{}\'".format(name))
        return
    if len(res) > 1:
        print("There were more than one match, which one would you like?")
        for i in range(len(res)):
            print("{}: {}, {}".format(i, res[i][8], res[i][6]))
        choice = input("Default is 0: ")
        try:
            if choice == "":
                c = 0
            elif int(choice) > 0:
                c = int(choice)
        except ValueError:
            print("\nChoice must be a number from 0 to {}. Cancelling request".format(len(res)-1))
            return
    res = res[c]
    string = ""
    string += "\nNumber: {}".format(res[0])
    string += "\nCommon Name: {}".format(res[8])
    string += "\nAlternative Name: {}".format(res[6])
    string += "\nRA: {}".format(res[1])
    string += "\nDEC: {}".format(res[2])
    string += "\nMagnitude: {0:.1f}".format(res[4])
    print(string + "\n")

# Gets all the data in a human readable format given a star number
def info(number):
    res = get_star_from_number(number)
    if res == None or len(res) < 1:
        print("No matches were found for star number {}".format(number))
        return
    res = res[0]
    string = ""
    string += "\nNumber: {}".format(res[0])
    string += "\nCommon Name: {}".format(res[8])
    string += "\nAlternative Name: {}".format(res[6])
    string += "\nRA: {}".format(res[1])
    string += "\nDEC: {}".format(res[2])
    string += "\nMagnitude: {0:.1f}".format(res[4])
    string += "\nSize: {}".format(res[3])
    string += "\nType and Description: {}".format(res[5])
    string += "\nQ Tags: {}".format(res[7])
    string += "\nComments: {}".format(res[9])
    print(string + "\n")
