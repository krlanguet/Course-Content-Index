from setuptools import setup

setup(
    name='Course Content Index',
    version='0.1',
    py_modules=['main'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        new_course=main:new_course
    '''
)
