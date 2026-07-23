from flask import jsonify, request

from db import db
from util.reflection import populate_object
from models.realms import Realms, realm_schema, realms_schema

def add_realm():
    post_data = request.form if request.form else request.json

    new_realm = Realms.new_realm_object()

    populate_object(new_realm, post_data)

    try:
        db.session.add(new_realm)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to create realm"}), 400
    
    return jsonify({"message": "realm created", "result": realm_schema.dump(new_realm)}), 201
