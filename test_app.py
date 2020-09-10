import unittest
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Movies, Actors
import json
import os

"""
- Includes at least one test for
            expected success and
            error behavior for
            each endpoint using the unittest library
- Includes tests demonstrating role-based access control,
at least two per role.
"""

Casting_Assistant_Token = f'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InBGa3BZWGxJZ3dnRV8xWWQxVjR5SyJ9.eyJpc3MiOiJodHRwczovL2Z1bGwtc3RhY2stcHJvamVjdC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY0ZjliNjQyMDc2YTcwMDY3OGYzYjdhIiwiYXVkIjoiYWdlbmN5IiwiaWF0IjoxNTk5NjIzOTQxLCJleHAiOjE1OTk3MTAzNDAsImF6cCI6IlNRa1ZMWFFhdWtlY1VQb3pPOElidjRvbmJXT3YzN29EIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWxsX2FjdG9ycyIsImdldDphbGxfbW92aWVzIl19.l_HKaVeNmnPQxbrwJe7WwYk9LWEPItDL3YrfEndD2G2SJHaAtK9aedf7zFIeLb_Nm_pz3KINYRrIC6_-rUUrb_uH8osqCuFjueIf-HxmLfB9-EUd2WGfFxsFSAEHoeMU20W5Rq0aqZJ1PT8NxGI4WD58_8YHMY2AO-K4NWAZwwXdy9jFZ-k9KTOoruiGC6NlfuKyfgWhozxFk34Yh8UhMAYkYNFaDY-OlpuZqcZ9NcJ51dRyT7tx09DXtavMsnYUFcX0gU6QalOvyL7jmlKmlRteAlXw9wHYut7ysjXgQGx49sOv4S_NMT-xenjXgHMev-u3qiW1SPIpnu3hiRZC0Q'
Casting_Director_Token = f'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InBGa3BZWGxJZ3dnRV8xWWQxVjR5SyJ9.eyJpc3MiOiJodHRwczovL2Z1bGwtc3RhY2stcHJvamVjdC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY0ZjlhOWYyMDc2YTcwMDY3OGYzYjZiIiwiYXVkIjoiYWdlbmN5IiwiaWF0IjoxNTk5NjIzNzU0LCJleHAiOjE1OTk3MTAxNTMsImF6cCI6IlNRa1ZMWFFhdWtlY1VQb3pPOElidjRvbmJXT3YzN29EIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJnZXQ6YWxsX2FjdG9ycyIsImdldDphbGxfbW92aWVzIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiXX0.ybho9nMa-8mC0MDdAGr4HqnM5YzdjZmtMVLr3XjoeQumEH6RahSbAqVjACNWuzzCpbU5PH0v9ute5SeVE9L9C3Gw07QO8gEkcBRpjkZXtuwdTxnRJGz1XRMKBILO3Y5eSLA4yyo1cuUlpAcBcxum8H6UQvKApge4LFRq_8yN1ZNcjb7osHK7ZRX6BfoyFSNHxQarruu8XrdAXmDKYXblx_uj_xolpdwiGF6mEWm_b4mgowASLmzWPwWtfNzbfTbEexJVg-oL-76BwfxIpKZGbTElkxxn_Gzoje3eIGqo6BXRCQRsZxtp1KBVg9qe5IjClabGwsGvIDbaTvf7dbPTEA'
Executive_Producer_Token = f'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InBGa3BZWGxJZ3dnRV8xWWQxVjR5SyJ9.eyJpc3MiOiJodHRwczovL2Z1bGwtc3RhY2stcHJvamVjdC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY0ZjlhNDBlOWVmNWYwMDY3YjYwNjM0IiwiYXVkIjoiYWdlbmN5IiwiaWF0IjoxNTk5NjIzNTI3LCJleHAiOjE1OTk3MDk5MjYsImF6cCI6IlNRa1ZMWFFhdWtlY1VQb3pPOElidjRvbmJXT3YzN29EIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJkZWxldGU6bW92aWUiLCJnZXQ6YWxsX2FjdG9ycyIsImdldDphbGxfbW92aWVzIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiLCJwb3N0Om1vdmllIl19.b1whVlKL7u8pDX1vGrYshmgDYTLSTWvVRljNBseRLOsrBBkNNc9A3SNHG8mSR2Sfy907I9DSckpRL-xnG59GcpcklnAPMSvcUjVTOONzt2Qk5eJzMeVlERwvYEZY4_4RxqxB5R1oTvc6jLWR4BAL2w25Gbw7RJvy6P52mSn5bUDEEMLl-mNN2DQmR0rUf8nu9wiTSk9rFKtQ9nvRQ16jTS-nY32mT09Chy7HXU284XpKNnthA1TI3X_W7BcTP0n86vAoW1ETydEMtL9xuuMf5TQ0Y56pihtr0OEg7ahdAiCGiZnlsfqVE391z3lmZRfy6Qt5o9tbxD7OGnYY1Ey_mQ'


