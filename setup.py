from setuptools import setup
import io


def readme():
    with io.open('README.md', encoding='utf-8') as f:
        return f.read()


setup(name='spbuTimetableAPI',
      version='1.0.3',
      description='Python SPbU TimeTable API.',
      long_description='',
      author='EeOneDown',
      author_email='st049378@student.spbu.ru',
      url='https://github.com/EeOneDown/spbuTimetableAPI',
      download_url='https://github.com/EeOneDown/spbuTimetableAPI.git',
      packages=['spbu'],
      license='GPL2',
      keywords='spbu timetable api tools',
      install_requires=['requests'],
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Programming Language :: Python :: 3.7',
          'Environment :: Console',
          'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
      ]
      )
