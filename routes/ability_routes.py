from flask import Blueprint
import controllers

ability = Blueprint('ability', __name__)

@ability.route("/ability", methods=["POST"])
def add_ability():
    return controllers.add_ability()