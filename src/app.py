from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy;
from models import db, People, User, Favorite, Planet
from flask_migrate import Migrate

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)



@app.route("/people", methods=["GET", "POST"])
def handle_people():
    if request.method == "GET":
        people = People.query.all()
        people_list = [person.to_dict() for person in people]
        return jsonify({
            "status": "OK",
            "body": people_list
        }), 200
    elif request.method == "POST":
        person = People()
        data = request.get_json()
        person.name = data["name"]
        person.lastname = data["name"]
        person.wheight = data["wheight"]
        db.session.add(person)
        db.session.commit()
        return ({
            "status": "OK",
            "body": person.to_dict()
        }), 200

@app.route("/people/<int:people_id>", methods=["GET", "DELETE"])
def handle_person(people_id):
    if request.method == "GET":
        person = People.query.get_or_404(people_id)
        return jsonify({
            "status": "OK",
            "body": person.to_dict()
        }), 200
    elif request.method == "DELETE":
        person = People.query.get_or_404(people_id)
        db.session.delete(person)
        db.session.commit()
        return jsonify({
            "status": "OK",
            "message": f"Persona {person.name} eliminada"
        })

@app.route("/planets", methods=["GET", "POST"])
def handle_planets():
    if request.method == "GET":
        planets = Planet.query.all()
        planets_list = [planet.to_dict() for planet in planets]
        return jsonify({
            "status": "OK",
            "body": planets_list
        }), 200
    elif request.method == "POST":
        planet = Planet()
        data = request.get_json()
        planet.name = data["name"]
        db.session.add(planet)
        db.session.commit()
        return jsonify({
            "status": "OK",
            "body": planet.to_dict()
        }), 200

@app.route("/planets/<int:planet_id>", methods=["DELETE"])
def delete_planet(planet_id):
    planet = Planet.query.get_or_404(planet_id)
    db.session.delete(planet)
    db.session.commit()
    return jsonify({
        "status": "OK",
        "message": f"Planeta {planet.name} eliminado"
    }), 200


@app.route("/planets/<int:planet_id>", methods=["GET"])
def get_planet(planet_id):
    planet = Planet.query.get_or_404(planet_id)
    return jsonify({
        "status": "OK",
        "body": planet.to_dict()
    }), 200

@app.route("/users", methods=["GET", "POST"])
def handle_users():
    if request.method =="GET":
        users = User.query.all()
        users_list = [user.to_dict() for user in users]
        return jsonify({
            "status": "OK",
            "body": users_list
        }), 200
    elif request.method == "POST":
        user = User()
        data = request.get_json()
        user.name = data["name"]
        user.username = data["username"]
        user.password = data["password"]
        db.session.add(user)
        db.session.commit()
        return jsonify({
            "status": "OK",
            "body": user.to_dict()
        }), 200
    
@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({
        "status" : "OK",
        "message": f"usuario {user.username} eliminado"
    }), 200

@app.route("/users/favorites", methods=["GET"])
def get_user_favorites():
    user_id = request.args.get('user_id')
    print(user_id)
    user = User.query.get_or_404(user_id)
    favorites = Favorite.query.filter_by(user_id=user_id).all()
    favorites_list = [favorite.to_dict_with_relations() for favorite in favorites]
    return jsonify({
        "status": "OK",
        "body": favorites_list
    }), 200

@app.route("/favorite/planet/<int:planet_id>", methods=["POST"])
def add_favorite_planet(planet_id):
    user_id = request.json.get('user_id')
    new_favorite = Favorite(user_id=user_id, user_planet_id=planet_id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({
        "status": "OK",
        "body": new_favorite.to_dict_with_relations()
    }), 201

@app.route("/favorite/people/<int:people_id>", methods=["POST"])
def add_favorite_person(people_id):
    user_id = request.json.get('user_id')
    new_favorite = Favorite(user_id=user_id, user_people_id=people_id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({
        "status": "OK",
        "body": new_favorite.to_dict_with_relations()
    }), 201

@app.route("/favorite/planet/<int:planet_id>", methods=["DELETE"])
def delete_favorite_planet(planet_id):
    user_id = request.json.get('user_id')
    favorite = Favorite.query.filter_by(user_id=user_id, user_planet_id=planet_id).first_or_404()
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({
        "status": "OK",
        "message": "Favorite planet deleted"
    }), 200

@app.route("/favorite/people/<int:people_id>", methods=["DELETE"])
def delete_favorite_person(people_id):
    user_id = request.json.get('user_id')
    favorite = Favorite.query.filter_by(user_id=user_id, user_people_id=people_id).first_or_404()
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({
        "status": "OK",
        "message": "Favorite person deleted"
    }), 200





with app.app_context():
    db.create_all()


if __name__=="__main__":
    app.run()
