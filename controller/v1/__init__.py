from flask import Blueprint

controller = Blueprint('controller', __name__)

from controller.v1 import auth_controller
from controller.v1 import user_controller
from controller.v1 import post_controller
from controller.v1 import message_controller
from controller.v1 import story_controller
from controller.v1 import admin_controller
