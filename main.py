# Execution time
#from time import time

# For running with command line
import click

# For database management
from database.util import init, shutdown


class course:
    def __init__(self, dict_from_json=None, name=None, resources=None, descriptions=None):
        if dict_from_json:
            d = dict_from_json
            self.name = d["name"]
            self.descriptions = d["descriptions"]
            self.resources = d["resources"]
        else:
            self.name = name
            self.descriptions = descriptions
            self.resources = resources


@click.command()
@click.argument('name')
@click.option('--description', '-d', type=(str, str), default=(), help='Course description and source', multiple=True)
@click.option('--resource', '-r', type=str, default='', help='Resource type used in course', multiple=True)
def new_course(name, description, resource):
    #start_time = time()

    course_list = init()

    # Multiple descriptions creates a single description tuple containing multiple inputs tuples
    descriptions = [{'text': d[0], 'source': d[1]} for d in description]

    resources = resource

    course_list.append(course(name=name, resources=resources, descriptions=descriptions))

    shutdown(course_list)

    #print("Total time: {} seconds".format(time() - start_time))
