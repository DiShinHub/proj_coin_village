# data transfer object (DTO) => swagger와 연결됨
from flask_restplus import Namespace, fields


class HealthCheckDto:
    api = Namespace('health_check', description='health_check related operations')
