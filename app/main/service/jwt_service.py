from app.main.commons.exceptions.exceptions import *
from app.main.commons.classes.mysql import *

from flask_jwt_extended import create_access_token,  get_jwt_identity
import logging
import os

log = logging.getLogger()


class JwtTokenService():

    def __init__(self):
        self.mysql = Mysql()

    def refresh_jwt_token(self):
        """ 
        def description : 토큰 재발급

        Returns
        response_object : 결과 (dict)
        -------
        """
        log.info(f" def: refresh_token")

        try:
            jwt_identity = get_jwt_identity()

            data_dict = self.select_reg_user(jwt_identity)
            if not data_dict:
                raise NotFoundException(msg="잘못된 정보입니다")

            user_claims = {
                "id": data_dict["id"],
                "user_id": data_dict["user_id"],
                "user_email": data_dict["user_email"],
                "user_uni_num": data_dict["user_uni_num"],
                "iss": os.getenv("JWT_ISS"),
                "aud": os.getenv("JWT_PATIENT_APP_AUD")
            }
            access_token = create_access_token(identity=jwt_identity, user_claims=user_claims)
            response_object = {
                "status": "success",
                "message": "success",
                "access_token": access_token
            }
            return response_object, 200

        except Exception as ex:
            raise InternalServerException(log_msg=f"{str(ex)[0:200]}")

    def select_reg_user(self, u_id):
        """ 
        def description : 토큰 재발급

        Parameters
        u_id : reg_user pk 
        ----------

        Returns
        data_dict : 결과 (dict)
        -------
        """

        bind_params = {
            "U_ID": u_id
        }
        query = """
        SELECT
            id,
            user_id,
            user_email,
            user_uni_num
        FROM
            hh_reg_user
        WHERE
            id = :U_ID;
        """
        response = self.mysql.read_one(query, bind_params)
        if not response:
            return {}

        data_dict = {
            "id": response["id"],
            "user_id": response["user_id"],
            "user_email": response["user_email"],
            "user_uni_num": response["user_uni_num"]
        }
        return data_dict
