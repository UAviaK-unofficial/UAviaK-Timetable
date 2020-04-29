#!/usr/bin/python3
from setuptools import setup, find_packages


def requirements():
    """Создание листа зависимостей для этого проекта."""
    requirements_list = []

    with open('requirements.txt') as requirements:
        for install in requirements:
            requirements_list.append(install.strip())

    return requirements_list


setup(
    name='uaviak_timetable',
    version='1.4.2',
    author='Gleb Liutsko',
    author_email='gleb290303@gmail.com',
    license='MIT',
    url='https://github.com/gleb-liutsko/UAviaK-Timetable',
    keywords='timetable uaviak Ulyanovsk',
    description="Python библиотека для получения расписания",
    packages=find_packages(),
    zip_safe=False,
    install_requires=requirements(),
    classifiers=[
		'Natural Language :: Russian',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
		'Topic :: Software Development :: Libraries :: Python Modules',
		'Programming Language :: Python',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
		'Programming Language :: Python :: 3.8'
	]
)
