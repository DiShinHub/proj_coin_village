from flask_restplus import Resource

from ..util.skills_dto import SkillsDto

from ..service.skills_service import *

api = SkillsDto.api


@api.route('/')
class Skills(Resource):
    @api.doc(security='apikey')
    def get(self):
        return