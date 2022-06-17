from pathlib import Path

from setuptools import (
    setup, find_packages
)

setup(
    name='drf_fsm',
    url='https://github.com/sainipray/drf-fsm',
    license='MIT',
    description='Create Django FSM transitions as a endpoint with Django REST Framework',
    long_description=Path('README.rst').read_text(encoding='utf-8'),
    long_description_content_type="text/markdown",
    author='Neeraj Kumar',
    author_email='sainineeraj1234@gmail.com',
    install_requires=[
        'django',
        'djangorestframework',
    ],
    version='1.0.1',
    packages=find_packages(),
    python_requires='>=3.6',
    include_package_data=True,
    zip_safe=False,
    platforms=['any'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        "Framework :: Django :: 3.1",
        "Framework :: Django :: 3.2",
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
