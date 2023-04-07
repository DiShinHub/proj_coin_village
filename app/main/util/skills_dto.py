# data transfer object (DTO) => swagger와 연결됨
from flask_restplus import Namespace, fields


class SkillsDto:
    api = Namespace('skills', description='skills related operations')
