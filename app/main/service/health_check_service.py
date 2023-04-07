from app.main.commons.classes.mysql import *


class APIHealthCheck():

    def __init__(self):
        self.mysql = Mysql()

    def health_check(self):
        bind_params = {}
        query = "SELECT 1 FROM dual"
        self.mysql.read_one(query, bind_params)

        return 1
