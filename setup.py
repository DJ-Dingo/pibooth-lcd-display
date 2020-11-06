#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from io import open
import os.path as osp
from setuptools import setup

import pibooth_lcd_i2c as plugin

HERE = osp.abspath(osp.dirname(__file__))
sys.path.insert(0, HERE)


def main():
    setup(
        name=plugin.__name__,
        version=plugin.__version__,
        description=plugin.__doc__,
        long_description=open(osp.join(HERE, 'README.rst'), encoding='utf-8').read(),
        long_description_content_type='text/x-rst',
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Environment :: Plugins',
            'Intended Audience :: Developers',
            'Intended Audience :: End Users/Desktop',
            'License :: OSI Approved :: GNU Affero General Public License v3',
            'Natural Language :: English',
            'Operating System :: POSIX :: Linux',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Topic :: Multimedia :: Graphics :: Capture :: Digital Camera',
        ],
        author="Kenneth Nicholas Jørgensen, Vincent Verdeil",
        url="https://github.com/DJ-Dingo/pibooth-lcd-I2c",
        download_url="https://github.com/DJ-Dingo/pibooth-lcd-I2c/archive/{}.tar.gz".format(plugin.__version__),
        license='GPLv3',
        platforms=['unix', 'linux'],
        keywords=[
            'Raspberry Pi',
            'camera',
            'photobooth',
            'pygame',
            'lcd'
        ],
        py_modules=['pibooth_lcd_i2c'],
        install_requires=[
            'pibooth>=2.0.0',
            'RPLCD>=1.3.0'
        ],
        include_package_data=True,
        options={
            'bdist_wheel':
                {'universal': True}
        },
        zip_safe=True,  # Don't install the lib as an .egg zipfile
        entry_points={'pibooth': ["pibooth_lcd_i2c = pibooth_lcd_i2c"]},
    )

if __name__ == '__main__':
    main()
