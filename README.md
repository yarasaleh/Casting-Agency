# Casting Agency
## About
This API models a company that is responsible for creating movies and managing and assigning actors to those movies.
## API
In order to use the API users need to be authenticated. 
Users can be a Casting Assistant , a Casting Director or Executive Producer. An overview of the API can be found below as well. 
### Models 
- **Movies** with attributes [title - release date]
- **Actors** with attributes [name - age - gender]


### Roles and Permissions 

permissions/roles  | Casting Assistant | Casting Director | Executive Producer
------------- | ------------- | ------------- | -------------
get:all_movies  | :white_check_mark: | :white_check_mark: |:white_check_mark: 
post:movies  |  | | :white_check_mark:
patch:movies  |  | :white_check_mark:|:white_check_mark: 
delete:movies  |  | | :white_check_mark:
get:all_actors  | :white_check_mark: | :white_check_mark: | :white_check_mark:
post:actors  |   |:white_check_mark: |:white_check_mark:
patch:actors  |   | :white_check_mark:|:white_check_mark:
delete:actors  |   |:white_check_mark: |:white_check_mark:


### Endpoints
soon..:clock130:


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
soon..:clock130:



