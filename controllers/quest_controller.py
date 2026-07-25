from flask import jsonify, request

from db import db
from util.reflection import populate_object
from models.quests import Quests, quest_schema, quests_schema


def add_quest():
    post_data = request.form if request.form else request.json

    new_quest = Quests.new_quest_object()

    populate_object(new_quest, post_data)

    try:
        db.session.add(new_quest)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to create quest"}), 400
    
    return jsonify({"message": "quest created", "result": quest_schema.dump(new_quest)}), 201


def get_quest_by_difficulty_level(difficulty_level):
    quests_query = db.session.query(Quests).filter(Quests.difficulty == difficulty_level).all()

    if not quests_query:
        return jsonify({
            "message": "No quests found with that difficulty level"
        }), 404

    return jsonify ({
        "message": "quest found",
        "results": quests_schema.dump(quests_query)
    }),200


def get_quest_by_id(quest_id):
    quest_query = db.session.query(Quests).filter(Quests.quest_id == quest_id).first()

    if not quest_query:
            return jsonify({
                "message": "No quest found"
            }), 404
    
    return jsonify ({
        "message": "quest found",
        "results": quest_schema.dump(quest_query)
    }),200

def update_quest_by_id(quest_id):
    post_data = request.form if request.form else request.json

    quest_query = db.session.query(Quests).filter(Quests.quest_id == quest_id).first()

    if quest_query:
        populate_object(quest_query, post_data)

        try:
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"message": "unable to update quest"}), 400
        
        return jsonify({
            "message": "quest updated",
            "result": quest_schema.dump(quest_query)
        }), 200
    
    return jsonify({"message": "unable to update record"}), 400

def complete_quest(quest_id):
    quest_query = db.session.query(Quests).filter(Quests.quest_id == quest_id).first()

    if quest_query:
        quest_query.is_completed = True

        try:
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"message": "unable to complete quest"}), 400
        
        return jsonify({
            "message": "quest completed",
            "result": quest_schema.dump(quest_query)
        }), 200
    
    return jsonify({"message": "unable to find quest"}), 404

def delete_quest_by_id(quest_id):
    quest_query = db.session.query(Quests).filter(Quests.quest_id == quest_id).first()

    if not quest_query:
        return jsonify({"message": "quest not found"}), 404

    db.session.delete(quest_query)
    db.session.commit()

    return jsonify({
        "message": "quest deleted"
    }), 200