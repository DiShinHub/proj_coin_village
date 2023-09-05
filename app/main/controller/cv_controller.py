from flask import request
from flask_restplus import Resource, fields

from ..util.cv_dto import CvDto
from ..service.cv_service import Cv

api = CvDto.api


@api.route('/')
class Skills(Resource):
    responses = {
        201: """ <pre> {
  "status": "success",
  "message": "정상 처리되었습니다"
} </pre> """,
        400: '필수 값 누락입니다, ',
        500: '관리자에게 문의하세요'
    }
    @api.doc(security='apikey')
    @api.expect(
        api.model(
            'SkillsPost',
            {
                'service_code': fields.String(),
                'ticker': fields.String(),
            }
        )
    )
    def post(self):
        """
        서비스 on
        """
        if request.json:
            req_data = request.json
        
        else:
            req_data = request.form

        cv = Cv()
        return cv.on_service(req_data)

    responses = {
        201: """ <pre> {
  "status": "success",
  "message": "정상 처리되었습니다"
} </pre> """,
        400: '필수 값 누락입니다, ',
        500: '관리자에게 문의하세요'
    }
    @api.doc(security='apikey')
    @api.expect(
        api.model(
            'SkillsPost',
            {
                'service_code': fields.String(),
                'ticker': fields.String(),
            }
        )
    )
    def delete(self):
        """
        서비스 off
        """
        if request.json:
            req_data = request.json
        
        else:
            req_data = request.form

        cv = Cv()
        return cv.off_night_owl(req_data)
