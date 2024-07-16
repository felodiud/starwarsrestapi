from flask_sqlalchemy import SQLAlchemy;

db = SQLAlchemy();

class Planet(db.Model):
    __tablename__ = "planet"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False) 

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }



class People(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)
    lastname = db.Column(db.String(50), nullable = True)
    wheight = db.Column(db.String(50), nullable = True)

    def to_dict(self):
        return{
            "id": self.id,
            "name": self.name,
            "lastname": self.lastname,
            "wheight": self.wheight
        }



class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    name  = db.Column(db.String(50), nullable = False)
    username = db.Column(db.String(30), nullable = False)
    password = db.Column(db.String(20), nullable = False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username
        }
    

class Favorite(db.Model):
    __tablename__= "favorite"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_favorite_user_id'))
    user_people_id = db.Column(db.Integer, db.ForeignKey('people.id', name='fk_favorite_user_people_id'), nullable=True)
    user_planet_id = db.Column(db.Integer, db.ForeignKey('planet.id', name='fk_favorite_user_planet_id'), nullable=True)
    
    user = db.relationship('User', backref='favorites')
    people = db.relationship('People', backref='favorites', foreign_keys=[user_people_id])
    planet = db.relationship('Planet', backref='favorites', foreign_keys=[user_planet_id])

    def to_dict_with_relations(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "user": self.user.to_dict() if self.user else None,
            "people": self.people.to_dict() if self.people else None,
            "planet": self.planet.to_dict() if self.planet else None
        }