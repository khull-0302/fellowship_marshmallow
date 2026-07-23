from flask import Blueprint
import controllers

race = Blueprint('race', __name__)

@race.route("/race", methods=["POST"])
def add_race():
    return controllers.add_race()

@race.route("/races", methods=["GET"])
def get_all_races():
    return controllers.get_all_races()