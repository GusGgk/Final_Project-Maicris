from flask import Flask
from controllers.user_controller import user_controller
from controllers.course_controller import course_controller


def register_controllers(app: Flask):
    app.register_blueprint(user_controller)
    app.register_blueprint(course_controller)
    
