#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from io import open
import os.path as osp
from setuptools import setup


HERE = osp.abspath(osp.dirname(__file__))
sys.path.insert(0, HERE)
import pibooth_lcd_display as plugin   # nopep8 : import shall be done after adding setup to paths


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
        url="https://github.com/DJ-Dingo/pibooth-lcd-display",
        download_url="https://github.com/DJ-Dingo/pibooth-lcd-display/archive/{}.tar.gz".format(plugin.__version__),
        license='GPLv3',
        platforms=['unix', 'linux'],
        keywords=[
            'Raspberry Pi',
            'camera',
            'photobooth',
            'pygame',
            'lcd'
        ],
        py_modules=['pibooth_lcd_display'],
        python_requires=">=3.6",
        install_requires=[
            'pibooth>=2.0.0',
            'RPLCD>=1.3.0'
        ],
        include_package_data=True,
        options={
            'bdist_wheel':
                {'universal': True}
        },
        zip_safe=False,  # Don't install the lib as an .egg zipfile
        entry_points={'pibooth': ["pibooth_lcd_display = pibooth_lcd_display"]},
    )

if __name__ == '__main__':
    main()
