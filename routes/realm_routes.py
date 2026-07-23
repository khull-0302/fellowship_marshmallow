from flask import Blueprint
import controllers

realm = Blueprint('realm', __name__)

@realm.route("/realm", methods=["POST"])
def add_realm():
    return controllers.add_realm()