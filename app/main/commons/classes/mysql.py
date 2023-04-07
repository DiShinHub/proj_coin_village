from app.main.commons.exceptions.exceptions import InternalServerException
from app.main import db
from sqlalchemy import text

import logging

log = logging.getLogger()


class Mysql():

    def __init__(self):
        self.status = True

    def defense_xxs(self, bind):
        """ def description : xxs 방어 

        Parameters : 
        bind : 바인드(tuple)

        Returns
        -------
        bind: 방어 적용 된 bind (dict)
        """
        bind_new = {}
        for key, val in bind.items():
            if isinstance(val, str):
                val = val.replace("<", "&lt")
                val = val.replace(">", "&gt")

            bind_new[key] = val

        return bind_new

    def read_one(self, query, bind_params):
        """ def description : 데이터 단일 조회 

        Parameters : 
        query: 쿼리문(str) 
        bind_params : 바인딩(dict) 

        Returns
        -------
        row : row proxy 객체
        """

        bind_params = self.defense_xxs(bind_params)

        try:
            row = db.engine.execute(text(query), **bind_params).fetchone()
            if not row:
                return None

            return row

        except Exception as ex:
            self.handle_db_exception(str(ex))
            raise InternalServerException(log_msg=f"{str(ex)}")

        finally:
            db.engine.dispose()

    def read_all(self, query, bind_params):
        """ def description : 데이터 복수 조회 

        Parameters : 
        query : 쿼리문(str) 
        bind_params : 바인딩(dict) 

        Returns
        -------
        rows : row proxy 객체
        """

        bind_params = self.defense_xxs(bind_params)

        try:
            rows = db.engine.execute(text(query), **bind_params).fetchall()
            if not rows:
                return None

            return rows

        except Exception as ex:
            self.handle_db_exception(str(ex))
            raise InternalServerException(log_msg=f"{str(ex)}")

        finally:
            db.engine.dispose()

    def read_all_found_rows(self, query, bind_params):
        """ def description : 데이터 복수 조회 (found rows)

        Parameters : 
        query : 쿼리문(str) 
        bind_params : 바인딩(dict) 

        Returns
        -------
        rows : row proxy 객체
        """

        bind_params = self.defense_xxs(bind_params)

        try:
            rows = db.engine.execute(text(query), **bind_params).fetchall()
            total_cnt = db.engine.execute("SELECT FOUND_ROWS() AS total_cnt").fetchone()[0]
            if not rows:
                return None

            data_dict = {
                "rows": rows,
                "total_cnt": total_cnt
            }
            return data_dict

        except Exception as ex:
            self.handle_db_exception(str(ex))
            raise InternalServerException(log_msg=f"{str(ex)}")

        finally:
            db.engine.dispose()

    def save_one(self, data):
        """ def description : 데이터 저장

        Parameters : 
        data : 데이터 객체(obj) 

        Returns
        -------
        response_object : 결과 오브젝트(dict)
        """

        try:
            db.session.add(data)

        except Exception as ex:
            self.handle_db_exception(str(ex))
            raise InternalServerException(log_msg=f"{str(ex)}")

    def save_all(self, data_obj_list):
        """ def description : 데이터 복수 저장

        Parameters : 
        data_obj_list : 데이터 객체 리스트(list) 
        """

        try:
            db.session.add_all(data_obj_list)

        except Exception as ex:
            self.handle_db_exception(str(ex))
            raise InternalServerException(log_msg=f"{str(ex)}")

    def save_one_commit(self, data):
        """ def description : 데이터 저장 with 커밋

        Parameters : 
        data : 데이터 객체(obj) 

        Returns
        -------
        pk : 신규데이터 pk
        """
        try:
            db.session.add(data)
            db.session.commit()
            pk = data.id
            return pk

        except Exception as ex:
            self.handle_db_exception(str(ex))
            raise InternalServerException(log_msg=f"{str(ex)}")

        finally:
            if self.status:
                db.session.close()
                db.session.remove()
                db.engine.dispose()

    def commit_db(self):
        """ 
        def description : 커밋
        """
        try:
            db.session.commit()

        except Exception as ex:
            self.handle_db_exception(str(ex))
            raise InternalServerException(log_msg=f"{str(ex)}")

        finally:
            if self.status:
                db.session.close()
                db.session.remove()
                db.engine.dispose()

    def close_db(self):
        """ 
        def description : DB 종료 
        """
        db.session.close()
        db.session.remove()

    def handle_db_exception(self, ex):
        """ 
        def description : 데이터 베이스 익셉션 핸들링

        Parameters : 
        ex : exception 메세지
        """
        self.status = False
        db.session.rollback()
        db.session.close()
        db.session.remove()
        db.engine.dispose()
