#!/usr/bin/python

from setuptools import setup, find_packages
from gfxn import VERSION

setup(name='gfxn',
    version=VERSION,
    packages=find_packages(),
    py_modules=['gfxn'],
    description='Gtk FX Notification',
    author='TANIGUCHI Takaki',
    author_email='takaki@asis.media-as.org',
    url='http://github.com/takkai/gfxn',
    license='GPL3',
#    install_requires=['gi'],
    entry_points = {
        'gui_scripts' : [
            'gfxn = gfxn:run',
        ]
    },
    data_files = [('/usr/share/icons',  ['gfxn.png'])]
)
