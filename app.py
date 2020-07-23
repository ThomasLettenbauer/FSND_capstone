import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, Movie, Actor, db

from auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    # GET /actors

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(payload):
        try:
            actors = Actor.query.all()
            formatted_actors = [actor.format() for actor in actors]

            return jsonify({
                'success': True,
                'actors': formatted_actors
            })
        except:
            abort(400)

    # GET /movies

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(payload):
        try:
            movies = Movie.query.all()
            formatted_movies = [movie.format() for movie in movies]

            return jsonify({
                'success': True,
                'movies': formatted_movies
            })
        except:
            abort(400)

    # DELETE /actors

    @app.route('/actors/<id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, id):
        try:
            actor = Actor.query.filter(Actor.id == id).one_or_none()

            if actor is None:
                abort(404)

            actor.delete()

            return jsonify({
                'success': True,
                'deleted': id
            })

        except Exception:
            abort(422)

    # DELETE /movies

    @app.route('/movies/<id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, id):
        try:
            movie = Movie.query.filter(Movie.id == id).one_or_none()

            if movie is None:
                abort(404)

            movie.delete()

            return jsonify({
                'success': True,
                'deleted': id
            })

        except Exception:
            abort(422)

    # POST /actors

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def post_actor(payload):
    #    try:
            age = request.get_json()['age']
            gender = request.get_json()['gender']
            name = request.get_json()['name']

            newactor = Actor(age=age,
                             gender=gender,
                             name=name)
            newactor.insert()
            return jsonify({
                'success': True,
                'actor': newactor.format()
            })
    #    except Exception:
     #       abort(400)

    # POST /movies
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def post_movie(payload):
        try:
            title = request.get_json()['title']
            releasedate = request.get_json()['releasedate']

            newmovie = Movie(title=title,
                             releasedate=releasedate)
            newmovie.insert()
            return jsonify({
                'success': True,
                'movie': newmovie.format()
            })
        except Exception:
            abort(400)

    # PATCH /actors

    @app.route('/actors/<id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def patch_actor(payload, id):
        try:
            actor = Actor.query.filter(Actor.id == id).one_or_none()

            if actor is None:
                abort(404)

            request_json = request.get_json()

            if 'name' in request_json:
                actor.name = request_json['name']

            if 'gender' in request_json:
                actor.gender = request_json['gender']

            if 'age' in request_json:
                actor.age = request_json['age']

            actor.update()

            return jsonify({
                'success': True,
                'actor': actor.format()
            })
        except Exception:
            abort(400)

    # PATCH /movies

    @app.route('/movies/<id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def patch_movie(payload, id):
        try:
            movie = Movie.query.filter(Movie.id == id).one_or_none()

            if movie is None:
                abort(404)

            request_json = request.get_json()

            if 'title' in request_json:
                movie.title = request_json['title']

            if 'releasedate' in request_json:
                movie.releasedate = request_json['releasedate']

            movie.update()

            return jsonify({
                'success': True,
                'movie': movie.format()
            })
        except Exception:
            abort(400)

    # Errorhandlers

    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response

    @app.errorhandler(400)
    def not_found(error):
        return jsonify({

            "success": False,
            "error": 400,
            "message": "Bad request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        }), 404

    @app.errorhandler(405)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method Not Allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        }), 500

    return app


app = create_app()
if __name__ == '__main__':
    app.run()
