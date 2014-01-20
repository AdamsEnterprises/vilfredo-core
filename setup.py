# -*- coding: utf-8 -*-
#
# This file is part of VilfredoReloadedCore.
#
# Copyright © 2009-2013 Pietro Speroni di Fenizio / Derek Paterson.
#
# VilfredoReloadedCore is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation version 3 of the License.
#
# VilfredoReloadedCore is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public
# License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with VilfredoReloadedCore.  If not, see
# <http://www.gnu.org/licenses/>.
#
###############################################################################


from setuptools import setup

with open('requirements/base.txt') as f:
     requirements_base = f.read().splitlines()

with open('requirements/test.txt') as f:
    requirements_test = f.read().splitlines()

setup(
    name='VilfredoCore',
    version=open('version.txt').read().strip(),
    author = 'Derek Paterson, Pietro Speroni',
    author_email='athens_code@gmx.com, 2013@pietrosperoni.it',
    packages=['VilfredoReloadedCore', 'VilfredoReloadedCore.test'],
    # namespace_packages=['VilfredoReloadedCore'],
    keywords = 'Vilfredo Pareto, Decision Making, e-democracy',
    url='https://github.com/fairdemocracy/vilfredo-core',
    license='GNU AFFERO GENERAL PUBLIC LICENSE (AGPL) Version 3',
    # long_description=open('README.rst').read(),
    description = ('VilfredoReloadedCore the core of vilfredo, a'
                   ' consensus-building and decision-making tool'),
    entry_points='''
        [console_scripts]
        vr = VilfredoReloadedCore.main:main
        ''',
    # To skip problems of local eggs we make fat requirements:
    # http://stackoverflow.com/questions/1843424/setup-py-test-egg-install-location
    install_requires=requirements_base + requirements_test,
    include_package_data=True,
    test_suite='nose.collector',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: AGPL License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
