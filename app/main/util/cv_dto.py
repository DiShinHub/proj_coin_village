# data transfer object (DTO) => swagger와 연결됨
from flask_restplus import Namespace, fields


class CvDto:
    api = Namespace('cv', description='CvDto related operations')
