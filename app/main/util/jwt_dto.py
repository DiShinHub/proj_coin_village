# data transfer object (DTO) => swagger와 연결됨
from flask_restplus import Namespace


class JwtDto:
    api = Namespace('jwt', description='jwt related operations')
