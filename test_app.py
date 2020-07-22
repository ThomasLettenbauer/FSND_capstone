import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie


class AgencyTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client
        self.database_name = "agency_test"
        self.database_path = "postgresql:///{}".format(self.database_name)
        setup_db(self.app, self.database_path)
        self.test_user = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImQxUDVUSHZaX1JJSHhWYXMwUjlkNSJ9.eyJpc3MiOiJodHRwczovL2ZzbmRjYXBzdG9uZS5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYxODg1NzZjNWE1ODUwMDE5YjE5MGYwIiwiYXVkIjoibW92aWVzYWN0b3JzIiwiaWF0IjoxNTk1NDQ0MjA5LCJleHAiOjE1OTU1MzA2MDgsImF6cCI6IjVnOHFjM0VhWUtHemxMeDVJZ1V0ZnBpdFJVUlFySHMwIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.dUvfQvMrVynHKxD7PXusYQpIg8FbTplqVM5ku4x_o22TOmr7xoixxUnz-OXqsWWI2dqORYAH_5aW3BpABIWzCHHnhJVQqwSfSIU_5KBsRE8wp9KmogVNfjK1Pm0HpwF5MTh4d2LPMmCuvQRVkbKKOZ4eyXtqsSesxWdSHUdCIFJXSCEFgSYRlks9BNdRgNaVXTo3SDy_sdcebm2GK2Uia7ytvCI8Jh9CPuhORK4t3IcC61Ktu0-a0tvxHEhPUiKRoJ6IgmmPmNjv3KgaQ5gO3S8BFjb6Vx1xvEWjUxi1sJWEq60yekiOzp5j6SOaw6fgqOjm8xrXynRuFMSzosslyQ'
        self.exec_prod = 'token_value_2'

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

        # Insert some test data
        Actor(age=20, gender='male', name='The Flash').insert()
        Movie(title='The Green Screen', releasedate='10/10/2020').insert()

    def tearDown(self):
        """Executed after each test"""
        pass

    # Test GET all actors (Test User)
    def test_get_actors(self):
        res = self.client().get('/actors',
                                headers={'Authorization':
                                         'Bearer ' + self.test_user})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    # Test GET all movies (Test User)
    def test_get_movies(self):
        res = self.client().get('/movies',
                                headers={'Authorization':
                                         'Bearer ' + self.test_user})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
