from flask import jsonify, request

from db import db
from util.reflection import populate_object
from models.heros import Heroes, hero_schema, heroes_schema
from models.quests import Quests, quest_schema, quests_schema

def add_hero():
    post_data = request.form if request.form else request.json

    new_hero = Heroes.new_hero_object()

    populate_object(new_hero, post_data)

    try:
        db.session.add(new_hero)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to create hero"}), 400
    
    return jsonify({"message": "hero created", "result": hero_schema.dump(new_hero)}), 201

def add_hero_quest_association():
    post_data = request.form if request.form else request.json
    hero_id = post_data.get('hero_id')
    quest_id = post_data.get('quest_id')

    hero_query = db.session.query(Heroes).filter(Heroes.hero_id == hero_id).first()
    quest_query = db.session.query(Quests).filter(Quests.quest_id == quest_id).first()

    if not hero_query or not quest_query:
        return jsonify({
            "message": "hero or quest record does not exist"
        }), 400
    
    if hero_query and quest_query:
        hero_query.quests.append(quest_query)
        db.session.commit()

    return jsonify({
        "message": "quest added to hero", "result": hero_schema.dump(hero_query)
    })

def get_all_heroes():
    heroes_query = db.session.query(Heroes).all()

    return jsonify ({
        "message": "heroes found",
        "results": heroes_schema.dump(heroes_query)
    }),200



def get_all_alive_heroes():
    heroes_query = db.session.query(Heroes).filter(Heroes.is_alive == True).all()

    return jsonify ({
        "message": "heroes found",
        "results": heroes_schema.dump(heroes_query)
    }),200


def get_hero_by_id(hero_id):
    hero_query = db.session.query(Heroes).filter(Heroes.hero_id == hero_id).first()
    
    return jsonify ({
        "message": "hero found",
        "results": hero_schema.dump(hero_query)
    }),200

