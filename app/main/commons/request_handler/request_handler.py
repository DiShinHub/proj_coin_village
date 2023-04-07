
from flask_jwt_extended import *
from flask import jsonify
from flask import request
from flask_jwt_extended import verify_jwt_in_request_optional, verify_jwt_refresh_token_in_request, get_jwt_claims

import json

from app.main import db
import logging

log = logging.getLogger()


def request_handler(app):

    @app.before_request
    def before_request():
        """
        request 요청이 처리되기전에 호출
        """
        # all_jwt_optional()

        # jwt 토큰 데이터 사용
        try:
            verify_jwt_in_request_optional()

        except Exception as ex:
            pass

        # jwt 토큰 유저정보
        jwt_data = get_jwt_claims()

        # request 데이터 정보
        method = request.method
        url = request.url

        if method == "POST":
            params = request.form.to_dict()
            params["jwt_data"] = jwt_data
            request.form = params

        else:
            params = request.args.to_dict()
            params["jwt_data"] = jwt_data

        # request info
        r_host = request.remote_addr
        user_agent = request.user_agent
        platform = request.user_agent.platform
        method = request.method
        url = request.url

        # JWT 토큰 유효성 검사 (개발 완성 된 뒤 호스팅 테스트)
        # 환자앱, 환자웹, 의사웹 분기 포인트 잡아서 토큰 유효성 검사 실행

        request.args = params

        # 로그 기록
        log.info(f"""
HOST : {r_host}
USER_AGENT : {user_agent}
PLATFORM : {platform}
METHOD : {method}
REQUEST_URL : {url}
jwt_data : {jwt_data}
params : {params}
        """)

    @app.after_request
    def after_request(response):
        """
        request 요청이 처리되고 나서 실행
        """

        # 로그 기록
        response_json = response.get_json()
        if type(response_json) is dict:
            if 'swagger' in response_json:
                response_json = {}

        # 결과값이 5000줄 이상 일 경우 문자열을 자르고 마지막 문자열에 '...' 을 붙인다.
        response_str = json.dumps(response_json)
        if len(response_str) > 5000:
            str_tail = ' ...'
        else:
            str_tail = ''

        log.info(f"response: {response_str[0:5000]}{str_tail}")
        return response

    @app.teardown_request
    def teardown_request(exception):
        """
        request 요청의 결과가 브라우저에 응답하고 나서 호출
        """

        # DB session close
        db.session.close()
        db.session.remove()

        # 로그 기록
        log.info(f"teardown: {exception}")
        logging.shutdown()
