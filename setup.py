from setuptools import setup, find_packages

setup(
    name='ppr2pandas',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests', 
        'pandas',
        'numpy',
    ],
    entry_points={
        'console_scripts': [
            'get_ppr=ppr2pandas.ppr:get_ppr',
        ],
    },
    author="Michael O'Neill",
    author_email='michaelon024@gmail.com',
    description=("Download Ireland's Property Price Register for data "
                 "analysis in Python/pandas"),
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/mon04/ppr2pandas',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
