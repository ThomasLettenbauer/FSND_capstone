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
        # Tokens for different access rights
        self.nopermissions = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImQxUDVUSHZaX1JJSHhWYXMwUjlkNSJ9.eyJpc3MiOiJodHRwczovL2ZzbmRjYXBzdG9uZS5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYxOWFjOWIxNzFkMjIwMDEzYWM2OTU1IiwiYXVkIjoibW92aWVzYWN0b3JzIiwiaWF0IjoxNTk1NTE4MTM0LCJleHAiOjE1OTU2MDQ1MzMsImF6cCI6IjVnOHFjM0VhWUtHemxMeDVJZ1V0ZnBpdFJVUlFySHMwIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6W119.e5WIalDuMNIwifPrmn4mI_BgYp5Puuj9jjMEMRzjsO-OlpA6KB2ApadUl-_Sje9gdv9MxwIKBQr3c1JEVUJbqK0IgiNzHcA9ZtZc8Ib917UjGigJUPzEo6iGe4H20QHiMkng-iVVEgyCTqzbzf28vMnjSUAbmnUZEKHDQwN4CCIFc_xSZCiB0yyZyauSYrQy69xUnCq6qxGv8r3AygUz_uqsuvc1jR-pWDSHmrL_uGKbgh9dyT_KGNNJc4HEhoNsHpXj5UmRmEG2oaNHU1Pfjc8EHd1kaPRErsI97NlmnS093KLAzrxGeCsD_Aa6Hp-RSouTkUg6UJPMofSvpYVgEw'
        self.cast_assistant = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImQxUDVUSHZaX1JJSHhWYXMwUjlkNSJ9.eyJpc3MiOiJodHRwczovL2ZzbmRjYXBzdG9uZS5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYxODg1NzZjNWE1ODUwMDE5YjE5MGYwIiwiYXVkIjoibW92aWVzYWN0b3JzIiwiaWF0IjoxNTk1NDQ0MjA5LCJleHAiOjE1OTU1MzA2MDgsImF6cCI6IjVnOHFjM0VhWUtHemxMeDVJZ1V0ZnBpdFJVUlFySHMwIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.dUvfQvMrVynHKxD7PXusYQpIg8FbTplqVM5ku4x_o22TOmr7xoixxUnz-OXqsWWI2dqORYAH_5aW3BpABIWzCHHnhJVQqwSfSIU_5KBsRE8wp9KmogVNfjK1Pm0HpwF5MTh4d2LPMmCuvQRVkbKKOZ4eyXtqsSesxWdSHUdCIFJXSCEFgSYRlks9BNdRgNaVXTo3SDy_sdcebm2GK2Uia7ytvCI8Jh9CPuhORK4t3IcC61Ktu0-a0tvxHEhPUiKRoJ6IgmmPmNjv3KgaQ5gO3S8BFjb6Vx1xvEWjUxi1sJWEq60yekiOzp5j6SOaw6fgqOjm8xrXynRuFMSzosslyQ'
        self.cast_director = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImQxUDVUSHZaX1JJSHhWYXMwUjlkNSJ9.eyJpc3MiOiJodHRwczovL2ZzbmRjYXBzdG9uZS5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYxOWE3MTlmMDAxNzQwMDE5YzI4NTI5IiwiYXVkIjoibW92aWVzYWN0b3JzIiwiaWF0IjoxNTk1NTE4MDI1LCJleHAiOjE1OTU2MDQ0MjQsImF6cCI6IjVnOHFjM0VhWUtHemxMeDVJZ1V0ZnBpdFJVUlFySHMwIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.sqja_SL0nzXGiYWopuPdE_ExRjZ0eOZktlSanAdHBoTBsfID2tFAMma0hwgDd4z5xeOPmI2NoDMjLrcmSaodUVPK4XDC2Mnuck45DsIEHN7UbgydJ40j5vLHJMD-AoJjB3EnFvLS7qU2kDsv-QemUYKRUMkRFVUxz7ecJRvyGCf4PwLOUs6-F3jvjjTW3-HpOx-QZkl7Yro5e30GASvPmExKDSdoWv3H5mvLk0fXuM0fbVGvyYIMQsfFJsDrOzxuTQHNaQraYW6CYQbelY6OOodwOK-TIjz2uqR8Gc7S1Lw5UqDqzr6iXohRAr3cGqPJzRLsIzio2r0d00m87RXzqg'
        self.exec_producer = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImQxUDVUSHZaX1JJSHhWYXMwUjlkNSJ9.eyJpc3MiOiJodHRwczovL2ZzbmRjYXBzdG9uZS5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYxOWFjOWIxNzFkMjIwMDEzYWM2OTU1IiwiYXVkIjoibW92aWVzYWN0b3JzIiwiaWF0IjoxNTk1NTE4Mzg5LCJleHAiOjE1OTU2MDQ3ODgsImF6cCI6IjVnOHFjM0VhWUtHemxMeDVJZ1V0ZnBpdFJVUlFySHMwIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.fwgTVeRts9Fbe8MBKWb6bnJNpVcq_25EEuM6CV_8E7L2BkMxzDxUNVzHmhg1KU1-UG3e0WJnPRj-GA4TnPj845FXZG576LcRJUGxQPObQ5rMRcUGtEegZIUt5WtzJ7nijrPuSLKWFzyb9ELIOBj_FNzR6rmgg_QtDxDbA4VaC0nSPoX8Q6eL7K0GvyuDaCoh_bTnJgukQUhR0rgszBGAzFZn7-kslMkmAizbDVMbRr8FHQ3ZKT02JrQq_Ebmg_FLyb2e8Lm_7CA_nWUoRXPczmGWhR6tw0GWNZcbsuySdp4aqNwb6sXA0hpcODUaY7CgAdhTKbutPdZIlgWxfln4_g'

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

    # Test GET all actors (no permissions - Unauthorized)
    def test_get_actors_nopermissions(self):
        res = self.client().get('/actors',
                                headers={'Authorization':
                                         'Bearer ' + self.nopermissions})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    # Test GET all actors (Executive Producer)
    def test_get_actors_producer(self):
        res = self.client().get('/actors',
                                headers={'Authorization':
                                         'Bearer ' + self.exec_producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    # Test GET all movies (nopermissions - Unauthorized)
    def test_get_movies_nopermissions(self):
        res = self.client().get('/movies',
                                headers={'Authorization':
                                         'Bearer ' + self.nopermissions})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    # Test GET all movies (Executive Producer)
    def test_get_movies_producer(self):
        res = self.client().get('/movies',
                                headers={'Authorization':
                                         'Bearer ' + self.exec_producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    # Test POST an actor (nopermissions - Unauthorized)
    def test_post_actors_nopermissions(self):

        body = {
            'name': 'Bibi Blueeyes',
            'age': 25,
            'gender': 'female'
        }

        res = self.client().post('/actors', data=json.dumps(body),
                                 headers={'Content-Type': 'application/json', 'Authorization':
                                          'Bearer ' + self.nopermissions})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    # Test POST an actor (Executive Producer)
    def test_post_actors_producer(self):

        body = {
            'name': 'Bibi Blueeyes',
            'age': 25,
            'gender': 'female'
        }

        res = self.client().post('/actors', data=json.dumps(body),
                                 headers={'Content-Type': 'application/json', 'Authorization':
                                          'Bearer ' + self.exec_producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Test POST a movie (nopermissions - Unauthorized)
    def test_post_movies_nopermissions(self):

        body = {
            'title': 'The Blue Screen',
            'releasedate': '10/10/2020'
        }

        res = self.client().post('/actors', data=json.dumps(body),
                                 headers={'Content-Type': 'application/json', 'Authorization':
                                          'Bearer ' + self.nopermissions})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    # Test POST a movie (Executive Producer)
    def test_post_movies_producer(self):

        body = {
            'title': 'The Blue Screen',
            'releasedate': '10/10/2020'
        }

        res = self.client().post('/movies', data=json.dumps(body),
                                 headers={'Content-Type': 'application/json', 'Authorization':
                                          'Bearer ' + self.exec_producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Test PATCH an actor (nopermissions - Unauthorized)
    def test_patch_actors_nopermissions(self):

        body = {
            'age': 35
        }

        res = self.client().patch('/actors/1', data=json.dumps(body),
                                  headers={'Content-Type': 'application/json', 'Authorization':
                                           'Bearer ' + self.nopermissions})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    # Test PATCH an actor (Executive Producer)
    def test_patch_actors_producer(self):

        body = {
            'age': 35
        }

        res = self.client().patch('/actors/1', data=json.dumps(body),
                                  headers={'Content-Type': 'application/json', 'Authorization':
                                           'Bearer ' + self.exec_producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Test PATCH a movie (nopermissions - Unauthorized)
    def test_patch_movies_nopermissions(self):

        body = {
            'title': 'The Yellow Screen'
        }

        res = self.client().patch('/movies/1', data=json.dumps(body),
                                  headers={'Content-Type': 'application/json', 'Authorization':
                                           'Bearer ' + self.nopermissions})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    # Test PATCH a movie (Executive Producer)
    def test_patch_movies_producer(self):

        body = {
            'title': 'The Yellow Screen'
        }

        res = self.client().patch('/movies/1', data=json.dumps(body),
                                  headers={'Content-Type': 'application/json', 'Authorization':
                                           'Bearer ' + self.exec_producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

   # Test DELETE an actor (no permissions - Unauthorized)
    def test_delete_actors_nopermissions(self):
        res = self.client().delete('/actors/1',
                                   headers={'Authorization':
                                            'Bearer ' + self.nopermissions})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    # Test DELETE an actor (Executive Producer)
    def test_delete_actors_producer(self):
        res = self.client().delete('/actors/1',
                                   headers={'Authorization':
                                            'Bearer ' + self.exec_producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Test DELETE a movie (nopermissions - Unauthorized)
    def test_delete_movies_nopermissions(self):
        res = self.client().delete('/movies/1',
                                   headers={'Authorization':
                                            'Bearer ' + self.nopermissions})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    # Test DELETE a movie (Executive Producer)
    def test_delete_movies_producer(self):
        res = self.client().delete('/movies/1',
                                   headers={'Authorization':
                                            'Bearer ' + self.exec_producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