class AgencyTestCase(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client()
        self.database_path = 'postgresql://yarasaleh@\
        localhost:5432/agency_test'
        setup_db(self.app, self.database_path)
        self.headers_Casting_Assistant = {'Content-Type': 'application/json',
                                          'Authorization': Casting_Assistant_Token}
        self.headers_Casting_Director = {'Content-Type': 'application/json',
                                         'Authorization': Casting_Director_Token}
        self.headers_Executive_Producer = {'Content-Type': 'application/json',
                                           'Authorization': Executive_Producer_Token}
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.drop_all()
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    Tests for successful operations and for expected errors.
    """
    # Endpoint [all_movies] == 1 --> fail
    def test010_404_get_movies(self):
        result = self.client.get('/all_movies',
                                 headers=self.headers_Casting_Assistant)
        data = json.loads(result.data)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["message"], "resource not found")

    # Endpoint [post:movie] == 2
    def test020_add_movie(self):
        # sample movie
        new_movie = {
            "id": 1,
            "title": "Shutter Island",
            "releaseDate": "2010-09-13T23:09:00Z"
        }
        result = self.client.post('/movie',
                                  json=new_movie,
                                  headers=self.headers_Executive_Producer)
        data = json.loads(result.data)
        self.assertEqual(data["success"], True)

    def test030_422_add_movie(self):
        # sample movie
        unp_movie = {
            "id": 2,
            "releaseDate": '2019-09-13T23:09:00Z'
        }
        result = self.client.post('/movie',
                                  json=unp_movie,
                                  headers=self.headers_Executive_Producer)
        data = json.loads(result.data)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 422)
        self.assertEqual(data["message"], "unprocessable")

    # Endpoint [all_movies] == 1 --> success
    def test040_get_movies(self):
        result = self.client.get('/all_movies',
                                 headers=self.headers_Casting_Assistant)
        data = json.loads(result.data)
        self.assertEqual(data["success"], True)

    # Endpoint [patch:movie] == 2
    def test050_update_movie(self):
        update_movie = {
            'releaseDate': '2020-02-15T23:09:00Z'
        }
        result = self.client.patch('/movie/1',
                                   json=update_movie,
                                   headers=self.headers_Casting_Director)
        data = json.loads(result.data)
        self.assertEqual(data["success"], True)

    def test060_404_update_movie(self):
        update_movie = {
            'title': 'Once Upon A Time'
        }
        result = self.client.patch('/movie/100',
                                   json=update_movie,
                                   headers=self.headers_Casting_Director)
        data = json.loads(result.data)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["message"], "resource not found")

    # Endpoint [all_actors] == 1 --> fail
    def test070_404_get_actors(self):
        result = self.client.get('/all_actors',
                                 headers=self.headers_Executive_Producer)
        data = json.loads(result.data)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["message"], "resource not found")

    # Endpoint [post:actor] == 2
    def test080_add_actor(self):
        # sample actors
        new_actor = {
            "id": 1,
            "name": 'Leonardo DiCaprio',
            "Age": 45,
            "gender": 'Male',
            "movie_id": 1
        }
        result = self.client.post('/actor',
                                  json=new_actor,
                                  headers=self.headers_Executive_Producer)
        data = json.loads(result.data)
        self.assertEqual(data["success"], True)

    def test090_422_add_actor(self):
        # sample actors
        new_actor = {
            "id": 2,
            "name": 'Zack',
            "gender": 'Male'
        }
        result = self.client.post('/actor',
                                  json=new_actor,
                                  headers=self.headers_Executive_Producer)
        data = json.loads(result.data)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 422)
        self.assertEqual(data["message"], "unprocessable")

    # Endpoint [all_actors] == 1 --> success
    def test0910_get_actors(self):
        result = self.client.get('/all_actors',
                                 headers=self.headers_Executive_Producer)
        data = json.loads(result.data)
        self.assertEqual(data["success"], True)

    # Endpoint [patch:actor] == 2
    def test0920_update_actor(self):
        # sample actors
        actor = {
            "age": 40
        }
        result = self.client.patch('/actor/1',
                                   json=actor,
                                   headers=self.headers_Casting_Director)
        data = json.loads(result.data)
        self.assertEqual(data["success"], True)

    def test0930_404_update_actor(self):
        # sample actors
        actor = {
            'name': 'Leo DiCaprio'
        }
        result = self.client.patch('/actor/100',
                                   json=actor,
                                   headers=self.headers_Casting_Director)
        data = json.loads(result.data)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["message"], "resource not found")

    # Endpoint [delete:actor] == 2
    def test0940_remove_actor(self):
        result = self.client.delete('/actor/1',
                                    headers=self.headers_Executive_Producer)
        data = json.loads(result.data)
        self.assertEqual(data["success"], True)

    def test0950_404_remove_actor(self):
        result = self.client.delete('/actor/100',
                                    headers=self.headers_Executive_Producer)
        data = json.loads(result.data)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["message"], "resource not found")

    # Endpoint [delete:movie] == 2
    def test0960_delete_movie(self):
        result = self.client.delete('/movie/1',
                                    headers=self.headers_Executive_Producer)
        data = json.loads(result.data)
        self.assertEqual(data["success"], True)

    def test0970_404_delete_movie(self):
        result = self.client.delete('/movie/100',
                                    headers=self.headers_Executive_Producer)
        data = json.loads(result.data)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["message"], "resource not found")

    # To test authorization for Casting Director
    def test0980_Casting_Director(self):
        # sample movie
        new_movie = {
            "id": 3,
            "title": "The Shape of Water",
            "releaseDate": "23-8-2017T23:09:00Z"
        }
        result = self.client.post('/movie',
                                  json=new_movie,
                                  headers=self.headers_Casting_Director)
        data = json.loads(result.data)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 401)
        self.assertEqual(data["message"]["code"], "unauthorized")

    # To test authorization for Casting Assistant
    def test0990_Casting_Assistant(self):
        # sample movie
        new_movie = {
            "id": 4,
            "title": "Summer of 84",
            "releaseDate": "29-6-2018T23:09:00Z"
        }
        result = self.client.post('/movie',
                                  json=new_movie,
                                  headers=self.headers_Casting_Assistant)
        data = json.loads(result.data)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 401)
        self.assertEqual(data["message"]["code"], "unauthorized")


# Make the tests conveniently executable
if __name__ == '__main__':
    unittest.main()
