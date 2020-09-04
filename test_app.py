import unittest
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Movies, Actors
import json



"""
- Includes at least one test for
            expected success and
            error behavior for
            each endpoint using the unittest library
- Includes tests demonstrating role-based access control,
at least two per role.
"""

Casting_Assistant_Token = f'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InBGa3BZWGxJZ3dnRV8xWWQxVjR5SyJ9.eyJpc3MiOiJodHRwczovL2Z1bGwtc3RhY2stcHJvamVjdC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY0ZjliNjQyMDc2YTcwMDY3OGYzYjdhIiwiYXVkIjoiYWdlbmN5IiwiaWF0IjoxNTk5MjIwMjM2LCJleHAiOjE1OTkzMDY2MzUsImF6cCI6IlNRa1ZMWFFhdWtlY1VQb3pPOElidjRvbmJXT3YzN29EIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWxsX2FjdG9ycyIsImdldDphbGxfbW92aWVzIl19.BWvJ-CuB4w3xfNllxyd2qvewWeCpaZr5H3qdhKJj76YCkQD3z-FlwrVPrgCavKSMDwAj4tksr_kKDalQlUBoO0Ww2KVkfJL2voeu8WNx6WDJZ-B6jALbC-y92GD58_25rrAxQ1ehRbjOOPd08U4DSJi4q4RNIPo0GS6Zw-bUuP4FCkgizv8ZWmoGkvboAocUgsPzrJ4NdGdb8d4ueXgdtuJ6F3tPYZrgHZNk2y_mnpFlJ4M2FxJZMdIHtd-LJy7oKEzbIVinH3z2ZobfklSvKb3_YwfaLIFFxnb_G_WvbuIuSFIcLX6jNAWU8QrW6Jsuua0PG5WkjkL2HGuB1zXJmw'
Casting_Director_Token = f'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InBGa3BZWGxJZ3dnRV8xWWQxVjR5SyJ9.eyJpc3MiOiJodHRwczovL2Z1bGwtc3RhY2stcHJvamVjdC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY0ZjlhOWYyMDc2YTcwMDY3OGYzYjZiIiwiYXVkIjoiYWdlbmN5IiwiaWF0IjoxNTk5MjE1MjYwLCJleHAiOjE1OTkzMDE2NTksImF6cCI6IlNRa1ZMWFFhdWtlY1VQb3pPOElidjRvbmJXT3YzN29EIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJnZXQ6YWxsX2FjdG9ycyIsImdldDphbGxfbW92aWVzIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiXX0.m1w7ir3274yFqkx755KLaheuELO8x0x9Ofpmdp47YyyaEkZdPxbhwxBvbp5-Fpeijd4Xy_j5uzG42vmyTmvASgJxzZs70V0JJV8K1igIDdoW_Ti-_OpO0ec3eVueDQbs4B1xYrtJvN8ow2CfyC-iY8D2YaBUw6arscfcxNL_M8FU6t1kScBbT6G_px9FfMYwyXWzUUP3Rj17V6U-zd1h86GXyUZktiBxfAcmOoNLLNWglz7uoUJMlH5DfixQQ6HiLpTBYLx14WGvCRSdT0W8HswB1ZQNYnevvzhKBsOc2yCqRTnu5yAmTJrOHw3eRn8KDDdswwXa9LYcIBlzh-mOzA'
Executive_Producer_Token = f'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InBGa3BZWGxJZ3dnRV8xWWQxVjR5SyJ9.eyJpc3MiOiJodHRwczovL2Z1bGwtc3RhY2stcHJvamVjdC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY0ZjlhNDBlOWVmNWYwMDY3YjYwNjM0IiwiYXVkIjoiYWdlbmN5IiwiaWF0IjoxNTk5MjIwNDQwLCJleHAiOjE1OTkzMDY4MzksImF6cCI6IlNRa1ZMWFFhdWtlY1VQb3pPOElidjRvbmJXT3YzN29EIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJkZWxldGU6bW92aWUiLCJnZXQ6YWxsX2FjdG9ycyIsImdldDphbGxfbW92aWVzIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiLCJwb3N0Om1vdmllIl19.exVUaMmYg8L9SW9VWOGCqKEf-p226cEiNztbQ4fi0m-Ft8yTNP1ji29Mh-c7USORYZDqXbwfvnhYevnfOUPAxq1n_McJDOZ3ig4Eo_86SG-UJjRuf2Ew6zsJyz8PM-nlVF4peMIthwAIGpYKdrlJLw2bN6yDhHhz1_Yj5x2Sn1GViyWHzy9N8Ctz1YscJQXZ4DIdbHdpxTD-6KgDCtLn3tpks4BSZQcQeeNqlAl2iHyVFtSZ22rxqTG9YnfjD6jhH_b7yzavldHIYNdVtx0qdCTY6AdnpSGrtKbbNcIKpxnweu0XYUHDi8edeEWz86RJ0aab_zauTAdRlFaHvvWUHQ'


