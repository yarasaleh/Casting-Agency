# Casting Agency
## About
This API models a company that is responsible for creating movies and managing and assigning actors to those movies. 
- https://aw-casting-agency-api.herokuapp.com/
## API
In order to use the API users need to be authenticated. 
Users can be a Casting Assistant , a Casting Director or Executive Producer. An overview of the API can be found below as well. 
### Models 
- **Movies** with attributes [id - title - releaseDate]
- **Actors** with attributes [id - name - age - gender - movie_id]


### Roles and Permissions 

permissions/roles  | Casting Assistant | Casting Director | Executive Producer
------------- | ------------- | ------------- | -------------
get:all_movies  | :white_check_mark: | :white_check_mark: |:white_check_mark: 
post:movie  |  | | :white_check_mark:
patch:movie  |  | :white_check_mark:|:white_check_mark: 
delete:movie  |  | | :white_check_mark:
get:all_actors  | :white_check_mark: | :white_check_mark: | :white_check_mark:
post:actor  |   |:white_check_mark: |:white_check_mark:
patch:actor  |   | :white_check_mark:|:white_check_mark:
delete:actor  |   |:white_check_mark: |:white_check_mark:


### Endpoints
#### GET /all_movies
  * Returns a list of avaliable movies objects and success value.
  ```
  curl -X GET https://aw-casting-agency-api.herokuapp.com/all_movies \
   -H 'Authorization: Bearer <INSERT_YOUR_TOKEN>'
  ```
#### POST /movie
  * Requires id , title and release Date.
  * Returns a list of new posted movie object and success value.
  ```
  curl -X POST https://aw-casting-agency-api.herokuapp.com/movie \
   -H 'Authorization: Bearer <INSERT_YOUR_TOKEN>' \
   -H 'Content-Type: application/json' \
   -d '{"id": 1 ,
    "title" : "Shutter Island",
    "releaseDate": "2010-09-13T23:09:00Z"
    }'
  ```
#### PATCH /movie/<int:id>
  * Returns a list of new edited movie object and success value.
  ```
  curl -X PATCH https://aw-casting-agency-api.herokuapp.com/movie/<int:id> \
   -H 'Authorization: Bearer <INSERT_YOUR_TOKEN>' \
   -H 'Content-Type: application/json' \
  ```
#### DELETE /movie/<int:id>
  Returns the id of the deleted movie object and success value.
  ```
  curl -X DELETE https://aw-casting-agency-api.herokuapp.com/movie/<int:id> \
   -H 'Authorization: Bearer <INSERT_YOUR_TOKEN>'
  ```
#### GET /all_actors
  * Returns a list of avaliable actors objects and success value.
  ```
  curl -X GET https://aw-casting-agency-api.herokuapp.com/all_actors \
   -H 'Authorization: Bearer <INSERT_YOUR_TOKEN>'
  ```
#### POST /actor
  * Requires id , name, age, gender and movie id that the actor participated in.
  * Returns a list of the new posted actor object and success value.
  ```
  curl -X POST https://aw-casting-agency-api.herokuapp.com/actor \
   -H 'Authorization: Bearer <INSERT_YOUR_TOKEN>' \
   -H 'Content-Type: application/json' \
   -d '{"id" : 1,
    "name" : 'Leonardo DiCaprio',
    "Age": 45,
    "gender" : 'Male',
    "movie_id": 1}'
  ```
#### PATCH /actor/<int:id>
  * Returns a list of the edited actor object and success value.
  ```
  curl -X PATCH https://aw-casting-agency-api.herokuapp.com/actor/<int:id> \
   -H 'Authorization: Bearer <INSERT_YOUR_TOKEN>' \
   -H 'Content-Type: application/json' \
  ```
#### DELETE /actor/<int:id>
  * Returns the id of the deleted actor object and success value.
  ```
  curl -X DELETE https://aw-casting-agency-api.herokuapp.com/actor/<int:id> \
   -H 'Authorization: Bearer <INSERT_YOUR_TOKEN>'
  ```


## :arrow_down: Installation
This project requires python3.
### Virtual Environment  -recommended-
This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).
### PIP Dependencies
Once you have your virtual environment setup and running, install dependencies by running :
```
pip3 install -r requirements.txt
```
### Database Setup
With Postgres running create a database:
```
createdb Agency
```
### Running The Server
To run the server, first ensure you are working using your created virtual environment and set the environment variables.
Each time you open a new terminal session, run:
```
export FLASK_APP=app.py
```
To run the server, execute:
```
flask run 
```
## :construction: Testing
To test the API, first create a test database in postgres and then execute the tests as follows:
```
createdb agency_test
python3 test_app.py
```



