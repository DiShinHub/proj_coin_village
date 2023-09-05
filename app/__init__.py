import os
from flask_restplus import Api
from flask import Blueprint, helpers
from .main.controller.health_check_controller import api as health_check_ns
from .main.controller.jwt_controller import api as jwt_ns
from .main.controller.cv_controller import api as cv_ns


class MyApi(Api):
    @property
    def specs_url(self):
        """Monkey patch for HTTPS"""

        return f"{os.getenv('API_DOC_URL')}/v1/swagger.json"


authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': "Type in the *'Value'* input box below: **'Bearer &lt;JWT&gt;'**, where JWT is the token"
    }
}


blueprint = Blueprint('api', __name__, url_prefix="/v1")

api = MyApi(blueprint,
            title='FLASK RESTPLUS API FOR COIN VILLAGE!',
            version='1.0',
            authorizations=authorizations)

api.add_namespace(health_check_ns, path='/health-check')
api.add_namespace(jwt_ns, path='/jwt')
api.add_namespace(cv_ns, path='/cv')
