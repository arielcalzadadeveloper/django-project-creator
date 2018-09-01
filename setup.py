import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-project-creator',
    version='0.0.2',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    description='Simple command line script for creating Django Projects.',
    long_description=README,
    url='https://github.com/arielcalzadadeveloper/django-project-creator',
    author='Ariel Calzada',
    author_email='ariel.calzada.developer@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: The GNU General Public License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
    scripts=[
        'bin/project_creator.py'
    ],
    install_requires=[
        'django',
    ],
)