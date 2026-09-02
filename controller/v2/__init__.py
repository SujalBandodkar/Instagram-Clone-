from flask import Blueprint

api = Blueprint('api', __name__, url_prefix='/api')

from controller.v2 import auth_controller
from controller.v2 import user_controller
from controller.v2 import post_controller
from controller.v2 import message_controller
from controller.v2 import story_controller
from controller.v2 import admin_controller