class AgencyTestCase(unittest.TestCase):
    """This class represents the API test cases"""
    def setUp(self):
        print("TEST!TEST!")
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = 'postgres://yarasaleh@localhost:5432/agency_test'
        setup_db(self.app,self.database_path)

        self.headers_Casting_Assistant = {'Content-Type': 'application/json', 'Authorization': Casting_Assistant_Token}
        self.headers_Casting_Director = {'Content-Type': 'application/json', 'Authorization': Casting_Director_Token}
        self.headers_Executive_Producer = {'Content-Type': 'application/json', 'Authorization': Executive_Producer_Token}



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
        # Endpoint [all_movies] == 1
        def test_get_movies(self):
            result = self.client().get('/all_movies',headers=self.headers_Casting_Assistant)
            data = json.load(result.data)
            self.assertEqual(data["success"],True)
            self.assertTrue(len(data["movies"]))

        # Endpoint [post:movie] == 2
        def test_add_movie(self):
            # sample movie
            new_movie = {
                'id' : 1,
                'title' : 'Shutter Island',
                'releaseDate': '13-2-2010'
            }
            result = self.client().post('/movie',json=new_movie,headers=self.headers_Executive_Producer)
            data = json.load(result.data)
            self.assertEqual(data["success"],True)
            self.assertTrue(len(data["movie"]))

        def test_422_add_movie(self):
            # sample movie
            unp_movie = {
                'id' : 2,
                'releaseDate': '22-10-2019'
            }
            result = self.client().post('/movie',json=unp_movie,headers=self.headers_Executive_Producer)
            data = json.load(result.data)
            self.assertEqual(data["success"],False)
            self.assertEqual(data["error"],422)
            self.assertEqual(data["message"],"unprocessable")


        # Endpoint [patch:movie] == 2
        def test_update_movie(self):
            update_movie = {
                'releaseDate': '15-2-2010'
            }
            result = self.client().patch('/movie/1',json=update_movie,headers = self.headers_Casting_Director)
            data = json.load(result.data)
            self.assertEqual(data["success"],True)
            self.assertTrue(len(data["movie"]))

        def test_404_update_movie(self):
            update_movie = {
                'title': 'Once Upon A Time '
            }
            result = self.client().patch('/movie/100',json=update_movie, headers = self.headers_Casting_Director)
            data = json.load(result.data)
            self.assertEqual(data["success"],False)
            self.assertEqual(data["error"],404)
            self.assertEqual(data["message"],"resource not found")


        # Endpoint [delete:movie] == 2
        def test_delete_movie(self):
            result = self.client().delete('/movie/1',headers=self.headers_Executive_Producer)
            data = json.load(result.data)
            self.assertEqual(data["success"],True)
            self.assertTrue(len(data["deleted_movie"]))

        def test_404_delete_movie(self):
            result = self.client().delete('/movie/1',headers=self.headers_Executive_Producer)
            data = json.load(result.data)
            self.assertEqual(data["success"],False)
            self.assertEqual(data["error"],404)
            self.assertEqual(data["message"],"resource not found")


        # Endpoint [get_actors] == 1
        def test_get_actors(self):
            result = self.client().get('/all_actors', headers = self.headers_Casting_Assistant)
            data = json.load(result.data)
            self.assertEqual(data["success"],True)
            self.assertTrue(len(data["actors"]))

        # def test_404_get_actors(self):
        #     result = self.client().get('/all_actors')
        #     data = json.load(result.data)
        #     self.assertEqual(data["success"],False)
        #     self.assertEqual(data["error"],404)
        #     self.assertEqual(data["message"],"resource not found")


        # Endpoint [post:actor] == 2
        def test_add_actor(self):
            # sample actors
            new_actor = {
                'id' : 1,
                'name' : 'Leonardo DiCaprio',
                'age': 45,
                'gender' : 'Male'
            }
            result = self.client().post('/actor',json=new_actor,headers=self.headers_Executive_Producer)
            data = json.load(result.data)
            self.assertEqual(data["success"],True)
            self.assertTrue(len(data["actor"]))

        def test_422_add_actor(self):
            # sample actors
            new_actor = {
                'id' : 2,
                'name' : 'Zack',
                'gender' : 'Male'
            }
            result = self.client().post('/actor',json=new_actor,headers=self.headers_Executive_Producer)
            data = json.load(result.data)
            self.assertEqual(data["success"],False)
            self.assertEqual(data["error"],422)
            self.assertEqual(data["message"],"unprocessable")


        # Endpoint [patch:actor] == 2
        def test_update_actor(self):
            # sample actors
            actor = {
                'age': 40
            }
            result = self.client().patch('/actor/1',json=new_actor, headers = self.headers_Casting_Director)
            data = json.load(result.data)
            self.assertEqual(data["success"],True)
            self.assertTrue(len(data["actor"]))

        def test_404_update_actor(self):
            # sample actors
            actor = {
                'name' : 'Leo DiCaprio'
            }
            result = self.client().patch('/actor/100',json=new_actor, headers= self.headers_Casting_Director)
            data = json.load(result.data)
            self.assertEqual(data["success"],False)
            self.assertEqual(data["error"],404)
            self.assertEqual(data["message"],"resource not found")


        # Endpoint [delete:actor] == 2
        def test_remove_actor(self):
            result = self.client().delete('/actor/1',headers=self.headers_Executive_Producer)
            data = json.load(result.data)
            self.assertEqual(data["success"],True)
            self.assertTrue(len(data["deleted_actor"]))

        def test_404_remove_actor(self):
            result = self.client().delete('/actor/1',headers=self.headers_Executive_Producer)
            data = json.load(result.data)
            self.assertEqual(data["success"],False)
            self.assertEqual(data["error"],404)
            self.assertEqual(data["message"],"resource not found")





# Make the tests conveniently executable
if __name__ == '__main__':
   unittest.main()
