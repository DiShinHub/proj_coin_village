from flask_restplus import Resource

from ..util.health_check_dto import HealthCheckDto

from ..service.health_check_service import *

api = HealthCheckDto.api


@api.route('/')
class HealthCheck(Resource):
    @api.doc(security='apikey')
    def get(self):
        api_health_check = APIHealthCheck()
        return api_health_check.health_check()
