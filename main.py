

# Execution time
from time import time

# For running with command line
import click

# For database storage
#from json import loads, dumps
from sqlite3 import connect

# For backing-up previous outputs
from os.path import isfile
from time import strftime
from shutil import copy


# Function for opening the database and preparing for any commands
def init():
    '''
    t = strftime('%H:%M:%S') # Local time in 24Hour, minute, seconds

    # Backup previous data output
    if isfile('courses.json'):
        copy('courses.json', 'data_backup/' + t + '.json')
    '''

    connection = connect("courses.db")

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses(
            course_id INTEGER PRIMARY KEY,
            name TEXT
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS descriptions(
            descr_id INTEGER PRIMARY KEY,
            course_id INT,
            text TEXT,
            source TEXT
        );
    """)

    return [connection, cursor]


# Function for saving to the databse and exiting after all commands are finished
def shutdown(connection):
    connection.commit()
    connection.close()


class course:
    def __init__(self, dict_from_json = None, name=None, descriptions=None):
        if dict_from_json:
            d = dict_from_json
            self.name = d["name"]
            self.descriptions = d["descriptions"]
            #self.resources = {}
        else:
            self.name = name
            self.descriptions = descriptions


@click.command()
@click.argument('name')
@click.option('--description', '-d', type=(str, str), default=(), help='Course description and source', multiple=True)
def new_course(name, description):
    start_time = time()

    con, curs = init()

    curs.execute("INSERT INTO courses (name) VALUES ('{}')".format(name))
    course_id = curs.lastrowid
    
    # Multiple descriptions creates a single description tuple containing multiple inputs tuples
    for d in description:
        curs.execute("INSERT INTO descriptions (course_id, text, source) VALUES ({}, '{}', '{}')".format(course_id, d[0], d[1]))


    shutdown(con)
    print("Total time: {} seconds".format(time() - start_time))
