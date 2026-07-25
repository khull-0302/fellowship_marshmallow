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


def get_realm_by_id(realm_id):
    realm_query = db.session.query(Realms).filter(Realms.realm_id == realm_id).first()

    if not realm_query:
            return jsonify({
                "message": "No realm found"
            }), 404
    
    return jsonify ({
        "message": "realm found",
        "results": realm_schema.dump(realm_query)
    }),200

def update_realm_by_id(realm_id):
    post_data = request.form if request.form else request.json

    realm_query = db.session.query(Realms).filter(Realms.realm_id == realm_id).first()

    if realm_query:
        populate_object(realm_query, post_data)

        try:
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"message": "unable to update realm"}), 400
        
        return jsonify({
            "message": "realm updated",
            "result": realm_schema.dump(realm_query)
        }), 200
    
    return jsonify({"message": "unable to update record"}), 400


def delete_realm_by_id(realm_id):
    realm_query = db.session.query(Realms).filter(Realms.realm_id == realm_id).first()

    if not realm_query:
        return jsonify({"message": "raelm not found"}), 404

    db.session.delete(realm_query)
    db.session.commit()

    return jsonify({
        "message": "realm deleted"
    }), 200