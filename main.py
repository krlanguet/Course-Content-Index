
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
        # Potential bug here !! need to create empty list if there is no file!

    for i, entry in enumerate(course_list):
        course_list[i] = course(dict_from_json = entry)

    return course_list


# Function for saving to the databse and exiting after all commands are finished
def shutdown(course_list):
    # Dumps potentially modified string back into file
    with open('courses.json', 'w+') as data_file:
        data_file.write('[\n')
        l = len(course_list)
        for i, course in enumerate(course_list):
            data_file.write(dumps(course.__dict__, indent=4))
            if (i + 1) < l:
                data_file.write(',\n')
        data_file.write('\n]')


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
    course_list = init()

    # Multiple descriptions creates a single description tuple containing multiple inputs tuples
    descriptions = []
    for d in description:
        descriptions.append({'text': d[0], 'source': d[1]})


    course_list.append(course(name=name, descriptions=descriptions))

    shutdown(course_list)
