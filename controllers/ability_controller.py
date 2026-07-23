from flask import jsonify, request

from db import db
from util.reflection import populate_object
from models.abilities import Abilities, ability_schema, abilities_schema

def add_ability():
    post_data = request.form if request.form else request.json

    new_ability = Abilities.new_ability_object()

    populate_object(new_ability, post_data)

    try:
        db.session.add(new_ability)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to create ability"}), 400
    
    return jsonify({"message": "ability created", "result": ability_schema.dump(new_ability)}), 201
