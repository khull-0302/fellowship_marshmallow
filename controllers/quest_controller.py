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
