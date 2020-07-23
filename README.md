# Full Stack Capstone Project Casting Agency

## Heroku Deployment

App can be found at https://fsndcapstoneapp.herokuapp.com

The Endpoints can be tested in Postman with the supplied Collection    

    **udacity-fsnd-capstone.postman_collection.json**

This Collection includes valid Tokens for the different roles
    

## Backend Installation and Startup

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies with 

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

## Running the server locally

From within the directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=app.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## API Endpoints

### GET /movies
* General:
	* Returns a list of movies and success value
* Sample: 

	    curl https://fsndcapstoneapp.herokuapp.com/movies

* Response:

        {
            "movies": [
                {
                    "id": 1,
                    "releasedate": "Wed, 09 Sep 2020 00:00:00 GMT",
                    "title": "The Green Screen"
                },
                {
                    "id": 2,
                    "releasedate": "Wed, 11 Nov 2020 00:00:00 GMT",
                    "title": "The Blue Lagoon"
                }
            ],
            "success": true
        }

### GET /actors
* General:
	* Returns a list of actors and success value
* Sample: 
	
	    curl https://fsndcapstoneapp.herokuapp.com/actors

* Response:

        {
            "actors": [
                {
                    "age": 55,
                    "gender": "male",
                    "id": 1,
                    "name": "Sean Canary"
                }
            ],
            "success": true
        }
  
### DELETE /movies/\<id\>
* General:
	*  Deletes the movie with id *id*

* Sample: 
	

	    curl -X DELETE curl https://fsndcapstoneapp.herokuapp.com/movies/1
* Response:

	    {
	      "deleted": 1, 
	      "success": true
	    }
	      
### DELETE /actors/\<id\>
* General:
	*  Deletes the actor with id *id*

* Sample: 
	

	    curl -X DELETE curl https://fsndcapstoneapp.herokuapp.com/actors/1
* Response:

	    {
	      "deleted": 1, 
	      "success": true
	    }

### POST /movies
* General:
	* Inserts a new movie with values for title and releasedate in the body
	* Returns a success value and movie data

* Sample: 

	    curl 	--header "Content-Type: application/json" --request POST \
				--data '{"title":"The Blue Lagoon","releasedate":"11/11/2020"}' \
				https://fsndcapstoneapp.herokuapp.com/movies
* Response:

        {
            "movie": {
                "id": 3,
                "releasedate": "Wed, 11 Nov 2020 00:00:00 GMT",
                "title": "The Blue Lagoon"
            },
            "success": true
        }

### POST /actors
* General:
	* Inserts a new actor with values for name, age and gender in the body
	* Returns a success value and actor data

* Sample: 

	    curl 	--header "Content-Type: application/json" --request POST \
				--data '{"name":"Babsi Streusand","age":40,"gender":"female"}' \
				https://fsndcapstoneapp.herokuapp.com/actors
* Response:

        {
            "actor": {
                "id": 3,
                "name": "Babsi Streusand",
                "age": 40,
                "gender": "female"
            },
            "success": true
        }

### PATCH /movies\<id\>
* General:
	* Update the movie with id *id* with values for title or releasedate in the body
	* Returns a success value and movie data

* Sample: 

	    curl 	--header "Content-Type: application/json" --request PATCH \
				--data '{"title":"The Green Lagoon","releasedate":"11/11/2020"}' \
				https://fsndcapstoneapp.herokuapp.com/movies/3
* Response:

        {
            "movie": {
                "id": 3,
                "releasedate": "Wed, 11 Nov 2020 00:00:00 GMT",
                "title": "The Green Lagoon"
            },
            "success": true
        }

### PATCH /actors\<id\>
* General:
	* Updates the actor with id *id* with values for name, age or gender in the body
	* Returns a success value and actor data

* Sample: 

	    curl 	--header "Content-Type: application/json" --request PATCH \
				--data '{"name":"Babsi Streusel","age":40,"gender":"female"}' \
				https://fsndcapstoneapp.herokuapp.com/actors/3
* Response:

        {
            "actor": {
                "id": 3,
                "name": "Babsi Streusel",
                "age": 40,
                "gender": "female"
            },
            "success": true
        }

## Roles
### Casting Assistant
    Can view actors and movies (get:actors, get:movies)
### Casting Director
    All permissions a Casting Assistant has and…
	Add or delete an actor from the database (post:actors, delete:actors)
	Modify actors or movies (patch:actors, patch:movies)
### Executive Producer
	All permissions a Casting Director has and…
    Add or delete a movie from the database (post:movies, delete:movies) 