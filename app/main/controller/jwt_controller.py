
from flask import request
from flask_restplus import Resource
from flask_jwt_extended import jwt_required, jwt_refresh_token_required
from app.main.commons.exceptions.exceptions import AuthException

from ..util.jwt_dto import JwtDto

from ..service.jwt_service import *

api = JwtDto.api


@api.route('/refresh')
class HhToken(Resource):
    @api.doc(security='apikey')
    @jwt_refresh_token_required
    def get(self):
        """
        jwt 재발급

        <i>request value:</i> </br>
        """
        platform = request.user_agent.platform
        block_platform = ["windows", "macos"]
        if platform in block_platform:
            raise AuthException(msg="재발급이 불가한 플랫폼입니다.")

        jwt_token_service = JwtTokenService()
        return jwt_token_service.refresh_jwt_token()
