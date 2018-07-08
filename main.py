

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


    cursor.execute("INSERT INTO courses (name) VALUES ('{}')".format(name))
    course_id = cursor.lastrowid
    
    # Multiple descriptions creates a single description tuple containing multiple inputs tuples
    for d in description:
        cursor.execute("INSERT INTO descriptions (course_id, text, source) VALUES ({}, '{}', '{}')".format(course_id, d[0], d[1]))


    connection.commit()
    connection.close()

    print("Total time: {} seconds".format(time() - start_time))
