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

def update_ability_by_id(ability_id):
    post_data = request.form if request.form else request.json

    ability_query = db.session.query(Abilities).filter(Abilities.ability_id == ability_id).first()

    if ability_query:
        populate_object(ability_query, post_data)

        try:
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"message": "unable to update ability"}), 400
        
        return jsonify({"message": "ability updated", "result": ability_schema.dump(ability_query)}), 200
    
    return jsonify({"message": "unable to update record"}), 400


def delete_ability_by_id(ability_id):
    ability_query = db.session.query(Abilities).filter(Abilities.ability_id == ability_id).first()

    if not ability_query:
        return jsonify({"message": "ability not found"}), 404

    db.session.delete(ability_query)
    db.session.commit()

    return jsonify({
        "message": "ability deleted"
    }), 200
