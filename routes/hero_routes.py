from flask import Blueprint
import controllers

hero = Blueprint('hero', __name__)

@hero.route("/hero", methods=["POST"])
def add_hero():
    return controllers.add_hero()

@hero.route("/hero-quest", methods=["POST"])
def add_hero_quest_association():
    return controllers.add_hero_quest_association()

@hero.route("/heroes", methods=["GET"])
def get_all_heroes():
    return controllers.get_all_heroes()

@hero.route("/heroes/alive", methods=["GET"])
def get_all_alive_heroes():
    return controllers.get_all_alive_heroes()

@hero.route("/hero/<hero_id>", methods=["GET"])
def get_hero_by_id(hero_id):
    return controllers.get_hero_by_id(hero_id)