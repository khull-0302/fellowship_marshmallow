from flask import Blueprint
import controllers

quest = Blueprint('quest', __name__)

@quest.route("/quest", methods=["POST"])
def add_quest():
    return controllers.add_quest()

