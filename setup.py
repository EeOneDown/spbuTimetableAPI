from setuptools import setup
from io import open


def readme():
    with open('README.md', encoding='utf-8') as f:
        return f.read()


setup(name='spbuTimetableAPI',
      version='0.1',
      description='Python SPbU TimeTable API.',
      long_description=readme(),
      author='',
      author_email='',
      url='',
      packages=['spbu'],
      license='GPL2',
      keywords='spbu timetable api tools',
      install_requires=['requests'],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Programming Language :: Python :: 3',
          'Environment :: Console',
          'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
      ]
      )
