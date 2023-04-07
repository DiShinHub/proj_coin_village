import os

from flask_migrate import Migrate, MigrateCommand
from flask_jwt_extended import JWTManager
from flask_script import Manager
from flask import jsonify

from app import blueprint
from app.main import create_app, db
from app.main.commons.request_handler.request_handler import request_handler
from app.main.commons.exceptions.error_handler import error_handler


app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')
app.register_blueprint(blueprint)
app.app_context().push()

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

request_handler(app)
error_handler(app)

jwt = JWTManager(app)


@jwt.expired_token_loader
def hd_expired_token_callback():
    return jsonify(status="fail", message="Auth_error: Token has expired"), 401


@manager.command
def run():
    app.run(port=50000)


if __name__ == '__main__':
    manager.run()
