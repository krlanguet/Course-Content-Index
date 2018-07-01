
# For running with command line
import click

# For database storage
from json import loads, dumps

# For backing-up previous outputs
from os.path import isfile
from time import strftime as time
from shutil import copy


# Function for opening the database and preparing for any commands
def init():
    t = time('%H:%M:%S') # Local time in 24Hour, minute, seconds

    # Backup previous data output
    if isfile('courses.json'):
        copy('courses.json', 'data_backup/' + t + '.json')

    # Copies entire contents of file into string
    with open('courses.json', 'r+') as data_file:
        course_list = loads(data_file.read())

    '''
    for i, entry in enumerate(course_list):
        course_list[i] = course(entry)
    '''

    return course_list


# Function for saving to the databse and exiting after all commands are finished
def shutdown():
    # Dumps potentially modified string back into file
    with open('courses.json', 'w+') as data_file:
        data_file.write('[\n')
        l = len(course_list)
        for i,course in enumerate(course_list):
            data_file.write(dumps(course, indent=4))
            if (i + 1) < l:
                data_file.write(',')
        data_file.write('\n]')


class course:
    def __init__(self, name='un-named'):
        self.name = name
        self.descriptions = []
        self.resources = {}


@click.command()
@click.argument('name')
@click.option('--description', '-d', type=(str, str), default=(), help='Course description and source', multiple=True)
def new_course(name, description):
    # Multiple descriptions creates a single description tuple containing multiple inputs tuples
    print(name)
    print(description)


if __name__ == '__main__':
    course_list = init()
    #new_course()
    shutdown()
