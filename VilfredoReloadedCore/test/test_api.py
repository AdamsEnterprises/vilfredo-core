# -*- coding: utf-8 -*-
#
# This file is part of VilfredoReloadedCore.
#
# Copyright (c) 2013 Derek Paterson <athens_code@gmx.com>
#
# VilfredoReloadedCore is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation version 3 of the License.
#
# VilfredoReloadedCore is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License
# for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with VilfredoReloadedCore.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

'''
Database Models test for VilfredoReloadedCore
'''

# unittest2 offers TestCase.assertMultiLineEqual that provide a nice
# diff output, sometimes it is called automagically by the old
# assertEqual

try:
    import unittest2 as unittest
except ImportError:
    # NOQA
    import unittest

from .. import app
from .. import views, api  # NOQA
from .. database import drop_db, init_db
import base64
import json
import os

DELETE_DB_ON_EXIT = True


class LoginTestCase(unittest.TestCase):
    def setUp(self):
        # app.logger.debug("Create DB")
        # init_db()
        # For SQLite development DB only
        if 'vr.db' in app.config['SQLALCHEMY_DATABASE_URI']:
            # Drop existing DB first
            if os.path.isfile('/var/tmp/vr.db'):
                app.logger.debug("Dropping existing sqlite db\n")
                drop_db()
            # Create empty SQLite test DB
            app.logger.debug("Initializing sqlite db\n")
            init_db()

        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self):
        # For SQLite development DB only
        if 'vr.db' in app.config['SQLALCHEMY_DATABASE_URI'] \
                and DELETE_DB_ON_EXIT:
            app.logger.debug("Dropping sqlite db\n")
            drop_db()

    def open_with_json_auth(self, url, method, data, username, password):
        return self.app.open(
            url,
            content_type='application/json',
            method=method,
            data=json.dumps(data),
            headers={'Authorization': 'Basic ' +
                     base64.b64encode(username + ":" + password)})

    def open_with_json(self, url, method, data):
        return self.app.open(url,
                             content_type='application/json',
                             method=method,
                             data=json.dumps(data))

    def open_with_auth(self, url, method, data, username, password):
        return self.app.open(
            url,
            method=method,
            headers={'Authorization': 'Basic ' +
                     base64.b64encode(username + ":" + password)})

    def get_message(self, rv):
        data = json.loads(rv.data)
        if 'message' in data:
            return data['message']
        else:
            return "No error message returned"

    def test_rest_api(self):
        #
        # Create Users
        #
        # rv = self.app.post('/api/v1/users', data=payload,
        #                    content_type='application/json')
        rv = self.open_with_json('/api/v1/users',
                                 'POST',
                                 dict(username='john',
                                      email='john@example.com',
                                      password='test123'))
        self.assertEqual(rv.status_code, 201)
        data = json.loads(rv.data)
        app.logger.debug("New user at = %s\n", data['object']['url'])
        # Log data received
        app.logger.debug("Data retrieved from Create User = %s\n", rv.data)

        # Attempt to create a user with a duplicate username
        rv = self.open_with_json('/api/v1/users',
                                 'POST',
                                 dict(username='john',
                                      email='john@example.com',
                                      password='test123'))
        self.assertEqual(rv.status_code, 400)
        self.assertEqual('Username not available',
                         self.get_message(rv),
                         self.get_message(rv))
        app.logger.debug("Create user with duplicate username: Message: %s",
                         self.get_message(rv))
        # Log data received
        app.logger.debug("Data retrieved from Create Duplicate User = %s\n",
                         rv.data)

        # Attempt to create a user with a duplicate email
        rv = self.open_with_json('/api/v1/users',
                                 'POST',
                                 dict(username='keith',
                                      email='john@example.com',
                                      password='test123'))
        self.assertEqual(rv.status_code, 400)
        self.assertEqual('Email not available', self.get_message(rv),
                         self.get_message(rv))
        app.logger.debug(
            "Create user with duplicate email address: Message: %s",
            self.get_message(rv))
        # Log data received
        app.logger.debug(
            "Data retrieved from Create User/dupicate email = %s\n",
            rv.data)

        # Attempt to create a user with too short a password
        rv = self.open_with_json('/api/v1/users',
                                 'POST',
                                 dict(username='keith',
                                      email='keith@example.com',
                                      password='12345'))
        self.assertEqual(rv.status_code, 400)
        self.assertIn('Password must be between',
                      self.get_message(rv),
                      self.get_message(rv))
        app.logger.debug("Create user with too short a password: Message: %s",
                         self.get_message(rv))

        rv = self.open_with_json('/api/v1/users',
                                 'POST',
                                 dict(username='susan',
                                      email='susan@example.com',
                                      password='test123'))
        self.assertEqual(rv.status_code, 201)

        rv = self.open_with_json('/api/v1/users',
                                 'POST',
                                 dict(username='bill',
                                      email='bill@example.com',
                                      password='test123'))
        self.assertEqual(rv.status_code, 201)

        rv = self.open_with_json('/api/v1/users',
                                 'POST',
                                 dict(username='jack',
                                      email='jack@example.com',
                                      password='test123'))
        self.assertEqual(rv.status_code, 201)

        rv = self.open_with_json('/api/v1/users',
                                 'POST',
                                 dict(username='harry',
                                      email='harry@example.com',
                                      password='test123'))
        self.assertEqual(rv.status_code, 201)

        #
        # Create Question
        #
        rv = self.open_with_json_auth('/api/v1/questions',
                                      'POST',
                                      dict(title='My question',
                                           blurb='My blurb',
                                           room='vilfredo',
                                           minimum_time=0),
                                      'john',
                                      'test123')
        self.assertEqual(rv.status_code, 201)
        data = json.loads(rv.data)
        app.logger.debug("New question at = %s\n", data['object']['url'])
        # Log data received
        app.logger.debug("Data retrieved from Create Question = %s\n",
                         rv.data)

        #
        # Create More Questions
        #
        rv = self.open_with_json_auth('/api/v1/questions',
                                      'POST',
                                      dict(title='Another Question',
                                           blurb='Blah blah Blah blah Blah',
                                           room='vilfredo',
                                           minimum_time=0),
                                      'john',
                                      'test123')
        self.assertEqual(rv.status_code, 201)

        rv = self.open_with_json_auth('/api/v1/questions',
                                      'POST',
                                      dict(title='Too Many Chefs',
                                           blurb='How to Spoil the broth?',
                                           room='vilfredo',
                                           minimum_time=0),
                                      'harry',
                                      'test123')
        self.assertEqual(rv.status_code, 201)

        #
        # Create Invites
        #
        rv = self.open_with_json_auth('/api/v1/questions/1/invitations',
                                      'POST',
                                      dict(invite_user_ids=[2, 3, 4, 5]),
                                      'john',
                                      'test123')
        self.assertEqual(rv.status_code, 201)
        # Log data received
        app.logger.debug("Data retrieved fro Create Invite = %s\n", rv.data)

        #
        # Create Subscriptions
        #
        rv = self.open_with_json_auth('/api/v1/users/1/subscriptions',
                                      'POST',
                                      dict(question_id=1, how='asap'),
                                      'john',
                                      'test123')
        self.assertEqual(rv.status_code, 201)
        # Log data received
        app.logger.debug("Data retrieved from Create Subscription = %s\n",
                         rv.data)

        rv = self.open_with_json_auth('/api/v1/users/1/subscriptions',
                                      'POST',
                                      dict(question_id=2, how='asap'),
                                      'john',
                                      'test123')
        self.assertEqual(rv.status_code, 201)

        rv = self.open_with_json_auth('/api/v1/users/1/subscriptions',
                                      'POST',
                                      dict(question_id=3, how='weekly'),
                                      'john',
                                      'test123')
        self.assertEqual(rv.status_code, 201)

        rv = self.open_with_json_auth('/api/v1/users/1/subscriptions',
                                      'GET',
                                      dict(),
                                      'john',
                                      'test123')
        self.assertEqual(rv.status_code, 200)
        # Log data received
        app.logger.debug("Data retrieved from Get Subscriptions = %s\n",
                         rv.data)

        #
        # Delete Subscription
        #
        rv = self.open_with_json_auth('/api/v1/users/1/subscriptions/3',
                                      'DELETE',
                                      dict(),
                                      'john',
                                      'test123')
        self.assertEqual(rv.status_code, 200)
        # Log data received
        app.logger.debug("Data retrieved from Delete Subscription = %s\n",
                         rv.data)

        #
        # Create Proposals
        #
        rv = self.open_with_json_auth(
            '/api/v1/questions/1/proposals',
            'POST',
            dict(title='Bills First Proposal',
                 blurb='Bills blurb of varying interest'),
            'bill',
            'test123')
        self.assertEqual(rv.status_code, 201)
        # Log data received
        app.logger.debug("Data retrieved from Create Proposal = %s\n",
                         rv.data)

        rv = self.open_with_json_auth(
            '/api/v1/questions/1/proposals',
            'POST',
            dict(title='Bills Second Proposal',
                 blurb='Bills blurb of varying disinterest',
                 abstract='This is too abstract for an abstract'),
            'bill',
            'test123')
        self.assertEqual(rv.status_code, 201)

        rv = self.open_with_json_auth(
            '/api/v1/questions/1/proposals',
            'POST',
            dict(title='Susans Only Proposal',
                 blurb='My blub is cool',
                 abstract='Blah blah blah'),
            'susan',
            'test123')
        self.assertEqual(rv.status_code, 201)

        rv = self.open_with_json_auth(
            '/api/v1/questions/1/proposals',
            'POST',
            dict(
                title='Harrys Cool Proposal',
                blurb='Harry wrties like a champ'),
            'harry',
            'test123')
        self.assertEqual(rv.status_code, 201)

        data = json.loads(rv.data)
        new_proposal_url = data['object']['url']
        app.logger.debug("New propoal URL = %s", new_proposal_url)

        # Harry edits his proposal
        rv = self.open_with_json_auth(
            new_proposal_url,
            'PATCH',
            dict(
                title='Harrys Cooler Proposal',
                blurb='Harry edits like a champ'),
            'harry',
            'test123')
        self.assertEqual(rv.status_code, 200, self.get_message(rv))
        # Log data received
        app.logger.debug("Data retrieved from Edit Proposal = %s\n",
                         rv.data)

        #
        # Author attempts to Delete a Question - Disallowed
        # because it has proposals
        #
        rv = self.open_with_json_auth('/api/v1/questions/1',
                                      'DELETE',
                                      dict(),
                                      'john',
                                      'test123')
        self.assertEqual(rv.status_code, 403, self.get_message(rv))
        self.assertIn("This question has proposals",
                      self.get_message(rv),
                      self.get_message(rv))
        app.logger.debug("Response message: %s", self.get_message(rv))
        # Log data received
        app.logger.debug("Data retrieved = %s\n", rv.data)

        #
        # Author move question on
        #
        rv = self.open_with_json_auth('/api/v1/questions/1',
                                      'PATCH',
                                      dict(move_on=True),
                                      'john',
                                      'test123')
        self.assertEqual(rv.status_code, 200, self.get_message(rv))
        # Log data received
        app.logger.debug("Data retrieved from Edit Question (Move On) = %s\n",
                         rv.data)

        #
        # Create Endorsements
        #
        # susans_prop1.endorse(susan)
        rv = self.open_with_json_auth(
            '/api/v1/questions/1/proposals/3/endorsements',
            'POST',
            dict(),
            'susan',
            'test123')
        self.assertEqual(rv.status_code, 201)
        # Log data received
        app.logger.debug("Data retrieved from Create Endorsement = %s\n",
                         rv.data)

        # susans_prop1.endorse(john)
        rv = self.open_with_json_auth(
            '/api/v1/questions/1/proposals/3/endorsements',
            'POST',
            dict(),
            'john',
            'test123')
        self.assertEqual(rv.status_code, 201)

        # bills_prop1.endorse(john)
        rv = self.open_with_json_auth(
            '/api/v1/questions/1/proposals/1/endorsements',
            'POST',
            dict(),
            'john',
            'test123')
        self.assertEqual(rv.status_code, 201)

        # bills_prop2.endorse(bill)
        rv = self.open_with_json_auth(
            '/api/v1/questions/1/proposals/2/endorsements',
            'POST',
            dict(),
            'bill',
            'test123')
        self.assertEqual(rv.status_code, 201)

        # harrys_prop1.endorse(jack)
        rv = self.open_with_json_auth(
            '/api/v1/questions/1/proposals/4/endorsements',
            'POST',
            dict(),
            'jack',
            'test123')
        self.assertEqual(rv.status_code, 201)

        # harrys_prop1.endorse(susan)
        rv = self.open_with_json_auth(
            '/api/v1/questions/1/proposals/4/endorsements',
            'POST',
            dict(),
            'susan',
            'test123')
        self.assertEqual(rv.status_code, 201)

        # bills_prop1.endorse(harry)
        rv = self.open_with_json_auth(
            '/api/v1/questions/1/proposals/1/endorsements',
            'POST',
            dict(),
            'harry',
            'test123')
        self.assertEqual(rv.status_code, 201)

        # susans_prop1.endorse(harry)
        rv = self.open_with_json_auth(
            '/api/v1/questions/1/proposals/3/endorsements',
            'POST',
            dict(),
            'harry',
            'test123')
        self.assertEqual(rv.status_code, 201)

        #
        # Get Proposal Endorsers
        #
        rv = self.open_with_json_auth(
            '/api/v1/questions/1/proposals/3/endorsers',
            'GET',
            dict(),
            'harry',
            'test123')
        self.assertEqual(rv.status_code, 200, rv.status_code)
        app.logger.debug("Data retrieved = %s\n", rv.data)
        # Log data received
        app.logger.debug("Data retrieved from Get Proposal Endorsers = %s\n",
                         rv.data)

        #
        # Get Question Pareto
        #
        rv = self.open_with_json_auth(
            '/api/v1/questions/1/pareto',
            'GET',
            dict(),
            'harry',
            'test123')
        self.assertEqual(rv.status_code, 200, rv.status_code)
        app.logger.debug("Data retrieved = %s\n", rv.data)
        # Log data received
        app.logger.debug("Data retrieved from Get Question Pareto = %s\n",
                         rv.data)

        #
        # Get Key Players
        #
        rv = self.open_with_json_auth(
            '/api/v1/questions/1/key_players',
            'GET',
            dict(),
            'harry',
            'test123')
        self.assertEqual(rv.status_code, 200, rv.status_code)
        app.logger.debug("Data retrieved = %s\n", rv.data)
        # Log data received
        app.logger.debug("Data retrieved from Get Key Players = %s\n",
                         rv.data)

        #
        # Get Endorser Effects
        #
        rv = self.open_with_json_auth(
            '/api/v1/questions/1/endorser_effects',
            'GET',
            dict(),
            'harry',
            'test123')
        self.assertEqual(rv.status_code, 200, rv.status_code)
        app.logger.debug("Endorser Effects data retrieved = %s\n", rv.data)
        # Log data received
        app.logger.debug("Data retrieved from Get Endorser Effects= %s\n",
                         rv.data)

        #
        # Get Proposal Relations
        #
        rv = self.open_with_json_auth(
            '/api/v1/questions/1/proposal_relations',
            'GET',
            dict(),
            'harry',
            'test123')
        self.assertEqual(rv.status_code, 200, rv.status_code)
        # Log data received
        app.logger.debug("Data retrieved from Get Proposal Relations = %s\n",
                         rv.data)

        #
        # Remove Endorsements
        #
        # John endorses proposal 2
        rv = self.open_with_json_auth(
            '/api/v1/questions/1/proposals/2/endorsements',
            'POST',
            dict(),
            'john',
            'test123')
        self.assertEqual(rv.status_code, 201)
        #
        # john removes endorsement from proposal 2
        rv = self.open_with_json_auth(
            '/api/v1/questions/1/proposals/2/endorsements',
            'DELETE',
            dict(),
            'john',
            'test123')
        self.assertEqual(rv.status_code, 200, self.get_message(rv))
        self.assertEqual("Endorsement removed",
                         self.get_message(rv),
                         self.get_message(rv))
        app.logger.debug("Response message: %s", self.get_message(rv))
        # Log data received
        app.logger.debug("Data retrieved from Remove Endorsement = %s\n",
                         rv.data)

        #
        # Create Another Question
        #
        rv = self.open_with_json_auth('/api/v1/questions',
                                      'POST',
                                      dict(title='My boring question',
                                           blurb='My boring blurb',
                                           room='test',
                                           minimum_time=0),
                                      'john',
                                      'test123')
        self.assertEqual(rv.status_code, 201)
        data = json.loads(rv.data)
        app.logger.debug("New question at = %s\n", data['object']['url'])
        new_question_url = data['object']['url']

        #
        # Author Deletes Question
        #
        rv = self.open_with_json_auth(new_question_url,
                                      'DELETE',
                                      dict(),
                                      'john',
                                      'test123')
        self.assertEqual(rv.status_code, 200, self.get_message(rv))
        self.assertIn("Question deleted",
                      self.get_message(rv),
                      self.get_message(rv))
        app.logger.debug("Response message: %s", self.get_message(rv))
        # Log data received
        app.logger.debug("Data retrieved from Delete Question = %s\n",
                         rv.data)

    def get_questions(self):
        rv = self.app.get('/api/v1/users')
        #  rv = self.open_with_auth(
        #    '/api/v1/users', 'GET', None, 'grippo', 'test123')
        app.logger.debug("Data retrieved = %s\n", rv.data)
        self.assertEqual(rv.status_code, 200)

        rv = self.open_with_auth('/api/v1/users/50', 'GET',
                                 None, 'grippo', 'test123')
        app.logger.debug("Data retrieved = %s\n", rv.data)

        data = json.loads(rv.data)
        self.assertNotIn('email', data['object'])

        rv = self.open_with_auth('/api/v1/users/638', 'GET',
                                 None, 'grippo', 'test123')
        app.logger.debug("Data retrieved = %s\n", rv.data)

        data = json.loads(rv.data)
        app.logger.debug("Email retrieved = %s\n", data['object']['email'])
        self.assertIn('email', data['object'])

    def empty_db(self):
        """Start with a blank database."""
        rv = self.app.get('/')
        self.assertTrue('no questions' in rv.data, rv.data)