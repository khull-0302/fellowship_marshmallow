from flask import jsonify, request

from db import db
from util.reflection import populate_object
from models.races import Races, race_schema, races_schema

def add_race():
    post_data = request.form if request.form else request.json

    new_race = Races.new_race_object()

    populate_object(new_race, post_data)

    try:
        db.session.add(new_race)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to create race"}), 400
    
    return jsonify({"message": "race created", "result": race_schema.dump(new_race)}), 201


def get_all_races():
    races_query = db.session.query(Races).all()

    return jsonify ({
        "message": "races found",
        "results": races_schema.dump(races_query)
    }),200

